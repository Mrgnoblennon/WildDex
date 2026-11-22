import os
from datetime import date as date_type

import questionary

from animal import Animal
from sighting import Sighting
from wilddex_manager import WildDexManager
from player_manager import PlayerManager
from locations import LOCATIONS
from inaturalistAPI import fetch_observations, search_species, generate_map
from conservation import get_conservation_status
from species_info import display_species_info


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to return...")


def heading(title):
    print("\n" + "=" * 48)
    print(f"  {title}")
    print("=" * 48)


def select_menu(title, options):
    """Select an option with arrow keys; Back returns None."""
    back_value = "__wilddex_back__"
    choices = [
        questionary.Choice(
            title=label,
            value=back_value if value is None else value
        )
        for label, value in options
    ]
    result = questionary.select(
        title, choices=choices, use_shortcuts=False
    ).ask()
    return None if result in (None, back_value) else result


def choose_location():
    """Choose an Australian state, then a wildlife location."""
    while True:
        clear_screen()
        heading("CHOOSE A STATE OR TERRITORY")
        state = select_menu(
            "Choose a state (select Back to return)",
            [(name, name) for name in LOCATIONS] + [("Back", None)],
        )
        if state is None:
            return None
        clear_screen()
        heading(state.upper())
        location = select_menu(
            "Choose a location (select Back to return)",
            [(name, name) for name in LOCATIONS[state]] + [("Back to states", None)],
        )
        if location is None:
            continue
        latitude, longitude, radius = LOCATIONS[state][location]
        return location, latitude, longitude, radius


def view_observation_details(observation):
    clear_screen()
    heading("OBSERVATION DETAILS")
    print(f"\nAnimal: {observation.animal.name}")
    print(f"Scientific name: {observation.animal.scientific_name}")
    print(f"Taxonomic rank: {observation.animal.rank}")
    print(f"Animal ID: {observation.animal.id}")
    print("-" * 48)
    print(f"Observer: {observation.observer}")
    print(f"Date: {observation.date or 'Unknown'}")
    print(f"Location: {observation.location or 'Unknown'}")
    print(f"Latitude: {observation.latitude}")
    print(f"Longitude: {observation.longitude}")
    print("-" * 48)
    if observation.image_urls:
        print("\nPhotographs:")
        for number, image_url in enumerate(observation.image_urls[:3], start=1):
            print(f"{number}. {image_url}")
    else:
        print("\nNo photographs available.")
    pause()


def browse_observations(observations):
    if not observations:
        print("Retrieve wildlife observations first.")
        pause()
        return
    page, page_size = 0, 5
    while True:
        clear_screen()
        heading("BROWSE WILDLIFE OBSERVATIONS")
        start = page * page_size
        current = observations[start:start + page_size]
        total_pages = (len(observations) + page_size - 1) // page_size
        print(f"\nPage {page + 1}/{total_pages} | {len(observations)} observations\n")
        options = []
        for index, observation in enumerate(current, start=start + 1):
            label = f"{index}. {observation.animal.name} | {observation.date or 'Unknown date'}"
            options.append((label, observation))
        if page > 0:
            options.append(("← Previous page", "previous"))
        if start + page_size < len(observations):
            options.append(("Next page →", "next"))
        options.append(("Back", None))
        choice = select_menu("Choose an observation", options)
        if choice is None:
            return
        if choice == "previous":
            page -= 1
        elif choice == "next":
            page += 1
        else:
            view_observation_details(choice)


