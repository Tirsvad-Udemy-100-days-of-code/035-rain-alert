"""Composition root and command line of Rain Alert."""

import argparse
import logging
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, tzinfo
from pathlib import Path
from typing import TextIO

from rain_alert import constants
from rain_alert.application.errors import ForecastUnavailableError, NotificationError
from rain_alert.application.ports import ForecastSource, Notifier
from rain_alert.application.rain_alert import run_rain_alert
from rain_alert.infrastructure.http import Transport, UrllibTransport
from rain_alert.infrastructure.notifiers import (
    DryRunNotifier,
    twilio_notifier_from_settings,
)
from rain_alert.infrastructure.openweather_client import (
    OpenWeatherClient,
    OpenWeatherForecastClient,
)
from rain_alert.infrastructure.scheduler import DailyScheduler, load_zone
from rain_alert.infrastructure.settings import (
    Settings,
    SettingsError,
    load_environment,
    load_settings,
)

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """@brief Describe the command line.

    @return The parser.
    """
    parser = argparse.ArgumentParser(
        prog="rain_alert",
        description="Send a WhatsApp message when rain is expected in the next "
        "12 hours. Without options it runs every day at ALERT_TIME.",
    )
    parser.add_argument("--once", action="store_true", help="check now, once, and exit")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the message instead of sending it (needs no Twilio settings)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(constants.CONFIG_FILE_NAME),
        help="settings file read when present (default: %(default)s)",
    )
    return parser


def _make_source(settings: Settings, transport: Transport) -> ForecastSource:
    """@brief Choose the forecast source named by the settings.

    @param settings The settings of the run.
    @param transport Fetches URLs.
    @return The One Call 4.0 client or the 2.5 forecast client.
    """
    if settings.forecast_api == constants.FORECAST_API_FORECAST25:
        return OpenWeatherForecastClient(
            transport, settings.api_key, settings.latitude, settings.longitude
        )
    return OpenWeatherClient(
        transport, settings.api_key, settings.latitude, settings.longitude
    )


def _make_job(source: ForecastSource, notifier: Notifier) -> Callable[[], None]:
    """@brief Wire the forecast source and the notifier into one job.

    @param source Where the hourly forecast comes from.
    @param notifier How the owner is told.
    @return A function that runs the rain alert once and logs the outcome.
    """

    def job() -> None:
        logger.info(
            "Checking the forecast for the next %d hours", constants.FORECAST_HOURS
        )
        if run_rain_alert(source, notifier):
            logger.info("Rain is expected: the alert was delivered")
        else:
            logger.info("No rain is expected: nothing was sent")

    return job


def main(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    transport: Transport | None = None,
    stdout: TextIO | None = None,
    clock: Callable[[tzinfo], datetime] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    max_runs: int | None = None,
) -> int:
    """@brief Run the program.

    @param argv The command-line arguments, by default ``sys.argv[1:]``.
    @param environ The environment, by default ``os.environ``.
    @param transport Web access, by default urllib.
    @param stdout Where the dry run writes, by default ``sys.stdout``.
    @param clock Gives the current moment in a time zone, by default the system clock.
    @param sleep Waits the given number of seconds, by default ``time.sleep``.
    @param max_runs Stop the daily loop after this many runs (for tests).
    @return The exit code: 0 success, 1 the check or the alert failed, 2 a setting
        is missing or invalid.
    """
    logging.basicConfig(level=logging.INFO, format=constants.LOG_FORMAT)
    args = build_parser().parse_args(argv)
    web = transport or UrllibTransport()
    try:
        settings = load_settings(load_environment(environ, args.config))
        notifier: Notifier
        if args.dry_run:
            notifier = DryRunNotifier(stdout or sys.stdout)
        else:
            notifier = twilio_notifier_from_settings(settings, web)
        job = _make_job(_make_source(settings, web), notifier)
        if args.once:
            job()
            return constants.EXIT_OK
        zone = load_zone(settings.timezone)
        scheduler = DailyScheduler(
            _logged(job),
            settings.alert_time,
            zone,
            clock or (lambda tz: datetime.now(tz)),
            sleep,
        )
        scheduler.run_forever(max_runs)
        return constants.EXIT_OK
    except SettingsError as error:
        logger.error("%s", error)
        return constants.EXIT_BAD_SETTINGS
    except (ForecastUnavailableError, NotificationError) as error:
        logger.error("%s", error)
        return constants.EXIT_FAILED


def _logged(job: Callable[[], None]) -> Callable[[], None]:
    """@brief Keep the daily loop alive when one run fails.

    @param job The job to run.
    @return A job that logs a failed run and returns, so tomorrow's run still happens.
    """

    def guarded() -> None:
        try:
            job()
        except (ForecastUnavailableError, NotificationError) as error:
            logger.error("%s", error)

    return guarded
