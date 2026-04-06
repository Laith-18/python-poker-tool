from flask import Flask, render_template, request, redirect, url_for, session
from game.login_system import LoginClass
from game.game_engine import GameEngine


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
                session["user_bank"] = user_data["bank"]
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
        state = game_engine.setup_new_game(username, session["bank"])
        state = game_engine.determine_blinds(state)

        active_games[username] = state
    
    state = active_games[username]

    if request.method=="POST":
        decision = request.form.get("decision")
        raise_amount = request.form.get("raise_amount",0,type=int)


        game_engine.run_betting_round(state, user_goes_first=True,decision=decision)

    return render_template("index.html", state=state)

if __name__ == "__main__":
    app.run(debug=True)

        