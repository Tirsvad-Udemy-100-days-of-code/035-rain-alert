"""Tests of the rain rule."""

import pytest

from rain_alert.domain.hourly_forecast import HourlyForecast
from rain_alert.domain.rain import will_rain


def _hour(*condition_ids: int) -> HourlyForecast:
    return HourlyForecast(time=0, condition_ids=condition_ids)


def test_no_forecast_means_no_rain() -> None:
    assert will_rain([]) is False


@pytest.mark.parametrize("condition_id", [200, 300, 500, 600, 699])
def test_condition_below_700_means_rain(condition_id: int) -> None:
    assert will_rain([_hour(800), _hour(condition_id)]) is True


@pytest.mark.parametrize("condition_id", [700, 741, 800, 804])
def test_condition_from_700_means_no_rain(condition_id: int) -> None:
    assert will_rain([_hour(condition_id), _hour(800)]) is False


def test_any_condition_of_an_hour_counts() -> None:
    assert will_rain([_hour(804, 500)]) is True


def test_forecast_is_immutable() -> None:
    hour = _hour(800)
    with pytest.raises(AttributeError):
        hour.time = 5  # type: ignore[misc]
