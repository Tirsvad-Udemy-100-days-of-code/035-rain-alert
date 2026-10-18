"""Tests of the daily scheduler arithmetic with a fake clock."""

from datetime import UTC, datetime, time, timedelta, timezone, tzinfo

import pytest

from rain_alert.infrastructure.scheduler import DailyScheduler, load_zone, next_run
from rain_alert.infrastructure.settings import SettingsError

KL = timezone(timedelta(hours=8))
SEVEN = time(7, 0)


def test_run_is_today_when_the_time_has_not_come() -> None:
    now = datetime(2026, 10, 18, 6, 30, tzinfo=KL)
    assert next_run(now, SEVEN, KL) == datetime(2026, 10, 18, 7, 0, tzinfo=KL)


def test_run_is_tomorrow_when_the_time_has_passed() -> None:
    now = datetime(2026, 10, 18, 7, 1, tzinfo=KL)
    assert next_run(now, SEVEN, KL) == datetime(2026, 10, 19, 7, 0, tzinfo=KL)


def test_run_is_tomorrow_at_exactly_the_alert_time() -> None:
    now = datetime(2026, 10, 18, 7, 0, tzinfo=KL)
    assert next_run(now, SEVEN, KL) == datetime(2026, 10, 19, 7, 0, tzinfo=KL)


def test_run_crosses_midnight_and_month_end() -> None:
    now = datetime(2026, 10, 31, 23, 59, tzinfo=KL)
    assert next_run(now, SEVEN, KL) == datetime(2026, 11, 1, 7, 0, tzinfo=KL)


def test_a_moment_in_another_zone_is_converted() -> None:
    now = datetime(2026, 10, 17, 23, 30, tzinfo=UTC)  # 07:30 in Kuala Lumpur
    assert next_run(now, SEVEN, KL) == datetime(2026, 10, 19, 7, 0, tzinfo=KL)


class FakeTime:
    """A clock that only moves when the scheduler sleeps."""

    def __init__(self, start: datetime) -> None:
        self.now = start
        self.sleeps: list[float] = []

    def clock(self, zone: tzinfo) -> datetime:
        return self.now.astimezone(zone)

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += timedelta(seconds=seconds)


def test_job_runs_at_the_due_moment_after_short_sleeps() -> None:
    fake = FakeTime(datetime(2026, 10, 18, 6, 0, tzinfo=KL))
    runs: list[datetime] = []
    scheduler = DailyScheduler(
        lambda: runs.append(fake.now), SEVEN, KL, fake.clock, fake.sleep
    )
    due = scheduler.run_next()
    assert due == datetime(2026, 10, 18, 7, 0, tzinfo=KL)
    assert runs == [due]
    assert max(fake.sleeps) <= 60
    assert sum(fake.sleeps) == 3600


def test_job_runs_once_a_day() -> None:
    fake = FakeTime(datetime(2026, 10, 18, 6, 0, tzinfo=KL))
    runs: list[datetime] = []
    scheduler = DailyScheduler(
        lambda: runs.append(fake.now), SEVEN, KL, fake.clock, fake.sleep
    )
    scheduler.run_forever(max_runs=3)
    assert [run.day for run in runs] == [18, 19, 20]


def test_known_zone_is_found() -> None:
    assert str(load_zone("Asia/Kuala_Lumpur")) == "Asia/Kuala_Lumpur"


@pytest.mark.parametrize("name", ["Mars/Olympus", "", "../etc/passwd"])
def test_unknown_zone_is_a_settings_error(name: str) -> None:
    with pytest.raises(SettingsError, match="TZ"):
        load_zone(name)
