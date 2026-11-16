
from flask import Flask, render_template, request, redirect
from animal import Animal
from sighting import Sighting
from player import Player
import json

app = Flask(__name__)


# player profile
@app.route("/")
def profile():
    with open("player.json", "r") as file:
        player = json.load(file)

    with open("sightings.json", "r") as file:
        sightings = json.load(file)

    return render_template(
        "profile.html",
        player=player,
        sightings=sightings
    )

# wildlife sightings
@app.route("/sightings", methods=["GET", "POST"])
def view_sightings():
    with open("sightings.json", "r") as file:
        sightings = json.load(file)

    if request.method == "POST":
        animal = Animal(
            int(request.form["animal_id"]),
            request.form["animal_name"],
            request.form["scientific_name"],
            "species"
        )

        sighting_id = max(
            (s["id"] for s in sightings),
            default=0
        ) + 1

        sighting = Sighting(
            sighting_id,
            animal,
            request.form["image"],
            request.form["date"],
            float(request.form["latitude"]),
            float(request.form["longitude"]),
            request.form["notes"]
        )

        sightings.append({
            "id": sighting.sighting_id,
            "animal_id": animal.id,
            "animal_name": animal.name,
            "scientific_name": animal.scientific_name,
            "rank": animal.rank,
            "image": sighting.image,
            "date": sighting.date,
            "latitude": sighting.latitude,
            "longitude": sighting.longitude,
            "notes": sighting.notes
        })

        with open("sightings.json", "w") as file:
            json.dump(sightings, file, indent=4)

        with open("player.json", "r") as file:
            player_data = json.load(file)

        player = Player(player_data["username"])
        player.level = player_data["level"]
        player.xp = player_data["xp"]
        player.discovered_species = set(
            player_data["discovered_species"]
        )

        player.discover_animal(animal)

        with open("player.json", "w") as file:
            json.dump({
                "username": player.username,
                "level": player.level,
                "xp": player.xp,
                "discovered_species": list(player.discovered_species)
            }, file, indent=4)

        return redirect("/sightings")

    return render_template(
        "sightings.html",
        sightings=sightings
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
