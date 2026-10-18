# Project foundation

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [728ff3e] |

---

## Purpose

Decides whether the repository has the configuration, structure, workflows and documentation skeleton that every later gateway builds on: a Python 3.13 project with a local `.venv`, pytest, constants, Doxygen, a git-ignored `config.env` with an example, a CI workflow and a public description.

## Deliverable

A pull request that adds `pyproject.toml`, `.gitignore`, `.dockerignore`, the package skeleton `src/rain_alert/` with `constants.py`, the folder `tests/` with a passing smoke test, the `Doxyfile`, `config.env.example`, the quality workflow, a first `README.md` from the framework template with `.venv` setup instructions, and the repository description and topics on the git host.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pyproject.toml` declares `requires-python = ">=3.13"` and an empty `dependencies` list | Both present | Either missing |
| 2 | A fresh `.venv` can be created and `python -m pip install --upgrade pip` and `python -m pip install -e ".[dev]"` succeed | Commands succeed | Any command fails |
| 3 | `python -m pytest` passes | 0 failures | Any failure |
| 4 | `.gitignore` ignores `.venv/`, `__pycache__/`, `.env` and `config.env`, `git ls-files` lists neither `.env` nor `config.env`, and `config.env.example` holds keys without secret values | All hold | Any fails |
| 5 | `Doxyfile` exists and `doxygen` is documented in the README | Present | Missing |
| 6 | The repository has a description and at least five topics on the git host | Both set | Either unset |
| 7 | `.gitea/workflows/quality.yml` calls the shared quality workflow of `TirSystem/github-action` at a pinned release tag, and `yamllint` passes | Both hold | Either fails |
| 8 | `bash framework/scripts/check-readme.sh` passes | Exit 0 | Non-zero |
| 9 | Python code has a `Go` review record against `QC-PY-001` | `Go` | Anything else |

## Dependencies

| Depends on | Reason |
| --- | --- |
| None | First gateway; it needs only the accepted baseline (Business Case, Stakeholder Analysis, Project Plan) |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O4, O6, O7, O8 | [BC-001] |
| SC4, SC7, SC8 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-19 — within the Business Case window of 2026-10-18 to 2026-10-25.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add pyproject.toml | Declare the project with `requires-python = ">=3.13"`, an empty runtime `dependencies` list, a `dev` extra with pytest, pytest-cov, ruff and mypy, the `src` layout and the pytest configuration. This keeps the runtime free of dependencies for S03. | No | ADR-0001 |
| 2 | Add Python .gitignore | Add a Python `.gitignore` that also ignores `.venv/`, `.env`, `config.env`, build output and Doxygen output, and a `.dockerignore` with the same secrets, so tokens, API keys and the phone number are never committed or copied into an image. | No |  |
| 3 | Create package skeleton and constants.py | Create `src/rain_alert/` with the layer packages `domain`, `application`, `infrastructure`, and `constants.py` with the first constants (API URLs, forecast hours, rain threshold 700, default alert time, environment variable names). Add `tests/unit`, `tests/integration` and a smoke test so pytest runs. | No | ADR-0001 |
| 4 | Add Doxyfile | Add a `Doxyfile` for the Python sources (`OPTIMIZE_OUTPUT_JAVA`, input `src/`, output `build/doxygen`) and the Doxygen comment style used in the source. | No |  |
| 5 | Add config.env.example | Add `config.env.example` listing `OPENWEATHER_APIKEY`, `PHONENUMBER`, `LATITUDE`, `LONGITUDE`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`, `ALERT_TIME` and `TZ` with no secret values, and set `LATITUDE=2.927761` and `LONGITUDE=101.897999` in S01's own git-ignored `config.env`. | No | ADR-0001 |
| 6 | Write README with venv setup | Write `README.md` from the framework template with the `.venv` creation, `python -m pip install --upgrade pip`, install, run, dry-run and test instructions for Windows and POSIX shells. Screenshots are added in MIL-004. | No |  |
| 7 | Install the quality workflow | Add `.gitea/workflows/quality.yml` that calls the reusable quality-checks workflow of `TirSystem/github-action` at a pinned release tag, as the other Day-NNN repositories do; the GitHub metadata mirror workflow is delivered by the host. | No |  |
| 8 | Set repository description and topics | Set the description and topics of the repository on the git host through its API, using the token in the git-ignored `.env`. The token is never printed, imported by the project or tested. | No |  |

---

[BC-001]: ../business-case.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
