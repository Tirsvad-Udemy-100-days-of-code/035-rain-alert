# Traceability Matrix: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001], [SA-001], [PP-001], [DICT-001], [GOV-001], [MIL-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added RC-013 (Python source of MIL-003) and RC-014 (Compose file) | [2c661f6] |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added RC-015 (MIL-005), RC-016 (ADR-0001 amendment) and RC-017 (dictionary amendment) | pending |

---

## Purpose

Tracks backward/forward links between artifact instances so that the Business Case's cross-artifact traceability objective (O9) is measurable. A row is added or updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| [BC-001] | BC | en | it | - | [SA-001], [PP-001], [DICT-001], [GOV-001], [ADR-0001] | [RC-001] |
| [SA-001] | SA | en | it | [BC-001] | [PP-001], [GOV-001] | [RC-002] |
| [PP-001] | PP | en | it | [BC-001], [SA-001] | [MIL-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005] | - (no checklist for the Project Plan) |
| [DICT-001] | DICT | en | it | [BC-001], [SA-001] | - | [RC-017] |
| [GOV-001] | GOV | en | it | [BC-001], [SA-001] | [TM-001] | [RC-004] |
| [ADR-0001] | ADR | - | - | [BC-001], [MIL-005] | source code under `src/` | [RC-016] |
| [MIL-001] | MIL | en | it | [BC-001], [PP-001] | source code, configuration and README | [RC-006] |
| [MIL-002] | MIL | en | it | [BC-001], [PP-001], [MIL-001] | source code and tests of the domain, application and settings | [RC-007] |
| [MIL-003] | MIL | en | it | [BC-001], [PP-001], [MIL-002] | source code, tests, Dockerfile and Compose file of the alert | [RC-008] |
| [MIL-004] | MIL | en | it | [BC-001], [PP-001], [MIL-003] | README, screenshots and wiki | [RC-009] |
| Python source of MIL-001 (`src/rain_alert`, `tests`) | PY | - | - | [ADR-0001], [MIL-001] | - | [RC-010] |
| CI workflow `.gitea/workflows/quality.yml` | WF | - | - | [MIL-001] | - | [RC-011] |
| Python source of MIL-002 (`domain`, `application`, `infrastructure` settings and OpenWeather client) | PY | - | - | [ADR-0001], [MIL-002] | - | [RC-012] |
| Python source of MIL-003 (`application` use case, notifiers, scheduler, `main`) | PY | - | - | [ADR-0001], [MIL-003] | - | [RC-013] |
| `compose.yaml` and `Dockerfile` | YML | - | - | [ADR-0001], [MIL-003] | - | [RC-014] |
| [MIL-005] | MIL | en | it | [BC-001], [PP-001], [MIL-003] | source code and tests of the forecast fallback | [RC-015] |

## Coverage Notes

- No instance exists yet of KPI, BMC, BPMN, UCD, US, UC, DM, SSD, OC, SD, DCD or ERD: the requirements come from the course assignment and S01's changes (see [BC-001]) and the design reference is [ADR-0001].
- In Upstream `-` means foundational; in Downstream `-` means nothing is built on it yet; in Last Reviewed `-` means no `RC-*` exists.
- Source code is reviewed against `QC-PY-001` before each pull request; those records are added to this matrix as they are written.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[DICT-001]: ../dictionary.md
[GOV-001]: ./governance.md
[ADR-0001]: ../adr/adr-0001-architecture-and-dependencies.md
[MIL-001]: ../milestones/mil-001-project-foundation.md
[MIL-002]: ../milestones/mil-002-rain-check-core.md
[MIL-003]: ../milestones/mil-003-whatsapp-alert-and-container.md
[MIL-004]: ../milestones/mil-004-documentation-and-wiki.md
[MIL-005]: ../milestones/mil-005-forecast-api-fallback.md
[RC-001]: ./reviews/rc-001-business-case.md
[RC-002]: ./reviews/rc-002-stakeholder-analysis.md
[RC-003]: ./reviews/rc-003-dictionary.md
[RC-004]: ./reviews/rc-004-governance.md
[RC-005]: ./reviews/rc-005-adr-0001.md
[RC-006]: ./reviews/rc-006-mil-001.md
[RC-007]: ./reviews/rc-007-mil-002.md
[RC-008]: ./reviews/rc-008-mil-003.md
[RC-009]: ./reviews/rc-009-mil-004.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
[RC-010]: ./reviews/rc-010-py-mil-001.md
[RC-011]: ./reviews/rc-011-ci-workflow-quality.md
[2f60adf]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/2f60adffb0c2083791d0cd4a0f9002a79d318654
[RC-012]: ./reviews/rc-012-py-mil-002.md
[4716b8d]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/4716b8d87a4273347d557f15557b667d555b0fc9
[RC-013]: ./reviews/rc-013-py-mil-003.md
[RC-014]: ./reviews/rc-014-compose-file.md
[2c661f6]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/2c661f6f3db29c96b4cf1a482f5565d80f6c72d9
[RC-015]: ./reviews/rc-015-mil-005.md
[RC-016]: ./reviews/rc-016-adr-0001-amendment.md
[RC-017]: ./reviews/rc-017-dictionary-amendment.md
