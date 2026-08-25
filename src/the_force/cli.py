#!/usr/bin/env python3
"""CLI interface for the-force Jedi toolkit."""

import argparse
import sys
import json
from typing import Optional

from the_force import __version__
from the_force.wisdom import get_random_wisdom, get_all_wisdom, format_wisdom, wisdom_count
from the_force.diagnostics import get_all_diagnostics, get_cpu_usage, get_memory_usage, get_disk_usage, get_force_sensitivity
from the_force.meditation import meditation_timer, format_duration, breathing_guide
from the_force.lightsaber import get_random_lightsaber, get_lightsaber_by_name, get_all_lightsaber_colors
from the_force.sith import get_random_sith_quote, get_all_sith_quotes, format_sith_quote, sith_quote_count, get_sith_code
from the_force.holocron import Holocron, HolocronError


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


def cmd_sensitivity(args: argparse.Namespace) -> int:
    """Handle sensitivity command."""
    sensitivity = get_force_sensitivity()
    print("\n=== Force Sensitivity Analysis ===\n")
    print(f"Score: {sensitivity['score']}/100")
    print(f"Level: {sensitivity['level']}")
    print(f"\n{sensitivity['message']}")
    return 0


def cmd_lightsaber(args: argparse.Namespace) -> int:
    """Handle lightsaber command."""
    if hasattr(args, 'list') and args.list:
        colors = get_all_lightsaber_colors()
        print("=== All Lightsaber Colors ===\n")
        for color in colors:
            print(f"  • {color}")
        return 0
    
    saber = get_random_lightsaber()
    color_codes = {
        'blue': '\033[94m',
        'green': '\033[92m',
        'red': '\033[91m',
        'purple': '\033[95m',
        'yellow': '\033[93m',
        'white': '\033[97m',
        'cyan': '\033[96m'
    }
    color_code = color_codes.get(saber['color'], '\033[96m')
    reset = '\033[0m'
    
    print("\n=== Random Lightsaber ===\n")
    print(f"{color_code}{saber['name']}'s Lightsaber{reset}")
    print(f"Color: {saber['color']}")
    print(f"Alignment: {saber['alignment']}")
    print(f"\n{saber['description']}")
    return 0


def cmd_sith(args: argparse.Namespace) -> int:
    """Handle sith command."""
    if args.list:
        quotes = get_all_sith_quotes()
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {quote}")
        print(f"\nTotal: {sith_quote_count()} Sith quotes")
        return 0
    
    if args.code:
        print("\n=== The Sith Code ===\n")
        print(format_sith_quote(get_sith_code(), color="red"))
        return 0
    
    quote = get_random_sith_quote()
    print(format_sith_quote(quote, args.color))
    return 0


