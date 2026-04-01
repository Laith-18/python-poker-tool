from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "poker"

@app.route("/")
def home():
    if request.method == "POST":
        return "BUTTON CLICKED"
    
    return """
    <form method="POST">
        <button type="submit">Click me</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
