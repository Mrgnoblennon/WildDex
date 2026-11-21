
# import my local classes
from sighting import Sighting


class WildDexManager:
    def __init__(self):
        # store the user's wildlife sightings
        self.sightings = []

    def add_sighting(self, sighting):
        # check that the object is a Sighting
        if not isinstance(sighting, Sighting):
            print("Invalid sighting.")
            return

        # add sighting to the collection
        self.sightings.append(sighting)

        print("Sighting added successfully!")
