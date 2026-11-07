# library imports
import requests

# import my local classes
from animal import Animal
from observation import Observation

# api url
url = "https://api.inaturalist.org/v1/observations"

# added arguments to change data retrieval
params = {
    "taxon_id": 1,
    "per_page": 200,
    # perth co-ordinates
    "lat": -32,
    "lng": 115.50,
    "radius": 7,
}

# try, except and finally are used for error handling, tries to prevent program crashes
try:
    print("Connection started...")

    # keep collection of each individual observation object
    observations = []


    # use request class to pull data from inaturalist, set params to params dictionary above
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    # format data so python can understand and assign it data
    data = response.json()
    print("----------------------------------")
    # iterate through data specifically the 'results' array and find the following data
    for result in data["results"]:
        # dont print blank or none entries as well as empty taxon data
        if result["species_guess"] is not None and result.get("taxon") is not None:
            # the following lines of code are set to grab specified data 
            print()
            # navigating through a returned api data object is insane, names like species guest and taxon are tough
            new_animal = Animal(result.get("species_guess"), result["taxon"]["name"], result["taxon"]["rank"])
            new_observation = Observation(new_animal, result["user"]["login"], result.get("observed_on"), result.get("place_guess"))

            observations.append(new_observation)

    print("----------------------------------")

    species_count = {}
    # i want observations based on chosen animal name
    
    for observation in observations:
        name = observation.animal.name

        if name in species_count:
            # increase existing animal count
            species_count[name] += 1
        else:
            # if animal not established yet add it then set its count to 1
            species_count[name] = 1
    
    # print animal species counts and highest animal count
    highest_count = 0
    highest_name = ""
    for animal_count in species_count:
        print(f"Species: {animal_count} | Sightings: {species_count[animal_count]}")
        if species_count[animal_count] > highest_count:
            highest_count = species_count[animal_count]
            highest_name = animal_count

    print(f"There have mostly been sightings of {highest_name} | sighted: {highest_count}")

    count = species_count.get("Quokka", 0)

    # because the observations list isnt empty, count assigned to correct no found 
    if count == 0:
        print(f"There aren't any recent sightings of Quokka in the area.")
    else:
        print(f"Quokka sightings found: {count}")
            
# any errors? except will try to resolve
except requests.exceptions.RequestException:
    print("Connection or API error")
else:
    print("Connection successful!")
# finally always runs last 
finally:
    print("Connection over")