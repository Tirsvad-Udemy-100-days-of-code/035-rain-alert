# RC-012: Python source of MIL-002

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-012 |
| CrossReference | [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [4716b8d] |

---

## Artifact Under Review

- Instance reviewed: Python source of MIL-002 (domain, application, settings, OpenWeather client and their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)
- Design reference: [ADR-0001]

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules and packages are snake_case, classes PascalCase (`HourlyForecast`, `OpenWeatherClient`, `UrllibTransport`), constants UPPER_SNAKE. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`will_rain`, `check_rain`, `ForecastUnavailableError`, `load_environment`); no single-letter names outside comprehensions. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` clean (ruff 0.17.1); one test suppression `# type: ignore[misc]` is explained by the test that asserts immutability. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function and method is annotated, including `-> None`; fakes in tests too. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; transport errors are mapped to `HttpError` subclasses and then to `ForecastUnavailableError` with `raise ... from error`; no exception is swallowed. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults; no builtin shadowed (`format` in the test server's `log_message` overrides the base class signature and is not used). |
| 7 | Files, locks and connections are managed with context managers | Pass | `urlopen` and file reading use `with`; the test server is shut down in a fixture. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | All public modules, classes and functions carry Doxygen docstrings that say what; `doxygen Doxyfile` reports no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No logging or printing in this change; errors name keys, statuses and service messages, never the API key, phone number or a setting's value (tests assert it). |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | Classes and operations trace to ADR-0001: `ForecastSource` port, `check_rain` use case, `OpenWeatherClient`, settings loader; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 58 tests named for behaviour; no network (a local server on 127.0.0.1 is used for the transport) and no order dependence. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict src tests` reports no issues; `Any` is used once for decoded JSON and is justified by a comment in `_parse`. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies = []`; dev extras declared; nothing unused. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The rain limit, hours, URL and setting names are defined once in `constants.py`; `will_rain` is the only place that applies the rule. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `domain` imports only `constants` and itself; `application` imports `domain`; `infrastructure` imports `application` and `domain`; no cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Each class has one reason to change; `ForecastSource`, `HttpGetter` and `FormPoster` are narrow protocols; `check_rain` receives its source. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Layers `domain`, `application`, `infrastructure` under `src/rain_alert/`; tests in `unit`, `integration` (the real transport against a local server) and `e2e` (empty until the entry point exists). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All file names are lowercase English with letters, digits and `_`. |

## Overall Verdict

Go — every criterion passes. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-architecture-and-dependencies.md
[4716b8d]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/4716b8d87a4273347d557f15557b667d555b0fc9
