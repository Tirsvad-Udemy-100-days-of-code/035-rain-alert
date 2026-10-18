"""Smoke test of the constants and the package."""

import rain_alert
from rain_alert import constants


def test_package_has_a_version() -> None:
    assert rain_alert.__version__ == "0.1.0"


def test_rain_rule_follows_the_course() -> None:
    assert constants.RAIN_CONDITION_LIMIT == 700
    assert constants.FORECAST_HOURS == 12


def test_forecast_url_is_one_call_4() -> None:
    assert constants.FORECAST_URL.endswith("/data/4.0/onecall/timeline/1h")


def test_twilio_url_takes_the_account_sid() -> None:
    url = constants.TWILIO_MESSAGES_URL.format(account_sid="AC123")
    assert "/Accounts/AC123/Messages.json" in url
