🌐 **English** · [Dansk](Usage-da) · [Bahasa Melayu](Usage-ms)

# Usage

With the `.venv` active and `config.env` filled in:

```bash
python -m rain_alert --once --dry-run
python -m rain_alert --once
python -m rain_alert
```

- `--once --dry-run` checks now and prints the message instead of sending it. It needs no Twilio settings.
- `--once` checks now and sends the WhatsApp message when rain is expected. With pywhatkit it opens WhatsApp Web in your default browser, which must be logged in.
- Without options the program runs every day at `ALERT_TIME`.

![A dry run that expects rain](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-rain.png)

![A dry run that expects no rain](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-no-rain.png)

The program sends one message when any weather condition id of the next 12 hours is below 700 (thunderstorm, drizzle, rain, snow), and nothing otherwise.

![The alert as it arrives in WhatsApp (everything except the message is blurred)](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/whatsapp-message.png)

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | The forecast or the message failed |
| 2 | A setting is missing or invalid (the message names the key, never its value) |

## Which forecast

`FORECAST_API=onecall4` uses the One Call 4.0 hourly forecast, which needs the separate One Call by Call subscription. `FORECAST_API=forecast25` uses the free 2.5 forecast with one entry per three hours, as the course does.

## If the message is typed but not sent

pywhatkit opens `web.whatsapp.com/send?phone=...&text=...`, clicks the centre of the **primary** screen, waits, and presses Enter.

- Keep the browser window on the primary monitor while it runs; on a second monitor the click lands elsewhere and the text stays in the message box.
- Close other WhatsApp Web tabs first, so the message is not typed into the chat that tab has open.
- Do not touch the keyboard or mouse during the wait (about 20 seconds).

## Every morning on Windows

pywhatkit needs your logged-in browser, so schedule `--once` with Windows Task Scheduler (the task runs while you are logged in). The commands create the daily task at 07:00, run it once now, and remove it:

```powershell
$python = (Resolve-Path .venv\Scripts\python.exe).Path
schtasks /Create /TN "Rain Alert" /SC DAILY /ST 07:00 /IT /TR "cmd /c cd /d $PWD && $python -m rain_alert --once"
schtasks /Run /TN "Rain Alert"
schtasks /Delete /TN "Rain Alert" /F
```

## Docker Desktop (with Twilio)

A container has no browser, so `compose.yaml` sets `NOTIFIER=twilio`.

```bash
docker compose up -d --build
docker compose logs -f
docker compose run --rm rain-alert python -m rain_alert --once --dry-run
docker compose down
```

![The container on Docker Desktop](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/docker-container.png)

The container reads `config.env` at start and checks the forecast every day at `ALERT_TIME`. It restarts with Docker Desktop.

## WhatsApp through Twilio (optional)

1. Open the Twilio Sandbox for WhatsApp in the Twilio console and join it from your phone.
2. Put the account SID, auth token and sandbox number in `config.env`, set `NOTIFIER=twilio`, and put your own number in `PHONENUMBER`.
3. The sandbox forgets your phone after 72 hours without a message; join again if nothing arrives.
