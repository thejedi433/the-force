# the-force

A Jedi CLI toolkit for wisdom, diagnostics, meditation, and dark side contemplation.

## Installation

```bash
cd /home/jrodin/projects/the-force
pip install -e .
```

## Commands

### wisdom
Receive wisdom from the Jedi Order.

```bash
# Random quote
the-force wisdom

# List all quotes
the-force wisdom --list

# Count quotes
the-force wisdom --count

# Colorized output
the-force wisdom --color green
```

### sith
Receive wisdom from the Sith - the dark side of the Force. Perfect for contrast and balance.

```bash
# Random dark side quote
the-force sith

# Display the Sith Code
the-force sith --code

# List all Sith quotes
the-force sith --list

# Custom color
the-force sith --color purple
```

### holocron
Your personal wisdom journal. Store, search, and manage your own Jedi insights with persistent storage.

```bash
# Add a new wisdom entry
the-force holocron --add "The best teacher is failure" --source "Yoda"

# List all entries
the-force holocron --list

# Search entries
the-force holocron --search "force"

# Delete an entry by ID
the-force holocron --delete 1

# Limit results
the-force holocron --list --limit 5
```

Holocron data is stored in `~/.the_force_holocron.json` and persists across sessions.

### diagnose
Check system health with Jedi precision.

```bash
# Human-readable diagnostics
the-force diagnose

# JSON output for scripting
the-force diagnose --json
```

### meditate
Center yourself with the Force.

```bash
# 60-second meditation (default)
the-force meditate

# Custom duration (in seconds)
the-force meditate --duration 120

# Quiet mode (no progress display)
the-force meditate --quiet

# Breathing guide
the-force meditate --guide
```

### version
Show version information.

```bash
the-force version
# or
the-force --version
```

### sensitivity
Measure Force sensitivity.

```bash
the-force sensitivity
```

### lightsaber
Get a random lightsaber.

```bash
# Random lightsaber
the-force lightsaber

# List all available colors
the-force lightsaber --list
```

## Examples

```bash
# Get wisdom before starting work
the-force wisdom

# Check system health
the-force diagnose

# Take a break
the-force meditate --duration 300

# Store your own insight
the-force holocron --add "Do. Or do not. There is no try." --source "My mentor"

# Contrast light and dark
the-force wisdom && the-force sith --code
```

## Features

- **30+ wisdom quotes** from Yoda, Obi-Wan, and other Jedi
- **22+ Sith quotes** from Darth Vader, Sidious, Maul, and the Sith Code
- **Personal holocron** - persistent wisdom journal with CRUD operations
- **System diagnostics** (CPU, memory, disk, uptime, load)
- **Meditation timer** with breathing guide
- **Colorized output** for terminal
- **JSON output** for scripting
- **Fully tested** with pytest (87 tests)

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=the_force
```

## License

MIT

---

*May the Force be with you.*
