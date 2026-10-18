# Forecast API fallback

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decides whether the program can get its forecast with the OpenWeather key S01 has. The first live run showed that One Call 4.0 answers HTTP 401 because it needs a separate subscription, while the free 2.5 forecast of the course answers; S01 chose to add the 2.5 forecast as a second, selectable source.

## Deliverable

A pull request with the 2.5 forecast client, the setting `FORECAST_API` and the choice of source in the composition root, the amended ADR-0001 and dictionary with their delta reviews, and the tests.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The 2.5 client requests `https://api.openweathermap.org/data/2.5/forecast` with `lat`, `lon`, `appid`, `units=metric` and `cnt=4` for 12 hours, and returns the periods of the answer's `list` | Test with a fake response passes | Test fails |
| 2 | `FORECAST_API` defaults to `onecall4`, accepts `forecast25`, and rejects any other value with an error that names the key and not the value | Tests pass | Test fails |
| 3 | `main` uses the source named by `FORECAST_API` | Tests with a fake transport show the right URL | Wrong URL |
| 4 | Errors of the 2.5 client never contain the API key | Tests pass | Key leaks |
| 5 | ADR-0001 and the dictionary carry a new Accepted row with a delta review record that is `Go` | Both `Go` | Anything else |
| 6 | `python -m pytest` passes without network access; one dry run against the live API with `FORECAST_API=forecast25` shows the decision or reports the failure to S01 | Both hold | Tests fail |
| 7 | Python code has a `Go` review record against `QC-PY-001` | `Go` | Anything else |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | Needs the entry point, the settings and the OpenWeather One Call 4.0 client it extends |

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

2026-10-23 — within the Business Case window of 2026-10-18 to 2026-10-25; it comes before [MIL-004], whose screenshots need a forecast that works.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Implement 2.5 forecast client | Add a second `ForecastSource` for the free OpenWeather 2.5 forecast (`/data/2.5/forecast`, `lat`, `lon`, `appid`, `units`, `cnt` = the number of three-hour periods that cover the next 12 hours, as in the course), parsing its `list` and sharing the request and error handling with the One Call 4.0 client, without echoing the API key. | No | ADR-0001 |
| 2 | Add FORECAST_API setting and choose the source | Add the optional setting `FORECAST_API` (`onecall4`, the default, or `forecast25`) to the settings loader, `config.env.example` and the composition root, so the program uses the forecast the API key is entitled to; an unknown value is a settings error that names the key. | No | ADR-0001 |
| 3 | Amend ADR-0001 and the dictionary | Record the second forecast source in ADR-0001 (new Version History row, reviewed as a delta) and add the forecast period to the domain dictionary, since a period is one hour for One Call 4.0 and three hours for the 2.5 forecast. | No | ADR-0001 |
| 4 | Add tests for the forecast fallback | Write pytest tests for the 2.5 request and parsing, the setting and its validation, and the choice of source in `main`, with fakes only and no network. | No | ADR-0001 |

---

[BC-001]: ../business-case.md
[MIL-004]: ./mil-004-documentation-and-wiki.md
