"""Jedi wisdom module - quotes and philosophical insights."""

import random
from typing import Optional


WISDOM_QUOTES = [
    # Yoda
    "Do or do not. There is no try.",
    "Luminous beings are we, not this crude matter.",
    "Fear is the path to the dark side.",
    "Size matters not.",
    "Truly wonderful, the mind of a child is.",
    "The dark side clouds everything.",
    "A Jedi uses the Force for knowledge and defense, never for attack.",
    "Difficult to see. The dark side of the Force clouds everything.",
    "Patience you must have, my young Padawan.",
    "The Force will be with you. Always.",
    "Your eyes can deceive you. Don't trust them.",
    "In my experience, there is no such thing as luck.",
    "Adventure. Excitement. A Jedi craves not these things.",
    "Wars not make one great.",
    "Ready are you? What know you of ready?",
    
    # Obi-Wan Kenobi
    "So uncivilized.",
    "You will find only what you bring in.",
    "The Force is what gives a Jedi his power.",
    "Who's the more foolish; the fool, or the fool who follows him?",
    "Your clone troopers will get the job done.",
    "The dark side of the Force is a pathway to many abilities some consider to be unnatural.",
    
    # Qui-Gon Jinn
    "Your focus determines your reality.",
    "Remember, your focus determines your reality.",
    "The ability to speak does not make you intelligent.",
    
    # Mace Windu
    "This is the moment. Everything we've worked towards.",
    "I'm getting too old for this sort of thing.",
    
    # Ahsoka Tano
    "A leader's strength is measured by the strength of those they lead.",
    "I am no Jedi.",
    
    # Miscellaneous
    "A long time ago in a galaxy far, far away...",
    "I have a bad feeling about this.",
    "Never tell me the odds!",
    "The Force is strong with this one.",
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
    """Return a random Jedi wisdom quote."""
    return random.choice(WISDOM_QUOTES)


def get_wisdom_by_index(index: int) -> Optional[str]:
    """Return wisdom quote by index, or None if out of range."""
    if 0 <= index < len(WISDOM_QUOTES):
        return WISDOM_QUOTES[index]
    return None


def get_all_wisdom() -> list[str]:
    """Return all wisdom quotes."""
    return WISDOM_QUOTES.copy()


def format_wisdom(quote: str, color: str = "cyan") -> str:
    """Format a wisdom quote with color."""
    color_code = COLORED_OUTPUT.get(color, COLORED_OUTPUT["cyan"])
    reset = COLORED_OUTPUT["reset"]
    bold = COLORED_OUTPUT["bold"]
    return f"{bold}{color_code}\"{quote}\"{reset}"


def wisdom_count() -> int:
    """Return total number of wisdom quotes."""
    return len(WISDOM_QUOTES)
