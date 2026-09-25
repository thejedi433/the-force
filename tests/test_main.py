"""Test __main__.py module execution."""

import subprocess
import sys


def test_main_module_execution():
    """python -m the_force should execute successfully."""
    result = subprocess.run(
        [sys.executable, "-m", "the_force", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Jedi CLI" in result.stdout


def test_main_module_import():
    """__main__.py should be importable."""
    import the_force.__main__
    assert hasattr(the_force.__main__, "main")
