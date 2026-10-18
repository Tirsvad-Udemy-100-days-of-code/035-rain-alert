# ADR-0001: Architecture, dependencies and delivery

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [MIL-005] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [728ff3e] |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Amendment: the forecast endpoint is selectable (free 2.5 forecast as fallback), reason: HTTP 401 on One Call 4.0 | [5da8060] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The course solution is one `main.py` that calls the OpenWeather forecast with `requests`, loops over the weather condition ids and sends a message. S01's earlier version used `pywhatkit`, which drives WhatsApp Web in a desktop browser. The Business Case ([BC-001]) asks for readable code that keeps the assignment's logic (S02), no runtime dependencies (S03, SC8), tests that need no network (SC5), secrets in `config.env` (O4) and a daily run in a Docker container on Docker Desktop (O5).

Options for the layout:

1. Keep one flat `main.py`, as in the course. Simple, but not testable without the network and it fails the layering criterion of the Python checklist.
2. Layers under `src/rain_alert/` with the assignment's names and logic kept inside them.

Options for the WhatsApp delivery:

1. `pywhatkit`. Needs a browser and a logged-in WhatsApp Web, so it cannot run in a container; it is also a heavy runtime dependency.
2. The Twilio WhatsApp sandbox, as the course's WhatsApp note describes, through Twilio's REST API.

Options for the HTTP client (OpenWeather and Twilio):

1. `requests` and the `twilio` package. Convenient, but runtime dependencies.
2. `urllib.request` and `json` from the standard library. A few more lines, no dependency.

Options for the forecast endpoint:

1. The 2.5 five-day, three-hour forecast with `cnt=4` as in the course.
2. The One Call 4.0 hourly timeline named by S01, with the next 12 hourly records.

Amendment of 2026-10-18 (forecast endpoint): the first live run answered HTTP 401 on One Call 4.0 because the API key has no One Call by Call subscription, while the free 2.5 forecast answered. A third option was evaluated:

3. Both endpoints behind the `ForecastSource` port, chosen by the setting `FORECAST_API`.

Options for the daily schedule:

1. Cron or Task Scheduler on the host. Outside the container and the repository.
2. A small scheduler loop inside the container, with `restart: unless-stopped`.

## Decision

We use layers: `domain` holds `HourlyForecast` and `will_rain`; `application` holds the `ForecastSource` and `Notifier` ports and the `check_rain` use case; `infrastructure` holds the settings loader, the One Call 4.0 client, the Twilio WhatsApp notifier, the dry-run notifier and the scheduler; `main.py` is the composition root. The program is a command-line entry point, so there is no presentation layer. We send WhatsApp through the Twilio sandbox, call both APIs with the standard library `urllib.request`, so the runtime `dependencies` list stays empty, and use the One Call 4.0 hourly timeline with `units=metric` and the first 12 records. The forecast endpoint is chosen by the optional setting `FORECAST_API`: `onecall4` (the default, option 2) or `forecast25` (the free 2.5 forecast with `cnt` three-hour periods, as in the course; option 3 of the amendment). The rain rule stays the assignment's: any condition id below 700. The scheduler runs inside the container, with the time `ALERT_TIME` (default 07:00) in the zone `TZ` (default `Asia/Kuala_Lumpur`). All constants live in `src/rain_alert/constants.py`.

Secrets and the location come from environment variables. Compose passes `config.env` with `env_file`; the image never contains it, `.gitignore` and `.dockerignore` exclude it, and `config.env.example` documents the keys. A small file reader in the settings loader lets a local run use the same file without overriding variables already set. The tokens in `.env` are for S01's repository administration only and are not read by the program.

## Consequences

**Positive:**

- The domain and application layers are tested without the network, Twilio or Docker, using fakes.
- No third-party runtime dependency to install or trust; the image is small.
- The container is self-contained: one `docker compose up -d` gives a daily alert.
- The assignment's logic remains recognisable to S02.

**Negative:**

- More files than the course has; the README maps the course script to the layers.
- Hand-written HTTP error handling instead of the `requests` and `twilio` conveniences.
- One Call 4.0 is a separate OpenWeather subscription; the second source (`FORECAST_API=forecast25`) covers a key without it, at the cost of a second client and a coarser three-hour period.
- The Twilio sandbox requires S01's phone to join it and expires after inactivity.
- A container that must stay running uses a little memory all day, and a restart of Docker Desktop at the alert time can miss one alert.

Quality-attribute impacts: portability improves (standard library only, container), security improves (secrets outside code and image), maintainability improves (inward dependencies), performance is unaffected for one request a day.

## Affected Artifacts

- [BC-001] — objectives O1 to O7 and success criteria SC4, SC5, SC6 and SC8 are met by this design.
- [MIL-005] — delivers the amendment.

---

[BC-001]: ../business-case.md
[MIL-005]: ../milestones/mil-005-forecast-api-fallback.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
[5da8060]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/5da8060e2000533a95fed0b380e9ba2aa8b25be2
