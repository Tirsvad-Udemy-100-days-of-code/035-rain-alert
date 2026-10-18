# RC-014: Docker Compose file

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-014 |
| CrossReference | [QC-YML-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [2c661f6] |

---

## Artifact Under Review

- Instance reviewed: `compose.yaml` (the `Dockerfile` has no framework checklist; it was built and inspected: base image `python:3.13-slim`, non-root user `rainalert`, no `config.env` in the image)
- Checklist used: [QC-YML-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)
- Design reference: [ADR-0001]

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The file parses with a safe YAML loader and has no duplicate keys in any mapping | Pass | yamllint parses `compose.yaml`; `docker compose config` accepts it; no duplicate keys. |
| 2 | Indentation is 2 spaces everywhere, never tabs; lines end with LF; the file ends with one newline and has no trailing spaces | Pass | 2 spaces, LF, final newline, no trailing spaces (yamllint 1.38.0). |
| 3 | Passes `yamllint` (or the project's YAML linter) with its configuration committed next to the code and no unexplained `disable` comments | Pass | yamllint with the committed `.yamllint.yml`; reports nothing. |
| 4 | A scalar that YAML would coerce to another type is quoted: `yes`, `no`, `on`, `off`, `null`, `~`, numbers with a leading zero, versions such as `1.10`, and values that contain `: ` or ` #` | Pass | No coercible scalars; `latest` is part of an image name string. |
| 5 | Only safe, plain types are used: no language-specific tags (`!!python/object`, `!ruby/object`) and no `!include`-style extension unless the consuming tool documents it | Pass | No tags. |
| 6 | No secret is written in the file: no password, token, key or private connection string; a secret is referenced by name and supplied by the consuming tool | Pass | No secret in the file; secrets come from `config.env` through `env_file`. |
| 7 | Embedded program text (shell, Python, SQL, `jq`, and so on) in a value is at most five lines; a longer one is moved to a file of its own, in its own language, and the YAML calls it | Pass | No embedded program text. |
| 8 | A block of keys or values repeated in the file or across files is defined once (an anchor, a template, an include or a reusable unit the consumer supports) | Pass | One service; nothing repeated. |
| 9 | Anchors, aliases and merge keys (`&`, `*`, `<<`) are used only where the consuming tool is known to support them | Pass | No anchors. |
| 10 | The file validates against the schema of the consuming tool where one exists, and the schema or tool version is stated | Pass | `docker compose config` (Docker Compose 5.6.0) validates the file against the Compose schema. |
| 11 | A header comment states what the file is for, which tool reads it, and where its decision or design is recorded | Pass | Header comment states what the file is for, the commands, and that `config.env` is not copied into the image; the decision is ADR-0001. |
| 12 | Key names follow the convention of the consuming tool; one case style is used within the file (kebab-case or snake_case, never mixed) | Pass | Compose keys are lowercase; `container_name` and `env_file` follow Compose's own names. |
| 13 | Multi-line strings use a block scalar (`\|` or `>`) and state the chomping indicator (`\|-`, `\|+`) where the trailing newline matters | N-A | No multi-line string. |
| 14 | The file name is lowercase kebab-case with one extension style (`.yml` or `.yaml`) used throughout the repository | Pass | `compose.yaml` is the name Docker Compose prefers; lowercase with `.yaml`. The repository's other YAML files use `.yml` because the CI host requires it for workflows; the difference is by tool convention. |
| 15 | A change is exercised by a check that runs without the real target: a parse and schema test, or a dry run of the consuming tool | Pass | `docker compose config` validates the file without running anything. |

## Overall Verdict

Go — every applicable Mandatory criterion passes. Mode: autonomous, not independent.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-YML-001]: ../../../framework/qc/code/qc-yaml.md
[ADR-0001]: ../../adr/adr-0001-architecture-and-dependencies.md
[2c661f6]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/2c661f6f3db29c96b4cf1a482f5565d80f6c72d9
