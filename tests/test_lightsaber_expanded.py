"""Tests for expanded lightsaber functionality.

TDD tests for:
- More iconic lightsabers (Ahsoka, Rey, Kylo Ren, Dooku, etc.)
- get_lightsabers_by_color()
- get_lightsabers_by_alignment()
- lightsaber_count()
- CLI flags: --name, --color, --alignment, --count
"""

import pytest
from unittest.mock import patch, MagicMock

from the_force.lightsaber import (
    get_random_lightsaber,
    get_lightsaber_by_name,
    get_all_lightsaber_colors,
    get_lightsabers_by_color,
    get_lightsabers_by_alignment,
    lightsaber_count,
    LIGHTSABERS,
)
from the_force.cli import main, cmd_lightsaber, create_parser


class TestExpandedLightsaberCollection:
    """Test that the expanded lightsaber collection includes iconic characters."""

    def test_has_minimum_count(self):
        """Collection should have at least 12 lightsabers."""
        assert lightsaber_count() >= 12

    def test_has_ahsoka(self):
        """Ahsoka Tano with white lightsabers should exist."""
        saber = get_lightsaber_by_name("Ahsoka")
        assert saber is not None
        assert saber["color"] == "white"
        assert saber["alignment"] == "Light"

    def test_has_rey(self):
        """Rey with yellow lightsaber should exist."""
        saber = get_lightsaber_by_name("Rey")
        assert saber is not None
        assert saber["color"] == "yellow"

    def test_has_kylo_ren(self):
        """Kylo Ren with crossguard red lightsaber should exist."""
        saber = get_lightsaber_by_name("Kylo Ren")
        assert saber is not None
        assert saber["color"] == "red"
        assert "crossguard" in saber["description"].lower() or "cross-guard" in saber["description"].lower()

    def test_has_dooku(self):
        """Count Dooku with curved-hilt lightsaber should exist."""
        saber = get_lightsaber_by_name("Dooku")
        assert saber is not None
        assert saber["color"] == "red"
        assert saber["alignment"] == "Dark"

    def test_all_sabers_have_required_fields(self):
        """Every lightsaber must have name, color, description, alignment."""
        required = {"name", "color", "description", "alignment"}
        for saber in LIGHTSABERS:
            missing = required - set(saber.keys())
            assert not missing, f"{saber.get('name', '?')} missing keys: {missing}"

    def test_all_alignments_are_valid(self):
        """Alignment must be Light, Dark, or Balanced."""
        valid = {"Light", "Dark", "Balanced"}
        for saber in LIGHTSABERS:
            assert saber["alignment"] in valid, f"{saber['name']} has invalid alignment {saber['alignment']}"


class TestLightsaberCount:
    """Test lightsaber_count()."""

    def test_returns_int(self):
        count = lightsaber_count()
        assert isinstance(count, int)
        assert count > 0

    def test_matches_list_length(self):
        assert lightsaber_count() == len(LIGHTSABERS)


class TestGetLightsabersByColor:
    """Test get_lightsabers_by_color()."""

    def test_filter_by_red(self):
        reds = get_lightsabers_by_color("red")
        assert len(reds) >= 3  # Vader, Sidious, Maul, Kylo, Dooku...
        assert all(s["color"] == "red" for s in reds)

    def test_filter_by_blue(self):
        blues = get_lightsabers_by_color("blue")
        assert len(blues) >= 2
        assert all(s["color"] == "blue" for s in blues)

    def test_filter_case_insensitive(self):
        """Color filter should be case-insensitive."""
        upper = get_lightsabers_by_color("RED")
        lower = get_lightsabers_by_color("red")
        assert len(upper) == len(lower)
        assert len(upper) > 0

    def test_filter_nonexistent_color(self):
        """Unknown color returns empty list, not error."""
        result = get_lightsabers_by_color("pink")
        assert result == []

    def test_returns_copy(self):
        """Returned list should be a copy (not the internal data)."""
        r1 = get_lightsabers_by_color("red")
        r2 = get_lightsabers_by_color("red")
        r1.clear()
        assert len(r2) > 0


