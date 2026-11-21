
# import my local classes
from animal import Animal
from sighting import Sighting
from wilddex_manager import WildDexManager

# create the manager
manager = WildDexManager()

# create an animal object
animal = Animal(
    1,
    "Quokka",
    "Setonix brachyurus",
    "species"
)

# create a sighting object
sighting = Sighting(
    1,
    animal,
    "quokka.jpg",
    "2026-11-21",
    -31.995,
    115.54,
    "Spotted near the beach"
)

# add the sighting
manager.add_sighting(sighting)

# display all sightings
manager.view_sightings()