def wildlife_field_guide(observations):
    """Browse unique taxa with searchable, sortable, filterable results."""
    if not observations:
        clear_screen()
        heading("WILDLIFE FIELD GUIDE")
        print("\nChoose a location and retrieve observations first.")
        pause()
        return

    species = {}
    for observation in observations:
        species.setdefault(observation.animal.id, []).append(observation)

    search_term = ""
    group_filter = "All groups"
    sort_mode = "A-Z"
    page = 0
    page_size = 8

    while True:
        clear_screen()
        heading("WILDLIFE FIELD GUIDE")
        available_groups = sorted({
            getattr(records[0].animal, "group", "Unknown") or "Unknown"
            for records in species.values()
        })
        if group_filter not in available_groups:
            group_filter = "All groups"

        visible_ids = []
        for animal_id, records in species.items():
            animal = records[0].animal
            name = (animal.name or "").casefold()
            scientific = (animal.scientific_name or "").casefold()
            group = getattr(animal, "group", "Unknown") or "Unknown"
            if search_term and search_term.casefold() not in name and search_term.casefold() not in scientific:
                continue
            if group_filter != "All groups" and group != group_filter:
                continue
            visible_ids.append(animal_id)

        if sort_mode == "Most observed":
            visible_ids.sort(key=lambda ident: (-len(species[ident]), (species[ident][0].animal.name or "").casefold()))
        elif sort_mode == "Least observed":
            visible_ids.sort(key=lambda ident: (len(species[ident]), (species[ident][0].animal.name or "").casefold()))
        else:
            visible_ids.sort(key=lambda ident: (species[ident][0].animal.name or "").casefold(), reverse=sort_mode == "Z-A")

        total_pages = max(1, (len(visible_ids) + page_size - 1) // page_size)
        page = min(page, total_pages - 1)
        start = page * page_size
        print(f"\nShowing {len(visible_ids)} of {len(species)} taxa | Page {page + 1}/{total_pages}")
        print(f"Search: {search_term or 'None'} | Group: {group_filter} | Sort: {sort_mode}\n")

        options = []
        for animal_id in visible_ids[start:start + page_size]:
            records = species[animal_id]
            animal = records[0].animal
            options.append((f"{animal.name} ({len(records)} observations)", animal_id))
        if not visible_ids:
            print("No matching species. Change or reset your filters.\n")
        if page > 0:
            options.append(("← Previous page", "__previous__"))
        if start + page_size < len(visible_ids):
            options.append(("Next page →", "__next__"))
        options.extend([
            ("Search species", "__search__"),
            ("Filter animal group", "__group__"),
            ("Sort species", "__sort__"),  
            ("Reset filters", "__reset__"),
            ("Back to Explore", None),
        ])
        selected = select_menu("Choose a species or refine results", options)
        if selected is None:
            return
        if selected == "__previous__":
            page -= 1
        elif selected == "__next__":
            page += 1
        elif selected == "__search__":
            entered = questionary.text("Common or scientific name (blank clears search):", default=search_term).ask()
            if entered is not None:
                search_term = entered.strip()
                page = 0
        elif selected == "__group__":
            group = select_menu("Choose animal group", [("All groups", "All groups")] + [(name, name) for name in available_groups] + [("Back", None)])
            if group is not None:
                group_filter = group
                page = 0
        elif selected == "__sort__":
            mode = select_menu("Sort field guide", [(name, name) for name in ("A-Z", "Z-A", "Most observed", "Least observed")] + [("Back", None)])
            if mode is not None:
                sort_mode = mode
                page = 0
        elif selected == "__reset__":
            search_term, group_filter, sort_mode, page = "", "All groups", "A-Z", 0
        else:
            view_field_guide_species(species[selected])


def view_field_guide_species(observations):
    """Display species information already available from iNaturalist."""
    animal = observations[0].animal
    while True:
        clear_screen()
        heading("FIELD GUIDE - SPECIES PROFILE")
        print(f"\nCommon name: {animal.name}")
        print(f"Scientific name: {animal.scientific_name}")
        print(f"Taxonomic rank: {animal.rank}")
        print(f"iNaturalist taxon ID: {animal.id}")
        print(f"Observations in current results: {len(observations)}")
        locations = sorted({
            str(o.location).strip()
            for o in observations if o.location
        })
        print(f"Recorded locations in results: {len(locations)}")
        for location in locations[:5]:
            print(f"  - {location}")
        if len(locations) > 5:
            print(f"  ... and {len(locations) - 5} more")
        photos = list(dict.fromkeys(
            url for o in observations for url in (o.image_urls or [])
        ))
        if photos:
            print("\nPhotograph URLs:")
            for url in photos[:3]:
                print(f"  {url}")
        else:
            print("\nNo photographs available.")
        
        print("\n" + "-" * 48)
        print("CONSERVATION INFORMATION")

        listings = get_conservation_status(animal.id)

        if not listings:
            print("Conservation listing: Not available")
            print("This does not mean the species is safe.")

        else:
            for listing in listings:
                code = listing["code"]
                name = listing["name"]

                if listing["threatened"]:
                    print("\n!!! THREATENED SPECIES !!!")
                elif code == "NT":
                    print("\n! NEAR THREATENED !")
                elif code in ("EW", "EX"):
                    print("\n!!! EXTINCTION STATUS !!!")

                print(f"\nStatus: {name} ({code})")
                print(f"Authority: {listing['authority']}")
                print(f"Scope: {listing['region']}")

        print("\nPopulation trend: Not available")
        print("Habitat and ecology: See More About This Species")

        print("Observation counts are not global population estimates.")
        selected = select_menu("Species options", [
            ("Browse observations for this species", "observations"),
            ("More About This Species", "information"),
            ("Back to Field Guide", None),
        ])
        if selected is None:
            return

        if selected == "observations":
            browse_observations(observations)

        elif selected == "information":
            clear_screen()
            display_species_info(animal)
            pause()

def view_species_profile(animal_id, sightings):
    clear_screen()
    heading("SPECIES PROFILE")
    species_sightings = [s for s in sightings if s.animal.id == animal_id]
    if not species_sightings:
        print("No saved sightings found for this species.")
        pause()
        return
    animal = species_sightings[0].animal
    print(f"\nAnimal: {animal.name}")
    print(f"Scientific name: {animal.scientific_name}")
    print(f"Taxonomic rank: {animal.rank}")
    print(f"Animal ID: {animal.id}")
    print(f"Times recorded: {len(species_sightings)}")
    print("\n" + "-" * 48)
    print("SIGHTING HISTORY")
    for number, sighting in enumerate(species_sightings, start=1):
        print(f"\nSighting {number}")
        print(f"Date: {sighting.date}")
        print(f"Latitude: {sighting.latitude}")
        print(f"Longitude: {sighting.longitude}")
        print(f"Notes: {sighting.notes or 'None'}")
        print("-" * 48)
    pause()


def view_discoveries(player, sightings):
    collection = {}
    for sighting in sightings:
        animal = sighting.animal
        if animal.id in player.discovered_species:
            if animal.id not in collection:
                collection[animal.id] = {"name": animal.name, "scientific_name": animal.scientific_name, "count": 0}
            collection[animal.id]["count"] += 1
    while True:
        clear_screen()
        heading("MY DISCOVERED SPECIES")
        print(f"\nLifetime species discovered: {len(player.discovered_species)}")
        print(f"Species with saved sightings: {len(collection)}")
        if not collection:
            print("\nNo discovered species with saved sightings.")
            pause()
            return
        options = []
        for animal_id, species in collection.items():
            options.append((f"{species['name']} ({species['count']} sightings)", animal_id))
        options.append(("Back", None))
        choice = select_menu("Choose a species to view its history", options)
        if choice is None:
            return
        view_species_profile(choice, sightings)


def view_wildlife_statistics(player, sightings):
    clear_screen()
    heading("WILDLIFE STATISTICS")
    species_counts = {}
    date_counts = {}
    for sighting in sightings:
        animal_id = sighting.animal.id
        if animal_id not in species_counts:
            species_counts[animal_id] = {"name": sighting.animal.name, "count": 0}
        species_counts[animal_id]["count"] += 1
        date_counts[sighting.date] = date_counts.get(sighting.date, 0) + 1
    print(f"\nPlayer: {player.username}")
    print(f"Level: {player.level} | XP: {player.xp}/100")
    print("-" * 48)
    print(f"Total saved sightings: {len(sightings)}")
    print(f"Unique species recorded: {len(species_counts)}")
    print(f"Lifetime species discovered: {len(player.discovered_species)}")
    if sightings:
        ranked = sorted(species_counts.values(), key=lambda item: item["count"], reverse=True)
        print("\nTOP 5 MOST RECORDED SPECIES")
        for number, species in enumerate(ranked[:5], start=1):
            print(f"{number}. {species['name']} - {species['count']} sightings")
        busiest_date = max(date_counts, key=date_counts.get)
        print("\nEXPLORATION ACTIVITY")
        print(f"Most recorded animal: {ranked[0]['name']}")
        print(f"Busiest sighting date: {busiest_date}")
        print(f"Sightings on that date: {date_counts[busiest_date]}")
    else:
        print("\nNo sightings available for statistics.")
    pause()


def view_sightings(manager):
    while True:
        clear_screen()
        heading("MY WILDLIFE SIGHTINGS")
        if not manager.sightings:
            print("\nNo wildlife sightings recorded yet.")
            pause()
            return
        options = [
            (f"#{s.sighting_id}  {s.animal.name} | {s.date}", s.sighting_id)
            for s in manager.sightings
        ]
        options.append(("Back", None))
        selected_id = select_menu("Select a sighting to view details", options)
        if selected_id is None:
            return
        sighting = next((s for s in manager.sightings if s.sighting_id == selected_id), None)
        if sighting is not None:
            clear_screen()
            heading("MY SIGHTING DETAILS")
            print(f"\nID: {sighting.sighting_id}")
            print(f"Animal: {sighting.animal.name}")
            print(f"Scientific name: {sighting.animal.scientific_name}")
            print(f"Date: {sighting.date}")
            print(f"Coordinates: {sighting.latitude}, {sighting.longitude}")
            print(f"Image: {sighting.image or 'None'}")
            print(f"Notes: {sighting.notes or 'None'}")
            pause()


def add_sighting(manager, player_manager):
    clear_screen()
    heading("ADD WILDLIFE SIGHTING")
    print("\nEnter the details of an animal you personally observed.")
    try:
        sighting_id = max((s.sighting_id for s in manager.sightings), default=0) + 1
        animal_id = int(input("Animal ID: "))
        animal_name = input("Animal name: ").strip()
        scientific_name = input("Scientific name: ").strip()
        image = input("Image filename or URL (optional): ").strip()
        sighting_date = input("Date (YYYY-MM-DD): ").strip()
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))
        notes = input("Notes (optional): ").strip()
        if not animal_name or not scientific_name or not sighting_date:
            print("\nAnimal name, scientific name and date are required.")
        elif not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            print("\nLatitude must be -90 to 90; longitude must be -180 to 180.")
        else:
            date_type.fromisoformat(sighting_date)
            animal = Animal(animal_id, animal_name, scientific_name, "species")
            sighting = Sighting(sighting_id, animal, image, sighting_date, latitude, longitude, notes)
            if manager.add_sighting(sighting):
                player = player_manager.player
                previous_xp, previous_level = player.xp, player.level
                previous_discoveries = player.discovered_species.copy()
                player.discover_animal(animal)
                if player_manager.save_player():
                    print("Player progress saved!")
                else:
                    player.xp, player.level = previous_xp, previous_level
                    player.discovered_species = previous_discoveries
                    print("Warning: Player progress could not be saved.")
    except ValueError:
        print("\nInvalid input. Check your numbers and date format.")
    pause()


