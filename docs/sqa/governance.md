# Governance: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | GOV-001 |
| CrossReference | [BC-001], [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Defines how this project applies Quality Criteria (QC) checklists to real artifact instances, producing SQA Review Records and Go/No-Go decisions. It serves objective O9 of the Business Case ([BC-001]): every gateway is reviewed and traceable.

## ARB Review Workflow

1. **Submission:** the artifact owner (S01, or the AI as stand-in author) submits an instance for review, naming its type's QC checklist (`framework/qc/*/qc-*.md`).
2. **QC Checklist Review:** the Responsible reviewer (S01, or the AI as stand-in for S01 in autonomous mode) applies the checklist criterion by criterion.
3. **Review Record:** the Responsible reviewer documents the outcome as an SQA Review Record (`RC-*` under `docs/sqa/reviews/`).
4. **Go/No-Go Decision:** the Accountable role for the artifact category (S01) decides; contested or cross-cutting cases escalate to the ARB Chair (S01).
5. **Sign-off:** the Accountable role (S01) records the result. On **Go**, the artifact's `## Version History` gets an `Accepted` row and the previous row becomes `Deprecated`. On **Go-with-conditions**, the status stays `Proposed` until the Action Items are closed. On **No-Go**, the artifact returns to its owner (S01).
6. **Traceability Update:** the Responsible reviewer (S01) updates the Traceability Matrix with the instance and its `RC-*` reference.

## RACI by Artifact Category

| Artifact Category | Responsible (runs the review) | Accountable (Go/No-Go owner) | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Strategic (Stakeholder Analysis, Business Case) | S01 | S01 | S02 | S03 |
| Process/Business (Project Plan, Milestones/Gateways) | S01 | S01 | S02 | S03 |
| Modeling/Design (Architecture Decision Record, Domain Dictionary) | S01 | S01 | S02 | S03 |
| Source code (Python) | S01 | S01 | S02 | S03 |
| Governance and traceability (Governance, Traceability Matrix) | S01 | S01 | S02 | S03 |
| Documentation (README, wiki) | S01 | S01 | S02, S03 | S02, S03 |

The Requirements category (Use Case Diagram, User Story, Use Case) is out of scope: the Business Case ([BC-001]) takes the requirements from the course assignment. Cross-cutting escalations and disputed verdicts are Accountable to the ARB Chair (S01), overriding the category-level Accountable role.

## Escalation Rules

- A **No-Go** verdict, or any disagreement between the Responsible reviewer and the category's Accountable owner, escalates to the ARB Chair (S01).
- A reviewer may not review an instance they authored. The one exception is autonomous mode: the AI may act as stand-in for a reviewer or an Accountable role, recorded as `AI as stand-in for S01` and `Mode: autonomous, not independent`; the Product Owner's acceptance of the plan is the authorisation for it. The named alternate for an author who is also S01 is therefore the AI as stand-in, challengeable by S01 in the run summary.
- Repeated No-Go verdicts (2 or more) on the same artifact type trigger a review of the corresponding `QC-*` checklist itself.

## Cadence

- Reviews are triggered per artifact instance as it is produced or revised.
- QC checklists are reviewed when the framework submodule is updated, and at least once a year.

## Related Process Artifacts

The review procedure is `framework/process/review-checklist-process.md`; traceability is kept in [TM-001].

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[TM-001]: ./traceability-matrix.md
