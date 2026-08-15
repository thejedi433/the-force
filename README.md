# the-force 🌟

A Jedi CLI toolkit for wisdom, diagnostics, and meditation.

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

## Examples

```bash
# Get wisdom before starting work
the-force wisdom

# Check system health
the-force diagnose

# Take a break
the-force meditate --duration 300
```

## Features

- **30+ wisdom quotes** from Yoda, Obi-Wan, and other Jedi
- **System diagnostics** (CPU, memory, disk, uptime, load)
- **Meditation timer** with breathing guide
- **Colorized output** for terminal
- **JSON output** for scripting
- **Fully tested** with pytest

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
