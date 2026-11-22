
# library imports
import unittest

# import my local classes
from animal import Animal
from player import Player

import tempfile
from pathlib import Path
from wilddex_manager import WildDexManager
from sighting import Sighting

import requests
from unittest.mock import patch, Mock
from inaturalistAPI import fetch_observations, search_species

class TestAnimal(unittest.TestCase):

    def test_animal_attributes(self):
        # create an animal
        animal = Animal(
            1,
            "Quokka",
            "Setonix brachyurus",
            "species"
        )

        # check the animal's attributes
        self.assertEqual(animal.id, 1)
        self.assertEqual(animal.name, "Quokka")
        self.assertEqual(animal.scientific_name, "Setonix brachyurus")
        self.assertEqual(animal.rank, "species")

    def test_animal_get_info(self):
        animal = Animal(
            1,
            "Quokka",
            "Setonix brachyurus",
            "species"
        )

        expected = "1, Quokka, Setonix brachyurus, species"

        self.assertEqual(animal.get_info(), expected)


class TestPlayer(unittest.TestCase):

    def test_player_creation(self):
        # create a new player
        player = Player("Explorer")

        self.assertEqual(player.username, "Explorer")
        self.assertEqual(player.xp, 0)
        self.assertEqual(player.level, 1)
        self.assertEqual(player.discovered_species, set())

    def test_gain_xp(self):
        player = Player("Explorer")

        player.gain_xp(50)

        self.assertEqual(player.xp, 50)
        self.assertEqual(player.level, 1)

    def test_level_up(self):
        player = Player("Explorer")

        player.gain_xp(120)

        self.assertEqual(player.level, 2)
        self.assertEqual(player.xp, 20)

    def test_new_species_discovery(self):
        player = Player("Explorer")
        animal = Animal(1, "Quokka", "Setonix brachyurus", "species")

        player.discover_animal(animal)

        self.assertEqual(player.xp, 50)
        self.assertIn(1, player.discovered_species)

    def test_repeat_species_discovery(self):
        player = Player("Explorer")
        animal = Animal(1, "Quokka", "Setonix brachyurus", "species")

        player.discover_animal(animal)
        player.discover_animal(animal)

        self.assertEqual(player.xp, 60)
        self.assertEqual(len(player.discovered_species), 1)


