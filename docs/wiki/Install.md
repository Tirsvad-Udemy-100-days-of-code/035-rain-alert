🌐 **English** · [Dansk](Install-da) · [Bahasa Melayu](Install-ms)

# Install

## Requirements

- Python 3.13 or later with `venv`.
- No third-party runtime dependencies. `pytest`, `ruff`, `mypy` (and `tzdata` on Windows) are development tools only.
- For the alert: an OpenWeather API key and a browser on your machine that is logged in to WhatsApp Web (pywhatkit).
- Optional: Docker Desktop with a Twilio account and its WhatsApp sandbox.

## Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Linux and macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

`python -m pip install --upgrade pip` upgrades pip inside the `.venv`. The `.venv` folder is ignored by git.

To send with pywhatkit, install the optional extra:

```bash
python -m pip install -e ".[whatsapp]"
```

## Settings

Copy the example and fill in your own values. `config.env` is ignored by git and never copied into the Docker image.

```bash
cp config.env.example config.env
```

| Setting | Meaning |
| --- | --- |
| `OPENWEATHER_APIKEY` | OpenWeather API key (used for the free 2.5 forecast) |
| `OPENWEATHER4_APIKEY` | Key of the One Call 4.0 subscription (falls back to the key above) |
| `FORECAST_API` | `onecall4` (default) or `forecast25` |
| `LATITUDE`, `LONGITUDE` | The place to check |
| `PHONENUMBER` | Your WhatsApp number, international format |
| `NOTIFIER` | `pywhatkit` (default) or `twilio` (used by the container) |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | From the Twilio console (only for `NOTIFIER=twilio`) |
| `TWILIO_WHATSAPP_FROM` | The Twilio sandbox number |
| `ALERT_TIME`, `TZ` | Local time of the daily check and its time zone |
