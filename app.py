from flask import Flask, render_template, request, redirect, url_for, session

from game.login_system import LoginClass
from game.game_engine import GameEngine


from utilities.card_loader import get_card_image_from_file


app = Flask(__name__)
app.secret_key = "poker"

login_system = LoginClass()
game_engine = GameEngine()

active_games = {} # Dictionary to store active game states for each user

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

        active_games[username] = state
    
    state = active_games[username]

    if request.method=="POST":
        decision = request.form.get("decision")
        raise_amount = request.form.get("raise_amount",0,type=int)


        if decision == "next_hand":

            #reset the game state for the next hand but keep the username and user bank
            active_games[username] = game_engine.setup_new_game(username, state.user_bank)
            active_games[username] = game_engine.determine_blinds(active_games[username])
            return redirect(url_for("play_game"))

        #otherwise we are in the middle of a hand and need to process the user's decision
        if decision in ["call","raise","fold"]:
            outcome = game_engine.run_betting_round(state, user_goes_first=state.small_blind, decision=decision, raise_amount=raise_amount)
        
        if outcome =="fold":
            state.phase = "game_over"
            state.round_message= "You folded. AI wins the pot."
            state.user_bank += state.pot
            state.pot = 0
        
        elif outcome == "round_over":
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
                state.phase = "showdown"


                user_strength = game_engine.evaluate_user_strength(state)
                ai_strength = game_engine.evaluate_ai_strength(state)

                if user_strength > ai_strength:
                    state.round_msg = f"You win the hand! Your hand was: {user_strength}, AI hand was: {ai_strength}."
                    state.user_bank += state.pot
                elif ai_strength > user_strength:
                    state.round_msg = f"AI wins the hand. Your hand was: {user_strength}, AI hand was: {ai_strength}."
                else:
                    state.round_msg = f"It's a tie! Your hand was: {user_strength}, AI hand was: {ai_strength}. Pot is split."
                    state.user_bank += state.pot // 2
                state.pot = 0

                session["bank"] = state.user_bank # Update the user's bank in the session after the hand is resolved



                #DEBUG DEBUG DEBUG


    
        elif outcome == "continue":
            state.round_msg = "Betting round continues. AI raise. Respond: call, raise, or fold."
        
    active_games[username] = state


    return render_template("index.html", state=state, get_card_image_from_file=get_card_image_from_file)

if __name__ == "__main__":
    app.run(debug=True)

        