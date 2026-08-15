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
