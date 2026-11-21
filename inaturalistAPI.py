
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


def search_species(observations, search_name):
    # convert search to lowercase and remove spaces
    search_name = search_name.strip().lower()

    # count sightings for each species
    species_count = {}

    for observation in observations:
        name = observation.animal.name.lower()

        if name in species_count:
            species_count[name] += 1
        else:
            species_count[name] = 1

    # find number of matching sightings
    count = species_count.get(search_name, 0)

    return count


def generate_map(observations):
    # create map centred on Rottnest Island
    wildlife_map = folium.Map(
        location=[-32, 115.50],
        zoom_start=11
    )

    # add a marker for each observation
    for observation in observations:
        popup = f"<b>{observation.animal.name}</b>"

        # add animal image if available
        if observation.image_urls:
            popup += (
                f'<p><img src="{observation.image_urls[0]}" '
                f'width="200"></p>'
            )

        folium.Marker(
            location=[
                observation.latitude,
                observation.longitude
            ],
            popup=folium.Popup(popup, max_width=250)
        ).add_to(wildlife_map)

    # save map as HTML
    wildlife_map.save("wilddex_map.html")

    print("WildDex map generated successfully!")

