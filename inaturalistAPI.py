
# library imports
import requests
import folium

# import my local classes
from animal import Animal
from observation import Observation

# api url
url = "https://api.inaturalist.org/v1/observations"

# added arguments to change data retrieval
params = {
    "taxon_id": 1,
    "per_page": 200,
    # rotto co-ordinates
    "lat": -32,
    "lng": 115.50,
    "radius": 7,
}


def fetch_observations():
    # keep collection of each individual observation object
    observations = []

    try:
        print("Connection started...")

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for result in data["results"]:
            if (
                result.get("species_guess") is not None
                and result.get("taxon") is not None
                and result.get("geojson") is not None
            ):
                coordinates = result["geojson"]["coordinates"]
                latitude = coordinates[1]
                longitude = coordinates[0]

                new_animal = Animal(
                    result["taxon"]["id"],
                    result.get("species_guess"),
                    result["taxon"]["name"],
                    result["taxon"]["rank"]
                )

                image_urls = []

                for photo in result.get("photos", []):
                    image_url = photo["url"].replace("square", "large")
                    image_urls.append(image_url)

                new_observation = Observation(
                    new_animal,
                    result.get("user", {}).get("login", "Unknown"),
                    result.get("observed_on"),
                    result.get("place_guess"),
                    latitude,
                    longitude,
                    image_urls
                )

                observations.append(new_observation)

    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError, IndexError) as error:
        print(f"Connection or API data error: {error}")

    else:
        print("Connection successful!")

    finally:
        print("Connection over")

    return observations
