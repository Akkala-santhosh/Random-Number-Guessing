from flask import Flask, render_template, request, session, redirect, url_for
import random, sqlite3, datetime

app = Flask(__name__)
app.secret_key = "secret123"  # required for session management


# --- Create Database Table (runs once automatically) ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            attempts INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    message = ""
    if request.method == "POST":
        try:
            player_name = request.form["player_name"].strip()
            guess = int(request.form["guess"])
            session["attempts"] += 1

            if guess < session["number"]:
                message = f"{player_name}, Too low! Try again ⬆️"
            elif guess > session["number"]:
                message = f"{player_name}, Too high! Try again ⬇️"
            else:
                message = f"🎉 {player_name} guessed it right in {session['attempts']} attempts!"
                
                # Save player data to database
                conn = sqlite3.connect("database.db")
                c = conn.cursor()
                c.execute(
                    "INSERT INTO players (name, attempts, timestamp) VALUES (?, ?, ?)",
                    (player_name, session["attempts"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
                conn.close()

        except ValueError:
            message = "⚠️ Please enter a valid number!"

    return render_template("index.html", message=message, attempts=session.get("attempts", 0))


@app.route("/players")
def show_players():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT name, attempts, timestamp FROM players ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("players.html", players=data)


@app.route("/reset")
def reset():
    session.pop("number", None)
    session.pop("attempts", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
