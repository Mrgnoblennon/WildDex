# Retrieve conservation listings for iNaturalist taxa

import requests

STATUS_NAMES = {
    "LC": "Least Concern",
    "NT": "Near Threatened",
    "VU": "Vulnerable",
    "EN": "Endangered",
    "CR": "Critically Endangered",
    "EW": "Extinct in the Wild",
    "EX": "Extinct",
    "DD": "Data Deficient",
    "NE": "Not Evaluated",
}

THREATENED = {"VU", "EN", "CR"}


def get_conservation_status(taxon_id):
    url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return []

        taxon = results[0]
        listings = []

        for entry in taxon.get("conservation_statuses", []):
            if not isinstance(entry, dict):
                continue

            code = str(entry.get("status") or "").upper()
            authority = entry.get("authority") or "Unspecified"
            place = entry.get("place")

            # Only interpret recognised IUCN category codes.
            if code not in STATUS_NAMES:
                continue

            region = "Global" if place is None else (
                place.get("display_name") or place.get("name")
                if isinstance(place, dict) else "Regional"
            )

            listings.append({
                "code": code,
                "name": STATUS_NAMES[code],
                "authority": authority,
                "region": region,
                "threatened": code in THREATENED,
            })

        return listings

    except (requests.RequestException, ValueError, TypeError, KeyError):
        return []
