# import animal class object
from animal import Animal

# import animal from inaturalist API, test with dictionary
api_animal = {"name": "Quokka",  "scientific_name": "Setonix brachyurus", "rank" : "species"}

# assign variable as newly created animal
quokka = Animal(api_animal["name"], api_animal["scientific_name"], api_animal["rank"])

# assign variable as the result of the animal class function
info = quokka.get_info()

# print result
print(info)