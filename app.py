from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secret123"  # required for session management

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize a random number in session if not already present
    if "number" not in session:
        session["number"] = random.randint(1,10)
        session["attempts"] = 0

    message = ""
    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
            session["attempts"] += 1

            if guess < session["number"]:
                message = "Too low! Try again ⬆️"
            elif guess > session["number"]:
                message = "Too high! Try again ⬇️"
            else:
                message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
        except ValueError:
            message = "⚠️ Please enter a valid number!"

    return render_template("index.html", message=message, attempts=session["attempts"])

@app.route("/reset")
def reset():
    session.pop("number", None)
    session.pop("attempts", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

