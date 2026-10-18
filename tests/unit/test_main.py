"""Tests of the composition root with fake web access."""

import io
import json
import logging
from collections.abc import Mapping
from datetime import datetime, timedelta, tzinfo
from pathlib import Path

import pytest

from rain_alert.infrastructure.http import HttpStatusError, NetworkError
from rain_alert.main import main

API_KEY = "owm-key-0123456789"
PHONE = "+60123456789"
SID = "ACabcdef0123"
TOKEN = "twilio-token-xyz"
SECRETS = (API_KEY, PHONE, SID, TOKEN)

# Never read the real config.env of the developer in a test.
NO_CONFIG = ("--config", "no-such-config.env")

ENVIRON = {
    "OPENWEATHER_APIKEY": API_KEY,
    "PHONENUMBER": PHONE,
    "LATITUDE": "2.927761",
    "LONGITUDE": "101.897999",
    "TWILIO_ACCOUNT_SID": SID,
    "TWILIO_AUTH_TOKEN": TOKEN,
    "TWILIO_WHATSAPP_FROM": "+14155238886",
}


def _forecast(condition_id: int) -> bytes:
    records = [
        {"dt": 1 + hour, "weather": [{"id": condition_id}]} for hour in range(20)
    ]
    return json.dumps({"data": records}).encode()


class FakeTransport:
    """Answers GET with queued answers and records every request."""

    def __init__(self, *answers: bytes | Exception) -> None:
        self.answers = list(answers)
        self.gets: list[str] = []
        self.posts: list[Mapping[str, str]] = []

    def get(self, url: str) -> bytes:
        self.gets.append(url)
        answer = self.answers[0] if len(self.answers) == 1 else self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    def post_form(
        self, url: str, form: Mapping[str, str], user: str, password: str
    ) -> bytes:
        self.posts.append(form)
        return b"{}"


def _run(
    transport: FakeTransport,
    *argv: str,
    environ: Mapping[str, str] = ENVIRON,
) -> tuple[int, str]:
    stdout = io.StringIO()
    code = main(
        [*argv, *NO_CONFIG], environ=environ, transport=transport, stdout=stdout
    )
    return code, stdout.getvalue()


def test_dry_run_with_rain_prints_the_message_and_sends_nothing() -> None:
    transport = FakeTransport(_forecast(500))
    code, out = _run(transport, "--once", "--dry-run")
    assert code == 0
    assert "[dry run] would send: It's going to rain today." in out
    assert transport.posts == []


def test_dry_run_without_rain_prints_nothing() -> None:
    transport = FakeTransport(_forecast(800))
    code, out = _run(transport, "--once", "--dry-run")
    assert (code, out) == (0, "")
    assert transport.posts == []


def test_dry_run_needs_no_twilio_settings() -> None:
    environ = {k: v for k, v in ENVIRON.items() if not k.startswith("TWILIO")}
    code, _ = _run(
        FakeTransport(_forecast(500)), "--once", "--dry-run", environ=environ
    )
    assert code == 0


def test_one_whatsapp_message_is_posted_when_rain_is_expected() -> None:
    transport = FakeTransport(_forecast(500))
    code, _ = _run(transport, "--once")
    assert code == 0
    assert len(transport.posts) == 1
    assert transport.posts[0]["To"] == f"whatsapp:{PHONE}"


def test_no_message_is_posted_when_no_rain_is_expected() -> None:
    transport = FakeTransport(_forecast(800))
    assert _run(transport, "--once")[0] == 0
    assert transport.posts == []


def test_missing_setting_gives_exit_code_2(caplog: pytest.LogCaptureFixture) -> None:
    environ = {k: v for k, v in ENVIRON.items() if k != "OPENWEATHER_APIKEY"}
    transport = FakeTransport(_forecast(500))
    assert _run(transport, "--once", environ=environ)[0] == 2
    assert "OPENWEATHER_APIKEY" in caplog.text
    assert transport.gets == []


def test_missing_twilio_setting_gives_exit_code_2(
    caplog: pytest.LogCaptureFixture,
) -> None:
    environ = {k: v for k, v in ENVIRON.items() if k != "TWILIO_AUTH_TOKEN"}
    assert _run(FakeTransport(_forecast(500)), "--once", environ=environ)[0] == 2
    assert "TWILIO_AUTH_TOKEN" in caplog.text


def test_forecast_failure_gives_exit_code_1() -> None:
    transport = FakeTransport(HttpStatusError(401, '{"message": "Invalid API key"}'))
    code, _ = _run(transport, "--once")
    assert code == 1
    assert transport.posts == []


def test_logs_never_contain_a_secret_or_the_number(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG)
    _run(FakeTransport(_forecast(500)), "--once")
    _run(FakeTransport(HttpStatusError(401, "{}")), "--once")
    _run(FakeTransport(NetworkError("down")), "--once")
    assert "Checking the forecast" in caplog.text
    for secret in SECRETS:
        assert secret not in caplog.text


def test_settings_file_is_read_when_present(tmp_path: Path) -> None:
    config = tmp_path / "config.env"
    config.write_text(
        "\n".join(f"{key}={value}" for key, value in ENVIRON.items()), encoding="utf-8"
    )
    transport = FakeTransport(_forecast(500))
    code = main(
        ["--once", "--dry-run", "--config", str(config)],
        environ={},
        transport=transport,
        stdout=io.StringIO(),
    )
    assert code == 0
    assert len(transport.gets) == 1


class StepClock:
    """A clock that only moves when the scheduler sleeps."""

    def __init__(self) -> None:
        self.now = datetime(2026, 10, 18, 6, 59).astimezone()

    def __call__(self, zone: tzinfo) -> datetime:
        return self.now.astimezone(zone)

    def sleep(self, seconds: float) -> None:
        self.now += timedelta(seconds=seconds)


def test_daily_mode_checks_once_per_day_and_survives_a_failed_day(
    caplog: pytest.LogCaptureFixture,
) -> None:
    transport = FakeTransport(NetworkError("down"), _forecast(500))
    clock = StepClock()
    code = main(
        [*NO_CONFIG],
        environ=ENVIRON,
        transport=transport,
        clock=clock,
        sleep=clock.sleep,
        max_runs=2,
    )
    assert code == 0
    assert len(transport.gets) == 2
    assert len(transport.posts) == 1
    assert "could not be reached" in caplog.text


def test_unknown_time_zone_gives_exit_code_2() -> None:
    environ = ENVIRON | {"TZ": "Mars/Olympus"}
    assert (
        main([*NO_CONFIG], environ=environ, transport=FakeTransport(_forecast(500)))
        == 2
    )
