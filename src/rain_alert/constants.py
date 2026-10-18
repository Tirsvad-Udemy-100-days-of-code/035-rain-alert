"""Constants of the Rain Alert application.

Documentation style: Doxygen ``##`` comment blocks with ``@brief`` placed
directly above each constant, and ``@name`` groups.
"""

from typing import Final

## @name OpenWeather One Call 4.0
## @{

## @brief Endpoint of the hourly timeline of the One Call 4.0 API.
FORECAST_URL: Final[str] = "https://api.openweathermap.org/data/4.0/onecall/timeline/1h"

## @brief Endpoint of the free 2.5 forecast (one entry per three hours).
FORECAST_25_URL: Final[str] = "https://api.openweathermap.org/data/2.5/forecast"

## @brief Hours covered by one entry of the 2.5 forecast.
FORECAST_25_PERIOD_HOURS: Final[int] = 3

## @brief Number of hourly forecasts checked (the next 12 hours).
FORECAST_HOURS: Final[int] = 12

## @brief Units requested from the API.
FORECAST_UNITS: Final[str] = "metric"

## @brief Seconds to wait for a web service before giving up.
REQUEST_TIMEOUT_SECONDS: Final[int] = 10

## @}

## @name Rain rule
## @{

## @brief Weather condition ids below this number mean rain or worse (course rule).
RAIN_CONDITION_LIMIT: Final[int] = 700

## @brief Text of the alert.
UMBRELLA_MESSAGE: Final[str] = (
    "It's going to rain today. Remember to bring an umbrella."
)

## @}

## @name Twilio WhatsApp
## @{

## @brief Messages endpoint of a Twilio account; fill in the account SID.
TWILIO_MESSAGES_URL: Final[str] = (
    "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
)

## @brief Prefix that makes a Twilio number a WhatsApp number.
WHATSAPP_PREFIX: Final[str] = "whatsapp:"

## @}

## @name Settings
## @{

## @brief Name of the file with the secrets and settings (git-ignored).
CONFIG_FILE_NAME: Final[str] = "config.env"

## @brief Environment variable: OpenWeather API key.
ENV_API_KEY: Final[str] = "OPENWEATHER_APIKEY"

## @brief Environment variable: recipient phone number.
ENV_PHONE_NUMBER: Final[str] = "PHONENUMBER"

## @brief Environment variable: latitude of the location.
ENV_LATITUDE: Final[str] = "LATITUDE"

## @brief Environment variable: longitude of the location.
ENV_LONGITUDE: Final[str] = "LONGITUDE"

## @brief Environment variable: Twilio account SID.
ENV_TWILIO_ACCOUNT_SID: Final[str] = "TWILIO_ACCOUNT_SID"

## @brief Environment variable: Twilio auth token.
ENV_TWILIO_AUTH_TOKEN: Final[str] = "TWILIO_AUTH_TOKEN"

## @brief Environment variable: Twilio WhatsApp sender number.
ENV_TWILIO_WHATSAPP_FROM: Final[str] = "TWILIO_WHATSAPP_FROM"

## @brief Environment variable: which OpenWeather forecast to use.
ENV_FORECAST_API: Final[str] = "FORECAST_API"

## @brief Value of FORECAST_API for the One Call 4.0 hourly forecast.
FORECAST_API_ONECALL4: Final[str] = "onecall4"

## @brief Value of FORECAST_API for the free 2.5 forecast.
FORECAST_API_FORECAST25: Final[str] = "forecast25"

## @brief Forecast used when none is configured.
DEFAULT_FORECAST_API: Final[str] = FORECAST_API_ONECALL4

## @brief Environment variable: local time of the daily check, HH:MM.
ENV_ALERT_TIME: Final[str] = "ALERT_TIME"

## @brief Environment variable: IANA time zone of the alert time.
ENV_TIMEZONE: Final[str] = "TZ"

## @brief Alert time used when none is configured.
DEFAULT_ALERT_TIME: Final[str] = "07:00"

## @brief Time zone used when none is configured.
DEFAULT_TIMEZONE: Final[str] = "Asia/Kuala_Lumpur"

## @}

## @name Web requests
## @{

## @brief Longest part of a service's error answer that is read.
MAX_ERROR_BODY_CHARS: Final[int] = 4000

## @brief Longest explanation of a service shown in an error message.
MAX_ERROR_MESSAGE_CHARS: Final[int] = 300

## @}

## @name Program
## @{

## @brief Longest sleep in one step, so a paused machine catches up on a long wait.
SLEEP_STEP_SECONDS: Final[int] = 60

## @brief Exit code: the run succeeded.
EXIT_OK: Final[int] = 0

## @brief Exit code: the forecast or the alert failed.
EXIT_FAILED: Final[int] = 1

## @brief Exit code: a setting is missing or invalid.
EXIT_BAD_SETTINGS: Final[int] = 2

## @brief Format of the log lines.
LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s %(message)s"

## @}
