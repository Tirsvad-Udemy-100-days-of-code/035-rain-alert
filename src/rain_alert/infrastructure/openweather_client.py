"""Forecasts from OpenWeather: One Call 4.0 (hourly) and the free 2.5 forecast."""

import json
import urllib.parse
from typing import Any

from rain_alert import constants
from rain_alert.application.errors import ForecastUnavailableError
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
            "units": constants.FORECAST_UNITS,
        }

    def request_url(self) -> str:
        """@brief The full URL of the request.

        @return The endpoint with its query string; contains the API key.
        """
        query = urllib.parse.urlencode(self.weather_params())
        return f"{constants.FORECAST_URL}?{query}"

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        """@brief Get the forecast of the coming hours.

        @param hours How many hourly forecasts are wanted.
        @return At most the requested number of hourly forecasts, soonest first.
        @throws ForecastUnavailableError When the service fails or answers
            something unusable; the message never contains the API key.
        """
        raw = _fetch(self._transport, self.request_url())
        return _parse(raw, hours, ("data", "hourly"))


class OpenWeatherForecastClient:
    """@brief A ForecastSource backed by the free OpenWeather 2.5 forecast.

    The 2.5 forecast has one entry per three hours, so each HourlyForecast it
    returns covers a period of three hours.
    """

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

    def weather_params(self, periods: int) -> dict[str, str | float | int]:
        """@brief The query parameters of the request (the course's weather_params).

        @param periods How many three-hour periods are wanted (the course's ``cnt``).
        @return Latitude, longitude, API key, units and the number of periods.
        """
        return {
            "lat": self._latitude,
            "lon": self._longitude,
            "appid": self._api_key,
            "units": constants.FORECAST_UNITS,
            "cnt": periods,
        }

    def request_url(self, periods: int) -> str:
        """@brief The full URL of the request.

        @param periods How many three-hour periods are wanted.
        @return The endpoint with its query string; contains the API key.
        """
        query = urllib.parse.urlencode(self.weather_params(periods))
        return f"{constants.FORECAST_25_URL}?{query}"

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        """@brief Get the forecast periods that cover the coming hours.

        @param hours How many hours are to be covered; rounded up to whole periods.
        @return The forecast periods, soonest first.
        @throws ForecastUnavailableError When the service fails or answers
            something unusable; the message never contains the API key.
        """
        periods = -(-hours // constants.FORECAST_25_PERIOD_HOURS)
        raw = _fetch(self._transport, self.request_url(periods))
        return _parse(raw, periods, ("list",))


def _fetch(transport: HttpGetter, url: str) -> bytes:
    """@brief Fetch a URL and turn a failure into a forecast error.

    @param transport Fetches URLs.
    @param url The full URL; it contains the API key and is never shown.
    @return The body of the answer.
    @throws ForecastUnavailableError When the request fails.
    """
    try:
        return transport.get(url)
    except HttpStatusError as error:
        raise ForecastUnavailableError(
            f"OpenWeather answered {error}: {explanation(error.body)}"
        ) from error
    except HttpError as error:
        raise ForecastUnavailableError("OpenWeather could not be reached.") from error


def _parse(raw: bytes, count: int, keys: tuple[str, ...]) -> list[HourlyForecast]:
    """@brief Turn an answer into forecast periods.

    @param raw The body of the answer.
    @param count How many periods to keep.
    @param keys The names under which the answer may keep its records.
    @return The first periods of the answer.
    @throws ForecastUnavailableError When the answer is not the expected JSON.
    """
    try:
        # json.loads returns Any; the try block validates every access.
        payload: Any = json.loads(raw)
        key = next(name for name in keys if name in payload)
        forecasts = [
            HourlyForecast(
                time=int(record["dt"]),
                condition_ids=tuple(int(item["id"]) for item in record["weather"]),
            )
            for record in payload[key][:count]
        ]
    except (ValueError, KeyError, TypeError, StopIteration) as error:
        raise ForecastUnavailableError(
            "OpenWeather answered something unexpected."
        ) from error
    if not forecasts:
        raise ForecastUnavailableError("OpenWeather gave no forecast.")
    return forecasts