class TestGetLightsabersByAlignment:
    """Test get_lightsabers_by_alignment()."""

    def test_filter_light(self):
        light = get_lightsabers_by_alignment("Light")
        assert len(light) >= 4
        assert all(s["alignment"] == "Light" for s in light)

    def test_filter_dark(self):
        dark = get_lightsabers_by_alignment("Dark")
        assert len(dark) >= 3
        assert all(s["alignment"] == "Dark" for s in dark)

    def test_filter_case_insensitive(self):
        upper = get_lightsabers_by_alignment("LIGHT")
        lower = get_lightsabers_by_alignment("Light")
        assert len(upper) == len(lower)

    def test_filter_invalid_alignment(self):
        result = get_lightsabers_by_alignment("Neutral")
        assert result == []

    def test_returns_copy(self):
        r1 = get_lightsabers_by_alignment("Light")
        r2 = get_lightsabers_by_alignment("Light")
        r1.clear()
        assert len(r2) > 0


class TestLightsaberCLI:
    """Test CLI flags for lightsaber command."""

    def test_cli_lookup_by_name(self, capsys):
        """lightsaber --name Anakin should show Anakin's lightsaber."""
        result = main(["lightsaber", "--name", "Anakin"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Anakin" in captured.out
        assert "blue" in captured.out

    def test_cli_lookup_by_name_case_insensitive(self, capsys):
        """Name lookup should be case-insensitive."""
        result = main(["lightsaber", "--name", "anakin"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Anakin" in captured.out

    def test_cli_lookup_unknown_name(self, capsys):
        """Unknown name should print not-found message and return 0."""
        result = main(["lightsaber", "--name", "JarJar"])
        assert result == 0
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "unknown" in captured.out.lower()

    def test_cli_filter_by_color(self, capsys):
        """lightsaber --color red should list all red sabers."""
        result = main(["lightsaber", "--color", "red"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Vader" in captured.out or "red" in captured.out.lower()

    def test_cli_filter_by_alignment(self, capsys):
        """lightsaber --alignment Dark should list dark-side sabers."""
        result = main(["lightsaber", "--alignment", "Dark"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Vader" in captured.out or "Dark" in captured.out

    def test_cli_count(self, capsys):
        """lightsaber --count should print total count."""
        result = main(["lightsaber", "--count"])
        assert result == 0
        captured = capsys.readouterr()
        assert str(lightsaber_count()) in captured.out

    def test_cli_list_shows_colors(self, capsys):
        """lightsaber --list should still work."""
        result = main(["lightsaber", "--list"])
        assert result == 0
        captured = capsys.readouterr()
        assert "All Lightsaber Colors" in captured.out

    def test_cli_random_default(self, capsys):
        """lightsaber with no flags should show a random saber."""
        result = main(["lightsaber"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Random Lightsaber" in captured.out or "Lightsaber" in captured.out


class TestCmdLightsaberDirect:
    """Test cmd_lightsaber handler directly with various args."""

    def test_cmd_name_found(self, capsys):
        args = MagicMock()
        args.name = "Mace Windu"
        args.list = False
        args.color = None
        args.alignment = None
        args.count = False
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "Mace Windu" in captured.out
        assert "purple" in captured.out

    def test_cmd_color_filter(self, capsys):
        args = MagicMock()
        args.name = None
        args.list = False
        args.color = "green"
        args.alignment = None
        args.count = False
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "Luke" in captured.out or "Yoda" in captured.out

    def test_cmd_alignment_filter(self, capsys):
        args = MagicMock()
        args.name = None
        args.list = False
        args.color = None
        args.alignment = "Dark"
        args.count = False
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "Dark" in captured.out

    def test_cmd_count(self, capsys):
        args = MagicMock()
        args.name = None
        args.list = False
        args.color = None
        args.alignment = None
        args.count = True
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert str(lightsaber_count()) in captured.out

    def test_cmd_unknown_color_returns_empty(self, capsys):
        args = MagicMock()
        args.name = None
        args.list = False
        args.color = "pink"
        args.alignment = None
        args.count = False
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "No lightsabers found" in captured.out or "0" in captured.out

    def test_cmd_unknown_alignment_returns_empty(self, capsys):
        args = MagicMock()
        args.name = None
        args.list = False
        args.color = None
        args.alignment = "Neutral"
        args.count = False
        result = cmd_lightsaber(args)
        assert result == 0
        captured = capsys.readouterr()
        assert "No lightsabers found" in captured.out or "Neutral" in captured.out
