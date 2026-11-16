
from flask import Flask, render_template
import json

# load saved wildlife sightings
with open("sightings.json", "r") as file:
    sightings = json.load(file)

app = Flask(__name__)

# display player profile
@app.route("/")
def profile():

    # load saved player information
    with open("player.json", "r") as file:
        player = json.load(file)

    # send player information to HTML
    return render_template(
    "profile.html",
    player=player,
    sightings=sightings
)


# start Flask
if __name__ == "__main__":
    app.run(debug=True)
