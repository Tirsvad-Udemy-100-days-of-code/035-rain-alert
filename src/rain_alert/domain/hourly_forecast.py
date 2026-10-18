"""The hourly forecast entity."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HourlyForecast:
    """@brief The expected weather of one hour.

    @param time Start of the hour as a Unix timestamp in seconds (UTC).
    @param condition_ids OpenWeather weather condition ids expected in that hour.
    """

    time: int
    condition_ids: tuple[int, ...]
