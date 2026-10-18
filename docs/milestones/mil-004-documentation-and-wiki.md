# Documentation and wiki

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [728ff3e] |

---

## Purpose

Decides whether S02 and S03 can understand, run and test the project from the README and the wiki, in English, Danish and Bahasa Malaysia, with screenshots.

## Deliverable

A pull request with screenshots of the running program, the finished README, the wiki in `docs/wiki/` in three languages with the same page set, the wiki publish workflow, and the generated-Doxygen check.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The README follows the framework template, has at least one screenshot and passes `bash framework/scripts/check-readme.sh` | Exit 0 | Non-zero |
| 2 | Following the README on a fresh clone reaches a dry run and a passing test run | Both succeed | Either fails |
| 3 | Every English wiki page has a Danish (`-da`) and a Bahasa Malaysia (`-ms`) page, and each starts with the language line | Same page set in 3 languages | A page missing |
| 4 | The wiki has at least one screenshot and `_Sidebar.md` lists every language | Present | Missing |
| 5 | `bash framework/scripts/check-languages.sh` passes | Exit 0 | Non-zero |
| 6 | `.gitea/workflows/publish-wiki.yml` is installed from the framework template or `TirSystem/github-action` at a pinned tag, and `yamllint` passes | Both hold | Either fails |
| 7 | `doxygen Doxyfile` runs without warnings, or Doxygen is not installed and the README says how to install it | Either holds | Warnings |
| 8 | No screenshot or document contains the API key, the auth token, a git host token or the phone number | A search for the `.env` and `config.env` values finds nothing | A match |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | The screenshots need the running program |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O7, O8, O9 | [BC-001] |
| SC7, SC9, SC10 | [BC-001] |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-25 — within the Business Case window of 2026-10-18 to 2026-10-25.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Capture screenshots | Run the program and capture screenshots of a dry run that expects rain, a dry run that expects none, and the container in Docker Desktop (or its log), stored in `docs/images/`, with every secret and the phone number masked. A WhatsApp chat screenshot is added only if S01 supplies one. | No |  |
| 2 | Finish README | Add the screenshot, the mapping from the course script to the layers, the Docker Desktop and WhatsApp sandbox set-up, and the links of the appendix to the finished documents. | No |  |
| 3 | Write English wiki | Write the English wiki pages in `docs/wiki/` (Home, Install, Usage, Architecture, Testing, Contributing) with screenshots and `_Sidebar.md`, following `framework/process/wiki.md`. | No |  |
| 4 | Translate wiki to Danish | Add the Danish pages (`<Page>-da.md`) page by page, with the language line and unchanged code blocks and commands. | No |  |
| 5 | Translate wiki to Bahasa Malaysia | Add the Bahasa Malaysia pages (`<Page>-ms.md`) page by page, with the language line and unchanged code blocks and commands. | No |  |
| 6 | Install the wiki publish workflow | Add the publish-wiki workflow from `framework/templates/ci/` (hardened as in the other Day-NNN repositories) so the wiki reaches the git host's wiki by merge. | No |  |
| 7 | Check Doxygen output | Run Doxygen on the `Doxyfile` and fix any warning in the source comments. | No |  |

---

[BC-001]: ../business-case.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
