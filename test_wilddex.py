
# library imports
import unittest

# import my local classes
from animal import Animal
from player import Player


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


if __name__ == "__main__":
    unittest.main()