def choose_saved_sighting(manager, title):
    if not manager.sightings:
        print("\nNo saved sightings available.")
        pause()
        return None
    options = [(f"#{s.sighting_id}  {s.animal.name} | {s.date}", s.sighting_id) for s in manager.sightings]
    options.append(("Cancel", None))
    return select_menu(title, options)


def edit_sighting(manager):
    clear_screen()
    heading("EDIT WILDLIFE SIGHTING")
    sighting_id = choose_saved_sighting(manager, "Which sighting would you like to edit?")
    if sighting_id is None:
        return
    selected = next((s for s in manager.sightings if s.sighting_id == sighting_id), None)
    if selected is None:
        print("Sighting not found.")
        pause()
        return
    print("\nPress Enter to keep the existing value.\n")
    updates = {}
    fields = {
        "animal_name": selected.animal.name,
        "scientific_name": selected.animal.scientific_name,
        "image": selected.image,
        "date": selected.date,
        "latitude": selected.latitude,
        "longitude": selected.longitude,
        "notes": selected.notes,
    }
    try:
        for field, current in fields.items():
            new_value = input(f"{field.replace('_', ' ').title()} [{current}]: ").strip()
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
    pause()


def delete_sighting(manager):
    clear_screen()
    heading("DELETE WILDLIFE SIGHTING")
    sighting_id = choose_saved_sighting(manager, "Which sighting would you like to delete?")
    if sighting_id is None:
        return
    selected = next((s for s in manager.sightings if s.sighting_id == sighting_id), None)
    if selected is None:
        print("Sighting not found.")
        pause()
        return
    confirmed = questionary.confirm(f"Delete {selected.animal.name} (#{sighting_id})?", default=False).ask()
    if confirmed:
        manager.delete_sighting(sighting_id)
    else:
        print("Deletion cancelled.")
    pause()


