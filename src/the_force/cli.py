#!/usr/bin/env python3
"""CLI interface for the-force Jedi toolkit."""

import argparse
import sys
import json
from typing import Optional

from the_force import __version__
from the_force.wisdom import get_random_wisdom, get_all_wisdom, format_wisdom, wisdom_count
from the_force.diagnostics import get_all_diagnostics, get_cpu_usage, get_memory_usage, get_disk_usage
from the_force.meditation import meditation_timer, format_duration, breathing_guide


def cmd_wisdom(args: argparse.Namespace) -> int:
    """Handle wisdom command."""
    if args.list:
        quotes = get_all_wisdom()
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {quote}")
        print(f"\nTotal: {wisdom_count()} wisdom quotes")
        return 0
    
    if args.count:
        print(f"The Force contains {wisdom_count()} wisdom quotes.")
        return 0
    
    quote = get_random_wisdom()
    print(format_wisdom(quote, args.color))
    return 0


def cmd_diagnose(args: argparse.Namespace) -> int:
    """Handle diagnose command."""
    if args.json:
        diagnostics = get_all_diagnostics()
        print(json.dumps(diagnostics, indent=2))
        return 0
    
    print("=== Jedi System Diagnostics ===\n")
    
    cpu = get_cpu_usage()
    if cpu:
        print(f"CPU Usage:     {cpu}")
    
    mem = get_memory_usage()
    if mem:
        print(f"Memory:        {mem['used']}{mem['unit']} / {mem['total']}{mem['unit']} ({mem['available']}{mem['unit']} available)")
    
    disk = get_disk_usage()
    if disk:
        print(f"Disk Usage:    {disk['used']} / {disk['size']} ({disk['percent']} used)")
    
    from the_force.diagnostics import get_uptime, get_load_average
    uptime = get_uptime()
    if uptime:
        print(f"Uptime:        {uptime}")
    
    load = get_load_average()
    if load:
        print(f"Load Average:  {load['1min']} / {load['5min']} / {load['15min']}")
    
    return 0


def cmd_meditate(args: argparse.Namespace) -> int:
    """Handle meditate command."""
    if args.guide:
        steps = breathing_guide()
        for step in steps:
            print(step)
        return 0
    
    duration = args.duration
    print(f"Meditation timer: {format_duration(duration)}")
    print("Close your eyes and connect to the Force...\n")
    
    def progress(elapsed: int, total: int) -> None:
        remaining = total - elapsed
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}" if mins else f"{secs:02d}s"
        sys.stdout.write(f"\rTime remaining: {timer}   ")
        sys.stdout.flush()
    
    result = meditation_timer(duration, progress_callback=progress if not args.quiet else None)
    
    print("\n")
    if result['completed']:
        print("Meditation complete. The Force is with you.")
    else:
        print(f"Meditation interrupted after {format_duration(result['duration'])}.")
    
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    """Handle version command."""
    print(f"the-force v{__version__}")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='the-force',
        description='A Jedi CLI for wisdom, diagnostics, and meditation',
        epilog='May the Force be with you.'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'the-force {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # wisdom command
    wisdom_parser = subparsers.add_parser(
        'wisdom',
        help='Get Jedi wisdom',
        description='Receive wisdom from the Jedi Order'
    )
    wisdom_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all wisdom quotes'
    )
    wisdom_parser.add_argument(
        '-c', '--count',
        action='store_true',
        help='Show total number of quotes'
    )
    wisdom_parser.add_argument(
        '--color',
        choices=['blue', 'cyan', 'green', 'yellow', 'red'],
        default='cyan',
        help='Color for the quote (default: cyan)'
    )
    
    # diagnose command
    diagnose_parser = subparsers.add_parser(
        'diagnose',
        help='Run system diagnostics',
        description='Check system health with Jedi precision'
    )
    diagnose_parser.add_argument(
        '--json',
        action='store_true',
        help='Output diagnostics as JSON'
    )
    
    # meditate command
    meditate_parser = subparsers.add_parser(
        'meditate',
        help='Meditation timer',
        description='Center yourself with the Force'
    )
    meditate_parser.add_argument(
        '-d', '--duration',
        type=int,
        default=60,
        help='Meditation duration in seconds (default: 60)'
    )
    meditate_parser.add_argument(
        '-g', '--guide',
        action='store_true',
        help='Show breathing guide'
    )
    meditate_parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode - no progress display'
    )
    
    # version command (explicit)
    subparsers.add_parser(
        'version',
        help='Show version information'
    )
    
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'wisdom':
            return cmd_wisdom(args)
        elif args.command == 'diagnose':
            return cmd_diagnose(args)
        elif args.command == 'meditate':
            return cmd_meditate(args)
        elif args.command == 'version':
            return cmd_version(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
