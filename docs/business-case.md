# Business Case: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Executive Summary

Rain Alert is a small command-line service built as the Day 35 assignment of Udemy's "100 Days of Code: The Complete Python Pro Bootcamp". Each morning it asks the OpenWeather One Call 4.0 API for the hourly forecast of one location (2.927761, 101.897999), decides whether it will rain in the next 12 hours, and if so sends the owner a WhatsApp message to bring an umbrella. It differs from the course in two ways chosen by S01: the message goes out as WhatsApp through the Twilio WhatsApp sandbox instead of SMS, and the program runs in a Docker container on S01's Docker Desktop instead of PythonAnywhere or GitHub Actions. The project is also a worked example of a documented, reviewed and tested Python repository that other course participants (S02) and repository visitors (S03) can read and run. We propose to build it in four reviewed gateways.

## Methodological and Standards Foundation

The project follows the SQA and QC framework mounted at `framework/` (artifact chain Business Case, Stakeholder Analysis, Project Plan, milestones, tasks, code; every step ends with a review record). Quality attributes follow ISO/IEC 25010:2023. Code follows PEP 8, PEP 257 and PEP 484 and a Clean Architecture layering; the program has no user interface or API, so no presentation pattern applies beyond a command-line entry point. Requirements come from the course assignment (the Day 35 lectures) and from S01's changes, rather than from use-case modelling, which is out of proportion for an assignment of this size.

## Problem Statement

The course solution is one script that prints or texts a message, with API keys and phone numbers typed into the code or into a hosting dashboard. Its SMS route no longer works from a free Twilio account for US and Canadian numbers, its host (PythonAnywhere) needs proxy changes on a free account, and the starter does not run on S01's own machine. Participants seldom publish a result that others can run: there is often no setup guide, no tests, no stated Python version and no separation of the weather logic from the sending of the message.

## Business Opportunity

A small, well-documented reference solution lets S02 compare their own solutions with readable code that keeps the assignment's logic (the `cnt` of four three-hour slots becomes the next twelve hourly slots; a weather condition id below 700 means rain or worse), and lets S03 find a clean example repository with a description, topics and README. For S01 it delivers a working morning alert on their own machine, with secrets kept out of the code in a git-ignored `config.env`.

## Objectives

| # | Objective |
| --- | --- |
| O1 | The program fetches the hourly forecast from the OpenWeather One Call 4.0 API for the latitude and longitude in `config.env` (2.927761, 101.897999) and keeps the next 12 hours. |
| O2 | The program decides that rain is expected when any of the next 12 hourly weather condition ids is below 700, as in the assignment. |
| O3 | When rain is expected the program sends a WhatsApp message to `PHONENUMBER` through the Twilio WhatsApp sandbox; otherwise it sends nothing. |
| O4 | `OPENWEATHER_APIKEY`, `PHONENUMBER`, the location and the Twilio credentials are read from the environment, supplied by `config.env`; none is in the code or in git. |
| O5 | The program runs once a day at a configurable local time (default 07:00) in a Docker container on Docker Desktop, started with one command. |
| O6 | The code is typed, documented with Doxygen comments, uses `constants.py` for constants and is covered by pytest tests that need neither network nor Docker. |
| O7 | A newcomer can create a local `.venv`, upgrade pip, run the program (also as a dry run) and the tests from the README alone. |
| O8 | The repository has a description, topics, CI workflows, a README with a screenshot and a wiki in English, Danish and Bahasa Malaysia. |
| O9 | Every step is traceable: each gateway is a reviewed milestone with tasks as issues, delivered by one pull request. |

## Scope

### In Scope

- The rain check: forecast model, rain decision, forecast source port, OpenWeather One Call 4.0 client, with the assignment's naming where it exists (`will_rain`, `weather_params`, `cnt` as the number of hours).
- The WhatsApp notifier through the Twilio WhatsApp sandbox REST API, and a dry run that prints the message instead of sending it.
- Configuration from environment variables, loaded from `config.env` by the container and by an optional small file reader for local runs; a committed `config.env.example`.
- A daily scheduler inside the container, a `Dockerfile` and a Compose file for Docker Desktop.
- Project configuration (`pyproject.toml`, Python 3.13 or later, `.gitignore`, `Doxyfile`, `constants.py`) and the folder structure `src/`, `tests/`, `docs/`.
- pytest tests, run from a local `.venv`.
- README from the framework template, with run and test instructions and a screenshot.
- Wiki pages in English, Danish and Bahasa Malaysia, with screenshots.
- Repository description and topics, and the CI workflows from `TirSystem/github-action` that fit the project (quality checks, wiki publishing; the GitHub metadata mirror is delivered to the repository by the host).

### Out of Scope

- SMS delivery, pywhatkit and WhatsApp Web automation (they need a desktop browser, not a container).
- Hosting on PythonAnywhere or scheduling by GitHub Actions (the course alternatives).
- Several locations, several recipients, snow or wind rules, message templates and a retry queue.
- Packaging for PyPI, and runtime dependencies (the standard library is enough).
- Capturing a WhatsApp chat screenshot from S01's phone: only S01 can supply it.

## Expected Benefits

### Tangible Benefits

- A morning WhatsApp alert that runs unattended on S01's machine.
- A passing test suite and a repository that builds in one `docker compose up` command.
- A README and a three-language wiki that a newcomer can follow without help.

### Intangible Benefits

