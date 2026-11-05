# library imports
import requests, json

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
            print(f"Species: {result.get("species_guess")}")
            print(f"Scientific name: {result["taxon"]["name"]}")
            print(f"Taxonomic rank: {result["taxon"]["rank"]}")
            print(f"Observer: {result["user"]["login"]}")
            print(f"Date: {result.get("observed_on")}")
            print(f"Location: {result.get("place_guess")}")
            # change blank entries to something else
            print(f"Notes: {result.get('description') or 'No notes were added'}")
            print(f"Quality: {result.get("quality_grade")}")
            # store photos for now, will implement image display
            if result["photos"]:
                print(f"Image URL: {result['photos'][0]['url']}")
            else:
                print("No image available")
            print()
    print("----------------------------------")
# any errors? except will try to resolve
except requests.exceptions.RequestException:
    print("Connection or API error")
else:
    print("Connection successful!")
# finally always runs last 
finally:
    print("Connection over")