# RC-013: Python source of MIL-003

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-013 |
| CrossReference | [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: Python source of MIL-003 (notifiers, scheduler, use case, main and their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)
- Design reference: [ADR-0001]

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules and packages are snake_case, classes PascalCase (`DailyScheduler`, `TwilioWhatsAppNotifier`), constants UPPER_SNAKE. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`run_rain_alert`, `twilio_notifier_from_settings`, `next_run`, `explanation`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` clean (ruff 0.17.1); the only suppressions are two `# type: ignore` in tests, each on a line that deliberately breaks a type (immutability, a settings factory). |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function and method is annotated, including `-> None` and the nested `job` and `guarded`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Only specific exceptions are caught (`HttpStatusError`, `HttpError`, `ForecastUnavailableError`, `NotificationError`, `SettingsError`); each is re-raised `from error` or logged and turned into an exit code; the daily loop logs a failed day and continues. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults; no builtin shadowed in the source. |
| 7 | Files, locks and connections are managed with context managers | Pass | `urlopen` uses `with`; the dry-run notifier writes to a stream it is given. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | All public modules, classes and functions carry Doxygen docstrings; `doxygen Doxyfile` reports no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | `logging` is used for all program output; the dry-run notifier writes its message to an injected stream, which is the product of a dry run and not a log. Tests assert that no log line contains the API key, token, SID or phone number, and `Settings.__repr__` hides them. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | Classes trace to ADR-0001: `Notifier` port, `run_rain_alert` use case, `TwilioWhatsAppNotifier`, `DryRunNotifier`, `DailyScheduler`, `main` as composition root; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 99 tests named for behaviour; no network and no order dependence; the end-to-end tests run the program as a process with no internet; the real settings file is never read (`--config` points to a missing file). |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict src tests` reports no issues; no `Any` was added in this change. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies = []`; `tzdata` is a Windows-only development dependency so the time zone tests find data. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The error explanation is read in one place (`explanation`) for both services; the umbrella text, URLs and setting names are defined once in `constants.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `domain` imports only `constants`; `application` imports `domain`; `infrastructure` imports `application` and `domain`; `main` is the only module that imports all layers; no cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `run_rain_alert` receives a `ForecastSource` and a `Notifier`; new notifiers are added by implementing the narrow protocol, not by editing the use case; the transport protocols are split into `HttpGetter` and `FormPoster`. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Layers under `src/rain_alert/` and `unit`, `integration`, `e2e` under `tests/` (all three now hold tests); no presentation layer because the program has no user interface (ADR-0001). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are lowercase English with letters, digits and `_`; `Dockerfile` and `compose.yaml` are well-known names. |

## Overall Verdict

Go — every criterion passes. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-architecture-and-dependencies.md
