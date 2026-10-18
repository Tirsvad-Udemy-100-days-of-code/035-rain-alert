"""Settings read from environment variables and from the config.env file."""

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import time
from pathlib import Path

from rain_alert import constants


class SettingsError(Exception):
    """@brief Raised when a setting is missing or invalid; names the key only."""


@dataclass(frozen=True, slots=True)
class Settings:
    """@brief The values of one run.

    @param api_key OpenWeather API key (secret) for the chosen forecast.
    @param phone_number Recipient number in international format (personal).
    @param latitude Latitude of the location, -90 to 90.
    @param longitude Longitude of the location, -180 to 180.
    @param alert_time Local time of the daily check.
    @param timezone IANA time zone name of the alert time.
    @param forecast_api OpenWeather forecast to use: ``onecall4`` or ``forecast25``.
    @param notifier How the alert is sent: ``pywhatkit`` or ``twilio``.
    @param twilio_account_sid Twilio account SID, when configured.
    @param twilio_auth_token Twilio auth token (secret), when configured.
    @param twilio_whatsapp_from Twilio WhatsApp sender number, when configured.
    """

    api_key: str
    phone_number: str
    latitude: float
    longitude: float
    alert_time: time
    timezone: str
    forecast_api: str = constants.DEFAULT_FORECAST_API
    notifier: str = constants.DEFAULT_NOTIFIER
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_whatsapp_from: str | None = None

    def __repr__(self) -> str:
        """@brief Describe the settings without any secret or personal value.

        @return A short text that is safe to log.
        """
        return f"Settings(latitude={self.latitude}, longitude={self.longitude})"


_QUOTES = ("'", '"')


def parse_env_file(text: str) -> dict[str, str]:
    """@brief Read the lines KEY=VALUE of a config.env file.

    Blank lines and lines starting with ``#`` are skipped; a value may be
    wrapped in single or double quotes.

    @param text The content of the file.
    @return The keys and their values.
    """
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in _QUOTES:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_environment(
    environ: Mapping[str, str] | None = None, config_file: Path | None = None
) -> dict[str, str]:
    """@brief Combine the environment with an optional config.env file.

    A variable that is already set always wins over the file.

    @param environ The environment, by default ``os.environ``.
    @param config_file The file to read, by default none.
    @return The merged variables.
    """
    merged: dict[str, str] = {}
    if config_file is not None and config_file.is_file():
        merged.update(parse_env_file(config_file.read_text(encoding="utf-8")))
    merged.update(os.environ if environ is None else environ)
    return merged


def _required(variables: Mapping[str, str], key: str) -> str:
    """@brief Get a mandatory, non-empty value.

    @param variables The variables to read from.
    @param key The name of the variable.
    @return The value.
    @throws SettingsError When the variable is missing or empty.
    """
    value = variables.get(key, "").strip()
    if not value:
        raise SettingsError(f"Setting {key} is missing.")
    return value


def _number(variables: Mapping[str, str], key: str, low: float, high: float) -> float:
    """@brief Get a mandatory number inside a range.

    @param variables The variables to read from.
    @param key The name of the variable.
    @param low Smallest allowed value.
    @param high Largest allowed value.
    @return The number.
    @throws SettingsError When the variable is missing, not a number or out of range.
    """
    raw = _required(variables, key)
    try:
        number = float(raw)
    except ValueError as error:
        raise SettingsError(f"Setting {key} must be a number.") from error
    if not low <= number <= high:
        raise SettingsError(f"Setting {key} must be between {low} and {high}.")
    return number


def _alert_time(raw: str) -> time:
    """@brief Read a time of day written HH:MM.

    @param raw The text.
    @return The time of day.
    @throws SettingsError When the text is not a valid time of day.
    """
    match = re.fullmatch(r"(\d{1,2}):(\d{2})", raw.strip())
    if match is None or int(match.group(1)) > 23 or int(match.group(2)) > 59:
        raise SettingsError(f"Setting {constants.ENV_ALERT_TIME} must be HH:MM.")
    return time(int(match.group(1)), int(match.group(2)))


