from player import Player
import json

# create player
player = Player("Chase")

# display starting stats
print(player.get_info())

# award XP for wildlife sightings
player.gain_xp(40)
print(player.get_info())

player.gain_xp(75)
print(player.get_info())

player.gain_xp(200)
print(player.get_info())
from player import Player
from animal import Animal

# create player
player = Player("Chase")

# create Rottnest animals
quokka = Animal(123, "Quokka", "Setonix brachyurus", "species")
dugite = Animal(456, "Rottnest Island Dugite", "Pseudonaja affinis", "species")
tern = Animal(789, "Crested Tern", "Thalasseus bergii", "species")

# discover a quokka for the first time
player.discover_animal(quokka)

# spot another quokka
player.discover_animal(quokka)

# discover two more species
player.discover_animal(dugite)
player.discover_animal(tern)

# display player stats
print(player.get_info())

# display total unique species discovered
print("Species discovered:", len(player.discovered_species))

# store player information
player_data = {
    "username": player.username,
    "level": player.level,
    "xp": player.xp,
    "discovered_species": list(player.discovered_species)
}

# create and save player.json
with open("player.json", "w") as file:
    json.dump(player_data, file, indent=2)

# load saved player data
with open("player.json", "r") as file:
    loaded_data = json.load(file)

# recreate player using saved data
restored_player = Player(loaded_data["username"])

restored_player.level = loaded_data["level"]
restored_player.xp = loaded_data["xp"]
restored_player.discovered_species = set(loaded_data["discovered_species"])

# display restored player
print(restored_player.get_info())
print("Discovered species:", restored_player.discovered_species)

# read saved player data
with open("player.json", "r") as file:
    loaded_data = json.load(file)

# recreate player from saved data
restored_player = Player(loaded_data["username"])

restored_player.level = loaded_data["level"]
restored_player.xp = loaded_data["xp"]
restored_player.discovered_species = set(loaded_data["discovered_species"])

# display restored player
print(restored_player.get_info())
print("Species discovered:", len(restored_player.discovered_species))