🌐 [English](Install) · **Dansk** · [Bahasa Melayu](Install-ms)

# Installation

## Krav

- Python 3.13 eller nyere med `venv`.
- Ingen eksterne afhængigheder ved kørsel. `pytest`, `ruff`, `mypy` (og `tzdata` på Windows) er kun udviklingsværktøjer.
- Til beskeden: en OpenWeather API-nøgle og en browser på din computer, der er logget ind på WhatsApp Web (pywhatkit).
- Valgfrit: Docker Desktop med en Twilio-konto og dens WhatsApp-sandbox.

## Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Linux og macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

`python -m pip install --upgrade pip` opgraderer pip i `.venv`. Mappen `.venv` ignoreres af git.

For at sende med pywhatkit installeres det valgfrie tillæg:

```bash
python -m pip install -e ".[whatsapp]"
```

## Indstillinger

Kopiér eksemplet og udfyld dine egne værdier. `config.env` ignoreres af git og kopieres aldrig ind i Docker-imaget.

```bash
cp config.env.example config.env
```

| Indstilling | Betydning |
| --- | --- |
| `OPENWEATHER_APIKEY` | OpenWeather API-nøgle (bruges til den gratis 2.5-udsigt) |
| `OPENWEATHER4_APIKEY` | Nøgle til One Call 4.0-abonnementet (falder tilbage til nøglen ovenfor) |
| `FORECAST_API` | `onecall4` (standard) eller `forecast25` |
| `LATITUDE`, `LONGITUDE` | Stedet, der tjekkes |
| `PHONENUMBER` | Dit WhatsApp-nummer i international form |
| `NOTIFIER` | `pywhatkit` (standard) eller `twilio` (bruges af containeren) |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | Fra Twilio-konsollen (kun for `NOTIFIER=twilio`) |
| `TWILIO_WHATSAPP_FROM` | Twilios sandbox-nummer |
| `ALERT_TIME`, `TZ` | Lokal tid for det daglige tjek og dens tidszone |
