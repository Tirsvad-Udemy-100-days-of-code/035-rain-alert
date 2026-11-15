# Project Plan: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | PP-001 |
| CrossReference | [BC-001], [SA-001], [MIL-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005], [MIL-006], [MIL-007] |
| Language | en |
| Domain | education |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added gateway MIL-005 (forecast API fallback) before MIL-004 after the live run showed HTTP 401 on One Call 4.0 | [5da8060] |
| 2026-10-18 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added gateway MIL-006 (pywhatkit notifier) before MIL-004 content is brought up to date | [6434347] |
| 2026-11-16 | Accepted | Jens Tirsvad Nielsen | S01 (AI as stand-in) | Added the baseline gateway (MIL-007) with its schedule row, scope coverage, dependency, risk and Gantt entries; linked the first six gateways to their milestones; noted that the third Open Issue is superseded by the fourth and fifth, and that the quality workflow now uses the shared git-workflows on the git host; set the domain to education; reviewed in autonomous mode, not independent | pending |

---

## Purpose

Schedules the six gateways that deliver Rain Alert within the Business Case window of 2026-10-18 to 2026-10-25 ([BC-001]), and the baseline gateway ([MIL-007]) that was added later. Each gateway is one milestone document, one Milestone on the git host and one pull request from its own branch.

## Planning Assumptions

- Week 1 starts 2026-10-18; the plan ends by 2026-10-25, per the Business Case constraint.
- The baseline gateway ([MIL-007]) starts 2026-11-16 and ends 2026-11-23, one week, as the Business Case constraint for it requires. It brings the finished project to the baseline of the framework (decision of S01); the first six gateways keep their dates.
- Phase length: two days per gateway. S01 is the only owner and reviewer ([SA-001]); the AI acts as stand-in author and reviewer in autonomous mode.
- The baseline (Business Case, Stakeholder Analysis, Project Plan, governance, dictionary, ADR-0001, milestones) is accepted when the user accepts this plan in chat; MIL-001 starts after that.
- Branch per step: `plan-baseline`, `mil-001-project-foundation`, `mil-002-rain-check-core`, `mil-003-whatsapp-alert-and-container`, `mil-004-documentation-and-wiki`.

## Gateway Schedule

| Gateway | Document | Window | Decision date | Owner | Stories | Main deliverable | Milestone |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Project foundation | [MIL-001] | 2026-10-18 to 2026-10-19 | 2026-10-19 | S01 | none | Configuration, skeleton, `config.env.example`, README, quality workflow, repository description and topics | [Milestone 206][M-206] |
| Rain check core | [MIL-002] | 2026-10-20 to 2026-10-21 | 2026-10-21 | S01 | none | Forecast model, rain decision, settings, One Call 4.0 client, tests | [Milestone 207][M-207] |
| WhatsApp alert and container | [MIL-003] | 2026-10-22 to 2026-10-23 | 2026-10-23 | S01 | none | Twilio WhatsApp notifier, scheduler, entry point, Dockerfile, Compose file, tests | [Milestone 208][M-208] |
| Forecast API fallback | [MIL-005] | 2026-10-18 to 2026-10-23 | 2026-10-23 | S01 | none | The free 2.5 forecast as a second, selectable forecast source | [Milestone 211][M-211] |
| pywhatkit notifier | [MIL-006] | 2026-10-18 to 2026-10-24 | 2026-10-24 | S01 | none | WhatsApp Web through pywhatkit as the default notifier, Twilio optional | [Milestone 212][M-212] |
| Documentation and wiki | [MIL-004] | 2026-10-24 to 2026-10-25 | 2026-10-25 | S01 | none | Screenshots, README, wiki in three languages, wiki workflow | [Milestone 209][M-209] |
| Framework baseline | [MIL-007] | 2026-11-16 to 2026-11-23 | 2026-11-23 | S01 | none | The adopted framework release, the wiki sidebar in the framework's shape, the README, licence metadata, the traceability matrix and review records | [Milestone 550][M-550] |

```plantuml
@startgantt
Project starts 2026-10-18
[Project foundation] starts 2026-10-18 and ends 2026-10-19
[Rain check core] starts 2026-10-20 and ends 2026-10-21
[WhatsApp alert and container] starts 2026-10-22 and ends 2026-10-23
[Forecast API fallback] starts 2026-10-18 and ends 2026-10-23
[pywhatkit notifier] starts 2026-10-18 and ends 2026-10-24
[Documentation and wiki] starts 2026-10-24 and ends 2026-10-25
[Foundation Go/No-Go] happens 2026-10-19
[Core Go/No-Go] happens 2026-10-21
[Alert Go/No-Go] happens 2026-10-23
[Fallback Go/No-Go] happens 2026-10-23
[Notifier Go/No-Go] happens 2026-10-24
[Documentation Go/No-Go] happens 2026-10-25
[Framework baseline] starts 2026-11-16 and ends 2026-11-23
[Baseline Go/No-Go] happens 2026-11-23
@endgantt
```

## Scope Coverage

| Business Case scope item | Gateway |
| --- | --- |
| Rain check: forecast model, decision, port, One Call 4.0 client | MIL-002 |
| WhatsApp notifier, dry run, scheduler, entry point | MIL-003 |
| Docker image and Compose file for Docker Desktop | MIL-003 |
| pywhatkit notifier, `NOTIFIER` setting, host run and schedule | MIL-006 |
| Second forecast source (free 2.5 forecast) chosen with `FORECAST_API` | MIL-005 |
| Configuration from `config.env`, `config.env.example` | MIL-001 (example, location), MIL-002 (loader) |
| Project configuration, folder structure, `constants.py`, `Doxyfile` | MIL-001 |
| pytest tests | MIL-001 (set-up), MIL-002 and MIL-003 (tests) |
| README with run and test instructions | MIL-001 (first version), MIL-004 (finished) |
| Screenshots, wiki in three languages | MIL-004 |
| Repository description and topics | MIL-001 |
| The baseline: framework release, wiki sidebar, README, licence metadata, traceability matrix, review records | [MIL-007] |
| CI workflows from `TirSystem/github-action` | MIL-001 (quality), MIL-004 (wiki) |

