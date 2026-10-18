"""The daily scheduler: run a job once a day at a local time."""

import logging
from collections.abc import Callable
from datetime import datetime, time, timedelta, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rain_alert.constants import SLEEP_STEP_SECONDS
from rain_alert.infrastructure.settings import SettingsError

logger = logging.getLogger(__name__)


def load_zone(name: str) -> ZoneInfo:
    """@brief Find a time zone by its IANA name.

    @param name The name, for example ``Asia/Kuala_Lumpur``.
    @return The time zone.
    @throws SettingsError When the name is unknown or the system has no zone data.
    """
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise SettingsError(
            "Setting TZ is not a known time zone (on Windows: install tzdata)."
        ) from error


def next_run(now: datetime, alert_time: time, zone: tzinfo) -> datetime:
    """@brief Find the next moment the job is due.

    @param now The current moment, with a time zone.
    @param alert_time The local time of day of the job.
    @param zone The time zone of the alert time.
    @return The first moment after ``now`` at which the local time is the alert time.
    """
    local_now = now.astimezone(zone)
    candidate = datetime.combine(local_now.date(), alert_time, tzinfo=zone)
    if candidate <= local_now:
        candidate = datetime.combine(
            local_now.date() + timedelta(days=1), alert_time, tzinfo=zone
        )
    return candidate


class DailyScheduler:
    """@brief Runs a job every day at the alert time."""

    def __init__(
        self,
        job: Callable[[], None],
        alert_time: time,
        zone: tzinfo,
        clock: Callable[[tzinfo], datetime],
        sleep: Callable[[float], None],
    ) -> None:
        """@brief Create the scheduler.

        @param job What to run each day.
        @param alert_time The local time of day of the job.
        @param zone The time zone of the alert time.
        @param clock Gives the current moment in a time zone.
        @param sleep Waits the given number of seconds.
        """
        self._job: Callable[[], None] = job
        self._alert_time: time = alert_time
        self._zone: tzinfo = zone
        self._clock: Callable[[tzinfo], datetime] = clock
        self._sleep: Callable[[float], None] = sleep

    def run_next(self) -> datetime:
        """@brief Wait for the next due moment and run the job once.

        The wait is split into short steps, so a machine that was paused catches up.

        @return The moment the job was due.
        """
        due = next_run(self._clock(self._zone), self._alert_time, self._zone)
        logger.info("Next check at %s", due.isoformat(timespec="minutes"))
        while True:
            remaining = (due - self._clock(self._zone)).total_seconds()
            if remaining <= 0:
                break
            self._sleep(min(remaining, SLEEP_STEP_SECONDS))
        self._job()
        return due

    def run_forever(self, max_runs: int | None = None) -> None:
        """@brief Run the job every day.

        @param max_runs Stop after this many runs; None means never stop.
        """
        runs = 0
        while max_runs is None or runs < max_runs:
            self.run_next()
            runs += 1
