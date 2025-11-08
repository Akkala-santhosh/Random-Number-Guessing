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