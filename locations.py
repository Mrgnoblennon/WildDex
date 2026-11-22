
# australian wildlife exploration locations
LOCATIONS = {
    "Western Australia": {
        "Rottnest Island": (-31.9965, 115.5404, 7),
        "Fitzgerald River National Park": (-33.95, 119.50, 40),
        "Kimberley": (-16.40, 126.50, 100)
    },
    "New South Wales": {
        "Blue Mountains": (-33.72, 150.31, 35),
        "Dorrigo National Park": (-30.36, 152.73, 15),
        "Royal National Park": (-34.12, 151.06, 20)
    },
    "Victoria": {
        "Great Otway National Park": (-38.70, 143.55, 35),
        "Wilsons Promontory": (-39.03, 146.32, 25),
        "Grampians": (-37.20, 142.50, 35)
    },
    "Queensland": {
        "Daintree Rainforest": (-16.17, 145.42, 35),
        "Lamington National Park": (-28.24, 153.13, 20),
        "Wet Tropics": (-17.25, 145.65, 60)
    },
    "South Australia": {
        "Kangaroo Island": (-35.82, 137.20, 65),
        "Flinders Ranges": (-31.45, 138.60, 60),
        "Coorong National Park": (-36.05, 139.55, 45)
    },
    "Tasmania": {
        "Cradle Mountain": (-41.68, 145.95, 20),
        "Southwest National Park": (-42.75, 146.15, 75),
        "Freycinet National Park": (-42.12, 148.30, 20)
    },
    "Northern Territory": {
        "Kakadu National Park": (-12.85, 132.85, 90),
        "Litchfield National Park": (-13.15, 130.70, 35),
        "Nitmiluk National Park": (-14.32, 132.42, 30)
    },
    "Australian Capital Territory": {
        "Namadgi National Park": (-35.65, 148.95, 35),
        "Tidbinbilla Nature Reserve": (-35.46, 148.89, 12),
        "Mulligans Flat Woodland Sanctuary": (-35.17, 149.17, 7)
    }
}


def choose_location():
    states = list(LOCATIONS.keys())

    print("\n===== SELECT A STATE OR TERRITORY =====")

    for number, state in enumerate(states, start=1):
        print(f"{number}. {state}")

    choice = input("\nSelect state (0 to cancel): ").strip()

    if choice == "0":
        return None

    if not choice.isdigit() or not 1 <= int(choice) <= len(states):
        print("Invalid state selection.")
        return None

    state = states[int(choice) - 1]
    locations = list(LOCATIONS[state].keys())

    print(f"\n===== {state.upper()} =====")

    for number, location in enumerate(locations, start=1):
        print(f"{number}. {location}")

    choice = input("\nSelect location (0 to cancel): ").strip()

    if choice == "0":
        return None

    if not choice.isdigit() or not 1 <= int(choice) <= len(locations):
        print("Invalid location selection.")
        return None

    name = locations[int(choice) - 1]
    latitude, longitude, radius = LOCATIONS[state][name]

    return name, latitude, longitude, radius
