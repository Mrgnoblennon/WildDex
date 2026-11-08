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
        if result["species_guess"] is not None and result.get("taxon") is not None and result.get("geojson") is not None:
            
            # latitude longitude data stored here
            coordinates = result["geojson"]["coordinates"]

            latitude = coordinates[1]
            longitude = coordinates[0]

            # the following lines of code are set to grab specified data 
            print()
            # navigating through a returned api data object is insane, names like species guest and taxon are tough
            new_animal = Animal(result.get("species_guess"), result["taxon"]["name"], result["taxon"]["rank"])
            new_observation = Observation(new_animal, result["user"]["login"], result.get("observed_on"), result.get("place_guess"), latitude, longitude)

            observations.append(new_observation)
    print("----------------------------------")


    # check if process worked. remove when done
    for observation in observations:
        print(f"Name: {observation.animal.name} | Lat: {observation.latitude}, Long: {observation.longitude}")




    species_count = {}
    # i want observations based on chosen animal name
    for observation in observations:
        # makes searches more consistent
        name = observation.animal.name.lower()

        if name in species_count:
            # increase existing animal count
            species_count[name] += 1
        else:
            # if animal not established yet add it then set its count to 1
            species_count[name] = 1
    
    # print animal species counts and highest animal count
    highest_count = 0
    highest_name = ""

    # check for animal who's count is highest by name
    for animal_count in species_count:
        #print(f"Species: {animal_count} | Sightings: {species_count[animal_count]}")
        if species_count[animal_count] > highest_count:
            highest_count = species_count[animal_count]
            highest_name = animal_count

    #print(f"There have mostly been sightings of {highest_name} | sighted: {highest_count}")

    # remove white space and lowercase the user input
    search_name = input("What animal are you searching for? ").strip().lower()

    search_name.lower()

    # get user input, retrive key from the species count dictionary with value, 
    count = species_count.get(search_name, 0)


    if search_name.strip() == "":
        print("That animal does not exist.")
    # because the observations list isnt empty, count assigned to correct no found 
    elif count == 0:
        print(f"There aren't any recent sightings of {search_name} in the area.")
    else:
        print(f"{search_name} sightings found: {count}")
            
# any errors? except will try to resolve
except requests.exceptions.RequestException:
    print("Connection or API error")
else:
    print("Connection successful!")
# finally always runs last 
finally:
    print("Connection over")