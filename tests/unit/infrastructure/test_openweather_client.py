"""Tests of the OpenWeather client with a fake transport."""

import json
import urllib.parse

import pytest

from rain_alert.application.errors import ForecastUnavailableError
from rain_alert.infrastructure.http import HttpStatusError, NetworkError
from rain_alert.infrastructure.openweather_client import OpenWeatherClient

API_KEY = "secret-api-key-123"


class FakeTransport:
    """Answers GET requests with a fixed body or raises a fixed error."""

    def __init__(self, body: bytes = b"", error: Exception | None = None) -> None:
        self._body = body
        self._error = error
        self.urls: list[str] = []

    def get(self, url: str) -> bytes:
        self.urls.append(url)
        if self._error is not None:
            raise self._error
        return self._body


def _answer(count: int, key: str = "data", condition_id: int = 800) -> bytes:
    records = [
        {"dt": 1_700_000_000 + 3600 * index, "weather": [{"id": condition_id}]}
        for index in range(count)
    ]
    return json.dumps({"lat": 2.9, "lon": 101.9, key: records}).encode()


def _client(transport: FakeTransport) -> OpenWeatherClient:
    return OpenWeatherClient(transport, API_KEY, 2.927761, 101.897999)


def test_request_carries_location_key_and_units() -> None:
    transport = FakeTransport(_answer(20))
    _client(transport).next_hours(12)
    url = urllib.parse.urlparse(transport.urls[0])
    query = urllib.parse.parse_qs(url.query)
    assert url.netloc == "api.openweathermap.org"
    assert url.path == "/data/4.0/onecall/timeline/1h"
    assert query == {
        "lat": ["2.927761"],
        "lon": ["101.897999"],
        "appid": [API_KEY],
        "units": ["metric"],
    }


def test_weather_params_are_the_course_names() -> None:
    params = _client(FakeTransport()).weather_params()
    assert set(params) == {"lat", "lon", "appid", "units"}


def test_first_twelve_hours_are_kept() -> None:
    forecasts = _client(FakeTransport(_answer(20))).next_hours(12)
    assert len(forecasts) == 12
    assert forecasts[0].time == 1_700_000_000
    assert forecasts[0].condition_ids == (800,)


def test_fewer_records_than_asked_are_returned_as_they_are() -> None:
    assert len(_client(FakeTransport(_answer(5))).next_hours(12)) == 5


def test_hourly_key_is_accepted_too() -> None:
    forecasts = _client(FakeTransport(_answer(3, key="hourly"))).next_hours(12)
    assert len(forecasts) == 3


def test_several_conditions_of_an_hour_are_kept() -> None:
    body = json.dumps(
        {"data": [{"dt": 1, "weather": [{"id": 500}, {"id": 211}]}]}
    ).encode()
    assert _client(FakeTransport(body)).next_hours(12)[0].condition_ids == (500, 211)


@pytest.mark.parametrize(
    "body", [b"not json", b"{}", b'{"data": [{"dt": 1}]}', b'{"data": []}', b"[]"]
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


def test_error_without_json_body_is_still_clear() -> None:
    with pytest.raises(ForecastUnavailableError, match="429"):
        _client(FakeTransport(error=HttpStatusError(429, "<html>"))).next_hours(12)


def test_network_failure_is_an_error() -> None:
    with pytest.raises(ForecastUnavailableError, match="could not be reached"):
        _client(FakeTransport(error=NetworkError("down"))).next_hours(12)


@pytest.mark.parametrize(
    "error",
    [
        HttpStatusError(401, "{}"),
        NetworkError("down"),
    ],
)
def test_api_key_never_appears_in_an_error(error: Exception) -> None:
    with pytest.raises(ForecastUnavailableError) as caught:
        _client(FakeTransport(error=error)).next_hours(12)
    assert API_KEY not in str(caught.value)
    assert API_KEY not in repr(caught.value)


def test_api_key_never_appears_when_the_answer_is_unusable() -> None:
    with pytest.raises(ForecastUnavailableError) as caught:
        _client(FakeTransport(b"nonsense")).next_hours(12)
    assert API_KEY not in str(caught.value)


def test_long_service_message_is_shortened_but_still_read() -> None:
    body = json.dumps({"cod": 401, "message": "Subscription needed. " + "x" * 900})
    with pytest.raises(ForecastUnavailableError) as caught:
        _client(FakeTransport(error=HttpStatusError(401, body))).next_hours(12)
    assert "Subscription needed." in str(caught.value)
    assert len(str(caught.value)) < 400
