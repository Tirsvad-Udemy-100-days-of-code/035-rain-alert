"""Tests of the dry-run notifier and the Twilio WhatsApp notifier."""

import importlib
import io
from collections.abc import Mapping
from datetime import time
from types import SimpleNamespace

import pytest

from rain_alert.application.errors import NotificationError
from rain_alert.infrastructure.http import HttpStatusError, NetworkError
from rain_alert.infrastructure.notifiers import (
    DryRunNotifier,
    PywhatkitNotifier,
    TwilioWhatsAppNotifier,
    pywhatkit_send,
    twilio_notifier_from_settings,
)
from rain_alert.infrastructure.settings import Settings, SettingsError

SID = "AC0123456789"
TOKEN = "auth-token-xyz"
SENDER = "+14155238886"
RECIPIENT = "+60123456789"


class FakePoster:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[tuple[str, Mapping[str, str], str, str]] = []

    def post_form(
        self, url: str, form: Mapping[str, str], user: str, password: str
    ) -> bytes:
        self.calls.append((url, form, user, password))
        if self.error is not None:
            raise self.error
        return b"{}"


def _notifier(poster: FakePoster) -> TwilioWhatsAppNotifier:
    return TwilioWhatsAppNotifier(poster, SID, TOKEN, SENDER, RECIPIENT)


def _settings(**changes: str | None) -> Settings:
    values: dict[str, object] = {
        "api_key": "k",
        "phone_number": RECIPIENT,
        "latitude": 2.9,
        "longitude": 101.9,
        "alert_time": time(7, 0),
        "timezone": "Asia/Kuala_Lumpur",
        "twilio_account_sid": SID,
        "twilio_auth_token": TOKEN,
        "twilio_whatsapp_from": SENDER,
    }
    values.update(changes)
    return Settings(**values)  # type: ignore[arg-type]


def test_dry_run_writes_the_message_and_sends_nothing() -> None:
    stream = io.StringIO()
    DryRunNotifier(stream).send("Take an umbrella")
    assert stream.getvalue() == "[dry run] would send: Take an umbrella\n"


def test_twilio_request_shape() -> None:
    poster = FakePoster()
    _notifier(poster).send("Take an umbrella")
    url, form, user, password = poster.calls[0]
    assert url == f"https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json"
    assert form == {
        "From": f"whatsapp:{SENDER}",
        "To": f"whatsapp:{RECIPIENT}",
        "Body": "Take an umbrella",
    }
    assert (user, password) == (SID, TOKEN)


def test_whatsapp_prefix_is_not_doubled() -> None:
    poster = FakePoster()
    TwilioWhatsAppNotifier(
        poster, SID, TOKEN, f"whatsapp:{SENDER}", f"whatsapp:{RECIPIENT}"
    ).send("x")
    assert poster.calls[0][1]["To"] == f"whatsapp:{RECIPIENT}"
    assert poster.calls[0][1]["From"] == f"whatsapp:{SENDER}"


def test_twilio_refusal_reports_twilios_message() -> None:
    error = HttpStatusError(400, '{"code": 63015, "message": "Join the sandbox first"}')
    with pytest.raises(NotificationError) as caught:
        _notifier(FakePoster(error)).send("x")
    assert "400" in str(caught.value)
    assert "Join the sandbox first" in str(caught.value)


def test_secrets_and_numbers_are_hidden_in_twilios_message() -> None:
    body = (
        '{"message": "The To number whatsapp:'
        + RECIPIENT
        + " and "
        + RECIPIENT
        + " from "
        + SENDER
        + " for "
        + SID
        + " with "
        + TOKEN
        + '"}'
    )
    with pytest.raises(NotificationError) as caught:
        _notifier(FakePoster(HttpStatusError(400, body))).send("x")
    for secret in (RECIPIENT, SENDER, SID, TOKEN):
        assert secret not in str(caught.value)
        assert secret not in repr(caught.value)


def test_unexplained_refusal_is_still_clear() -> None:
    with pytest.raises(NotificationError, match="500"):
        _notifier(FakePoster(HttpStatusError(500, "<html>"))).send("x")


def test_unreachable_twilio_is_a_notification_error() -> None:
    with pytest.raises(NotificationError, match="could not be reached"):
        _notifier(FakePoster(NetworkError("down"))).send("x")


def test_notifier_is_built_from_settings() -> None:
    poster = FakePoster()
    twilio_notifier_from_settings(_settings(), poster).send("x")
    assert poster.calls[0][1]["To"] == f"whatsapp:{RECIPIENT}"


def test_missing_twilio_settings_are_named() -> None:
    settings = _settings(twilio_account_sid=None, twilio_auth_token=None)
    with pytest.raises(SettingsError) as caught:
        twilio_notifier_from_settings(settings, FakePoster())
    assert "TWILIO_ACCOUNT_SID" in str(caught.value)
    assert "TWILIO_AUTH_TOKEN" in str(caught.value)
    assert "TWILIO_WHATSAPP_FROM" not in str(caught.value)


def test_refusal_with_json_but_no_message_is_still_clear() -> None:
    with pytest.raises(NotificationError, match="no explanation given"):
        _notifier(FakePoster(HttpStatusError(400, "[]"))).send("x")


class RecordingSender:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def __call__(self, phone_number: str, message: str) -> None:
        self.calls.append((phone_number, message))
        if self.error is not None:
            raise self.error


def test_pywhatkit_notifier_sends_once_to_the_number() -> None:
    sender = RecordingSender()
    PywhatkitNotifier(RECIPIENT, sender).send("Take an umbrella")
    assert sender.calls == [(RECIPIENT, "Take an umbrella")]


def test_pywhatkit_notifier_accepts_a_whatsapp_prefixed_number() -> None:
    sender = RecordingSender()
    PywhatkitNotifier(f"whatsapp:{RECIPIENT}", sender).send("x")
    assert sender.calls[0][0] == RECIPIENT


def test_number_without_country_code_is_refused_without_sending() -> None:
    sender = RecordingSender()
    with pytest.raises(NotificationError, match="PHONENUMBER") as caught:
        PywhatkitNotifier("0123456789", sender).send("x")
    assert sender.calls == []
    assert "0123456789" not in str(caught.value)


def test_failed_send_is_a_notification_error_without_the_number() -> None:
    sender = RecordingSender(RuntimeError("could not reach " + RECIPIENT))
    with pytest.raises(NotificationError) as caught:
        PywhatkitNotifier(RECIPIENT, sender).send("x")
    assert "RuntimeError" in str(caught.value)
    assert RECIPIENT not in str(caught.value)


def test_notification_error_of_the_sender_is_passed_on() -> None:
    sender = RecordingSender(NotificationError("not installed"))
    with pytest.raises(NotificationError, match="not installed"):
        PywhatkitNotifier(RECIPIENT, sender).send("x")


def test_missing_pywhatkit_package_is_explained(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def refuse(name: str) -> None:
        raise ImportError(name)

    monkeypatch.setattr(importlib, "import_module", refuse)
    with pytest.raises(NotificationError, match="whatsapp"):
        pywhatkit_send(RECIPIENT, "x")


def test_pywhatkit_is_called_with_the_waiting_times(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []
    fake = SimpleNamespace(sendwhatmsg_instantly=lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(importlib, "import_module", lambda name: fake)
    pywhatkit_send(RECIPIENT, "x")
    assert calls == [
        {
            "phone_no": RECIPIENT,
            "message": "x",
            "wait_time": 15,
            "tab_close": True,
            "close_time": 3,
        }
    ]
