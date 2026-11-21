
# library imports
import os
from datetime import date as date_type

# import my local classes
from animal import Animal
from sighting import Sighting
from wilddex_manager import WildDexManager
from player_manager import PlayerManager

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
    player_manager = PlayerManager()

    while True:
        clear_screen()

        heading("WILDDEX - WILDLIFE DISCOVERY")

        print("  1. Retrieve wildlife observations")
        print("  2. Search for an animal")
        print("  3. Generate wildlife map")
        print("  4. View my sightings")
        print("  5. Add a sighting")
        print("  6. Delete a sighting")
        print("  7. Edit a sighting")
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

                    # add the sighting and award XP only if it was saved
                    previous_count = len(manager.sightings)

                    manager.add_sighting(sighting)

                    if len(manager.sightings) > previous_count:
                        player_manager.player.discover_animal(animal)

                        if player_manager.save_player():
                            print("Player progress saved!")
                        else:
                            print("Warning: Player progress could not be saved.")
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
        
        elif choice == "7":
            heading("EDIT WILDLIFE SIGHTING")

            if not manager.sightings:
                print("No sightings available to edit.")

            else:
                manager.view_sightings()

                try:
                    sighting_id = int(input("\nEnter sighting ID to edit: "))

                    selected = next(
                        (
                            s for s in manager.sightings
                            if s.sighting_id == sighting_id
                        ),
                        None
                    )

                    if selected is None:
                        print("Sighting not found.")

                    else:
                        print("\nPress Enter to keep the existing value.\n")

                        updates = {}

                        fields = {
                            "animal_name": selected.animal.name,
                            "scientific_name": selected.animal.scientific_name,
                            "image": selected.image,
                            "date": selected.date,
                            "latitude": selected.latitude,
                            "longitude": selected.longitude,
                            "notes": selected.notes
                        }

                        for field, current in fields.items():
                            new_value = input(
                                f"{field.replace('_', ' ').title()} [{current}]: "
                            ).strip()

                            if new_value:
                                if field in ("latitude", "longitude"):
                                    new_value = float(new_value)

                                    if field == "latitude" and not -90 <= new_value <= 90:
                                        raise ValueError("Latitude must be between -90 and 90.")

                                    if field == "longitude" and not -180 <= new_value <= 180:
                                        raise ValueError("Longitude must be between -180 and 180.")

                                elif field == "date":
                                    date_type.fromisoformat(new_value)

                                updates[field] = new_value

                        if updates:
                            manager.edit_sighting(sighting_id, updates)
                        else:
                            print("No changes made.")

                except ValueError as error:
                    print(f"Invalid input: {error}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

        pause()


if __name__ == "__main__":
    main()
