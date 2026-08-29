"""Lightsaber module - iconic weapons of the Jedi and Sith."""

import random
from typing import Optional


LIGHTSABERS = [
    {
        'name': 'Anakin',
        'color': 'blue',
        'description': 'The legendary lightsaber of Anakin Skywalker, later wielded by Luke Skywalker and Rey.',
        'alignment': 'Light'
    },
    {
        'name': 'Luke',
        'color': 'green',
        'description': 'Luke Skywalker\'s second lightsaber, constructed during his training on Dagobah.',
        'alignment': 'Light'
    },
    {
        'name': 'Mace Windu',
        'color': 'purple',
        'description': 'The unique purple-bladed lightsaber of Jedi Master Mace Windu.',
        'alignment': 'Light'
    },
    {
        'name': 'Yoda',
        'color': 'green',
        'description': 'The small but powerful lightsaber of Grand Master Yoda.',
        'alignment': 'Light'
    },
    {
        'name': 'Obi-Wan',
        'color': 'blue',
        'description': 'Obi-Wan Kenobi\'s elegant lightsaber, passed down through generations.',
        'alignment': 'Light'
    },
    {
        'name': 'Ahsoka',
        'color': 'white',
        'description': 'The purified white lightsabers of Ahsoka Tano, symbolizing her independence from Jedi and Sith.',
        'alignment': 'Light'
    },
    {
        'name': 'Rey',
        'color': 'yellow',
        'description': 'Rey Skywalker\'s yellow-bladed lightsaber, representing her unique path as a Jedi.',
        'alignment': 'Light'
    },
    {
        'name': 'Kylo Ren',
        'color': 'red',
        'description': 'Kylo Ren\'s unstable red crossguard lightsaber, forged in a cracked kyber crystal.',
        'alignment': 'Dark'
    },
    {
        'name': 'Dooku',
        'color': 'red',
        'description': 'Count Dooku\'s elegant curved-hilt lightsaber, reflecting his aristocratic style.',
        'alignment': 'Dark'
    },
    {
        'name': 'Vader',
        'color': 'red',
        'description': 'The crimson-bladed lightsaber of Darth Vader, symbol of the dark side.',
        'alignment': 'Dark'
    },
    {
        'name': 'Sidious',
        'color': 'red',
        'description': 'The double-bladed red lightsaber of Emperor Palpatine.',
        'alignment': 'Dark'
    },
    {
        'name': 'Maul',
        'color': 'red',
        'description': 'The iconic double-bladed red lightsaber of Darth Maul.',
        'alignment': 'Dark'
    }
]


def get_random_lightsaber() -> dict:
    """Return a random lightsaber from the collection."""
    return random.choice(LIGHTSABERS).copy()


def get_lightsaber_by_name(name: str) -> Optional[dict]:
    """Return lightsaber by name, or None if not found."""
    for saber in LIGHTSABERS:
        if saber['name'].lower() == name.lower():
            return saber.copy()
    return None


def get_all_lightsaber_colors() -> list[str]:
    """Return list of all unique lightsaber colors."""
    colors = list(set(saber['color'] for saber in LIGHTSABERS))
    return sorted(colors)


def get_lightsabers_by_color(color: str) -> list[dict]:
    """Return all lightsabers of a given color (case-insensitive)."""
    color_lower = color.lower()
    return [saber.copy() for saber in LIGHTSABERS if saber['color'].lower() == color_lower]


def get_lightsabers_by_alignment(alignment: str) -> list[dict]:
    """Return all lightsabers of a given alignment (Light/Dark/Balanced, case-insensitive)."""
    alignment_lower = alignment.lower()
    return [saber.copy() for saber in LIGHTSABERS if saber['alignment'].lower() == alignment_lower]


def lightsaber_count() -> int:
    """Return the total number of lightsabers in the collection."""
    return len(LIGHTSABERS)
