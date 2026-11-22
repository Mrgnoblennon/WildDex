
# library imports
import os
from datetime import date as date_type

# import my local classes
from animal import Animal
from sighting import Sighting
from wilddex_manager import WildDexManager
from player_manager import PlayerManager
from locations import choose_location

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


def browse_observations(observations):
    if not observations:
        print("Please retrieve observations first.")
        return

    page = 0
    page_size = 5

    while True:
        clear_screen()
        heading("WILDLIFE OBSERVATIONS")

        start = page * page_size
        end = start + page_size
        current_page = observations[start:end]

        print(f"\nTotal observations: {len(observations)}")
        print(f"Showing {start + 1}-{min(end, len(observations))}\n")

        for number, observation in enumerate(current_page, start=start + 1):
            print(f"{number}. {observation.animal.name}")
            print(f"   Scientific name: {observation.animal.scientific_name}")
            print(f"   Observer: {observation.observer}")
            print(f"   Date: {observation.date}")
            print(f"   Location: {observation.location}")
            print("-" * 45)

        print("\n[N] Next page")
        print("[P] Previous page")
        print("[0] Return to menu")

        choice = input("\nSelect an option: ").strip().lower()

        if choice == "0":
            break
        elif choice == "n":
            if end < len(observations):
                page += 1
            else:
                print("Already on the last page.")
                pause()
        elif choice == "p":
            if page > 0:
                page -= 1
            else:
                print("Already on the first page.")
                pause()
        else:
            print("Invalid option.")
            pause()



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
        print("  8. View Player Profile")
        print("  9. Browse wildlife observations")
        print("  0. Exit")

        print("-" * 45)

        choice = input("Select an option: ").strip()

        clear_screen()

        if choice == "1":
            heading("RETRIEVE OBSERVATIONS")

            selected_location = choose_location()

            if selected_location is not None:
                name, latitude, longitude, radius = selected_location

                print(f"\nSearching for wildlife near {name}...")

                new_observations = fetch_observations(
                    latitude, longitude, radius
                )

                if new_observations:
                    observations = new_observations
                    print(f"\nLocation: {name}")
                    print(f"Retrieved {len(observations)} observations.")
                else:
                    observations = []
                    print("\nNo observations retrieved for this location.")

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

                    if count > 0:
                        shown = 0

                        for observation in observations:
                            if observation.animal.name.lower() == animal_name.lower():
                                print("-" * 45)
                                print(f"Animal: {observation.animal.name}")
                                print(f"Scientific name: {observation.animal.scientific_name}")
                                print(f"Observer: {observation.observer}")
                                print(f"Date: {observation.date}")
                                print(f"Location: {observation.location}")

                                shown += 1

                                if shown == 10:
                                    break

                        if count > 10:
                            print(f"\nShowing 10 of {count} matching observations.")

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


                    # add the sighting and check if it saved
                    if manager.add_sighting(sighting):

                        # remember player progress before awarding XP
                        player = player_manager.player

                        previous_xp = player.xp
                        previous_level = player.level
                        previous_discoveries = player.discovered_species.copy()

                        # award XP for discovering an animal
                        player.discover_animal(animal)

                        # save updated player progress
                        if player_manager.save_player():
                            print("Player progress saved!")

                        else:
                            # restore progress if saving fails
                            player.xp = previous_xp
                            player.level = previous_level
                            player.discovered_species = previous_discoveries

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

        elif choice == "8":
            heading("WILDDEX PLAYER PROFILE")

            # get the current player
            player = player_manager.player

            # display player information
            print(f"\nUsername: {player.username}")
            print(f"Level: {player.level}")
            print(f"XP: {player.xp}/100")

            print("-" * 45)

            # display wildlife statistics
            print(f"Species Discovered: {len(player.discovered_species)}")
            print(f"Total Sightings: {len(manager.sightings)}")

            print("-" * 45)

        elif choice == "9":
            browse_observations(observations)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

        pause()


if __name__ == "__main__":
    main()
