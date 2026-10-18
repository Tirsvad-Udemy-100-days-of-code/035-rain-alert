"""Tests of the rain-check use case."""

import pytest

from rain_alert.application.check_rain import check_rain
from rain_alert.application.errors import ForecastUnavailableError
from rain_alert.constants import FORECAST_HOURS
from rain_alert.domain.hourly_forecast import HourlyForecast


class FakeSource:
    """A forecast source that answers from a list and remembers the request."""

    def __init__(self, condition_ids: list[int]) -> None:
        self._forecasts = [
            HourlyForecast(time=index, condition_ids=(condition_id,))
            for index, condition_id in enumerate(condition_ids)
        ]
        self.requested_hours: int | None = None

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        self.requested_hours = hours
        return self._forecasts[:hours]


class BrokenSource:
    """A forecast source that always fails."""

    def next_hours(self, hours: int) -> list[HourlyForecast]:
        raise ForecastUnavailableError("down")


def test_rain_is_reported_when_expected() -> None:
    assert check_rain(FakeSource([800, 801, 500])) is True


def test_no_rain_is_reported_when_clear() -> None:
    assert check_rain(FakeSource([800, 801, 802])) is False


def test_next_twelve_hours_are_asked_for_by_default() -> None:
    source = FakeSource([800])
    check_rain(source)
    assert source.requested_hours == FORECAST_HOURS == 12


def test_only_the_requested_hours_count() -> None:
    assert check_rain(FakeSource([800, 800, 500]), hours=2) is False


def test_source_failure_is_not_hidden() -> None:
    with pytest.raises(ForecastUnavailableError):
        check_rain(BrokenSource())
