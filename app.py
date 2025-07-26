from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

nba = pd.read_csv('nba_players.csv')


def find_player(player_name):
    # Turn player name into lower case
    name_lowercase = player_name.lower()
    
    # Filter rows where the 'NAME' column matches the input
    result = nba[nba['NAME'].str.lower() == name_lowercase]

    # Return the first match as a dictionary
    if not result.empty:
        return result.iloc[0].to_dict()  
    else:
        return "Player not found"


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        playername = request.form["player"]
        player = find_player(playername)
        lebron = find_player('Lebron James')
        return render_template("base.html", player=player, lebron=lebron)
        # return redirect(url_for("user", usr=playername))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    player = find_player(usr)
    return f"<h1> {player} </h1>"

if __name__ == "__main__":
    app.run(debug=True)
