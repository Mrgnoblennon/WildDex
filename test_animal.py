# import animal class object
from animal import Animal
import os

os.system("clear")

# import animal from inaturalist API, test with dictionary
api_animal = [
  {"name": "Quokka",  "scientific_name": "Setonix brachyurus", "rank" : "species"},
  {"name": "Wombat",  "scientific_name": "Vombatus ursinus", "rank" : "species"},
  {"name": "Koala",  "scientific_name": "Phascolarctos cinereus", "rank" : "species"}
]

# container for newly created animals
animals = []
# create new animals list with for loop
for animal in api_animal:
  # assign variable as newly created animal
  new_animal = Animal(animal["name"], animal["scientific_name"], animal["rank"])
  # assign variable as the result of the animal class function
  info = new_animal.get_info()
  print(info)
  # add newly created animal to animals list
  animals.append(new_animal)



