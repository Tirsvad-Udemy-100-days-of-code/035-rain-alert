# Review Record: PP-001 against QC-PP-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-026 |
| CrossReference | [PP-001], [QC-PP-001], [QC-LANG-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-16 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial review record; verdict Go (autonomous, not independent) | pending |

---

## Artifact Under Review

- Instance reviewed: [PP-001]
- Checklist used: [QC-PP-001] and [QC-LANG-001]
- Scope: full review
- Language and domain: en / education
- Language reviewer: none (the stand-in reads English and knows the education domain)
- Mode: autonomous, not independent (AI as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The plan states its start date, end date and the constraint it must fit | Pass | Planning Assumptions give the start date 2026-10-18, the end of the first six gateways (2026-10-25, the Business Case window) and the window 2026-11-16 to 2026-11-23 of the baseline; the Business Case constraints give the window and the one-pull-request-per-milestone rule. |
| 2 | Every milestone or gateway is listed once with its document, decision date and owner | Pass | The Gateway Schedule lists the seven gateways once each with document, decision date and owner; every document exists, including MIL-007. |
| 3 | Every decision date lies inside the plan's window and is consistent with the dates in the linked `MIL-*` document | Pass | The decision dates of MIL-001 to MIL-006 equal the Target Dates of their milestone documents (read for this review: 2026-10-19, 2026-10-21, 2026-10-23, 2026-10-25, 2026-10-23 for MIL-005 and 2026-10-24 for MIL-006) and lie in the window of the Business Case; MIL-007 decides on 2026-11-23, which is its Target Date and the end of the window that the Business Case sets for the baseline. |
| 4 | Every in-scope item of the Business Case is delivered at a named gateway (scope coverage) | Pass | Scope Coverage maps every In Scope item of BC-001 to a gateway; the new baseline item maps to MIL-007. |
| 5 | Dependencies between gateways are stated, acyclic and consistent with the schedule order | Pass | Dependencies state the chain MIL-001, MIL-002, MIL-003, MIL-005, MIL-006, MIL-004 and MIL-007; it is acyclic and agrees with the order of the dates. |
| 6 | The plan states what happens to later gateways and to the end date when a gateway is No-Go | Pass | Dependencies state that a No-Go stops the chain, that later windows move, that S01 decides the new dates and that a No-Go on MIL-007 leaves the program and the earlier gateways as they are. |
| 7 | Owners, reviewers and escalation roles use Stakeholder Analysis IDs and match the governance RACI | Pass | Owner S01 and reviewer S01 (stand-in for the baseline) are stakeholder IDs of SA-001; the governance RACI of GOV-001 names S01 as Responsible and Accountable for the Process/Business documents, so nothing contradicts it. |
| 8 | Planning assumptions are listed with their source, and a changed baseline is recorded with its reason | Pass | Each planning assumption names its source or is a decision of S01 (stated in the plan); the added baseline gateway is recorded with its reason. |
| 9 | Plan risks are listed with impact and a mitigation, and trace to Business Case risks where they come from there | Pass | Plan Risks give impact and mitigation for each of the six risks; the CI risk of MIL-007 traces to SC11 of BC-001 and the others to the risks of BC-001 (token scope, screenshots). |
| 10 | Open issues are listed, and none contradicts a statement elsewhere in the plan | Pass | Open Issues lists the repository path, the course differences, the HTTP 401 of One Call 4.0, the move to pywhatkit, the unchecked Bahasa Malaysia text, the earlier lack of a checklist, the domain of the unchanged documents, the removed wiki workflow and the note that the third issue is superseded by the fourth and fifth; no remaining statement contradicts another. |
| 11 | Each gateway's main deliverable is stated and matches the deliverable of its `MIL-*` document | Pass | The main deliverable of MIL-007 names the same items as its Deliverable section; the rows of MIL-001 to MIL-006 match their milestone documents. |
| 12 | Gateways that deliver user stories name them, and those that do not say why | Pass | The Stories column of every gateway says none; the Business Case takes its requirements from the course assignment and the changes of S01. |
| 13 | The schedule view (table, Gantt) and the dependency view agree with each other | Pass | The Gantt bars use the dates of the schedule table and the dependency line is the same chain as the schedule order. |
| 14 | Each gateway is linked to its issue-tracker milestone, or marked as not yet synced | Pass | Each gateway links its milestone on the git host (206, 207, 208, 209, 211 and 212 exist; the milestone of MIL-007 is linked after the sync). |
| 15 | The plan is a singleton: one Project Plan per project, changes recorded in Version History | Pass | PP-001 is the only Project Plan; its Version History records each change in its own row and only the latest row is Accepted. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | The Metadata table has `Language | en` and `Domain | education`; neither is a placeholder. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is a BCP 47 code and `education` is a row of the domain list of docs/artifact-registry.md. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The prose and the table cells are English; only file names, commands and IDs are code. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | The registry gives the register `IT Executive English` for this type; the text is written for that reader. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | DICT-001 exists. The text added by the baseline uses none of its terms (forecast, rain, notifier, alert and similar) under a second name, found by reading. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, section headings, IDs and statuses are the framework's English ones. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | No file `<name>.<language>.md` exists beside the document. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | The `Domain` row changed from `it` to `education` in this version (the language `en` is unchanged). The Version History row records the change and this review covers it. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The stand-in reads English and knows the education domain and checked the terms; the check is autonomous and not independent. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Fail | Some abbreviations of the earlier text (ADR, API, HTML, PEP, PyPI, UI and similar) are not spelled out at first use; the abbreviations added in this change are. Optional, deferred. |

## Overall Verdict

Go — every Mandatory criterion of QC-PP-001 and QC-LANG-001 passes; the domain of the unchanged documents is recorded as an Open Issue. The plan is reviewed against its checklist for the first time. Review of the whole document after the edits of this change.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Criterion LANG 10 (Optional) failed: Abbreviations are spelled out on first use, in the stated language; fix or accept the deferral | S01 | 2026-11-23 |

---

[PP-001]: ../../project-plan.md
[QC-PP-001]: ../../../framework/qc/artifacts/qc-project-plan.md
[QC-LANG-001]: ../../../framework/qc/artifacts/qc-language-domain.md
