class Player:
    def __init__(self, username):
        self.username = username
        self.xp = 0
        self.level = 1

        # store unique animal IDs
        self.discovered_species = set()

    # give player XP and check for level up
    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= 100:
            self.xp -= 100
            self.level += 1

    # award XP for spotting an animal
    def discover_animal(self, animal):
        if animal.id not in self.discovered_species:
            self.discovered_species.add(animal.id)
            self.gain_xp(50)
            print(f"New discovery: {animal.name} (+50 XP)")
        else:
            self.gain_xp(10)
            print(f"Another {animal.name} spotted (+10 XP)")

    # display player information
    def get_info(self):
        return f"{self.username} | Level: {self.level} | XP: {self.xp}/100"