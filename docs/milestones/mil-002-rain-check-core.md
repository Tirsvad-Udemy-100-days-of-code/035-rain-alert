# Rain check core

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decides whether the weather logic works and is tested without the network, Twilio or Docker: the forecast model, the rain decision, the settings and the OpenWeather One Call 4.0 client, so the notification gateway can build on them.

## Deliverable

A pull request with the domain and application layers (`HourlyForecast`, `will_rain`, the `ForecastSource` port, the `check_rain` use case), the settings loader, the OpenWeather client, and their pytest tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `will_rain` returns true when any of the next 12 condition ids is below 700 and false otherwise, including the boundaries 699, 700 and 800 | Tests pass | Any test fails |
| 2 | The client requests `https://api.openweathermap.org/data/4.0/onecall/timeline/1h` with `lat`, `lon`, `appid` and `units=metric` from the settings and returns the first 12 hourly records | Test with a fake response passes | Test fails |
| 3 | The settings loader reads the environment variables, can read a `config.env` file without overriding variables already set, and names the missing key in its error | Tests pass | Test fails |
| 4 | An unreachable API, an HTTP error (401, 429) or invalid JSON raises a specific error whose text never contains the API key | Tests pass | Test fails or key leaks |
| 5 | `python -m pytest` passes without network access and line coverage of `domain` and `application` is at least 90 % | Both hold | Either fails |
| 6 | Python code has a `Go` review record against `QC-PY-001` | `Go` | Anything else |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-001 | Needs `pyproject.toml`, the package skeleton, `constants.py` and the pytest set-up |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1, O2, O4, O6 | [BC-001] |
| SC1, SC2, SC5 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-21 — within the Business Case window of 2026-10-18 to 2026-10-25.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Implement HourlyForecast and will_rain | Add the immutable `HourlyForecast` (time and condition ids) and `will_rain` in the domain layer, applying the assignment's rule that an id below 700 means rain, with Doxygen comments and tests for the boundaries. | No | ADR-0001 |
| 2 | Implement settings loader | Add the `Settings` value (API key, phone number, latitude, longitude, Twilio values, alert time, zone) read from environment variables, with a small `config.env` file reader for local runs that never overrides a variable already set and never prints a value. | No | ADR-0001 |
| 3 | Add ForecastSource port and check_rain use case | Define the `ForecastSource` protocol and the `check_rain` use case that asks the source for the next 12 hours and returns the decision, so the domain does not know the API. | No | ADR-0001 |
| 4 | Implement OpenWeather One Call 4.0 client | Build the request from `constants.py` and `weather_params` (`lat`, `lon`, `appid`, `units`), fetch it with `urllib.request`, parse the hourly `data` list, keep the first 12 records, and raise a specific error on network failure, HTTP error or invalid JSON without echoing the key. | No | ADR-0001 |
| 5 | Add unit tests for the core | Write pytest tests for `will_rain`, the settings, the use case and the client using a fake source and a fake HTTP response, with no network access. | No | ADR-0001 |

---

[BC-001]: ../business-case.md
