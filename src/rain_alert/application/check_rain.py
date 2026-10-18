"""The rain check: is rain expected in the coming hours?"""

from rain_alert.application.ports import ForecastSource
from rain_alert.constants import FORECAST_HOURS
from rain_alert.domain.rain import will_rain


def check_rain(source: ForecastSource, hours: int = FORECAST_HOURS) -> bool:
    """@brief Ask the forecast source and apply the rain rule.

    @param source Where the hourly forecast comes from.
    @param hours How many coming hours to look at.
    @return True when rain is expected in any of those hours.
    @throws ForecastUnavailableError When the source cannot give a forecast.
    """
    return will_rain(source.next_hours(hours))
