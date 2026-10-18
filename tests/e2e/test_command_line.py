"""End-to-end tests: run the program as a separate process (no network)."""

import os
import subprocess
import sys

SECRET = "owm-secret-key-should-not-show"


def _run(*args: str, **env: str) -> subprocess.CompletedProcess[str]:
    clean = {
        key: value
        for key, value in os.environ.items()
        if key not in {"OPENWEATHER_APIKEY", "PHONENUMBER", "LATITUDE", "LONGITUDE"}
    }
    return subprocess.run(
        [sys.executable, "-m", "rain_alert", *args, "--config", "no-such-config.env"],
        capture_output=True,
        text=True,
        env=clean | env,
        cwd=os.environ.get("TEMP", "."),
        timeout=60,
        check=False,
    )


def test_help_describes_the_options() -> None:
    result = _run("--help")
    assert result.returncode == 0
    assert "--once" in result.stdout
    assert "--dry-run" in result.stdout


def test_missing_settings_exit_with_code_2_and_name_the_key() -> None:
    result = _run("--once", "--dry-run", PHONENUMBER="+60123456789")
    assert result.returncode == 2
    assert "OPENWEATHER_APIKEY" in result.stderr
    assert "+60123456789" not in result.stderr + result.stdout


def test_invalid_setting_exit_code_and_no_value_is_shown() -> None:
    result = _run(
        "--once",
        "--dry-run",
        OPENWEATHER_APIKEY=SECRET,
        PHONENUMBER="+60123456789",
        LATITUDE="north",
        LONGITUDE="101",
    )
    assert result.returncode == 2
    assert "LATITUDE" in result.stderr
    assert SECRET not in result.stderr + result.stdout
