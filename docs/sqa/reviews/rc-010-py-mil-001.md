# RC-010: Python source of MIL-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-010 |
| CrossReference | [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [2f60adf] |

---

## Artifact Under Review

- Instance reviewed: Python source of MIL-001 (src/rain_alert, tests/unit)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)
- Design reference: [ADR-0001]

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Packages `domain`, `application`, `infrastructure`; constants in UPPER_SNAKE; module `rain_alert`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Constant names state purpose (`FORECAST_HOURS`, `RAIN_CONDITION_LIMIT`, `ENV_API_KEY`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` clean (ruff 0.17.1). |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Constants are annotated with `Final[...]`; the test functions are `-> None`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No exception handling in this change. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No functions with defaults; no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | No files or connections opened. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Module docstrings and a Doxygen `@brief` comment on every constant. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No output or logging in this change. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | Constants trace to ADR-0001 (all constants in `constants.py`); no classes yet. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | `tests/unit/test_constants.py` has 4 behaviour tests, no network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict src tests` reports no issues. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies = []`; dev extras declared in `pyproject.toml`. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Each constant is defined once in `constants.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | Layer packages are empty; `constants.py` imports only `typing`. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | No classes yet. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `domain`, `application`, `infrastructure` under `src/rain_alert/`, `unit`, `integration` and `e2e` under `tests/`; no presentation layer because the program has no user interface (ADR-0001). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are lowercase English with letters, digits and `_`; `README.md` and `LICENSE` are well-known names. |

## Overall Verdict

Go — every criterion passes. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-architecture-and-dependencies.md
[2f60adf]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/2f60adffb0c2083791d0cd4a0f9002a79d318654