- Practice in applying the course topics (APIs, authentication, environment variables, scheduling) with professional review discipline.
- A reusable pattern for the other Day-NNN repositories of the course.

## Strategic Alignment

The project supports S01's goal of completing the bootcamp with portfolio-quality results, and the course repository group's goal of consistent, reviewable projects built on one framework.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| SC1 | Forecast request | The request carries `lat`, `lon`, `appid`, `units=metric` and returns the next 12 hourly records | Unit test of the client with a fake response; one manual dry run against the live API |
| SC2 | Rain decision | 100 % of tested forecasts give the expected `will_rain` result, including the boundary ids 699, 700 and 800 | Unit tests |
| SC3 | Notification | A message is sent to the configured number only when rain is expected; exactly one message per run | Unit tests with a fake sender; Twilio request shape asserted |
| SC4 | Secrets | 0 secrets in git, in the image layers or in the logs | `git ls-files` and history search for the `config.env` values; `.dockerignore` check; log tests |
| SC5 | Test suite | 100 % of tests pass; line coverage of the domain and application layers at least 90 % | `python -m pytest` output |
| SC6 | Container | `docker compose up -d` starts a container that runs the check at the configured time, and `--once` runs it immediately | Manual run recorded in a screenshot; unit tests of the scheduler clock |
| SC7 | Setup from README | A fresh clone reaches a dry run in 5 commands or fewer | Dry run of the README steps |
| SC8 | Runtime dependencies | 0 third-party runtime dependencies | `dependencies = []` in `pyproject.toml` |
| SC9 | Languages | Wiki has 3 languages with the same page set | Page listing and `framework/scripts/check-languages.sh` |
| SC10 | Traceability | 4 of 4 milestones `Accepted` with a `Go` review; every task closed by a pull request | Milestone documents and issue list |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The One Call 4.0 API is a separate OpenWeather subscription and S01's key may be refused (HTTP 401) | No forecast | The client raises a specific error naming the status; the endpoint URL is a constant, so a fallback to the 3.0 or 2.5 forecast is a one-line change; S01 is told at the first live dry run |
| The Twilio WhatsApp sandbox needs S01's phone to have joined it and expires after 72 hours of silence | The message is not delivered | The README and wiki describe joining the sandbox; the error text from Twilio is shown in the log |
| Twilio credentials are not yet in `config.env` | The notifier cannot send | `config.env.example` lists the keys; the work stops at the first live send and reports which key is missing |
| The container's time zone differs from S01's | The alert arrives at the wrong hour | `TZ` and the alert time are settings; the scheduler computes the next run from the configured zone, with unit tests |
| A secret reaches git, an image or a screenshot | Disclosure | `config.env` and `.env` are git-ignored and `.dockerignore`d, the container receives them at run time only, and screenshots show no values |
| Danish or Bahasa Malaysia text contains errors | S02 and S03 are misled | English is authoritative, translations follow it page by page, S01 is asked to check Danish, and Bahasa Malaysia is flagged as unchecked until a reader has checked it |
| Docker Desktop is not available in the build session | The image cannot be built or run here | The Dockerfile and Compose file are checked by a linter and by reading; the image is built on S01's machine and the result is reported |

## Assumptions

- S01 is Product Owner, developer and reviewer; the AI acts as stand-in author and reviewer in autonomous mode and says so on every record.
- "Python greater than 3.13" is read as 3.13 or later (`requires-python = ">=3.13"`).
- The repository is the one named by `origin` (`Tirsvad-Udemy-100-days-of-code/035-rain-alert` on `git.tirsystem.com`); the URL in the request (`Tirsvad-Udemy-100_days_of_code`) is taken as the organisation of that repository.
- S01 supplies the Twilio account SID, auth token and WhatsApp sandbox number in `config.env`; the file already holds `OPENWEATHER_APIKEY` and `PHONENUMBER`.
- The alert reads "rain" as the assignment does: a condition id below 700 (thunderstorm, drizzle, rain, snow).
- The tokens in `.env` (git host and GitHub) are for S01's personal use: the AI uses them only to set the repository description and topics and to publish milestones, and the project neither imports nor tests them.

## Constraints

- Python 3.13 or later, `venv` for the environment, pytest for tests, `constants.py` for constants, `pyproject.toml` for configuration.
- Folder structure `src/`, `tests/`, `docs/`; Doxygen comments in the source and a `Doxyfile`.
- One pull request per milestone, from a branch; a reviewer other than the author merges (in autonomous mode the AI merges after green checks), and the AI never bypasses a required check.
- Target window: 2026-10-18 to 2026-10-25.

## Cost–Benefit Assessment

The assessment is qualitative: the project is a learning exercise with no revenue, and effort is the only cost, so a monetary ROI would be invented.

| Costs | Benefits |
| --- | --- |
| About 20 hours of S01's review time and about 4 hours of AI effort across four gateways | A working daily alert and a published reference solution |
| Twilio sandbox and OpenWeather free tier, existing git host and Docker Desktop | A findable repository for S02 and S03 |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Owns, builds, runs and reviews the result for the bootcamp (O1 to O9) |
| S02 | Needs readable, runnable code with the assignment's logic and names and README instructions (O2, O6, O7) |
| S03 | Needs a clear description, topics, README and no runtime dependencies (O7, O8) |

## Recommendation

Proceed — the scope is small, the risks have mitigations and every objective is verifiable by a milestone gate.

---

[SA-001]: ./stakeholder-analysis.md
