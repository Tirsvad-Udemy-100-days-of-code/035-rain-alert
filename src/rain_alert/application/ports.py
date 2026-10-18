"""Ports: what the use cases need from the outside world."""

from typing import Protocol

from rain_alert.domain.hourly_forecast import HourlyForecast


class ForecastSource(Protocol):
    """@brief A service that supplies the hourly forecast of one location."""

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        """@brief Get the forecast of the coming hours.

        @param hours How many hourly forecasts are wanted.
        @return At most the requested number of hourly forecasts, soonest first.
        @throws ForecastUnavailableError When no usable forecast can be given.
        """
        ...


class Notifier(Protocol):
    """@brief A channel that tells the owner something."""

    def send(self, message: str) -> None:
        """@brief Deliver one message.

        @param message The text to deliver.
        @throws NotificationError When the message could not be delivered.
        """
        ...