## Dependencies

```
MIL-001 → MIL-002 → MIL-003 → MIL-005 → MIL-006 → MIL-004 → MIL-007
```

A No-Go on a gateway stops the chain: later windows move by the days needed to fix it, and the Business Case window is renegotiated with S01 if it runs past 2026-10-25. S01 decides the new dates. A No-Go on [MIL-007] leaves the program and the earlier gateways as they are.

## Plan Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The git host API or token fails when setting description and topics | MIL-001 cannot close criterion 6 | The tool stops and reports; S01 sets them by hand in the web UI |
| A required CI check on the host fails for a reason outside the project | A pull request cannot merge | Stop after three attempts on the same cause and report, as AGENTS.md requires |
| The OpenWeather key has no One Call 4.0 subscription, or Twilio values are missing from `config.env` | The live dry run or live send in MIL-003 cannot succeed | Everything else is tested with fakes; the run stops and reports which key or subscription is missing |
| Docker Desktop is not reachable from the build session | The image is not built here | Compose file validated by reading and `docker compose config` if available; S01 builds and reports |
| Screenshots need a desktop session | MIL-004 delay | Capture the terminal dry run and Docker Desktop on S01's own Windows desktop, masking secrets |
| A continuous integration (CI) check fails on the pull request of [MIL-007] | The merge is delayed past 2026-11-23 | The failure is fixed on the same branch and the checks run again; after three failed rounds on one cause the work stops and S01 decides (trace: SC11 of [BC-001]) |

## Open Issues

- The repository URL in the request (`Tirsvad-Udemy-100_days_of_code`) differs from `origin` (`Tirsvad-Udemy-100-days-of-code/035-rain-alert`); the plan uses `origin`.
- The request's course text names Twilio SMS, PythonAnywhere and GitHub Actions; S01's changes (WhatsApp, Docker container, `config.env`) replace them, and the course alternatives are out of scope ([BC-001]).
- The reference script in S01's earlier repository used pywhatkit (WhatsApp Web in a browser) and the 2.5 forecast; a container has no browser, so this project sends through the Twilio WhatsApp sandbox and uses One Call 4.0.
- The first live run (2026-10-18) showed that the OpenWeather key has no One Call by Call subscription (HTTP 401 on One Call 4.0 and 3.0; the free 2.5 forecast answers). S01 chose to add the 2.5 forecast as a second source ([MIL-005]). [BC-001] objective O1 names One Call 4.0 and stays as accepted: One Call 4.0 remains the default, the 2.5 forecast is the fallback, and this note records the difference.
- S01 uses pywhatkit and runs the program on their own machine, not Twilio in the container ([MIL-006]). [BC-001] is amended for it (objectives O3 and O5). pywhatkit is the default notifier; Twilio stays an optional notifier for the Docker container. The documentation gateway [MIL-004] was already merged and is brought up to date by [MIL-006] (README, wiki in three languages).
- The Twilio values are needed only for the optional Twilio notifier.
- Bahasa Malaysia text cannot be checked by S01 or the AI as a reader of the language; it stays flagged as unchecked in the wiki.
- The plan was accepted without a QC checklist until [MIL-007]; since then it is reviewed against `QC-PP-001` ([RC-026]).
- Domain: since [MIL-007] the plan, the Business Case, the Traceability Matrix and the baseline milestone have the domain `education`. The other documents (Stakeholder Analysis, Domain Dictionary, Governance, milestones MIL-001 to MIL-006 and the review records RC-001 to RC-024) keep the domain `it` they were accepted with; they are not changed by the baseline, and a change of their domain would need a new review of each. The Domain Dictionary still names `it` as the PO domain in its Purpose and Scope.
- The wiki publishing workflow that MIL-004 added (its task 6, issue 26) was removed in the commit "Use git-workflows and the scoped workflows" (pull request #47), because the shared workflows of the git host publish `docs/wiki/`; the task stays in MIL-004 as the accepted record. The same commit moved `.gitea/workflows/quality.yml` to the shared repository `TirSystem/git-workflows`; the earlier documents still name it `TirSystem/github-action`.
- The third Open Issue above describes the first design (Twilio in the container, One Call 4.0). The fourth and fifth Open Issues, [MIL-005] and [MIL-006] supersede it: One Call 4.0 stays the default with the 2.5 forecast as the fallback, and pywhatkit is the default notifier with Twilio optional.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
[MIL-001]: ./milestones/mil-001-project-foundation.md
[MIL-002]: ./milestones/mil-002-rain-check-core.md
[MIL-003]: ./milestones/mil-003-whatsapp-alert-and-container.md
[MIL-004]: ./milestones/mil-004-documentation-and-wiki.md
[MIL-005]: ./milestones/mil-005-forecast-api-fallback.md
[MIL-006]: ./milestones/mil-006-pywhatkit-notifier.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
[5da8060]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/5da8060e2000533a95fed0b380e9ba2aa8b25be2
[6434347]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/64343473499f718679459bbf4b580073ffafa370
[M-206]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/206
[M-207]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/207
[M-208]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/208
[M-211]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/211
[M-212]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/212
[M-209]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/209
[MIL-007]: ./milestones/mil-007-framework-baseline.md
[RC-026]: ./sqa/reviews/rc-026-project-plan-baseline.md
[M-550]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/milestones/550
