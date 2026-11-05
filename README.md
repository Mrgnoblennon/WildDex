# WildDex 🌿

**WildDex** is a Python-based wildlife discovery and sighting management application developed as part of my Diploma of Cyber Security at SAE Perth.

The project uses the [iNaturalist API](https://www.inaturalist.org/) to retrieve real-world wildlife observations, allowing users to explore animal sightings, record their own discoveries and learn about biodiversity.

WildDex supports **United Nations Sustainable Development Goal 15 – Life on Land**.

## Project Status

**Currently in Development – Stage 2: Python Classes and Data Organisation**

The application can currently retrieve and process wildlife observation data from the iNaturalist API.

## Planned Features

- Retrieve wildlife observations from the iNaturalist API.
- Display animal information, photographs and observation details.
- Explore wildlife sightings on an interactive world map.
- Filter observations by species, location and date.
- Add, view, edit and delete personal wildlife sightings.
- Save user observations using persistent storage.
- Earn experience points (XP) for wildlife discoveries.
- View wildlife statistics through graphs and charts.
- Access WildDex through a mobile-friendly web interface.

## Technologies

| Technology | Purpose |
|------------|---------|
| Python | Core application logic and data processing |
| Requests | iNaturalist API integration |
| JSON | API responses and potential local storage |
| Flask | Planned web interface |
| Folium | Planned interactive mapping |
| Matplotlib | Planned data visualisation |
| HTML/CSS | Planned graphical interface |

## Development Roadmap

- [x] Stage 1 – Connect to the iNaturalist API
- [ ] Stage 2 – Python classes and data organisation
- [ ] Stage 3 – Interactive world map
- [ ] Stage 4 – User sighting management
- [ ] Stage 5 – XP and rewards system
- [ ] Stage 6 – Web interface and GPS
- [ ] Stage 7 – Wildlife statistics and charts
- [ ] Stage 8 – Testing, documentation and presentation

## Getting Started

### Requirements

- Python 3
- Requests library
- Internet connection

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/WildDex.git
```

Navigate into the project directory:

```bash
cd WildDex
```

Install Requests:

```bash
pip install requests
```

Run the Python script using Thonny or your preferred Python environment.

*Installation instructions will be updated as development progresses.*

## Data Sources

WildDex uses the public [iNaturalist API](https://api.inaturalist.org/v1/observations) to retrieve existing wildlife observations.

The application will distinguish between two sources:

- **iNaturalist Observations:** Existing wildlife records retrieved from the API.
- **User Sightings:** Personal wildlife observations created and managed within WildDex.

## Sustainable Development Goals

### SDG 15 – Life on Land

WildDex aims to encourage wildlife exploration and biodiversity awareness by making animal observation data accessible and interactive.

### SDG 14 – Life Below Water

The application may also support awareness of marine biodiversity through observations of aquatic wildlife.

## Project Objectives

This project aims to demonstrate Python programming skills, including:

- Object-oriented programming
- Classes and objects
- Lists and dictionaries
- Functions and methods
- API integration and JSON processing
- File handling and persistent storage
- Input validation and exception handling
- Data analysis and visualisation

## Author

Chase Barrett-Brown  
Diploma of Cyber Security – SAE Perth  
CST182 Programming Project 2

## Acknowledgements

Wildlife observation data is provided by the iNaturalist API.

Individual observations and photographs remain subject to their respective attribution and licensing requirements.