def _optional(variables: Mapping[str, str], key: str) -> str | None:
    """@brief Get a value that may be absent.

    @param variables The variables to read from.
    @param key The name of the variable.
    @return The value, or None when it is missing or empty.
    """
    return variables.get(key, "").strip() or None


def _forecast_api(raw: str) -> str:
    """@brief Read the name of the forecast to use.

    @param raw The text, possibly empty.
    @return The name, by default ``onecall4``.
    @throws SettingsError When the name is unknown.
    """
    name = raw.strip().lower() or constants.DEFAULT_FORECAST_API
    if name not in (constants.FORECAST_API_ONECALL4, constants.FORECAST_API_FORECAST25):
        raise SettingsError(
            f"Setting {constants.ENV_FORECAST_API} must be "
            f"{constants.FORECAST_API_ONECALL4} or {constants.FORECAST_API_FORECAST25}."
        )
    return name


def _notifier(raw: str) -> str:
    """@brief Read the name of the notifier to use.

    @param raw The text, possibly empty.
    @return The name, by default ``pywhatkit``.
    @throws SettingsError When the name is unknown.
    """
    name = raw.strip().lower() or constants.DEFAULT_NOTIFIER
    if name not in (constants.NOTIFIER_PYWHATKIT, constants.NOTIFIER_TWILIO):
        raise SettingsError(
            f"Setting {constants.ENV_NOTIFIER} must be "
            f"{constants.NOTIFIER_PYWHATKIT} or {constants.NOTIFIER_TWILIO}."
        )
    return name


def _api_key(variables: Mapping[str, str], forecast_api: str) -> str:
    """@brief Get the API key for the chosen forecast.

    One Call 4.0 uses ``OPENWEATHER4_APIKEY`` when it is set and otherwise the
    general ``OPENWEATHER_APIKEY``; the 2.5 forecast uses the general key.

    @param variables The variables to read from.
    @param forecast_api The chosen forecast.
    @return The API key.
    @throws SettingsError When the key is missing; names the key.
    """
    if forecast_api == constants.FORECAST_API_ONECALL4:
        specific = _optional(variables, constants.ENV_API_KEY_ONECALL4)
        if specific is not None:
            return specific
    return _required(variables, constants.ENV_API_KEY)


def load_settings(variables: Mapping[str, str]) -> Settings:
    """@brief Build the settings of a run from variables.

    @param variables The variables, for example from ``load_environment``.
    @return The settings.
    @throws SettingsError When a mandatory setting is missing or invalid; the
        message names the key and never shows a value.
    """
    alert_time = variables.get(constants.ENV_ALERT_TIME, "").strip()
    forecast_api = _forecast_api(variables.get(constants.ENV_FORECAST_API, ""))
    return Settings(
        api_key=_api_key(variables, forecast_api),
        phone_number=_required(variables, constants.ENV_PHONE_NUMBER),
        latitude=_number(variables, constants.ENV_LATITUDE, -90.0, 90.0),
        longitude=_number(variables, constants.ENV_LONGITUDE, -180.0, 180.0),
        alert_time=_alert_time(alert_time or constants.DEFAULT_ALERT_TIME),
        timezone=_optional(variables, constants.ENV_TIMEZONE)
        or constants.DEFAULT_TIMEZONE,
        forecast_api=forecast_api,
        notifier=_notifier(variables.get(constants.ENV_NOTIFIER, "")),
        twilio_account_sid=_optional(variables, constants.ENV_TWILIO_ACCOUNT_SID),
        twilio_auth_token=_optional(variables, constants.ENV_TWILIO_AUTH_TOKEN),
        twilio_whatsapp_from=_optional(variables, constants.ENV_TWILIO_WHATSAPP_FROM),
    )
