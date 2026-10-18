"""Tests of the urllib transport against a local web server (no internet)."""

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from rain_alert.infrastructure.http import (
    HttpStatusError,
    NetworkError,
    UrllibTransport,
)

RECEIVED: dict[str, str] = {}


class Handler(BaseHTTPRequestHandler):
    """Answers /ok, /post and everything else with 401."""

    def do_GET(self) -> None:
        if self.path == "/ok":
            self._answer(200, b'{"fine": true}')
        else:
            self._answer(401, b'{"message": "no"}')

    def do_POST(self) -> None:
        length = int(self.headers["Content-Length"])
        RECEIVED["body"] = self.rfile.read(length).decode()
        RECEIVED["auth"] = self.headers["Authorization"] or ""
        self._answer(201, b'{"sid": "SM1"}')

    def _answer(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def base_url() -> Iterator[str]:
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.server_close()


def test_get_returns_the_body(base_url: str) -> None:
    assert UrllibTransport().get(base_url + "/ok") == b'{"fine": true}'


def test_error_status_is_raised_with_the_start_of_the_answer(base_url: str) -> None:
    with pytest.raises(HttpStatusError) as caught:
        UrllibTransport().get(base_url + "/denied")
    assert caught.value.status == 401
    assert "no" in caught.value.body


def test_post_sends_form_and_basic_authentication(base_url: str) -> None:
    body = UrllibTransport().post_form(
        base_url + "/post", {"To": "whatsapp:+1", "Body": "a b"}, "user", "pass"
    )
    assert body == b'{"sid": "SM1"}'
    assert RECEIVED["body"] == "To=whatsapp%3A%2B1&Body=a+b"
    assert RECEIVED["auth"] == "Basic dXNlcjpwYXNz"


def test_unreachable_service_is_a_network_error() -> None:
    with pytest.raises(NetworkError):
        UrllibTransport(timeout_seconds=1).get("http://127.0.0.1:9/")