class TestWildDexManager(unittest.TestCase):

    def setUp(self):
        # create a temporary folder for test data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "sightings.json"

        # create manager without loading real sightings
        self.manager = WildDexManager.__new__(WildDexManager)
        self.manager.sightings = []
        self.manager.file_path = self.file_path

        # create a test animal and sighting
        self.animal = Animal(
            1, "Quokka", "Setonix brachyurus", "species"
        )

        self.sighting = Sighting(
            1,
            self.animal,
            "quokka.jpg",
            "2026-11-22",
            -31.995,
            115.54,
            "Test sighting"
        )

    def tearDown(self):
        # delete temporary test files
        self.temp_dir.cleanup()

    def test_add_sighting(self):
        self.manager.add_sighting(self.sighting)

        self.assertEqual(len(self.manager.sightings), 1)
        self.assertEqual(self.manager.sightings[0].animal.name, "Quokka")

    def test_save_and_load(self):
        self.manager.add_sighting(self.sighting)

        # create another manager using the same test file
        new_manager = WildDexManager.__new__(WildDexManager)
        new_manager.sightings = []
        new_manager.file_path = self.file_path

        new_manager.load_sightings()

        self.assertEqual(len(new_manager.sightings), 1)
        self.assertEqual(new_manager.sightings[0].animal.name, "Quokka")

    def test_duplicate_id(self):
        self.manager.add_sighting(self.sighting)
        self.manager.add_sighting(self.sighting)

        self.assertEqual(len(self.manager.sightings), 1)

    def test_edit_sighting(self):
        self.manager.add_sighting(self.sighting)

        result = self.manager.edit_sighting(
            1, {"animal_name": "Updated Quokka"}
        )

        self.assertTrue(result)
        self.assertEqual(
            self.manager.sightings[0].animal.name,
            "Updated Quokka"
        )

    def test_delete_sighting(self):
        self.manager.add_sighting(self.sighting)

        result = self.manager.delete_sighting(1)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.sightings), 0)

    def test_delete_nonexistent_sighting(self):
        result = self.manager.delete_sighting(999)

        self.assertFalse(result)
        self.assertEqual(len(self.manager.sightings), 0)


    def test_invalid_latitude(self):
        self.sighting.latitude = 200

        result = self.manager.add_sighting(self.sighting)

        self.assertFalse(result)
        self.assertEqual(len(self.manager.sightings), 0)

    def test_invalid_date(self):
        self.sighting.date = "2026-99-99"

        result = self.manager.add_sighting(self.sighting)

        self.assertFalse(result)
        self.assertEqual(len(self.manager.sightings), 0)

    def test_empty_animal_name(self):
        self.sighting.animal.name = ""

        result = self.manager.add_sighting(self.sighting)

        self.assertFalse(result)
        self.assertEqual(len(self.manager.sightings), 0)


    def test_edit_invalid_latitude(self):
        self.manager.add_sighting(self.sighting)

        result = self.manager.edit_sighting(
            1, {"latitude": 200}
        )

        self.assertFalse(result)
        self.assertEqual(
            self.manager.sightings[0].latitude,
            -31.995
        )

    def test_edit_invalid_date(self):
        self.manager.add_sighting(self.sighting)

        result = self.manager.edit_sighting(
            1, {"date": "2026-99-99"}
        )

        self.assertFalse(result)
        self.assertEqual(
            self.manager.sightings[0].date,
            "2026-11-22"
        )

    def test_edit_empty_animal_name(self):
        self.manager.add_sighting(self.sighting)

        result = self.manager.edit_sighting(
            1, {"animal_name": ""}
        )

        self.assertFalse(result)
        self.assertEqual(
            self.manager.sightings[0].animal.name,
            "Quokka"
        )


class TestINaturalistAPI(unittest.TestCase):

    def setUp(self):
        # sample API response for testing
        self.sample_data = {
            "results": [
                {
                    "species_guess": "Quokka",
                    "taxon": {
                        "id": 1,
                        "name": "Setonix brachyurus",
                        "rank": "species"
                    },
                    "geojson": {
                        "coordinates": [115.54, -31.995]
                    },
                    "photos": [
                        {
                            "url": "https://example.com/square.jpg"
                        }
                    ],
                    "user": {
                        "login": "test_user"
                    },
                    "observed_on": "2026-11-22",
                    "place_guess": "Rottnest Island"
                }
            ]
        }

    @patch("inaturalistAPI.requests.get")
    def test_fetch_observations(self, mock_get):
        # simulate a successful API response
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response

        observations = fetch_observations()

        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0].animal.name, "Quokka")
        self.assertEqual(observations[0].observer, "test_user")

    @patch("inaturalistAPI.requests.get")
    def test_api_connection_failure(self, mock_get):
        # simulate a failed connection
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        observations = fetch_observations()

        self.assertEqual(observations, [])

    @patch("inaturalistAPI.requests.get")
    def test_missing_species(self, mock_get):
        # simulate an observation without a species name
        data = {
            "results": [
                {
                    "species_guess": None,
                    "taxon": None,
                    "geojson": None
                }
            ]
        }

        mock_response = Mock()
        mock_response.json.return_value = data
        mock_get.return_value = mock_response

        observations = fetch_observations()

        self.assertEqual(len(observations), 0)

    def test_search_species(self):
        # create a sample observation
        from observation import Observation

        animal = Animal(
            1,
            "Quokka",
            "Setonix brachyurus",
            "species"
        )

        observation = Observation(
            animal,
            "test_user",
            "2026-11-22",
            "Rottnest Island",
            -31.995,
            115.54,
            []
        )

        observations = [observation, observation]

        # search should ignore capitalisation and spaces
        count = search_species(observations, "  QUOKKA  ")

        self.assertEqual(count, 2)
        self.assertEqual(
            search_species(observations, "Kangaroo"),
            0
        )



if __name__ == "__main__":
    unittest.main()
