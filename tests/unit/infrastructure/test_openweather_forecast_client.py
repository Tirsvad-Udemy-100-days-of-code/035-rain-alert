"""Tests of the free 2.5 forecast client with a fake transport."""

import json
import urllib.parse

import pytest

from rain_alert.application.errors import ForecastUnavailableError
from rain_alert.infrastructure.http import HttpStatusError, NetworkError
from rain_alert.infrastructure.openweather_client import OpenWeatherForecastClient

API_KEY = "secret-api-key-123"


class FakeTransport:
    def __init__(self, body: bytes = b"", error: Exception | None = None) -> None:
        self._body = body
        self._error = error
        self.urls: list[str] = []

    def get(self, url: str) -> bytes:
        self.urls.append(url)
        if self._error is not None:
            raise self._error
        return self._body


def _answer(count: int, condition_id: int = 800) -> bytes:
    records = [
        {
            "dt": 1_700_000_000 + 10_800 * index,
            "weather": [{"id": condition_id, "main": "Clear"}],
        }
        for index in range(count)
    ]
    return json.dumps({"cod": "200", "cnt": count, "list": records}).encode()


def _client(transport: FakeTransport) -> OpenWeatherForecastClient:
    return OpenWeatherForecastClient(transport, API_KEY, 2.927761, 101.897999)


def test_twelve_hours_are_four_periods_in_the_request() -> None:
    transport = FakeTransport(_answer(4))
    _client(transport).next_hours(12)
    url = urllib.parse.urlparse(transport.urls[0])
    assert url.netloc == "api.openweathermap.org"
    assert url.path == "/data/2.5/forecast"
    assert urllib.parse.parse_qs(url.query) == {
        "lat": ["2.927761"],
        "lon": ["101.897999"],
        "appid": [API_KEY],
        "units": ["metric"],
        "cnt": ["4"],
    }


@pytest.mark.parametrize(("hours", "periods"), [(1, 1), (3, 1), (4, 2), (12, 4)])
def test_hours_are_rounded_up_to_whole_periods(hours: int, periods: int) -> None:
    transport = FakeTransport(_answer(8))
    forecasts = _client(transport).next_hours(hours)
    assert f"cnt={periods}" in transport.urls[0]
    assert len(forecasts) == periods


def test_periods_are_read_from_the_list() -> None:
    forecasts = _client(FakeTransport(_answer(4, condition_id=501))).next_hours(12)
    assert forecasts[0].time == 1_700_000_000
    assert forecasts[0].condition_ids == (501,)


@pytest.mark.parametrize(
    "body", [b"not json", b"{}", b'{"list": [{"dt": 1}]}', b'{"list": []}']
)
def test_unusable_answer_is_an_error(body: bytes) -> None:
    with pytest.raises(ForecastUnavailableError):
        _client(FakeTransport(body)).next_hours(12)


def test_unauthorised_answer_names_status_and_service_message() -> None:
    error = HttpStatusError(401, '{"cod": 401, "message": "Invalid API key"}')
    with pytest.raises(ForecastUnavailableError) as caught:
        _client(FakeTransport(error=error)).next_hours(12)
    assert "401" in str(caught.value)
    assert "Invalid API key" in str(caught.value)


@pytest.mark.parametrize(
    "error", [HttpStatusError(401, "{}"), NetworkError("down"), ValueError("x")]
)
def test_api_key_never_appears_in_an_error(error: Exception) -> None:
    transport = FakeTransport(error=error)
    if isinstance(error, ValueError):
        transport = FakeTransport(b"nonsense")
    with pytest.raises(ForecastUnavailableError) as caught:
        _client(transport).next_hours(12)
    assert API_KEY not in str(caught.value)
    assert API_KEY not in repr(caught.value)