def cmd_holocron(args: argparse.Namespace) -> int:
    """Handle holocron command."""
    import os
    db_path = os.path.expanduser("~/.the_force_holocron.json")
    holocron = Holocron(db_path)
    
    if args.add is not None:
        source = args.source or ""
        tags = getattr(args, 'tag', None) or []
        try:
            entry_id = holocron.add_entry(args.add, source, tags=tags if tags else None)
            print(f"✓ Wisdom recorded (ID: {entry_id})")
        except HolocronError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        return 0
    
    if args.delete is not None:
        if holocron.delete_entry(args.delete):
            print(f"✓ Entry {args.delete} deleted")
        else:
            print(f"Entry {args.delete} not found")
        return 0
    
    if args.update is not None:
        if args.text is None and args.source is None and not getattr(args, 'tag', None):
            print("Error: --update requires at least one of --text, --source, or --tag")
            return 1
        try:
            tags = getattr(args, 'tag', None)
            if holocron.update_entry(args.update, text=args.text, source=args.source, tags=tags):
                print(f"✓ Entry {args.update} updated")
            else:
                print(f"Entry {args.update} not found")
                return 1
        except HolocronError as e:
            print(f"Error: {e}")
            return 1
        return 0
    
    if getattr(args, 'tags', False):
        all_tags = holocron.get_all_tags()
        if not all_tags:
            print("No tags found in your holocron.")
            return 0
        print("=== Holocron Tags ===\n")
        for tag in all_tags:
            print(f"  • {tag}")
        print(f"\n{len(all_tags)} unique tags")
        return 0
    
    if args.list:
        entries = holocron.list_entries(limit=args.limit)
        if not entries:
            print("Your holocron is empty. Record wisdom with: the-force holocron --add \"text\"")
            return 0
        for entry in entries:
            source_str = f" — {entry['source']}" if entry['source'] else ""
            tags_str = ""
            if entry.get('tags'):
                tags_str = f" [{', '.join(entry['tags'])}]"
            print(f"[{entry['id']}] {entry['text']}{source_str}{tags_str}")
        print(f"\n{holocron.entry_count()} total entries")
        return 0
    
    if args.search is not None or getattr(args, 'tag', None):
        tag_filter = getattr(args, 'tag', None)
        # If --tag used alone (no --search), use first tag as filter
        if args.search is None and tag_filter:
            tag_filter = tag_filter[0]
        try:
            results = holocron.search_entries(
                query=args.search,
                tag=tag_filter if tag_filter else None
            )
            if not results:
                search_desc = args.search or ""
                if tag_filter:
                    search_desc += f" tag:{tag_filter}"
                print(f"No entries found matching '{search_desc.strip()}'")
                return 0
            for entry in results:
                source_str = f" — {entry['source']}" if entry['source'] else ""
                tags_str = ""
                if entry.get('tags'):
                    tags_str = f" [{', '.join(entry['tags'])}]"
                print(f"[{entry['id']}] {entry['text']}{source_str}{tags_str}")
            print(f"\n{len(results)} entries found")
        except HolocronError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        return 0
    
    # Default: show count and recent
    count = holocron.entry_count()
    print(f"Your holocron contains {count} entries.")
    if count > 0:
        print("\nRecent entries:")
        for entry in holocron.list_entries(limit=3):
            source_str = f" — {entry['source']}" if entry['source'] else ""
            tags_str = ""
            if entry.get('tags'):
                tags_str = f" [{', '.join(entry['tags'])}]"
            print(f"  [{entry['id']}] {entry['text']}{source_str}{tags_str}")
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
    
    # sensitivity command
    subparsers.add_parser(
        'sensitivity',
        help='Measure Force sensitivity',
        description='Analyze system\'s connection to the Force'
    )
    
    # lightsaber command
    lightsaber_parser = subparsers.add_parser(
        'lightsaber',
        help='Get a random lightsaber',
        description='Discover lightsabers from the Star Wars universe'
    )
    lightsaber_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all available lightsaber colors'
    )
    
    # sith command
    sith_parser = subparsers.add_parser(
        'sith',
        help='Dark side quotes for contrast',
        description='Receive wisdom from the Sith - the dark side of the Force'
    )
    sith_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all Sith quotes'
    )
    sith_parser.add_argument(
        '-c', '--code',
        action='store_true',
        help='Display the Sith Code'
    )
    sith_parser.add_argument(
        '--color',
        choices=['red', 'purple', 'yellow'],
        default='red',
        help='Color for the quote (default: red)'
    )
    
    # holocron command
    holocron_parser = subparsers.add_parser(
        'holocron',
        help='Personal wisdom journal',
        description='Record and retrieve your own Jedi wisdom'
    )
    holocron_parser.add_argument(
        '-a', '--add',
        type=str,
        metavar='TEXT',
        help='Add a wisdom entry'
    )
    holocron_parser.add_argument(
        '-s', '--source',
        type=str,
        help='Source/author of the wisdom (used with --add)'
    )
    holocron_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all holocron entries'
    )
    holocron_parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of entries shown'
    )
    holocron_parser.add_argument(
        '--search',
        type=str,
        metavar='QUERY',
        help='Search entries by text'
    )
    holocron_parser.add_argument(
        '-d', '--delete',
        type=int,
        metavar='ID',
        help='Delete an entry by ID'
    )
    
    holocron_parser.add_argument(
        '-u', '--update',
        type=int,
        metavar='ID',
        help='Update an entry by ID (use with --text and/or --source)'
    )
    
    holocron_parser.add_argument(
        '--text',
        type=str,
        help='New text for update (used with --update)'
    )
    
    holocron_parser.add_argument(
        '--tag',
        type=str,
        action='append',
        metavar='TAG',
        help='Tag for entry (used with --add, --update, --search, or --tag alone to search by tag)'
    )
    
    holocron_parser.add_argument(
        '--tags',
        action='store_true',
        help='List all unique tags'
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
        elif args.command == 'sensitivity':
            return cmd_sensitivity(args)
        elif args.command == 'lightsaber':
            return cmd_lightsaber(args)
        elif args.command == 'sith':
            return cmd_sith(args)
        elif args.command == 'holocron':
            return cmd_holocron(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
