"""Hourly forecast from the OpenWeather One Call 4.0 API."""

import json
import urllib.parse
from typing import Any

from rain_alert.application.errors import ForecastUnavailableError
from rain_alert.constants import FORECAST_UNITS, FORECAST_URL
from rain_alert.domain.hourly_forecast import HourlyForecast
from rain_alert.infrastructure.http import (
    HttpError,
    HttpGetter,
    HttpStatusError,
    explanation,
)


class OpenWeatherClient:
    """@brief A ForecastSource backed by the OpenWeather One Call 4.0 API."""

    def __init__(
        self, transport: HttpGetter, api_key: str, latitude: float, longitude: float
    ) -> None:
        """@brief Create the client.

        @param transport Fetches URLs.
        @param api_key The OpenWeather API key; never shown in an error.
        @param latitude Latitude of the location.
        @param longitude Longitude of the location.
        """
        self._transport: HttpGetter = transport
        self._api_key: str = api_key
        self._latitude: float = latitude
        self._longitude: float = longitude

    def weather_params(self) -> dict[str, str | float]:
        """@brief The query parameters of the request (the course's weather_params).

        @return Latitude, longitude, API key and units.
        """
        return {
            "lat": self._latitude,
            "lon": self._longitude,
            "appid": self._api_key,
            "units": FORECAST_UNITS,
        }

    def request_url(self) -> str:
        """@brief The full URL of the request.

        @return The endpoint with its query string; contains the API key.
        """
        return f"{FORECAST_URL}?{urllib.parse.urlencode(self.weather_params())}"

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        """@brief Get the forecast of the coming hours.

        @param hours How many hourly forecasts are wanted.
        @return At most the requested number of hourly forecasts, soonest first.
        @throws ForecastUnavailableError When the service fails or answers
            something unusable; the message never contains the API key.
        """
        try:
            raw = self._transport.get(self.request_url())
        except HttpStatusError as error:
            raise ForecastUnavailableError(
                f"OpenWeather answered {error}: {explanation(error.body)}"
            ) from error
        except HttpError as error:
            raise ForecastUnavailableError(
                "OpenWeather could not be reached."
            ) from error
        return _parse(raw, hours)


def _parse(raw: bytes, hours: int) -> list[HourlyForecast]:
    """@brief Turn an answer into hourly forecasts.

    @param raw The body of the answer.
    @param hours How many forecasts to keep.
    @return The first forecasts of the answer.
    @throws ForecastUnavailableError When the answer is not the expected JSON.
    """
    try:
        # json.loads returns Any; the try block validates every access.
        payload: Any = json.loads(raw)
        records = payload["data"] if "data" in payload else payload["hourly"]
        forecasts = [
            HourlyForecast(
                time=int(record["dt"]),
                condition_ids=tuple(int(item["id"]) for item in record["weather"]),
            )
            for record in records[:hours]
        ]
    except (ValueError, KeyError, TypeError) as error:
        raise ForecastUnavailableError(
            "OpenWeather answered something unexpected."
        ) from error
    if not forecasts:
        raise ForecastUnavailableError("OpenWeather gave no hourly forecast.")
    return forecasts
