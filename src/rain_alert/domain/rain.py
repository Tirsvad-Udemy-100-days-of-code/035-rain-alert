"""The rain rule of the course: a condition id below 700 means rain."""

from collections.abc import Iterable

from rain_alert.constants import RAIN_CONDITION_LIMIT
from rain_alert.domain.hourly_forecast import HourlyForecast


def will_rain(forecasts: Iterable[HourlyForecast]) -> bool:
    """@brief Tell whether rain is expected in any of the given hours.

    Condition ids below 700 are thunderstorm, drizzle, rain or snow; 700 and
    above are mist, clear sky and clouds. The course checks the first
    condition of each hour; every condition of the hour is checked here.

    @param forecasts The hourly forecasts to look at.
    @return True when at least one condition id is below the rain limit.
    """
    return any(
        condition_id < RAIN_CONDITION_LIMIT
        for forecast in forecasts
        for condition_id in forecast.condition_ids
    )
