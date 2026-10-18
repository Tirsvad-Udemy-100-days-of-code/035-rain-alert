"""Web requests with the standard library, and the errors they can raise."""

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from typing import Protocol

from rain_alert.constants import (
    MAX_ERROR_BODY_CHARS,
    MAX_ERROR_MESSAGE_CHARS,
    REQUEST_TIMEOUT_SECONDS,
)


class HttpError(Exception):
    """@brief Base class of the errors of a web request."""


class NetworkError(HttpError):
    """@brief Raised when the service cannot be reached."""


class HttpStatusError(HttpError):
    """@brief Raised when the service answers with an error status."""

    def __init__(self, status: int, body: str) -> None:
        """@brief Create the error.

        @param status The HTTP status code.
        @param body The start of the answer, which may explain the error.
        """
        super().__init__(f"HTTP status {status}")
        self.status: int = status
        self.body: str = body


def explanation(body: str) -> str:
    """@brief Pick the explanation out of a service's error answer.

    @param body The start of the answer.
    @return The ``message`` field when the answer is JSON (shortened), otherwise
        a hint.
    """
    try:
        payload = json.loads(body)
    except ValueError:
        return "no explanation given"
    if isinstance(payload, dict) and isinstance(payload.get("message"), str):
        return str(payload["message"])[:MAX_ERROR_MESSAGE_CHARS]
    return "no explanation given"


class HttpGetter(Protocol):
    """@brief Something that can fetch a URL."""

    def get(self, url: str) -> bytes:
        """@brief Fetch a URL with GET.

        @param url The full URL, query string included.
        @return The body of the answer.
        @throws HttpError When the request fails.
        """
        ...


class FormPoster(Protocol):
    """@brief Something that can post a form with a user name and password."""

    def post_form(
        self, url: str, form: Mapping[str, str], user: str, password: str
    ) -> bytes:
        """@brief Post a form with HTTP Basic authentication.

        @param url The full URL.
        @param form The form fields.
        @param user The user name.
        @param password The password.
        @return The body of the answer.
        @throws HttpError When the request fails.
        """
        ...


class UrllibTransport:
    """@brief Web requests with urllib; implements HttpGetter and FormPoster."""

    def __init__(self, timeout_seconds: float = REQUEST_TIMEOUT_SECONDS) -> None:
        """@brief Create the transport.

        @param timeout_seconds Seconds to wait for an answer.
        """
        self._timeout: float = timeout_seconds

    def get(self, url: str) -> bytes:
        """@brief Fetch a URL with GET.

        @param url The full URL, query string included.
        @return The body of the answer.
        @throws HttpError When the request fails.
        """
        return self._send(urllib.request.Request(url))

    def post_form(
        self, url: str, form: Mapping[str, str], user: str, password: str
    ) -> bytes:
        """@brief Post a form with HTTP Basic authentication.

        @param url The full URL.
        @param form The form fields.
        @param user The user name.
        @param password The password.
        @return The body of the answer.
        @throws HttpError When the request fails.
        """
        token = base64.b64encode(f"{user}:{password}".encode()).decode("ascii")
        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(form).encode("utf-8"),
            headers={"Authorization": f"Basic {token}"},
            method="POST",
        )
        return self._send(request)

    def _send(self, request: urllib.request.Request) -> bytes:
        """@brief Send a prepared request and map failures to our errors.

        @param request The request to send.
        @return The body of the answer.
        @throws HttpError When the request fails.
        """
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                body: bytes = response.read()
                return body
        except urllib.error.HTTPError as error:
            text = error.read().decode("utf-8", errors="replace")
            raise HttpStatusError(error.code, text[:MAX_ERROR_BODY_CHARS]) from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise NetworkError("The service could not be reached.") from error


class Transport(HttpGetter, FormPoster, Protocol):
    """@brief Something that can both fetch a URL and post a form."""
