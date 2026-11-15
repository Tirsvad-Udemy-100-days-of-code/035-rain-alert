# Framework baseline

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-007 |
| CrossReference | [BC-001], [PP-001], [MIL-006] |
| Language | en |
| Domain | education |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-16 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version; accepted with the Go verdict of the review record (autonomous, not independent) | pending |

---

## Purpose

This gate decides whether Rain Alert has the baseline of the framework: the adopted framework release, the wiki in English, Danish and Bahasa Malaysia with the sidebar in the framework's shape (title, one list of the English pages, the Languages section last), the README in the framework template with an appendix that lists only the documents of the repository, complete licence and project URL metadata, a current traceability matrix and reviewed documents, merged to the default branch with a green build. The work is delivered on the branch `mil-007-baseline` and one pull request. It changes no behaviour of the program.

## Deliverable

A merged pull request that holds: the updated Business Case, Project Plan, Artifact Registry and Traceability Matrix and their review records; the wiki sidebar in `docs/wiki/`; the README without the private framework files in its appendix; `pyproject.toml` with the project URLs, the author and a build requirement that reads the licence expression; `.editorconfig` and `.env.example` of the framework baseline; and the framework release adopted by the project. The program and its tests do not change.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | BC-001, PP-001 and MIL-007 each have an `Accepted` Version History row and a review record, and the wiki has a review record | Verdict `Go` (the wiki `Go-with-conditions` until it is checked on the host) | Any missing or `No-Go` |
| 2 | `python -m pytest` runs (the tests use fakes and need no network, no browser and no WhatsApp or Twilio account; no message is sent; the continuous integration (CI) of the pull request runs the quality checks of the sources) | Exit code 0 | Any failure |
| 3 | `docs/wiki/` has `_Sidebar.md` and the pages Home, Install, Usage, Architecture, Testing and Contributing in en, da and ms, each starting with the language line, and the sidebar has the title, one list of the English pages and the Languages section last, with no Related section | 18 pages and the sidebar | A page or language missing, a page without the language line first, or a sidebar of another shape |
| 4 | `framework/scripts/check-readme.sh`, `framework/scripts/check-languages.sh` and `framework/scripts/check-editorconfig.sh` run | Exit code 0 | Any finding |
| 5 | `pyproject.toml` sets `license`, `license-files`, the authors and the project URLs for the repository, the documentation and the issue tracker, and requires a setuptools version that reads the licence expression | All set | Any missing |
| 6 | All CI checks of the pull request | Green | Red or pending |
| 7 | The pull request carries one `Closes #N` line per task of this milestone | Every issue is closed after the merge | An issue stays open |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-006] accepted | Documents and baselines the finished program, its tests, its README and its wiki |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1 to O9 | Criterion 2 (the behaviour is unchanged and its tests pass) |
| O10 | Criteria 1, 3, 4, 5 and 7 (documents, wiki, README, licence and issues) |
| SC11 | Criteria 1 and 6 |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 (AI as stand-in, autonomous mode, not independent) |

## Target Date

2026-11-23: one week after the start, as the Business Case constraint for this milestone requires.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Adopt the framework release | Track the `framework/` submodule and `.gitmodules` (lowercase repository URL), install the skills and hooks, add `.editorconfig`, bring `.env.example` to the framework's template and ignore the AI prompt log, so the project follows the same rules as the other projects of the portfolio. | No | BC-001 O8 |
| 2 | Update and review the planning documents | Add this milestone to the Business Case and Project Plan, link the six earlier gateways to their milestones, set the domain of the changed documents to education, bring the Traceability Matrix and the Artifact Registry up to date and review each changed document against its QC checklist, so the plan-first gate is met. | No | BC-001 O8 |
| 3 | Bring the wiki sidebar to the framework's shape | Remove the Related section of the sidebar (the wiki has no related wiki), keep the existing pages and their names, and add a review record for the wiki. | No | BC-001 O8 |
| 4 | Bring the README to the framework template | Keep the text of the README, add the framework files to the description of the layout, name the licence expression and give the appendix only the documents that are in the repository, so the README is complete and checkable. | No | BC-001 O8 |
| 5 | Complete the package metadata | Set the author and the project URLs in `pyproject.toml` and raise the build requirement to the setuptools version that reads a licence expression, so package tools can read them. | No | BC-001 O8 |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[MIL-006]: ./mil-006-pywhatkit-notifier.md