def view_player_profile(player, manager):
    clear_screen()
    heading("PLAYER PROFILE")
    print(f"\nUsername: {player.username}")
    print(f"Level: {player.level}")
    print(f"XP: {player.xp}/100")
    print("-" * 48)
    print(f"Species Discovered: {len(player.discovered_species)}")
    print(f"Total Saved Sightings: {len(manager.sightings)}")
    pause()


def explore_menu(observations):
    """Return updated observations; preserve old data on cancellation/failure."""
    while True:
        clear_screen()
        heading("EXPLORE WILDLIFE")
        print(f"\nObservations currently loaded: {len(observations)}\n")
        choice = select_menu("Explore", [
            ("Choose Location & Retrieve Observations", "retrieve"),
            ("Wildlife Field Guide", "guide"),
            ("Browse Observations", "browse"),
            ("Search for an Animal", "search"),
            ("Generate Wildlife Map", "map"),
            ("Back to Main Menu", None),
        ])
        if choice is None:
            return observations
        if choice == "retrieve":
            selected_location = choose_location()
            if selected_location is None:
                continue
            name, latitude, longitude, radius = selected_location
            clear_screen()
            heading("RETRIEVE OBSERVATIONS")
            print(f"\nSearching for wildlife near {name}...\n")
            new_observations = fetch_observations(latitude, longitude, radius)
            if new_observations:
                observations = new_observations
                print(f"\nLocation: {name}")
                print(f"Retrieved {len(observations)} observations.")
            else:
                print("\nNo observations retrieved. Previous results kept.")
            pause()
        elif choice == "guide":
            wildlife_field_guide(observations)
        elif choice == "browse":
            browse_observations(observations)
        elif choice == "search":
            clear_screen()
            heading("SEARCH FOR AN ANIMAL")
            if not observations:
                print("Retrieve observations first.")
            else:
                animal_name = input("\nEnter animal name: ").strip()
                if not animal_name:
                    print("Please enter an animal name.")
                else:
                    count = search_species(observations, animal_name)
                    print(f"\nMatching observations: {count}")
                    shown = 0
                    for observation in observations:
                        if observation.animal.name.lower() == animal_name.lower():
                            print("-" * 48)
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
            pause()
        elif choice == "map":
            clear_screen()
            heading("GENERATE WILDLIFE MAP")
            if not observations:
                print("Retrieve observations first.")
            else:
                generate_map(observations)
                print("Open generated/wilddex_map.html in your browser.")
            pause()


