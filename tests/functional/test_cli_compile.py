import subprocess

EXPECTED_HELP_TEXT = "Vyper compiler"


def test_compile_help():
    result = subprocess.run(
        ["gab", "compile", "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        EXPECTED_HELP_TEXT in result.stdout
    ), "Help output does not contain expected text"
    assert result.returncode == 0
