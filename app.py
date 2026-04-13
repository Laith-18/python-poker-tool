from flask import Flask, render_template, request, redirect, url_for, session

from game.login_system import LoginClass
from game.game_engine import GameEngine


from utilities.card_loader import get_card_image_from_file


app = Flask(__name__)
app.secret_key = "poker"

login_system = LoginClass()
game_engine = GameEngine()

active_games = {} # Dictionary to store active game states for each user

MAX_LOG_MESSAGES = 10


def add_game_message(state, message):
    if not message:
        return

    if state.message_log is None:
        state.message_log = []

    state.message_log.append(message)
    state.message_log = state.message_log[-MAX_LOG_MESSAGES:]
    state.round_message = message


def log_blinds_message(state):
    if state.small_blind:
        user_small_blind = max(1, state.ai_bet // 2)
        add_game_message(state, f"Blinds posted: you {user_small_blind} (small), AI {state.ai_bet} (big).")
    else:
        add_game_message(state, f"Blinds posted: AI {state.ai_bet} (small), you {state.recent_bet} (big).")


def settle_showdown(state, username):
    state.phase = "showdown"

    user_strength = game_engine.evaluate_user_strength(state)
    ai_strength = game_engine.evaluate_ai_strength(state)

    if user_strength > ai_strength:
        state.round_message = f"You win the hand! Your hand was: {user_strength}, AI hand was: {ai_strength}."
        state.user_bank += state.pot
    elif ai_strength > user_strength:
        state.round_message = f"AI wins the hand. Your hand was: {user_strength}, AI hand was: {ai_strength}."
    else:
        from game.strength_determiner import rank_to_value

        user_high_card = max([rank_to_value(card[0]) for card in state.user_deck])
        ai_high_card = max([rank_to_value(card[0]) for card in state.ai_deck])

        if user_high_card > ai_high_card:
            state.round_message = f"You win the hand with a higher card! Your hand was: {user_strength} with high card {user_high_card}, AI hand was: {ai_strength} with high card {ai_high_card}."
            state.user_bank += state.pot
        elif ai_high_card > user_high_card:
            state.round_message = f"AI wins the hand with a higher card. Your hand was: {user_strength} with high card {user_high_card}, AI hand was: {ai_strength} with high card {ai_high_card}."
        else:
            state.round_message = f"It's a tie! Your hand was: {user_strength}, AI hand was: {ai_strength}. Pot is split."
            state.user_bank += state.pot // 2

    winning_summary = state.round_message
    state.pot = 0
    session["user_bank"] = state.user_bank
    login_system.update_bank(username, state.user_bank)
    add_game_message(state, winning_summary)


def resolve_all_in_if_needed(state, username):
    if state.user_bank > 0 or state.phase in ["showdown", "game_over"]:
        return

    add_game_message(state, "You're all-in. Remaining community cards are dealt automatically.")
    missing_cards = 5 - len(state.community_deck)
    if missing_cards > 0:
        state.community_deck = game_engine.community_cards(state.community_deck, count=missing_cards)

    settle_showdown(state, username)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")

        if action == "login":
            user_data = login_system.login(username, password)
            if user_data:
                session["username"] = username
                session["user_bank"] = user_data[1] 
                return redirect(url_for("play_game"))
            else:
                return render_template("login.html", error="Invalid username or password")
            
        elif action == "register":
            message = login_system.register(username, password)
            if message == "Registration successful":
                return render_template("login.html", message="Registration successful, please log in")
            else:
                return render_template("login.html", error=message)
    
    return render_template("login.html")

@app.route("/game", methods=["GET", "POST"])
def play_game():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]

    if username not in active_games:
        state = game_engine.setup_new_game(username, session["user_bank"])
        state = game_engine.determine_blinds(state)
        log_blinds_message(state)

        active_games[username] = state
    
    state = active_games[username]
    resolve_all_in_if_needed(state, username)

    if request.method=="POST":
        decision = request.form.get("decision")
        raise_amount = request.form.get("raise_amount",0,type=int)
        outcome = None


        if decision == "next_hand":
            if state.user_bank <= 0:
                state.phase = "game_over"
                add_game_message(state, "You are out of chips. Restart from login to play again.")
                active_games[username] = state
                return redirect(url_for("play_game"))

            #reset the game state for the next hand but keep the username and user bank
            active_games[username] = game_engine.setup_new_game(username, state.user_bank)
            active_games[username] = game_engine.determine_blinds(active_games[username])
            log_blinds_message(active_games[username])
            return redirect(url_for("play_game"))

        #otherwise we are in the middle of a hand and need to process the user's decision
        if decision in ["call","raise","fold"]:
            outcome = game_engine.run_betting_round(state, user_goes_first=state.small_blind, decision=decision, raise_amount=raise_amount)
        
        if outcome == "fold":
            state.phase = "game_over"
            add_game_message(state, "You folded. AI wins the pot.")
            state.pot = 0
        
        elif outcome == "ai_folded":
            state.phase = "game_over"
            add_game_message(state, "AI folded. You win the pot!")
            state.user_bank += state.pot
            state.pot = 0
            login_system.update_bank(username, state.user_bank) # Update the user's bank in the database after winning the pot
        
        elif outcome == "round_over":
            if decision == "call":
                add_game_message(state, "You call/check.")
            elif decision == "raise":
                add_game_message(state, f"You raise by {raise_amount}.")
                add_game_message(state,f"AI {state.ai_last_action}. Round over.")
            state.recent_bet = 0 # Reset recent bet for the next round
        
            if state.phase =="preflop":
                state.community_deck= game_engine.community_cards(state.community_deck, count=3)
                state.phase = "flop"
            elif state.phase == "flop":
                state.community_deck = game_engine.community_cards(state.community_deck, count=1)
                state.phase = "turn"
            elif state.phase == "turn":
                state.community_deck = game_engine.community_cards(state.community_deck, count=1)
                state.phase = "river"
            elif state.phase == "river":
                settle_showdown(state, username)

        elif outcome == "continue":
            add_game_message(state, f"A {state.ai_last_action}. Respond with call, raise, or fold.")
        elif outcome == "invalid_funds":
            add_game_message(state, "Insufficient funds for that move. Try a smaller raise or call/fold.")
        elif outcome == "invalid_action":
            add_game_message(state, "Invalid action for the current state. Please choose call, raise, or fold.")

        resolve_all_in_if_needed(state, username)
        
    active_games[username] = state


    return render_template("index.html", state=state, get_card_image_from_file=get_card_image_from_file)

if __name__ == "__main__":
    app.run(debug=True)

        