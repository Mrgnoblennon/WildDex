
# library imports
import requests
import folium
from pathlib import Path

# import my local classes
from animal import Animal
from observation import Observation

# api url
url = "https://api.inaturalist.org/v1/observations"

# added arguments to change data retrieval
params = {
    "taxon_id": 1,
    "per_page": 200,
    "lat": -31.9965,
    "lng": 115.5404,
    "radius": 7
}



def fetch_observations(latitude=-31.9965, longitude=115.5404, radius=7):
    # keep collection of each individual observation object
    observations = []
    search_params = params.copy()
    search_params["lat"] = latitude
    search_params["lng"] = longitude
    search_params["radius"] = radius
    try:
        print("Connection started...")

        response = requests.get(url, params=search_params, timeout=10)
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

                groups = {
                    "Aves": "Birds",
                    "Mammalia": "Mammals",
                    "Reptilia": "Reptiles",
                    "Amphibia": "Amphibians",
                    "Insecta": "Insects",
                    "Arachnida": "Arachnids",
                    "Actinopterygii": "Fish",
                    "Mollusca": "Molluscs",
                    "Plantae": "Plants",
                    "Fungi": "Fungi"
                }

                iconic_group = result["taxon"].get(
                    "iconic_taxon_name"
                )

                new_animal.group = groups.get(
                    iconic_group, "Other"
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
    # centre map around the retrieved observations
    first = observations[0]

    wildlife_map = folium.Map(
        location=[first.latitude, first.longitude],
        zoom_start=10
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
    output_folder = Path(__file__).resolve().parent / "generated"
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "wilddex_map.html"
    wildlife_map.save(str(output_file))
    print("WildDex map generated successfully!")


def main():
    # retrieve observations from iNaturalist
    observations = fetch_observations()

    # check if observations were retrieved
    if not observations:
        print("No observations found.")
        return

    # display retrieved observations
    print("----------------------------------")

    for observation in observations:
        print(
            f"ID: {observation.animal.id}, "
            f"Name: {observation.animal.name} | "
            f"Lat: {observation.latitude}, "
            f"Long: {observation.longitude}"
        )

    print("----------------------------------")
    print(f"Total observations: {len(observations)}")

    # generate wildlife map
    generate_map(observations)


if __name__ == "__main__":
    main()


