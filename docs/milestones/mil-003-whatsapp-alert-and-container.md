# WhatsApp alert and container

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [728ff3e] |

---

## Purpose

Decides whether the program sends the WhatsApp alert through Twilio when rain is expected, runs daily by itself, and runs in a Docker container on Docker Desktop with its secrets supplied at run time.

## Deliverable

A pull request with the `Notifier` port, the Twilio WhatsApp notifier, the dry-run notifier, the daily scheduler, the entry point (`python -m rain_alert`, options `--once` and `--dry-run`), the `Dockerfile` and `compose.yaml`, and their tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The Twilio notifier posts to the Messages endpoint of the account with HTTP Basic authentication, `From=whatsapp:<TWILIO_WHATSAPP_FROM>`, `To=whatsapp:<PHONENUMBER>` and the umbrella text, and reports Twilio's error text on failure | Request-shape test passes | Test fails |
| 2 | A run sends exactly one message when rain is expected and none when not; `--dry-run` prints the message and sends nothing | Tests pass | Test fails |
| 3 | The scheduler computes the next run at `ALERT_TIME` in zone `TZ` (default 07:00, `Asia/Kuala_Lumpur`), including across midnight, with an injectable clock and sleep | Tests pass | Test fails |
| 4 | No log line, error text or exception contains the API key, the auth token or the phone number | Test with a captured log passes | A value appears |
| 5 | `docker compose config` is valid, the image runs as a non-root user, `config.env` is passed with `env_file` and is not copied into the image, and `.dockerignore` excludes it | All hold, or Docker is unavailable here and the files pass a read-through recorded in the review | Any fails |
| 6 | `python -m pytest` passes without network access or Docker, and one dry run against the live API either shows the decision or reports the failure (for example a 401) to S01 | Both hold | Tests fail |
| 7 | Python code has a `Go` review record against `QC-PY-001` | `Go` | Anything else |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-002 | Needs the settings, the forecast source and the rain decision |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O3, O4, O5, O6 | [BC-001] |
| SC3, SC4, SC6 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-23 — within the Business Case window of 2026-10-18 to 2026-10-25.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add Notifier port and dry-run notifier | Define the `Notifier` protocol in the application layer and the dry-run notifier in the infrastructure layer that prints the message; the use case sends at most one message per run. | No | ADR-0001 |
| 2 | Implement Twilio WhatsApp notifier | Post the form-encoded message to the Twilio Messages REST endpoint with `urllib.request` and Basic authentication, using `whatsapp:`-prefixed numbers, and raise a specific error carrying Twilio's message on failure. | No | ADR-0001 |
| 3 | Implement daily scheduler | Add the scheduler that sleeps until the next `ALERT_TIME` in the configured zone and runs the check once a day, with an injectable clock; `--once` skips the wait. | No | ADR-0001 |
| 4 | Add entry point (main.py) | Add `main.py` as the composition root and `__main__.py`: it reads the settings, wires the client and the notifier, handles `--once` and `--dry-run`, and logs without secrets. | No | ADR-0001 |
| 5 | Add Dockerfile and compose.yaml | Build a slim Python 3.13 image with a non-root user and zone data; the Compose file uses `env_file: config.env`, `restart: unless-stopped` and `TZ`. Document `docker compose up -d` for Docker Desktop. | No | ADR-0001 |
| 6 | Add tests for notification, scheduling and secrets | Write pytest tests for the Twilio request shape, the one-message rule, the scheduler arithmetic and the absence of secrets in logs and errors, with fakes only. | No | ADR-0001 |

---

[BC-001]: ../business-case.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
