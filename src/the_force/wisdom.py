"""Jedi wisdom module - quotes and philosophical insights."""

import random
from typing import Optional


WISDOM_QUOTES = [
    # Yoda
    {"quote": "Do or do not. There is no try.", "author": "Yoda"},
    {"quote": "Luminous beings are we, not this crude matter.", "author": "Yoda"},
    {"quote": "Fear is the path to the dark side.", "author": "Yoda"},
    {"quote": "Size matters not.", "author": "Yoda"},
    {"quote": "Truly wonderful, the mind of a child is.", "author": "Yoda"},
    {"quote": "The dark side clouds everything.", "author": "Yoda"},
    {"quote": "A Jedi uses the Force for knowledge and defense, never for attack.", "author": "Yoda"},
    {"quote": "Difficult to see. The dark side of the Force clouds everything.", "author": "Yoda"},
    {"quote": "Patience you must have, my young Padawan.", "author": "Yoda"},
    {"quote": "The Force will be with you. Always.", "author": "Yoda"},
    {"quote": "Your eyes can deceive you. Don't trust them.", "author": "Yoda"},
    {"quote": "In my experience, there is no such thing as luck.", "author": "Yoda"},
    {"quote": "Adventure. Excitement. A Jedi craves not these things.", "author": "Yoda"},
    {"quote": "Wars not make one great.", "author": "Yoda"},
    {"quote": "Ready are you? What know you of ready?", "author": "Yoda"},
    
    # Obi-Wan Kenobi
    {"quote": "So uncivilized.", "author": "Obi-Wan Kenobi"},
    {"quote": "You will find only what you bring in.", "author": "Obi-Wan Kenobi"},
    {"quote": "The Force is what gives a Jedi his power.", "author": "Obi-Wan Kenobi"},
    {"quote": "Who's the more foolish; the fool, or the fool who follows him?", "author": "Obi-Wan Kenobi"},
    {"quote": "Your clone troopers will get the job done.", "author": "Obi-Wan Kenobi"},
    {"quote": "The dark side of the Force is a pathway to many abilities some consider to be unnatural.", "author": "Obi-Wan Kenobi"},
    
    # Qui-Gon Jinn
    {"quote": "Your focus determines your reality.", "author": "Qui-Gon Jinn"},
    {"quote": "The ability to speak does not make you intelligent.", "author": "Qui-Gon Jinn"},
    
    # Mace Windu
    {"quote": "This is the moment. Everything we've worked towards.", "author": "Mace Windu"},
    {"quote": "I'm getting too old for this sort of thing.", "author": "Mace Windu"},
    
    # Ahsoka Tano
    {"quote": "A leader's strength is measured by the strength of those they lead.", "author": "Ahsoka Tano"},
    {"quote": "I am no Jedi.", "author": "Ahsoka Tano"},
    
    # Miscellaneous
    {"quote": "A long time ago in a galaxy far, far away...", "author": "Narrator"},
    {"quote": "I have a bad feeling about this.", "author": "Various"},
    {"quote": "Never tell me the odds!", "author": "Han Solo"},
    {"quote": "The Force is strong with this one.", "author": "Darth Vader"},
]

COLORED_OUTPUT = {
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


def get_random_wisdom() -> str:
    """Return a random Jedi wisdom quote (as a formatted string with author)."""
    entry = random.choice(WISDOM_QUOTES)
    return f"{entry['quote']} — {entry['author']}"


def get_random_wisdom_with_author() -> dict:
    """Return a random Jedi wisdom quote with author as a dict."""
    return random.choice(WISDOM_QUOTES).copy()


def get_wisdom_by_index(index: int) -> Optional[str]:
    """Return wisdom quote by index, or None if out of range."""
    if 0 <= index < len(WISDOM_QUOTES):
        entry = WISDOM_QUOTES[index]
        return f"{entry['quote']} — {entry['author']}"
    return None


def get_all_wisdom() -> list[str]:
    """Return all wisdom quotes as formatted strings."""
    return [f"{entry['quote']} — {entry['author']}" for entry in WISDOM_QUOTES]


def format_wisdom(quote: str, color: str = "cyan") -> str:
    """Format a wisdom quote with color."""
    color_code = COLORED_OUTPUT.get(color, COLORED_OUTPUT["cyan"])
    reset = COLORED_OUTPUT["reset"]
    bold = COLORED_OUTPUT["bold"]
    return f"{bold}{color_code}\"{quote}\"{reset}"


def wisdom_count() -> int:
    """Return total number of wisdom quotes."""
    return len(WISDOM_QUOTES)
