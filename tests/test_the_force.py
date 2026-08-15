"""Tests for the-force CLI toolkit."""

import pytest
from unittest.mock import patch, MagicMock
import json
import sys

from the_force.wisdom import (
    get_random_wisdom,
    get_all_wisdom,
    get_wisdom_by_index,
    format_wisdom,
    wisdom_count,
    WISDOM_QUOTES
)
from the_force.diagnostics import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
    get_load_average,
    get_all_diagnostics
)
from the_force.meditation import (
    meditation_timer,
    format_duration,
    breathing_guide
)
from the_force.cli import main, create_parser


class TestWisdom:
    """Test wisdom module."""
    
    def test_get_random_wisdom_returns_string(self):
        """Random wisdom should return a string."""
        quote = get_random_wisdom()
        assert isinstance(quote, str)
        assert len(quote) > 0
    
    def test_get_random_wisdom_returns_known_quote(self):
        """Random wisdom should be from the quotes list."""
        quote = get_random_wisdom()
        assert quote in WISDOM_QUOTES
    
    def test_get_all_wisdom_returns_list(self):
        """get_all_wisdom should return a list."""
        quotes = get_all_wisdom()
        assert isinstance(quotes, list)
        assert len(quotes) > 0
    
    def test_get_all_wisdom_returns_copy(self):
        """get_all_wisdom should return a copy, not the original."""
        quotes1 = get_all_wisdom()
        quotes2 = get_all_wisdom()
        quotes1.append("test")
        assert len(quotes1) != len(quotes2)
    
    def test_get_wisdom_by_index_valid(self):
        """get_wisdom_by_index with valid index should return quote."""
        quote = get_wisdom_by_index(0)
        assert quote is not None
        assert quote == WISDOM_QUOTES[0]
    
    def test_get_wisdom_by_index_invalid(self):
        """get_wisdom_by_index with invalid index should return None."""
        quote = get_wisdom_by_index(9999)
        assert quote is None
    
    def test_format_wisdom_with_color(self):
        """format_wisdom should add color codes."""
        quote = "Test quote"
        formatted = format_wisdom(quote, "green")
        assert quote in formatted
        assert "\033[" in formatted  # ANSI codes
    
    def test_format_wisdom_default_color(self):
        """format_wisdom should default to cyan."""
        quote = "Test"
        formatted = format_wisdom(quote)
        assert "\033[96m" in formatted  # Cyan
    
    def test_wisdom_count(self):
        """wisdom_count should match list length."""
        count = wisdom_count()
        assert count == len(WISDOM_QUOTES)
        assert count > 0


class TestDiagnostics:
    """Test diagnostics module."""
    
    @patch('subprocess.run')
    def test_get_cpu_usage_success(self, mock_run):
        """get_cpu_usage should parse top output."""
        mock_run.return_value = MagicMock(
            stdout="top output\n%Cpu(s): 12.3 us, 0.0 sy\nmore stuff"
        )
        cpu = get_cpu_usage()
        assert cpu == "12.3 us%"
    
    @patch('subprocess.run')
    def test_get_cpu_usage_failure(self, mock_run):
        """get_cpu_usage should handle errors."""
        mock_run.side_effect = Exception("Command failed")
        cpu = get_cpu_usage()
        assert cpu is None
    
    @patch('subprocess.run')
    def test_get_memory_usage_success(self, mock_run):
        """get_memory_usage should parse free output."""
        mock_run.return_value = MagicMock(
            stdout="              total        used        free\nMem:           3795        1287        2508\n"
        )
        mem = get_memory_usage()
        assert mem is not None
        assert mem['total'] == 3795
        assert mem['used'] == 1287
        assert mem['unit'] == 'MB'
    
    @patch('subprocess.run')
    def test_get_memory_usage_failure(self, mock_run):
        """get_memory_usage should handle errors."""
        mock_run.side_effect = Exception("Command failed")
        mem = get_memory_usage()
        assert mem is None
    
    @patch('subprocess.run')
    def test_get_disk_usage_success(self, mock_run):
        """get_disk_usage should parse df output."""
        mock_run.return_value = MagicMock(
            stdout="Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        29G  5.1G   23G  18% /\n"
        )
        disk = get_disk_usage()
        assert disk is not None
        assert disk['percent'] == '18%'
        assert disk['mount'] == '/'
    
    @patch('subprocess.run')
    def test_get_disk_usage_failure(self, mock_run):
        """get_disk_usage should handle errors."""
        mock_run.side_effect = Exception("Command failed")
        disk = get_disk_usage()
        assert disk is None
    
    @patch('subprocess.run')
    def test_get_uptime_success(self, mock_run):
        """get_uptime should parse uptime -p output."""
        mock_run.return_value = MagicMock(stdout="up 2 hours, 30 minutes")
        uptime = get_uptime()
        assert uptime == "up 2 hours, 30 minutes"
    
    def test_get_load_average(self):
        """get_load_average should return load averages."""
        load = get_load_average()
        assert load is not None
        assert '1min' in load
        assert '5min' in load
        assert '15min' in load
    
    @patch('the_force.diagnostics.get_cpu_usage')
    @patch('the_force.diagnostics.get_memory_usage')
    @patch('the_force.diagnostics.get_disk_usage')
    @patch('the_force.diagnostics.get_uptime')
    @patch('the_force.diagnostics.get_load_average')
    @patch('the_force.diagnostics.get_network_interfaces')
    def test_get_all_diagnostics(self, mock_net, mock_load, mock_uptime, 
                                  mock_disk, mock_mem, mock_cpu):
        """get_all_diagnostics should combine all metrics."""
        mock_cpu.return_value = "10%"
        mock_mem.return_value = {'total': 1000, 'used': 500, 'available': 500, 'unit': 'MB'}
        mock_disk.return_value = {'percent': '50%'}
        mock_uptime.return_value = "up 1 hour"
        mock_load.return_value = {'1min': '0.5', '5min': '0.3', '15min': '0.2'}
        mock_net.return_value = []
        
        diagnostics = get_all_diagnostics()
        assert diagnostics['cpu'] == "10%"
        assert diagnostics['memory']['total'] == 1000
        assert diagnostics['disk']['percent'] == "50%"


