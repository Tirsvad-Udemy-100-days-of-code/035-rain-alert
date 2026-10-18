# ☔ Rain Alert

A small program that checks the weather forecast every morning and sends you a WhatsApp message when it will rain in the next 12 hours; it is the Day 35 project of Udemy's "100 Days of Code: The Complete Python Pro Bootcamp", written for course participants and anyone browsing for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

Rain Alert asks OpenWeather for the forecast of one place (One Call 4.0 hourly, or the free 2.5 forecast, as you choose), looks at the next 12 hours, and decides that rain is expected when any weather condition id is below 700 (the rule of the course). If so, it sends one WhatsApp message with pywhatkit through WhatsApp Web on your own machine (or, with `NOTIFIER=twilio`, through the Twilio WhatsApp sandbox); otherwise it stays silent. It runs once a day at a time you choose (Windows Task Scheduler or its own daily loop, or a Docker container that uses Twilio), and all secrets stay in a git-ignored `config.env`.

![A dry run that expects rain][screenshot-rain]

The repository is laid out in layers under `src/rain_alert/`:

| Folder | What it holds |
| --- | --- |
| `domain/` | The hourly forecast and the `will_rain` rule (the course's loop over condition ids) |
| `application/` | The forecast and notifier ports and the rain-check use case |
| `infrastructure/` | Settings, web access, the OpenWeather clients, the pywhatkit, Twilio WhatsApp and dry-run notifiers and the daily scheduler (standard library only; pywhatkit is an optional extra) |
| `main.py` | The entry point that wires the layers together (`python -m rain_alert`) |
| `constants.py` | All constants (API URLs, 12 hours, the limit 700, setting names) |

Where the course script went:

| Course script | Rain Alert |
| --- | --- |
| `weather_params` (`lat`, `lon`, `appid`, `cnt`) | `weather_params` of the OpenWeather clients |
| `requests.get(...)` | `UrllibTransport` (standard library) |
| loop over `weather[0]["id"] < 700` | `will_rain` in `domain/rain.py` |
| `pywhatkit.sendwhatmsg(...)` | `PywhatkitNotifier` (the default; `sendwhatmsg_instantly`) |
| `client.messages.create(...)` of `twilio` | `TwilioWhatsAppNotifier` (optional; Twilio REST API with `urllib`) |
| a schedule on PythonAnywhere or GitHub Actions | Windows Task Scheduler, or `DailyScheduler` (also in the Docker container) |
| keys in `os.environ.get(...)` | `Settings` read from `config.env` and the environment |

There are no runtime dependencies. The wiki ([English][wiki], [Dansk][wiki-da], [Bahasa Melayu][wiki-ms]) explains the design in more detail.

Tests are in `tests/`, project documents in `docs/`. The code has Doxygen comments and a `Doxyfile`.

## 📋 Requirements

- Python 3.13 or later, with `venv` to create a local virtual environment.
- No third-party runtime dependencies. `pytest` (and optionally `ruff`, `mypy`) are installed only for development.
- For the alert: an OpenWeather API key, and a browser on your machine that is logged in to [WhatsApp Web](https://web.whatsapp.com/) (pywhatkit). Optional: [Docker Desktop](https://www.docker.com/products/docker-desktop/) with a Twilio account and its WhatsApp sandbox.
- Optional: [Doxygen](https://www.doxygen.nl/) to build the API documentation.

## 🛠️ Setup

Create and activate a local `.venv`, then upgrade pip and install the project with its development tools.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

To send with pywhatkit, install the optional extra (it brings pywhatkit and its browser automation):

```bash
python -m pip install -e ".[whatsapp]"
```

Then copy the settings file and fill in your own values. `config.env` is git-ignored and is never copied into an image.

```bash
cp config.env.example config.env
```

| Setting | Meaning |
| --- | --- |
| `OPENWEATHER_APIKEY` | Your OpenWeather API key (used for the free 2.5 forecast) |
| `OPENWEATHER4_APIKEY` | Key of your One Call 4.0 subscription (used when `FORECAST_API=onecall4`; falls back to the key above) |
| `FORECAST_API` | `onecall4` (One Call 4.0, needs the One Call by Call subscription; default) or `forecast25` (the free 2.5 forecast, one entry per three hours) |
| `LATITUDE`, `LONGITUDE` | The place to check (default 2.927761, 101.897999) |
| `PHONENUMBER` | Your WhatsApp number, international format |
| `NOTIFIER` | `pywhatkit` (default; WhatsApp Web on this machine) or `twilio` (the Twilio sandbox; used by the container) |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | From the Twilio console (only for `NOTIFIER=twilio`) |
| `TWILIO_WHATSAPP_FROM` | The sandbox number (default +14155238886) |
| `ALERT_TIME`, `TZ` | Local time of the daily check and its time zone (default 07:00, Asia/Kuala_Lumpur) |

## ▶️ Run

With the `.venv` active and `config.env` filled in, check the forecast once and print the message instead of sending it:

```bash
python -m rain_alert --once --dry-run
```

Send the WhatsApp message for real (pywhatkit opens WhatsApp Web in your default browser, which must be logged in, and presses send), or run the daily loop in the foreground:

```bash
python -m rain_alert --once
python -m rain_alert
```

The alert as it arrives in WhatsApp (everything except the message is blurred):

![The alert in WhatsApp][screenshot-whatsapp]

| Rain expected | No rain expected |
| --- | --- |
| ![Rain expected][screenshot-rain] | ![No rain expected][screenshot-dry] |

Exit codes: 0 success, 1 the forecast or the message failed, 2 a setting is missing or invalid (the message names the key, never its value). On Windows, install `tzdata` (part of the `dev` extra) so the time zone is found.

### Every morning on Windows

pywhatkit needs your logged-in browser, so schedule the one-off check with Windows Task Scheduler instead of a container. In PowerShell, from the repository folder (the task runs only while you are logged in, because it opens a browser):

```powershell
$python = (Resolve-Path .venv\Scripts\python.exe).Path
schtasks /Create /TN "Rain Alert" /SC DAILY /ST 07:00 /IT /TR "cmd /c cd /d $PWD && $python -m rain_alert --once"
schtasks /Run /TN "Rain Alert"
schtasks /Delete /TN "Rain Alert" /F
```

The three commands create the daily task at 07:00, run it once now, and remove it again.

### In a Docker container (with Twilio)

A container has no browser, so it cannot use pywhatkit: `compose.yaml` sets `NOTIFIER=twilio`. Docker Desktop builds the image and keeps the container running; it checks the forecast every day at `ALERT_TIME`. `config.env` is passed to the container at run time and is never copied into the image.

```bash
docker compose up -d --build
docker compose logs -f
docker compose run --rm rain-alert python -m rain_alert --once --dry-run
docker compose down
```

![The container on Docker Desktop][screenshot-docker]

### WhatsApp through Twilio (optional)

1. Open the Twilio Sandbox for WhatsApp in the Twilio console and join it from your phone (send the join code to the sandbox number).
2. Put the account SID, auth token and sandbox number in `config.env`, set `NOTIFIER=twilio`, and put your own number in `PHONENUMBER`.
3. The sandbox forgets your phone after 72 hours without a message; join again if the message does not arrive.

## 🧪 Tests

```bash
python -m pytest
```

The tests use fakes and need no network. To see coverage: `python -m pytest --cov=rain_alert`. To build the API documentation: `doxygen Doxyfile` (output in `doxygen/html`).

## 📄 License

GNU Affero General Public License v3, see [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [AGENTS.md][agents] | The rules AI agents follow in this repository |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Domain dictionary][DICT-001] | The PO terms and the IT terms |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Governance][GOV-001] | The review workflow, who decides and how disputes escalate |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[license]: ./LICENSE
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/issues
[screenshot-whatsapp]: ./docs/images/whatsapp-message.png
[screenshot-rain]: ./docs/images/dry-run-rain.png
[screenshot-dry]: ./docs/images/dry-run-no-rain.png
[screenshot-docker]: ./docs/images/docker-container.png
[wiki]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/wiki
[wiki-da]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/wiki/Home-da
[wiki-ms]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/wiki/Home-ms
[agents]: ./AGENTS.md
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[DICT-001]: ./docs/dictionary.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[GOV-001]: ./docs/sqa/governance.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
