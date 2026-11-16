
from animal import Animal
from sighting import Sighting
import json

# store all sightings
sightings = {}
next_id = 1

# create animals
quokka = Animal(123, "Quokka", "Setonix brachyurus", "species")
dugite = Animal(456, "Rottnest Island Dugite", "Pseudonaja affinis", "species")
tern = Animal(789, "Crested Tern", "Thalasseus bergii", "species")

# create first sighting
new_sighting = Sighting(
    next_id,
    quokka,
    "https://example.com/quokka.jpg",
    "2026-11-16",
    -31.9965,
    115.5404,
    "Quokka spotted near Thomson Bay"
)

# store sighting and increase ID
sightings[next_id] = new_sighting
next_id += 1

# create second sighting
new_sighting_2 = Sighting(
    next_id,
    dugite,
    "https://example.com/dugite.jpg",
    "2026-11-16",
    -32.0078,
    115.5182,
    "Dugite spotted near Wadjemup Lighthouse"
)

# store sighting and increase ID
sightings[next_id] = new_sighting_2
next_id += 1

# create third sighting
new_sighting_3 = Sighting(
    next_id,
    tern,
    "https://example.com/tern.jpg",
    "2026-11-16",
    -31.9898,
    115.5355,
    "Crested tern spotted near The Basin"
)

# store sighting and increase ID
sightings[next_id] = new_sighting_3
next_id += 1

# display all sightings
for sighting in sightings.values():
    print(sighting.get_info())

# search for a specific sighting
search_id = 2

try:
    print(sightings[search_id].get_info())
except KeyError:
    print("Sighting not found.")

# create a list to save all sightings
sightings_data = []

# convert each sighting into a dictionary
for sighting in sightings.values():
    sighting_data = {
        "id": sighting.sighting_id,
        "animal_id": sighting.animal.id,
        "animal_name": sighting.animal.name,
        "scientific_name": sighting.animal.scientific_name,
        "rank": sighting.animal.rank,
        "image": sighting.image,
        "date": sighting.date,
        "latitude": sighting.latitude,
        "longitude": sighting.longitude,
        "notes": sighting.notes
    }

    # add dictionary to the list
    sightings_data.append(sighting_data)

# save all sightings to JSON
with open("sightings.json", "w") as file:
    json.dump(sightings_data, file, indent=4)

# load saved sightings from JSON
with open("sightings.json", "r") as file:
    loaded_data = json.load(file)

# display loaded sightings
for sighting in loaded_data:
    print(sighting)
