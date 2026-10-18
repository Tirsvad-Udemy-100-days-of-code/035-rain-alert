"""Notifiers: the dry-run notifier and the Twilio WhatsApp notifier."""

import importlib
from collections.abc import Callable
from typing import TextIO

from rain_alert import constants
from rain_alert.application.errors import NotificationError
from rain_alert.infrastructure.http import (
    FormPoster,
    HttpError,
    HttpStatusError,
    explanation,
)
from rain_alert.infrastructure.settings import Settings, SettingsError


class DryRunNotifier:
    """@brief A Notifier that writes the message to a stream and sends nothing."""

    def __init__(self, stream: TextIO) -> None:
        """@brief Create the notifier.

        @param stream Where the message is written, for example ``sys.stdout``.
        """
        self._stream: TextIO = stream

    def send(self, message: str) -> None:
        """@brief Write the message instead of sending it.

        @param message The text that would have been sent.
        """
        self._stream.write(f"[dry run] would send: {message}\n")


def pywhatkit_send(phone_number: str, message: str) -> None:
    """@brief Send a WhatsApp message with pywhatkit through WhatsApp Web.

    pywhatkit opens WhatsApp Web in the default browser of this machine, which
    must be logged in, and presses send. The package is the optional extra
    ``whatsapp`` and is imported only here.

    @param phone_number The recipient in international format, starting with ``+``.
    @param message The text to send.
    @throws NotificationError When pywhatkit is not installed.
    """
    try:
        pywhatkit = importlib.import_module("pywhatkit")
    except ImportError as error:
        raise NotificationError(
            "pywhatkit is not installed; run: python -m pip install -e .[whatsapp]"
        ) from error
    pywhatkit.sendwhatmsg_instantly(
        phone_no=phone_number,
        message=message,
        wait_time=constants.WHATSAPP_WEB_WAIT_SECONDS,
        tab_close=True,
        close_time=constants.WHATSAPP_WEB_CLOSE_SECONDS,
    )


class PywhatkitNotifier:
    """@brief A Notifier that sends a WhatsApp message through WhatsApp Web."""

    def __init__(
        self,
        phone_number: str,
        send: Callable[[str, str], None] = pywhatkit_send,
    ) -> None:
        """@brief Create the notifier.

        @param phone_number The recipient in international format, with ``+``.
        @param send Sends one message; by default pywhatkit.
        """
        self._phone_number: str = phone_number.strip().removeprefix(
            constants.WHATSAPP_PREFIX
        )
        self._send: Callable[[str, str], None] = send

    def send(self, message: str) -> None:
        """@brief Send one WhatsApp message.

        @param message The text to send.
        @throws NotificationError When the number has no country code, pywhatkit
            is missing or the send fails; the text never contains the number.
        """
        if not self._phone_number.startswith("+"):
            raise NotificationError(
                f"Setting {constants.ENV_PHONE_NUMBER} must start with + and the "
                "country code."
            )
        try:
            self._send(self._phone_number, message)
        except NotificationError:
            raise
        except Exception as error:  # third-party browser automation raises many types
            raise NotificationError(
                f"WhatsApp Web could not send the message ({type(error).__name__}); "
                "is the browser logged in to WhatsApp Web?"
            ) from error


class TwilioWhatsAppNotifier:
    """@brief A Notifier that sends a WhatsApp message through the Twilio sandbox."""

    def __init__(
        self,
        poster: FormPoster,
        account_sid: str,
        auth_token: str,
        sender: str,
        recipient: str,
    ) -> None:
        """@brief Create the notifier.

        @param poster Posts the form to the Twilio REST API.
        @param account_sid The Twilio account SID.
        @param auth_token The Twilio auth token (secret).
        @param sender The Twilio WhatsApp number, with or without ``whatsapp:``.
        @param recipient The owner's number, with or without ``whatsapp:``.
        """
        self._poster: FormPoster = poster
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token
        self._sender: str = _whatsapp(sender)
        self._recipient: str = _whatsapp(recipient)

    def form(self, message: str) -> dict[str, str]:
        """@brief The form fields of one message.

        @param message The text to send.
        @return The fields ``From``, ``To`` and ``Body``.
        """
        return {"From": self._sender, "To": self._recipient, "Body": message}

    def send(self, message: str) -> None:
        """@brief Send one WhatsApp message.

        @param message The text to send.
        @throws NotificationError When Twilio refuses the message or cannot be
            reached; the text never contains the token or the phone numbers.
        """
        url = constants.TWILIO_MESSAGES_URL.format(account_sid=self._account_sid)
        try:
            self._poster.post_form(
                url, self.form(message), self._account_sid, self._auth_token
            )
        except HttpStatusError as error:
            detail = self._redact(explanation(error.body))
            raise NotificationError(f"Twilio answered {error}: {detail}") from error
        except HttpError as error:
            raise NotificationError("Twilio could not be reached.") from error

    def _redact(self, text: str) -> str:
        """@brief Hide everything personal or secret in a text.

        @param text The text from the service.
        @return The text with the numbers, SID and token replaced by ``***``.
        """
        for secret in (
            self._sender,
            self._recipient,
            self._sender.removeprefix(constants.WHATSAPP_PREFIX),
            self._recipient.removeprefix(constants.WHATSAPP_PREFIX),
            self._account_sid,
            self._auth_token,
        ):
            text = text.replace(secret, "***")
        return text


def _whatsapp(number: str) -> str:
    """@brief Give a phone number the ``whatsapp:`` prefix once.

    @param number The number, with or without the prefix.
    @return The number with the prefix.
    """
    plain = number.strip().removeprefix(constants.WHATSAPP_PREFIX)
    return f"{constants.WHATSAPP_PREFIX}{plain}"


def twilio_notifier_from_settings(
    settings: Settings, poster: FormPoster
) -> TwilioWhatsAppNotifier:
    """@brief Build the Twilio notifier from the settings.

    @param settings The settings of the run.
    @param poster Posts the form to the Twilio REST API.
    @return The notifier.
    @throws SettingsError When a Twilio setting is missing; names the keys.
    """
    wanted = {
        constants.ENV_TWILIO_ACCOUNT_SID: settings.twilio_account_sid,
        constants.ENV_TWILIO_AUTH_TOKEN: settings.twilio_auth_token,
        constants.ENV_TWILIO_WHATSAPP_FROM: settings.twilio_whatsapp_from,
    }
    missing = [key for key, value in wanted.items() if not value]
    if missing:
        raise SettingsError("Setting " + ", ".join(missing) + " is missing.")
    return TwilioWhatsAppNotifier(
        poster,
        account_sid=str(settings.twilio_account_sid),
        auth_token=str(settings.twilio_auth_token),
        sender=str(settings.twilio_whatsapp_from),
        recipient=settings.phone_number,
    )
