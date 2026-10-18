# Stakeholder Analysis: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [728ff3e] |

---

## Purpose

This analysis names the people who shape or use Rain Alert and fixes their stable IDs for owners, reviewers and RACI in every other artifact. It uses the Power/Interest grid and maps concerns to FURPS+.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant: Product Owner, developer and reviewer | Tirsvad (personal learning project) | HIGH | HIGH | Manage Closely | A correct, well-documented result that completes the assignment and delivers the morning alert |
| S02 | Udemy coursists | Fellow course participants who share code and compare solutions | Udemy 100 Days of Code community | LOW | HIGH | Keep Informed | Readable, runnable code with the assignment's function names and README instructions to run it |
| S03 | GitHub viewers | Visitors who browse the repository for ideas | Public (GitHub and the git host) | LOW | MEDIUM | Keep Informed | A clear repository description, topics and README, and no runtime dependencies |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** decides scope, reviews and accepts every gateway, runs the container and is the only person who can change the plan.
- **Keep Informed (S02, S03):** they cannot change the project, but their ability to use the result defines its quality. They are informed through the README, the wiki and the repository page. S03 has medium interest because they browse and leave.

## Primary Concerns and FURPS+ Mapping

| ID | Concern | FURPS+ attribute |
| --- | --- | --- |
| S01 | The alert behaves as the assignment describes and arrives on WhatsApp | Functionality |
| S01 | Secrets stay out of git and out of the image | Reliability, Implementation |
| S01 | Every step is reviewed and traceable | Supportability |
| S02 | Code is readable and keeps the assignment's names and logic | Supportability, Usability |
| S02 | Setup and run steps work on a fresh machine | Usability, Implementation (Python 3.13, venv) |
| S03 | Description, topics and README make the repository findable and clear | Usability |
| S03 | No runtime dependencies to install or trust | Implementation, Reliability |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| S01 | Chat and pull request review | Per gateway | Pull request, run summary, review records | MIL-001 to MIL-004 |
| S02 | README and wiki | At release | Setup, run and test instructions in three languages | MIL-004 |
| S03 | Repository description, topics, README | At release | Description, topics, README with screenshot | MIL-001 and MIL-004 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S02 wants solutions close to the course code; S01 wants a layered, tested, containerised structure | S01, S02 | Keep the assignment's names and logic inside the layers and explain the mapping in the README and the architecture decision record |
| S03 wants no dependencies; Twilio's library, requests and testing tools are dependencies | S01, S03 | Standard library `urllib` for both APIs; test and lint tools are optional development dependencies; runtime dependencies stay empty |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | Alert works, secrets safe, traceable steps | O1 to O5, O9 ([BC-001]) |
| S02 | Readable code, runnable instructions | O2, O6, O7 ([BC-001]) |
| S03 | Findable repository, no dependencies | O7, O8 ([BC-001]) |

## Sign-Off

Product Owner: S01. Accepted when the review record says Go and the user has accepted the plan in chat.

---

[BC-001]: ./business-case.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