class TestMeditation:
    """Test meditation module."""
    
    def test_format_duration_seconds(self):
        """format_duration should format seconds."""
        assert format_duration(45) == "45s"
    
    def test_format_duration_minutes(self):
        """format_duration should format minutes."""
        assert format_duration(120) == "2m"
    
    def test_format_duration_mixed(self):
        """format_duration should format minutes and seconds."""
        assert format_duration(90) == "1m 30s"
    
    def test_breathing_guide_returns_list(self):
        """breathing_guide should return a list of steps."""
        guide = breathing_guide()
        assert isinstance(guide, list)
        assert len(guide) > 0
    
    def test_meditation_timer_short(self):
        """meditation_timer should complete for short duration."""
        result = meditation_timer(duration=1, tick=0.5)
        assert result['completed'] is True
        assert result['duration'] == 1
    
    def test_meditation_timer_with_callback(self):
        """meditation_timer should call progress callback."""
        callback_calls = []
        def callback(elapsed, total):
            callback_calls.append((elapsed, total))
        
        result = meditation_timer(duration=1, progress_callback=callback, tick=0.5)
        assert result['completed'] is True
        assert len(callback_calls) > 0


class TestCLI:
    """Test CLI module."""
    
    def test_create_parser(self):
        """create_parser should return ArgumentParser."""
        parser = create_parser()
        assert parser is not None
    
    def test_main_no_args(self, capsys):
        """main with no args should print help and return 0."""
        result = main([])
        assert result == 0
        captured = capsys.readouterr()
        assert "Jedi CLI" in captured.out
    
    def test_main_wisdom_command(self, capsys):
        """main with wisdom command should print quote."""
        result = main(['wisdom'])
        assert result == 0
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    def test_main_wisdom_list(self, capsys):
        """main with wisdom --list should print all quotes."""
        result = main(['wisdom', '--list'])
        assert result == 0
        captured = capsys.readouterr()
        assert "Total:" in captured.out
    
    def test_main_wisdom_count(self, capsys):
        """main with wisdom --count should print count."""
        result = main(['wisdom', '--count'])
        assert result == 0
        captured = capsys.readouterr()
        assert "contains" in captured.out
    
    def test_main_diagnose_command(self, capsys):
        """main with diagnose command should print diagnostics."""
        result = main(['diagnose'])
        assert result == 0
        captured = capsys.readouterr()
        assert "Jedi System Diagnostics" in captured.out
    
    def test_main_diagnose_json(self, capsys):
        """main with diagnose --json should output JSON."""
        result = main(['diagnose', '--json'])
        assert result == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert 'cpu' in data
        assert 'memory' in data
    
    def test_main_meditate_guide(self, capsys):
        """main with meditate --guide should print breathing guide."""
        result = main(['meditate', '--guide'])
        assert result == 0
        captured = capsys.readouterr()
        assert "breathe" in captured.out.lower() or "inhale" in captured.out.lower()
    
    def test_main_version_command(self, capsys):
        """main with version command should print version."""
        result = main(['version'])
        assert result == 0
        captured = capsys.readouterr()
        assert "the-force" in captured.out


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
