# pywhatkit notifier

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decides whether the alert can be sent as S01 wants: with pywhatkit through WhatsApp Web on S01's own machine, not through Twilio. S01 chose this after the first release, and chose to run the program on the host instead of in the container, because pywhatkit needs a desktop browser that is logged in to WhatsApp Web.

## Deliverable

A pull request with the pywhatkit notifier, the setting `NOTIFIER`, the optional extra `whatsapp`, the Compose file set to Twilio, the README and the three-language wiki for the host run and its schedule, the amended Business Case, ADR-0001, dictionary and plan with their reviews, and the tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `PywhatkitNotifier` calls `sendwhatmsg_instantly` once per message with the phone number of `PHONENUMBER` and the umbrella text, and a missing package or a failed send raises `NotificationError` without the phone number | Tests pass | Test fails or number leaks |
| 2 | `NOTIFIER` defaults to `pywhatkit`, accepts `twilio`, and rejects any other value with an error that names the key and not the value; the Twilio values are required only for `twilio` | Tests pass | Test fails |
| 3 | `main` uses the notifier named by `NOTIFIER`, and `--dry-run` still sends nothing and needs neither pywhatkit nor Twilio settings | Tests pass | Test fails |
| 4 | `dependencies` in `pyproject.toml` is still empty and `pywhatkit` is declared only in the optional extra `whatsapp` | Both hold | Either fails |
| 5 | `compose.yaml` sets `NOTIFIER=twilio`, and the README and the wiki in three languages describe the host run, the schedule and the Docker route | All hold | Any missing |
| 6 | BC-001, ADR-0001 and the dictionary carry a new Accepted row with a review record that is `Go` | All `Go` | Anything else |
| 7 | `python -m pytest` passes without network access or a browser; a real WhatsApp message is not sent by the AI | Tests pass | Tests fail |
| 8 | Python code has a `Go` review record against `QC-PY-001` | `Go` | Anything else |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-005 | Needs the settings, the notifier port and the forecast sources it extends |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O3, O4, O5, O6 | [BC-001] |
| SC3, SC4, SC8 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-24 — within the Business Case window of 2026-10-18 to 2026-10-25.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Implement pywhatkit notifier | Add `PywhatkitNotifier`, a `Notifier` that sends the message to `PHONENUMBER` with `pywhatkit.sendwhatmsg_instantly` through WhatsApp Web in the default browser of the host. The package is imported only when a message is sent and is the optional extra `whatsapp`, so `dependencies` stays empty; a missing package or a failed send is a `NotificationError` that never shows the phone number. | No | ADR-0001 |
| 2 | Add NOTIFIER setting and choose the notifier | Add the optional setting `NOTIFIER` (`pywhatkit`, the default, or `twilio`) to the settings loader, `config.env.example` and the composition root; the Twilio values are required only for `twilio`; set `NOTIFIER=twilio` in `compose.yaml`, because a container has no browser; an unknown value is a settings error that names the key. | No | ADR-0001 |
| 3 | Document the host run and its schedule | Describe in the README and in the wiki (English, Danish, Bahasa Malaysia) how to install the `whatsapp` extra, stay logged in to WhatsApp Web, run `--once` or the daily loop, and schedule `--once` with Windows Task Scheduler (`schtasks`); the Twilio and Docker route stays documented as the optional one. | No |  |
| 4 | Amend the Business Case, ADR-0001, dictionary and plan | Record the change in BC-001 (objectives O3 and O5, scope, assumptions), ADR-0001, the dictionary and the Project Plan, each with a new Version History row and a review record. | No | ADR-0001 |
| 5 | Add tests for the pywhatkit notifier | Write pytest tests with a fake send function: the call arguments, the missing package, a failed send, the no-leak rule, the `NOTIFIER` setting and the choice of notifier in `main`, with no browser and no network. | No | ADR-0001 |

---

[BC-001]: ../business-case.md
