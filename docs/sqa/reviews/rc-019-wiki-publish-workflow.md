# RC-019: Wiki publish workflow

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-019 |
| CrossReference | [QC-WF-001], [QC-YML-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Proposed | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [80a3886] |

---

## Artifact Under Review

- Instance reviewed: CI workflow `.gitea/workflows/publish-wiki.yml`
- Checklist used: [QC-WF-001] and [QC-YML-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)

## Checklist Results

### QC-WF-001

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The file meets the YAML checklist ([QC-YML-001]) | Pass | See the YAML results below. |
| 2 | The file is in `.gitea/workflows/` or `.github/workflows/` with the extension `.yml` or `.yaml`, and the same workflow does not exist in both directories | Pass | `publish-wiki.yml` is in `.gitea/workflows/` with `.yml`; it is not in `.github/workflows/`. Host: Gitea 1.27.3. |
| 3 | The file declares `name`, `on` and `jobs`; `on` lists explicit events and, where it matters, `branches` or `paths` | Pass | `name`, `on` (push to main with `paths`, and a manual run) and `jobs` are present. |
| 4 | A header comment states the purpose, the triggers, the inputs, the secrets it needs, what it changes outside the repository, and the decision or milestone it implements | Pass | Header comment states purpose, triggers, secret, changes outside the repository, decision and pin. |
| 5 | Every job and step has a descriptive `name`, unique within its job | Pass | The job has a `name`. |
| 6 | The file passes `actionlint` (or the project's workflow validation test) and the tool version is stated | Pass | `actionlint` 1.7.12 reports nothing. |
| 7 | Every job declares `permissions` explicitly with the least access that works (`contents: read` or none by default); write access only on the job that needs it | Pass | The job sets `permissions: contents: read`. |
| 8 | Every action used is pinned to a full commit SHA or an exact release tag, never to a branch; a moving major tag (`@v1`) is accepted only for an action published by the same organisation under a stated release policy | Pass | The major tag `v1` of an action of the same organisation (release policy: the CHANGELOG of `TirSystem/github-action`). |
| 9 | No secret is written in the file; a secret is read as `secrets.NAME`, passed to a step through `env:`, never placed on a command line or echoed | Pass | No secret in the file; `TOKEN_FOR_GITEA_WIKI` is passed by name. |
| 10 | Untrusted text (`inputs.*`, event fields such as a title, branch name or label, step outputs derived from them) is never interpolated into a `run:` script; it is passed through `env:` and used as a quoted variable | Pass | No `run:` script and no untrusted text. |
| 11 | A trigger that gives a run secrets or a write token on code from a fork or an untrusted branch (`pull_request_target`, `workflow_run`) does not check out or execute that code | N-A | No `pull_request_target` or `workflow_run` trigger. |
| 12 | A workflow that changes state outside the repository (release, tag, publish, sync, deploy) is started by hand or by a protected branch, and a manual run defaults to a dry run with an explicit input to apply | Fail | The workflow changes the wiki only on a push to main or a manual run, and the pages come from a reviewed folder, but a manual run has no dry-run input because the called shared workflow offers none. |
| 13 | The token the workflow uses has only the scope the job needs, and where the host's built-in token is enough it is used instead of a personal token | Pass | The token is the narrowest scope the shared guide names (`write:repository`). |
| 14 | Every job sets `runs-on` to an explicit label and `timeout-minutes` | N-A | The job calls a reusable workflow; `runs-on` and `timeout-minutes` are set inside it. |
| 15 | `concurrency` is set where two runs would conflict: a check cancels the older run (`cancel-in-progress: true`); a publishing job queues (`cancel-in-progress: false`) | Pass | Publishing queues (`cancel-in-progress: false`). |
| 16 | Triggers are filtered (`branches`, `paths`, `types`) so the workflow runs only for the changes it concerns | Pass | `paths` and `branches` filters. |
| 17 | Tools and dependencies are installed at pinned versions; a version is a workflow input with a default or a value in one place | N-A | No tool is installed by this file; the shared workflow pins its own. |
| 18 | A dependency cache is used where the install is slow enough to matter | N-A | Optional; no installation. |
| 19 | A failing step names the tool, the file and the reason in its log (annotation or `::error::` line) | N-A | Optional; the shared workflow reports. |
| 20 | A `run:` block is within the limit on embedded program text of criterion 7 of [QC-YML-001]; a longer script is a file (`tools/`, or a shared repository fetched at a pinned ref) that the step calls with one command, and the workflow passes its settings through `env:` | Pass | No `run:` block. |
| 21 | Logic used by more than one workflow or repository is a reusable workflow (`workflow_call`) or a composite action; each input has a `description`, a `type` and a `default` where one is sensible | Pass | The job calls a reusable workflow; nothing is duplicated. |
| 22 | Every workflow feature used is verified on the instance that runs it, and the host and version are recorded; a feature the target hosts differ on is noted in the header | Pass | The shared guide records the reusable workflow as verified on Gitea 1.27.3; its first run in this repository follows the merge of this pull request. |
| 23 | A reusable workflow states, in its header, how a caller pins it and the script it fetches, so the workflow and its script are the same release | N-A | Optional; the header names the major tag and the release policy. |
| 24 | A static test of the repository's workflows exists and runs on every pull request: valid YAML, required keys, explicit permissions and runner, no inline script above the limit | N-A | Optional; no static workflow test in this repository. |

### QC-YML-001

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The file parses with a safe YAML loader and has no duplicate keys in any mapping | Pass | yamllint parses the file; no duplicate keys. |
| 2 | Indentation is 2 spaces everywhere, never tabs; lines end with LF; the file ends with one newline and has no trailing spaces | Pass | 2 spaces, LF, final newline, no trailing spaces (yamllint 1.38.0). |
| 3 | Passes `yamllint` (or the project's YAML linter) with its configuration committed next to the code and no unexplained `disable` comments | Pass | yamllint with the committed `.yamllint.yml`; reports nothing. |
| 4 | A scalar that YAML would coerce to another type is quoted: `yes`, `no`, `on`, `off`, `null`, `~`, numbers with a leading zero, versions such as `1.10`, and values that contain `: ` or ` #` | Pass | `prune: "true"` is quoted; no other coercible scalars. |
| 5 | Only safe, plain types are used: no language-specific tags (`!!python/object`, `!ruby/object`) and no `!include`-style extension unless the consuming tool documents it | Pass | No tags. |
| 6 | No secret is written in the file: no password, token, key or private connection string; a secret is referenced by name and supplied by the consuming tool | Pass | No secret value. |
| 7 | Embedded program text (shell, Python, SQL, `jq`, and so on) in a value is at most five lines; a longer one is moved to a file of its own, in its own language, and the YAML calls it | Pass | No embedded program text. |
| 8 | A block of keys or values repeated in the file or across files is defined once (an anchor, a template, an include or a reusable unit the consumer supports) | Pass | No repeated blocks. |
| 9 | Anchors, aliases and merge keys (`&`, `*`, `<<`) are used only where the consuming tool is known to support them | Pass | No anchors. |
| 10 | The file validates against the schema of the consuming tool where one exists, and the schema or tool version is stated | Pass | actionlint checks the workflow schema (1.7.12). |
| 11 | A header comment states what the file is for, which tool reads it, and where its decision or design is recorded | Pass | The header states purpose, tool and decision. |
| 12 | Key names follow the convention of the consuming tool; one case style is used within the file (kebab-case or snake_case, never mixed) | Pass | kebab-case keys as the host requires; `wiki_dir` and `TOKEN_FOR_GITEA_WIKI` are input and secret names fixed by the called workflow. |
| 13 | Multi-line strings use a block scalar (`\|` or `>`) and state the chomping indicator (`\|-`, `\|+`) where the trailing newline matters | N-A | No multi-line string. |
| 14 | The file name is lowercase kebab-case with one extension style (`.yml` or `.yaml`) used throughout the repository | Pass | `publish-wiki.yml` is lowercase kebab-case with `.yml`. |
| 15 | A change is exercised by a check that runs without the real target: a parse and schema test, or a dry run of the consuming tool | Pass | actionlint and yamllint run without the target. |

## Overall Verdict

Go-with-conditions — every other applicable Mandatory criterion passes; criterion 12 of QC-WF-001 fails because a manual run has no dry-run input, which the shared workflow of `TirSystem/github-action` would have to add. The workflow stays `Proposed` until condition 1 is closed. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Condition 1: accept the missing dry-run input as a recorded deviation, or ask `TirSystem/github-action` to add one | S01 | 2026-10-25 |
| Condition 2: after the merge, confirm the first run of Publish wiki on the host (runner online, organization secret `TOKEN_FOR_GITEA_WIKI` set) | S01 | 2026-10-25 |

---

[QC-WF-001]: ../../../framework/qc/code/qc-workflow.md
[QC-YML-001]: ../../../framework/qc/code/qc-yaml.md
[80a3886]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/80a388609738516d3cdd6444ca3c42ad6457c3c0
