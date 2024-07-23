import subprocess
from pathlib import Path
from tests.base_test import COUNTER_PROJECT_PATH
import os

EXPECTED_HELP_TEXT = "Runs a script"


def test_run_help():
    result = subprocess.run(
        ["gab", "run", "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        EXPECTED_HELP_TEXT in result.stdout
    ), "Help output does not contain expected text"
    assert result.returncode == 0


def test_run_gaboon_project():
    current_dir = Path.cwd()
    try:
        os.chdir(COUNTER_PROJECT_PATH)
        result = subprocess.run(
            ["gab", "run", "deploy"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "Running run command" in result.stderr
        assert result.returncode == 0
    finally:
        os.chdir(current_dir)
