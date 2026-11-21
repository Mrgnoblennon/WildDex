
# library imports
import json
from pathlib import Path

# import my local class
from player import Player


class PlayerManager:
    def __init__(self):
        # player data stored in the project folder
        self.file_path = Path(__file__).resolve().parent / "player.json"

        # load the existing player
        self.player = self.load_player()

    def load_player(self):
        # create a default player
        player = Player("Explorer")

        if not self.file_path.exists():
            return player

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)

            # restore saved player progress
            player.username = data["username"]
            player.level = data["level"]
            player.xp = data["xp"]
            player.discovered_species = set(
                data["discovered_species"]
            )

            return player

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Error loading player: {error}")
            return player

    def save_player(self):
        # convert player data into a dictionary
        data = {
            "username": self.player.username,
            "level": self.player.level,
            "xp": self.player.xp,
            "discovered_species": list(
                self.player.discovered_species
            )
        }

        try:
            # write to a temporary file first
            temporary_file = self.file_path.with_suffix(".json.tmp")

            with open(temporary_file, "w") as file:
                json.dump(data, file, indent=4)

            temporary_file.replace(self.file_path)
            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"Error saving player: {error}")
            return False
