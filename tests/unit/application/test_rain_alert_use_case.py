"""Tests of the rain-alert use case: one message when rain, none otherwise."""

import pytest

from rain_alert.application.errors import ForecastUnavailableError, NotificationError
from rain_alert.application.rain_alert import run_rain_alert
from rain_alert.constants import UMBRELLA_MESSAGE
from rain_alert.domain.hourly_forecast import HourlyForecast


class FakeSource:
    def __init__(self, condition_id: int) -> None:
        self._condition_id = condition_id

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        return [HourlyForecast(time=0, condition_ids=(self._condition_id,))] * hours


class RecordingNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


class FailingNotifier:
    def send(self, message: str) -> None:
        raise NotificationError("refused")


class BrokenSource:
    def next_hours(self, hours: int) -> list[HourlyForecast]:
        raise ForecastUnavailableError("down")


def test_exactly_one_message_is_sent_when_rain_is_expected() -> None:
    notifier = RecordingNotifier()
    assert run_rain_alert(FakeSource(500), notifier) is True
    assert notifier.messages == [UMBRELLA_MESSAGE]


def test_nothing_is_sent_when_no_rain_is_expected() -> None:
    notifier = RecordingNotifier()
    assert run_rain_alert(FakeSource(800), notifier) is False
    assert notifier.messages == []


def test_delivery_failure_is_not_hidden() -> None:
    with pytest.raises(NotificationError):
        run_rain_alert(FakeSource(500), FailingNotifier())


def test_forecast_failure_sends_nothing() -> None:
    notifier = RecordingNotifier()
    with pytest.raises(ForecastUnavailableError):
        run_rain_alert(BrokenSource(), notifier)
    assert notifier.messages == []