def collection_menu(manager, player_manager):
    while True:
        clear_screen()
        heading("MY COLLECTION")
        print(f"\nSaved sightings: {len(manager.sightings)}\n")
        choice = select_menu("Collection", [
            ("View My Sightings", "view"),
            ("Add a Sighting", "add"),
            ("Edit a Sighting", "edit"),
            ("Delete a Sighting", "delete"),
            ("Back to Main Menu", None),
        ])
        if choice is None:
            return
        if choice == "view":
            view_sightings(manager)
        elif choice == "add":
            add_sighting(manager, player_manager)
        elif choice == "edit":
            edit_sighting(manager)
        elif choice == "delete":
            delete_sighting(manager)


def progress_menu(manager, player_manager):
    while True:
        clear_screen()
        heading("MY PROGRESS")
        choice = select_menu("Progress", [
            ("View Player Profile", "profile"),
            ("View Discovered Species", "discoveries"),
            ("Wildlife Statistics", "statistics"),
            ("Back to Main Menu", None),
        ])
        if choice is None:
            return
        if choice == "profile":
            view_player_profile(player_manager.player, manager)
        elif choice == "discoveries":
            view_discoveries(player_manager.player, manager.sightings)
        elif choice == "statistics":
            view_wildlife_statistics(player_manager.player, manager.sightings)


def main():
    observations = []
    manager = WildDexManager()
    player_manager = PlayerManager()
    while True:
        clear_screen()
        heading("WILDDEX - WILDLIFE DISCOVERY")
        print(f"\nWelcome, {player_manager.player.username}!")
        print(f"Level {player_manager.player.level} | {len(manager.sightings)} saved sightings\n")
        choice = select_menu("What would you like to do?", [
            ("Explore Wildlife", "explore"),
            ("My Collection", "collection"),
            ("My Progress", "progress"),
            ("Exit WildDex", "exit"),
        ])
        if choice == "explore":
            observations = explore_menu(observations)
        elif choice == "collection":
            collection_menu(manager, player_manager)
        elif choice == "progress":
            progress_menu(manager, player_manager)
        elif choice in ("exit", None):
            clear_screen()
            print("Thanks for exploring WildDex. Goodbye!")
            break


if __name__ == "__main__":
    main()
