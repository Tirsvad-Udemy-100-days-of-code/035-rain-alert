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

Rain Alert asks the OpenWeather One Call 4.0 API for the hourly forecast of one place, looks at the next 12 hours, and decides that rain is expected when any weather condition id is below 700 (the rule of the course). If so, it sends one WhatsApp message through the Twilio WhatsApp sandbox; otherwise it stays silent. It runs once a day at a time you choose, in a Docker container on Docker Desktop, and all secrets stay in a git-ignored `config.env`.

The repository is laid out in layers under `src/rain_alert/`:

| Folder | What it holds |
| --- | --- |
| `domain/` | The hourly forecast and the `will_rain` rule (the course's loop over condition ids) |
| `application/` | The forecast and notifier ports and the rain-check use case |
| `infrastructure/` | Settings, the OpenWeather client, the Twilio WhatsApp notifier and the scheduler (standard library only) |
| `constants.py` | All constants (API URLs, 12 hours, the limit 700, setting names) |

The course's `weather_params` (`lat`, `lon`, `appid`, `cnt`) become the request of the OpenWeather client, and its `requests` and `twilio` calls are replaced by the standard library, so there are no runtime dependencies.

Tests are in `tests/`, project documents in `docs/`. The code has Doxygen comments and a `Doxyfile`.

## 📋 Requirements

- Python 3.13 or later, with `venv` to create a local virtual environment.
- No third-party runtime dependencies. `pytest` (and optionally `ruff`, `mypy`) are installed only for development.
- For the daily alert: [Docker Desktop](https://www.docker.com/products/docker-desktop/), an OpenWeather API key with the One Call subscription, and a Twilio account with the WhatsApp sandbox joined from your phone.
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

Then copy the settings file and fill in your own values. `config.env` is git-ignored and is never copied into an image.

```bash
cp config.env.example config.env
```

| Setting | Meaning |
| --- | --- |
| `OPENWEATHER_APIKEY` | Your OpenWeather API key |
| `LATITUDE`, `LONGITUDE` | The place to check (default 2.927761, 101.897999) |
| `PHONENUMBER` | Your WhatsApp number, international format |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | From the Twilio console |
| `TWILIO_WHATSAPP_FROM` | The sandbox number (default +14155238886) |
| `ALERT_TIME`, `TZ` | Local time of the daily check and its time zone (default 07:00, Asia/Kuala_Lumpur) |

## ▶️ Run

The program itself arrives in a later gateway of the plan (see the milestones in the appendix); this section is completed there with the commands to run it once, as a dry run, and in a Docker container.

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
