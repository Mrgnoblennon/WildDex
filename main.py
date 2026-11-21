
# library imports
import os
from datetime import date as date_type

# import my local classes
from animal import Animal
from sighting import Sighting
from wilddex_manager import WildDexManager

# import API functions
from inaturalistAPI import fetch_observations, search_species, generate_map


def clear_screen():
    # clear the terminal on Mac
    os.system("clear")


def pause():
    # wait before returning to the menu
    input("\nPress Enter to continue...")


def heading(title):
    # display a consistent heading
    print("\n" + "=" * 45)
    print(f"  {title}")
    print("=" * 45)


def main():
    # store observations retrieved from iNaturalist
    observations = []

    # load saved personal sightings
    manager = WildDexManager()

    while True:
        clear_screen()

        heading("WILDDEX - WILDLIFE DISCOVERY")

        print("  1. Retrieve wildlife observations")
        print("  2. Search for an animal")
        print("  3. Generate wildlife map")
        print("  4. View my sightings")
        print("  5. Add a sighting")
        print("  6. Delete a sighting")
        print("  0. Exit")

        print("-" * 45)

        choice = input("Select an option: ").strip()

        clear_screen()

        if choice == "1":
            heading("RETRIEVE OBSERVATIONS")

            observations = fetch_observations()

            print(f"\nRetrieved {len(observations)} observations.")

        elif choice == "2":
            heading("SEARCH FOR AN ANIMAL")

            if not observations:
                print("Please retrieve observations first.")

            else:
                animal_name = input("Enter animal name: ").strip()

                if not animal_name:
                    print("Please enter an animal name.")

                else:
                    count = search_species(observations, animal_name)

                    print(f"\nMatching sightings: {count}")

        elif choice == "3":
            heading("GENERATE WILDLIFE MAP")

            if not observations:
                print("Please retrieve observations first.")

            else:
                generate_map(observations)

        elif choice == "4":
            heading("MY WILDLIFE SIGHTINGS")

            manager.view_sightings()

        elif choice == "5":
            heading("ADD WILDLIFE SIGHTING")

            try:
                # generate a unique sighting ID
                sighting_id = max(
                    (s.sighting_id for s in manager.sightings),
                    default=0
                ) + 1

                animal_id = int(input("Animal ID: "))
                animal_name = input("Animal name: ").strip()
                scientific_name = input("Scientific name: ").strip()
                image = input("Image filename or URL: ").strip()
                sighting_date = input("Date (YYYY-MM-DD): ").strip()
                latitude = float(input("Latitude: "))
                longitude = float(input("Longitude: "))
                notes = input("Notes: ").strip()

                # validate required fields
                if not animal_name or not scientific_name or not sighting_date:
                    print("\nAnimal name, scientific name and date are required.")

                elif not -90 <= latitude <= 90:
                    print("\nLatitude must be between -90 and 90.")

                elif not -180 <= longitude <= 180:
                    print("\nLongitude must be between -180 and 180.")

                else:
                    # validate the date format
                    date_type.fromisoformat(sighting_date)

                    # create Animal object
                    animal = Animal(
                        animal_id,
                        animal_name,
                        scientific_name,
                        "species"
                    )

                    # create Sighting object
                    sighting = Sighting(
                        sighting_id,
                        animal,
                        image,
                        sighting_date,
                        latitude,
                        longitude,
                        notes
                    )

                    # add and save the sighting
                    manager.add_sighting(sighting)

            except ValueError:
                print("\nInvalid input. Check your numbers and date format.")
        
        elif choice == "6":
            heading("DELETE WILDLIFE SIGHTING")

            if not manager.sightings:
                print("No sightings available to delete.")

            else:
                manager.view_sightings()

                try:
                    sighting_id = int(input("\nEnter sighting ID to delete: "))

                    # find the selected sighting
                    selected = None

                    for sighting in manager.sightings:
                        if sighting.sighting_id == sighting_id:
                            selected = sighting
                            break

                    if selected is None:
                        print("Sighting not found.")

                    else:
                        print(f"\nSelected: {selected.animal.name}")

                        confirmation = input(
                            "Are you sure you want to delete this sighting? (y/n): "
                        ).strip().lower()

                        if confirmation == "y":
                            manager.delete_sighting(sighting_id)
                        else:
                            print("Deletion cancelled.")

                except ValueError:
                    print("Please enter a valid sighting ID.")


        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

        pause()


if __name__ == "__main__":
    main()
