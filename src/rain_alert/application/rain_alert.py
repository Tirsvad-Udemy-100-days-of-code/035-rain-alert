"""The rain alert: check the forecast and tell the owner when rain is expected."""

from rain_alert.application.check_rain import check_rain
from rain_alert.application.ports import ForecastSource, Notifier
from rain_alert.constants import FORECAST_HOURS, UMBRELLA_MESSAGE


def run_rain_alert(
    source: ForecastSource, notifier: Notifier, hours: int = FORECAST_HOURS
) -> bool:
    """@brief Check for rain and send one message when it is expected.

    @param source Where the hourly forecast comes from.
    @param notifier How the owner is told.
    @param hours How many coming hours to look at.
    @return True when rain was expected and the message was sent.
    @throws ForecastUnavailableError When the source cannot give a forecast.
    @throws NotificationError When the message could not be delivered.
    """
    if not check_rain(source, hours):
        return False
    notifier.send(UMBRELLA_MESSAGE)
    return True
