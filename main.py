
# import API functions
from inaturalistAPI import fetch_observations, search_species, generate_map


def main():
    observations = []

    while True:
        print("\n===== WILDDEX =====")
        print("1. Retrieve wildlife observations")
        print("2. Search for an animal")
        print("3. Generate wildlife map")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            observations = fetch_observations()
            print(f"Retrieved {len(observations)} observations.")

        elif choice == "2":
            if not observations:
                print("Please retrieve observations first.")
                continue

            animal_name = input("Enter animal name: ")
            count = search_species(observations, animal_name)

            print(f"Matching sightings: {count}")

        elif choice == "3":
            if not observations:
                print("Please retrieve observations first.")
                continue

            generate_map(observations)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
