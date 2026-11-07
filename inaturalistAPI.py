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
    "per_page": 50,
    # perth co-ordinates
    "lat": -31.95,
    "lng": 115.86,
    "radius": 20,
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
        # dont print blank or none entries
        if result["species_guess"] is not None:
            # the following lines of code are set to grab specified data 
            print()
            # navigating through a returned api data object is insane, names like species guest and taxon are tough
            new_animal = Animal(result.get("species_guess"), result["taxon"]["name"], result["taxon"]["rank"])
            new_observation = Observation(new_animal, result["user"]["login"], {result.get("observed_on")}, {result.get("place_guess")})

            observations.append(new_observation)

    print("----------------------------------")


# any errors? except will try to resolve
except requests.exceptions.RequestException:
    print("Connection or API error")
else:
    print("Connection successful!")
# finally always runs last 
finally:
    print("Connection over")