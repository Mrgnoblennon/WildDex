from player import Player

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