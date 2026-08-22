"""Tests for uncovered CLI and diagnostics paths."""

import pytest
from unittest.mock import patch, MagicMock, Mock
import tempfile
import os
import json

from the_force.cli import (
    cmd_meditate, cmd_lightsaber, cmd_holocron, main
)
from the_force.diagnostics import get_force_sensitivity
from the_force.holocron import Holocron, HolocronError


class TestCLIUncoveredPaths:
    """Test uncovered CLI command paths."""

    def test_cmd_meditate_with_duration(self, capsys):
        """cmd_meditate with duration should run timer."""
        parser = MagicMock()
        args = MagicMock()
        args.guide = False
        args.duration = 1
        args.quiet = True
        
        with patch('the_force.cli.meditation_timer') as mock_timer:
            mock_timer.return_value = {'completed': True, 'duration': 1}
            result = cmd_meditate(args)
            
        assert result == 0
        captured = capsys.readouterr()
        assert "Meditation timer:" in captured.out
        assert "Meditation complete" in captured.out

    def test_cmd_meditate_interrupted(self, capsys):
        """cmd_meditate should handle interrupted meditation."""
        args = MagicMock()
        args.guide = False
        args.duration = 1
        args.quiet = True
        
        with patch('the_force.cli.meditation_timer') as mock_timer:
            mock_timer.return_value = {'completed': False, 'duration': 0}
            result = cmd_meditate(args)
            
        assert result == 0
        captured = capsys.readouterr()
        assert "Meditation interrupted" in captured.out

    def test_cmd_lightsaber_list(self, capsys):
        """cmd_lightsaber with --list should show all colors."""
        args = MagicMock()
        args.list = True
        
        result = cmd_lightsaber(args)
        
        assert result == 0
        captured = capsys.readouterr()
        assert "All Lightsaber Colors" in captured.out
        assert "•" in captured.out

    def test_cmd_holocron_update_no_args(self, capsys):
        """cmd_holocron --update without text/source/tag should error."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = 1
        args.text = None
        args.source = None
        args.tag = None
        args.tags = False
        args.list = False
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron'):
            result = cmd_holocron(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: --update requires" in captured.out

    def test_cmd_holocron_update_not_found(self, capsys):
        """cmd_holocron --update with non-existent ID should fail."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = 999
        args.text = "Updated text"
        args.source = None
        args.tag = None
        args.tags = False
        args.list = False
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.update_entry.return_value = False
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_cmd_holocron_tags_empty(self, capsys):
        """cmd_holocron --tags with empty holocron should show message."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = True
        args.list = False
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.get_all_tags.return_value = []
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "No tags found" in captured.out

    def test_cmd_holocron_tags_with_entries(self, capsys):
        """cmd_holocron --tags with tags should display them."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = True
        args.list = False
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.get_all_tags.return_value = ['jedi', 'wisdom']
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "jedi" in captured.out
        assert "2 unique tags" in captured.out

    def test_cmd_holocron_list_empty(self, capsys):
        """cmd_holocron --list with empty holocron should show message."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = True
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.list_entries.return_value = []
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Your holocron is empty" in captured.out

    def test_cmd_holocron_list_with_entries(self, capsys):
        """cmd_holocron --list with entries should display them."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = True
        args.search = None
        args.limit = 10

        entries = [
            {"id": 1, "text": "First wisdom", "source": "Yoda", "tags": ["jedi"]},
            {"id": 2, "text": "Second wisdom", "source": None, "tags": []}
        ]

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.list_entries.return_value = entries
            mock_instance.entry_count.return_value = 2
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "First wisdom" in captured.out
        assert "Yoda" in captured.out
        assert "[jedi]" in captured.out
        assert "2 total entries" in captured.out

    def test_cmd_holocron_search_no_results(self, capsys):
        """cmd_holocron --search with no matches should show message."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = "nonexistent"
        args.tag = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.search_entries.return_value = []
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "No entries found" in captured.out

    def test_cmd_holocron_search_with_tag_filter(self, capsys):
        """cmd_holocron --search --tag should filter by tag."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = "wisdom"
        args.tag = ["jedi"]
        args.limit = 10

        results = [
            {"id": 1, "text": "Test wisdom", "source": None, "tags": ["jedi"]}
        ]

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.search_entries.return_value = results
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Test wisdom" in captured.out
        assert "1 entries found" in captured.out

    def test_cmd_holocron_search_tag_only(self, capsys):
        """cmd_holocron --tag (no --search) should use tag as filter."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = None
        args.tag = ["jedi"]
        args.limit = 10

        results = [
            {"id": 1, "text": "Tagged wisdom", "source": None, "tags": ["jedi"]}
        ]

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.search_entries.return_value = results
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Tagged wisdom" in captured.out

    def test_cmd_holocron_search_holocron_error(self, capsys):
        """cmd_holocron --search raising HolocronError should handle gracefully."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = "test"
        args.tag = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.search_entries.side_effect = HolocronError("DB error")
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: DB error" in captured.err

    def test_cmd_holocron_default_with_entries(self, capsys):
        """cmd_holocron with no args should show count and recent entries."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = None
        args.tag = None
        args.limit = 10

        entries = [
            {"id": 1, "text": "First wisdom", "source": "Yoda", "tags": ["jedi"]},
            {"id": 2, "text": "Second wisdom", "source": None, "tags": []}
        ]

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.entry_count.return_value = 2
            mock_instance.list_entries.return_value = entries
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Your holocron contains 2 entries" in captured.out
        assert "Recent entries:" in captured.out

    def test_cmd_holocron_default_empty(self, capsys):
        """cmd_holocron with no args and empty holocron should just show count."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = None
        args.tags = False
        args.list = False
        args.search = None
        args.tag = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.entry_count.return_value = 0
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Your holocron contains 0 entries" in captured.out

    def test_cmd_holocron_add_holocron_error(self, capsys):
        """cmd_holocron --add raising HolocronError should handle gracefully."""
        args = MagicMock()
        args.add = "Some wisdom"
        args.source = "Yoda"
        args.tag = None

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.add_entry.side_effect = HolocronError("DB error")
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: DB error" in captured.err

    def test_cmd_holocron_update_holocron_error(self, capsys):
        """cmd_holocron --update raising HolocronError should handle gracefully."""
        args = MagicMock()
        args.add = None
        args.delete = None
        args.update = 1
        args.text = "New text"
        args.source = None
        args.tag = None
        args.tags = False
        args.list = False
        args.search = None
        args.limit = 10

        with patch('the_force.cli.Holocron') as MockHolocron:
            mock_instance = MagicMock()
            mock_instance.update_entry.side_effect = HolocronError("DB error")
            MockHolocron.return_value = mock_instance
            result = cmd_holocron(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: DB error" in captured.out

    def test_main_keyboard_interrupt(self, capsys):
        """main should handle KeyboardInterrupt gracefully."""
        with patch('the_force.cli.create_parser') as mock_parser:
            mock_instance = MagicMock()
            mock_args = MagicMock()
            mock_args.command = 'wisdom'
            mock_instance.parse_args.return_value = mock_args
            mock_parser.return_value = mock_instance
            
            with patch('the_force.cli.cmd_wisdom', side_effect=KeyboardInterrupt()):
                result = main()
            
            assert result == 130
            captured = capsys.readouterr()
            assert "Interrupted" in captured.out

    def test_main_generic_exception(self, capsys):
        """main should handle generic exceptions."""
        with patch('the_force.cli.create_parser') as mock_parser:
            mock_instance = MagicMock()
            mock_args = MagicMock()
            mock_args.command = 'wisdom'
            mock_instance.parse_args.return_value = mock_args
            mock_parser.return_value = mock_instance
            
            with patch('the_force.cli.cmd_wisdom', side_effect=Exception("Test error")):
                result = main()
            
            assert result == 1
            captured = capsys.readouterr()
            assert "Error: Test error" in captured.err

    def test_main_unknown_command(self, capsys):
        """main with unknown command should print help."""
        with patch('the_force.cli.create_parser') as mock_parser:
            mock_instance = MagicMock()
            mock_args = MagicMock()
            mock_args.command = 'unknown_cmd'
            mock_instance.parse_args.return_value = mock_args
            mock_parser.return_value = mock_instance
            
            result = main()
            
            assert result == 1
            mock_instance.print_help.assert_called()


class TestDiagnosticsUncoveredPaths:
    """Test uncovered diagnostics error handling paths."""

    @patch('the_force.diagnostics.subprocess.run')
    @patch('the_force.diagnostics.get_load_average')
    @patch('the_force.diagnostics.get_memory_usage')
    @patch('the_force.diagnostics.get_cpu_usage')
    def test_force_sensitivity_cpu_parse_error(self, mock_cpu, mock_mem, mock_load, mock_net):
        """get_force_sensitivity should handle CPU parse errors."""
        mock_cpu.return_value = "invalid%"
        mock_mem.return_value = {'used': 4000, 'total': 8000, 'unit': 'MB'}
        mock_load.return_value = {'1min': 1.0, '5min': 0.8, '15min': 0.6}
        mock_net.return_value = []
        
        result = get_force_sensitivity()
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'level' in result

    @patch('the_force.diagnostics.subprocess.run')
    @patch('the_force.diagnostics.get_load_average')
    @patch('the_force.diagnostics.get_memory_usage')
    @patch('the_force.diagnostics.get_cpu_usage')
    def test_force_sensitivity_load_parse_error(self, mock_cpu, mock_mem, mock_load, mock_net):
        """get_force_sensitivity should handle load average parse errors."""
        mock_cpu.return_value = "10.0%"
        mock_mem.return_value = {'used': 4000, 'total': 8000, 'unit': 'MB'}
        mock_load.return_value = {'1min': 'invalid'}
        mock_net.return_value = []
        
        result = get_force_sensitivity()
        
        assert isinstance(result, dict)
        assert 'score' in result

    @patch('the_force.diagnostics.subprocess.run')
    @patch('the_force.diagnostics.get_load_average')
    @patch('the_force.diagnostics.get_memory_usage')
    @patch('the_force.diagnostics.get_cpu_usage')
    def test_force_sensitivity_memory_zero_division(self, mock_cpu, mock_mem, mock_load, mock_net):
        """get_force_sensitivity should handle zero memory total."""
        mock_cpu.return_value = "10.0%"
        mock_mem.return_value = {'used': 0, 'total': 0, 'unit': 'MB'}
        mock_load.return_value = {'1min': 1.0, '5min': 0.8, '15min': 0.6}
        mock_net.return_value = []
        
        result = get_force_sensitivity()
        
        assert isinstance(result, dict)
        assert 'score' in result

    @patch('the_force.diagnostics.get_cpu_usage')
    @patch('the_force.diagnostics.get_memory_usage')
    @patch('the_force.diagnostics.get_load_average')
    @patch('the_force.diagnostics.get_network_interfaces')
    def test_force_sensitivity_levels(self, mock_net, mock_load, mock_mem, mock_cpu):
        """get_force_sensitivity should return correct level for different scores."""
        # Test Master level (score >= 90)
        mock_cpu.return_value = "1.0%"
        mock_mem.return_value = {'used': 5000, 'total': 10000, 'unit': 'MB'}
        mock_load.return_value = {'1min': 0.1, '5min': 0.1, '15min': 0.1}
        mock_net.return_value = []
        result = get_force_sensitivity()
        assert result['level'] == 'Master'
        assert result['score'] >= 90

        # Test Weak level (score < 30)
        mock_cpu.return_value = "80.0%"
        mock_mem.return_value = {'used': 9800, 'total': 10000, 'unit': 'MB'}
        mock_load.return_value = {'1min': 4.0, '5min': 4.0, '15min': 4.0}
        result = get_force_sensitivity()
        assert result['level'] == 'Weak'
        assert result['score'] < 50
