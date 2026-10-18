# RC-018: Python source of MIL-005

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-018 |
| CrossReference | [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [a79371a] |

---

## Artifact Under Review

- Instance reviewed: Python source of MIL-005 (OpenWeatherForecastClient, FORECAST_API setting, main and their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)
- Design reference: [ADR-0001]

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Classes `OpenWeatherForecastClient` (PascalCase), module `openweather_client`, constants UPPER_SNAKE. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`FORECAST_25_PERIOD_HOURS`, `_forecast_api`, `_make_source`, `_fetch`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` clean, with ruff 0.17.1 and with the pinned 0.6.9 of the shared workflow; no suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function and method is annotated, including `-> None`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Specific exceptions only; `_fetch` and `_parse` re-raise `from error`; the `StopIteration` of an answer without the expected key is caught by name and turned into a forecast error. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults; no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | No files opened in this change. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | All new modules, classes and functions carry Doxygen docstrings; `doxygen Doxyfile` reports no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No printing; no new log line carries a secret; tests assert the API key is absent from errors of both clients and from logs. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | Classes trace to ADR-0001 as amended (RC-016): the second `ForecastSource` and the setting `FORECAST_API`. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 21 new tests (120 in all) named for behaviour, no network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict src tests` clean, with mypy 2.4.0 and with the pinned 1.11.2 of the shared workflow; the single `Any` stays justified in `_parse`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies = []` unchanged. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Request sending, error mapping and parsing are shared by both clients in `_fetch` and `_parse`; the endpoint, period length and setting values are defined once in `constants.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | Import direction unchanged: `infrastructure` imports `application` and `domain`; no cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `main` picks the source in `_make_source`; both clients implement the same narrow `ForecastSource` protocol and the use case is unchanged (open for extension). |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Layers and test folders unchanged. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are lowercase English with letters, digits and `_`. |

## Overall Verdict

Go — every criterion passes. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-architecture-and-dependencies.md
[a79371a]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/a79371a39d620ce761ca009ad1680d07ed2c61e0
