"""Meditation timer module - for when a Jedi needs to center themselves."""

import time
import sys
from typing import Callable, Optional


DEFAULT_MEDITATION_SECONDS = 60


def format_duration(seconds: int) -> str:
    """Format seconds into a human-readable duration string."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    remaining = seconds % 60
    if remaining == 0:
        return f"{minutes}m"
    return f"{minutes}m {remaining}s"


def meditation_timer(
    duration: int = DEFAULT_MEDITATION_SECONDS,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    tick: float = 1.0
) -> dict:
    """Run a meditation timer for the specified duration.
    
    Args:
        duration: How long to meditate in seconds
        progress_callback: Optional callback(seconds_elapsed, total_seconds)
        tick: How often to call the callback (default 1s)
    
    Returns:
        Dict with 'duration', 'completed' status
    """
    start = time.time()
    end = start + duration
    
    try:
        while time.time() < end:
            elapsed = int(time.time() - start)
            if progress_callback:
                progress_callback(elapsed, duration)
            remaining = end - time.time()
            if remaining > 0:
                time.sleep(min(tick, remaining))
        return {'duration': duration, 'completed': True}
    except KeyboardInterrupt:
        elapsed = int(time.time() - start)
        return {'duration': elapsed, 'completed': False}


def breathing_guide() -> list[str]:
    """Return a simple breathing exercise guide."""
    return [
        "Close your eyes and connect to the Force...",
        "Inhale slowly... 1... 2... 3... 4...",
        "Hold... 1... 2... 3... 4...",
        "Exhale slowly... 1... 2... 3... 4...",
        "Hold... 1... 2... 3... 4...",
        "Repeat. Let the Force flow through you."
    ]
