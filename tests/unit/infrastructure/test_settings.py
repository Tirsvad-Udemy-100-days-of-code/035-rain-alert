"""Tests of the settings loader."""

from datetime import time
from pathlib import Path

import pytest

from rain_alert.infrastructure.settings import (
    SettingsError,
    load_environment,
    load_settings,
    parse_env_file,
)

SECRET_KEY = "key-1234567890"
PHONE = "+60123456789"
BASE = {
    "OPENWEATHER_APIKEY": SECRET_KEY,
    "PHONENUMBER": PHONE,
    "LATITUDE": "2.927761",
    "LONGITUDE": "101.897999",
}


def test_minimal_settings_use_defaults() -> None:
    settings = load_settings(BASE)
    assert settings.latitude == 2.927761
    assert settings.longitude == 101.897999
    assert settings.alert_time == time(7, 0)
    assert settings.timezone == "Asia/Kuala_Lumpur"
    assert settings.twilio_account_sid is None


def test_all_settings_are_read() -> None:
    settings = load_settings(
        BASE
        | {
            "ALERT_TIME": "6:45",
            "TZ": "Europe/Copenhagen",
            "TWILIO_ACCOUNT_SID": "AC1",
            "TWILIO_AUTH_TOKEN": "tok",
            "TWILIO_WHATSAPP_FROM": "+14155238886",
        }
    )
    assert settings.alert_time == time(6, 45)
    assert settings.timezone == "Europe/Copenhagen"
    assert settings.twilio_account_sid == "AC1"
    assert settings.twilio_whatsapp_from == "+14155238886"


@pytest.mark.parametrize(
    "key", ["OPENWEATHER_APIKEY", "PHONENUMBER", "LATITUDE", "LONGITUDE"]
)
def test_missing_setting_is_named(key: str) -> None:
    variables = {name: value for name, value in BASE.items() if name != key}
    with pytest.raises(SettingsError, match=key):
        load_settings(variables)


def test_blank_setting_counts_as_missing() -> None:
    with pytest.raises(SettingsError, match="PHONENUMBER"):
        load_settings(BASE | {"PHONENUMBER": "  "})


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("LATITUDE", "north"),
        ("LATITUDE", "91"),
        ("LONGITUDE", "-181"),
        ("ALERT_TIME", "25:00"),
        ("ALERT_TIME", "7am"),
    ],
)
def test_invalid_setting_is_named_without_its_value(key: str, value: str) -> None:
    with pytest.raises(SettingsError, match=key) as caught:
        load_settings(BASE | {key: value})
    assert value not in str(caught.value)


def test_text_form_of_settings_hides_secrets() -> None:
    text = repr(load_settings(BASE | {"TWILIO_AUTH_TOKEN": "tok-secret"}))
    for secret in (SECRET_KEY, PHONE, "tok-secret"):
        assert secret not in text


def test_env_file_lines_are_parsed() -> None:
    parsed = parse_env_file(
        "# comment\n\nA=1\nB = two \nC='quoted value'\nD=\"double\"\nnot a line\nE=\n"
    )
    assert parsed == {"A": "1", "B": "two", "C": "quoted value", "D": "double", "E": ""}


def test_variable_already_set_wins_over_the_file(tmp_path: Path) -> None:
    config = tmp_path / "config.env"
    config.write_text("A=from-file\nB=only-in-file\n", encoding="utf-8")
    merged = load_environment({"A": "from-environment"}, config)
    assert merged == {"A": "from-environment", "B": "only-in-file"}


def test_missing_file_is_ignored(tmp_path: Path) -> None:
    assert load_environment({"A": "1"}, tmp_path / "absent.env") == {"A": "1"}
