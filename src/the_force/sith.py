"""Sith module - quotes from the dark side for contrast."""

import random
from typing import Optional


SITH_QUOTES = [
    # Darth Vader
    {"quote": "I find your lack of faith disturbing.", "author": "Darth Vader"},
    {"quote": "The Force is with me, and I am strong with the Force.", "author": "Darth Vader"},
    {"quote": "Impressive. Most impressive.", "author": "Darth Vader"},
    {"quote": "You are unwise to lower your defenses.", "author": "Darth Vader"},
    {"quote": "Perhaps you think you're being treated unfairly.", "author": "Darth Vader"},
    {"quote": "The circle is now complete. When I left you, I was but the learner. Now I am the master.", "author": "Darth Vader"},
    {"quote": "Obi-Wan was wise, but he was a fool to trust you.", "author": "Darth Vader"},
    {"quote": "It is your destiny.", "author": "Darth Vader"},
    
    # Darth Sidious (Emperor Palpatine)
    {"quote": "Everything is proceeding as I have foreseen.", "author": "Darth Sidious"},
    {"quote": "Your hatred has made you powerful.", "author": "Darth Sidious"},
    {"quote": "Good. Use your aggressive feelings, boy.", "author": "Darth Sidious"},
    {"quote": "The dark side of the Force is a pathway to many abilities some consider to be unnatural.", "author": "Darth Sidious"},
    {"quote": "Unlimited power!", "author": "Darth Sidious"},
    
    # Darth Maul
    {"quote": "At last we will reveal ourselves to the Jedi. At last we will have revenge.", "author": "Darth Maul"},
    {"quote": "I was promised power from the Dark Side.", "author": "Darth Maul"},
    
    # Count Dooku
    {"quote": "Only a Sith deals in absolutes.", "author": "Count Dooku"},
    {"quote": "The Republic will soon disintegrate. This army of mine will destroy it.", "author": "Count Dooku"},
    
    # Darth Bane
    {"quote": "Three there should be; no more, no less. One to embody power, one to crave it, and one to desire it.", "author": "Darth Bane"},
    
    # Miscellaneous Dark Side
    {"quote": "Peace is a lie, there is only passion.", "author": "Sith Code"},
    {"quote": "Through passion, I gain strength. Through strength, I gain power.", "author": "Sith Code"},
    {"quote": "Through victory, my chains are broken. The Force shall free me.", "author": "Sith Code"},
]


SITH_COLORS = {
    "red": "\033[91m",
    "purple": "\033[95m",
    "yellow": "\033[93m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def get_random_sith_quote() -> str:
    """Return a random Sith quote as a formatted string with author."""
    entry = random.choice(SITH_QUOTES)
    return f"{entry['quote']} — {entry['author']}"


def get_all_sith_quotes() -> list[str]:
    """Return all Sith quotes as formatted strings."""
    return [f"{entry['quote']} — {entry['author']}" for entry in SITH_QUOTES]


def sith_quote_count() -> int:
    """Return total number of Sith quotes."""
    return len(SITH_QUOTES)


def get_sith_quote_by_index(index: int) -> Optional[str]:
    """Return Sith quote by index, or None if out of range."""
    if 0 <= index < len(SITH_QUOTES):
        entry = SITH_QUOTES[index]
        return f"{entry['quote']} — {entry['author']}"
    return None


def format_sith_quote(quote: str, color: str = "red") -> str:
    """Format a Sith quote with color (default red for the dark side)."""
    color_code = SITH_COLORS.get(color, SITH_COLORS["red"])
    reset = SITH_COLORS["reset"]
    bold = SITH_COLORS["bold"]
    return f"{bold}{color_code}\"{quote}\"{reset}"


def get_sith_code() -> str:
    """Return the Sith Code as a string."""
    return """Peace is a lie, there is only passion.
Through passion, I gain strength.
Through strength, I gain power.
Through power, I gain victory.
Through victory, my chains are broken.
The Force shall free me."""
