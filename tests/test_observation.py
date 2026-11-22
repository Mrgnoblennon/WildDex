from animal import Animal
from observation import Observation 

quokka = Animal("Quokka","Setonix brachyurus", "species")

observation = Observation(quokka, "Chase", "Sunday", "Rottnest Island")

info = observation.get_info()

print(info)