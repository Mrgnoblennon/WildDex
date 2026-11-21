
# library imports
import json
from pathlib import Path

# import my local classes
from animal import Animal
from sighting import Sighting


class WildDexManager:
    def __init__(self):
        # store the user's wildlife sightings
        self.sightings = []

        # JSON file in the WildDex project folder
        self.file_path = Path(__file__).resolve().parent / "sightings.json"

        # load previously saved sightings
        self.load_sightings()

    def add_sighting(self, sighting):
        # check that the object is a Sighting
        if not isinstance(sighting, Sighting):
            print("Invalid sighting.")
            return

        # check for duplicate sighting IDs
        for existing in self.sightings:
            if existing.sighting_id == sighting.sighting_id:
                print("A sighting with this ID already exists.")
                return

        # add sighting to the collection
        self.sightings.append(sighting)

        # save updated collection
        if self.save_sightings():
            print("Sighting added successfully!")
        else:
            self.sightings.remove(sighting)
            print("Sighting was not added.")

    def view_sightings(self):
        # check if there are any sightings
        if not self.sightings:
            print("No wildlife sightings recorded.")
            return

        # display each recorded sighting
        print("\n===== MY WILDLIFE SIGHTINGS =====")

        for sighting in self.sightings:
            print(sighting.get_info())

    def save_sightings(self):
        # convert Sighting objects into dictionaries
        data = []

        for sighting in self.sightings:
            data.append({
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
            })

        try:
            # write to a temporary file first
            temporary_file = self.file_path.with_suffix(".json.tmp")

            with open(temporary_file, "w") as file:
                json.dump(data, file, indent=4)

            # replace original only after writing succeeds
            temporary_file.replace(self.file_path)
            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"Error saving sightings: {error}")
            return False

    def load_sightings(self):
        # check whether the JSON file exists
        if not self.file_path.exists():
            print("No saved sightings file found.")
            return

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Sightings JSON must contain a list.")

            loaded_sightings = []

            for item in data:
                # recreate the Animal object
                animal = Animal(
                    item["animal_id"],
                    item["animal_name"],
                    item["scientific_name"],
                    item["rank"]
                )

                # recreate the Sighting object
                sighting = Sighting(
                    item["id"],
                    animal,
                    item["image"],
                    item["date"],
                    item["latitude"],
                    item["longitude"],
                    item.get("notes", "")
                )

                loaded_sightings.append(sighting)

            self.sightings = loaded_sightings
            print(f"Loaded {len(self.sightings)} saved sightings.")

        except (OSError, json.JSONDecodeError, KeyError,
                TypeError, ValueError) as error:
            print(f"Error loading sightings: {error}")
