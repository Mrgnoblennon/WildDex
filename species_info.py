# Retrieve educational species information from Wikipedia

import requests
import textwrap
from urllib.parse import quote
from html.parser import HTMLParser
from html import unescape


def get_species_info(scientific_name):
    """Fetch a Wikipedia article using a scientific name."""

    if not scientific_name:
        return None

    page_title = quote(
        scientific_name.strip().replace(" ", "_"),
        safe=""
    )

    url = (
        "https://en.wikipedia.org/api/rest_v1/"
        f"page/summary/{page_title}"
    )

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "WildDex/1.0 "
                    "(educational wildlife discovery project)"
                ),
                "Accept": "application/json",
            },
            timeout=10
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()

        # Avoid displaying disambiguation pages
        if data.get("type") != "standard":
            return None

        summary = data.get("extract")

        if not summary:
            return None

        article_url = (
            data.get("content_urls", {})
                .get("desktop", {})
                .get("page")
        )

        return {
            "title": data.get("title", scientific_name),
            "description": data.get("description"),
            "summary": summary,
            "source": article_url or url,
        }

    except (requests.RequestException, ValueError, TypeError):
        return None


def display_species_info(animal):
    """Display educational information about a species."""

    print("\n" + "=" * 48)
    print("  MORE ABOUT THIS SPECIES")
    print("=" * 48)

    print(f"\nSpecies: {animal.name}")
    print(f"Scientific name: {animal.scientific_name}")

    # Genus-level taxa and higher ranks are not
    # necessarily individual species.
    if animal.rank != "species":
        print(
            "\nThis taxon is not identified at species level."
        )
        print(
            "An exact species profile may not be available."
        )
        return

    print("\nRetrieving species information...")

    info = get_species_info(animal.scientific_name)

    if info is None:
        print("\nNo matching species article was found.")
        print("Try another species from the Field Guide.")
        return

    print(f"\nArticle: {info['title']}")

    if info["description"]:
        print(f"Description: {info['description']}")

    print("\nSPECIES OVERVIEW")
    print("-" * 48)

    for paragraph in info["summary"].split("\n"):
        if paragraph.strip():
            print(textwrap.fill(paragraph, width=76))
            print()


    ecology = get_ecological_info(animal.scientific_name)

    print("\nHABITAT AND DISTRIBUTION")
    print("-" * 48)
    print(textwrap.fill(
        ecology["habitat"] or
        "No dedicated habitat or distribution section available.",
        width=76
    ))

    print("\nECOLOGY AND BEHAVIOUR")
    print("-" * 48)
    print(textwrap.fill(
        ecology["ecology"] or
        "No dedicated ecology section available.",
        width=76
    ))

    print("\nPopulation trend: Not verified")
    print("Ecological role: Not separately verified")
    print("Major threats: Not separately verified")

    if ecology["source"]:
        print("\nEcological information source:")
        print(ecology["source"])

    print("\nSource:")
    print(info["source"])

    print(
        "\nNote: This is a general reference article, "
        "not an official conservation assessment."
    )


class SectionTextParser(HTMLParser):
    """Convert a Wikipedia section into readable text."""

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("sup", "style", "script"):
            self.skip += 1
        elif tag in ("p", "li") and not self.skip:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("sup", "style", "script") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def get_text(self):
        return " ".join(
            unescape("".join(self.parts)).split()
        )


def get_ecological_info(scientific_name):
    """Find relevant habitat and ecology article sections."""

    result = {
        "habitat": None,
        "ecology": None,
        "source": None,
    }

    if not scientific_name:
        return result

    api_url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "WildDex/1.0 (educational project)"
    }

    try:
        response = requests.get(
            api_url,
            params={
                "action": "parse",
                "page": scientific_name,
                "prop": "sections",
                "format": "json",
                "redirects": 1,
            },
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json().get("parse", {})
        sections = data.get("sections", [])

        if not data:
            return result

        title = data.get("title", scientific_name)
        result["source"] = (
            "https://en.wikipedia.org/wiki/"
            + quote(title.replace(" ", "_"), safe="")
        )

        keywords = {
            "habitat": (
                "habitat", "distribution", "range"
            ),
            "ecology": (
                "ecology", "behaviour", "behavior",
                "diet", "feeding"
            ),
        }

        for section in sections:
            heading = section.get("line", "").lower()

            for category, terms in keywords.items():
                if result[category] is not None:
                    continue

                if not any(term in heading for term in terms):
                    continue

                detail = requests.get(
                    api_url,
                    params={
                        "action": "parse",
                        "page": title,
                        "prop": "text",
                        "section": section["index"],
                        "format": "json",
                    },
                    headers=headers,
                    timeout=10,
                )
                detail.raise_for_status()

                html = (
                    detail.json()
                    .get("parse", {})
                    .get("text", {})
                    .get("*", "")
                )

                parser = SectionTextParser()
                parser.feed(html)
                text = parser.get_text()

                if text:
                    result[category] = text[:1200]

        return result

    except (requests.RequestException, ValueError, KeyError):
        return result
