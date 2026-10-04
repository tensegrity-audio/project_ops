# <Project Name> Agent Instructions

These instructions apply to the whole repository. Every human and agent follows this file. `CLAUDE.md` only points here; do not duplicate rules there.

## Mission

<One paragraph: what this repository is for, who it serves, and the one or two qualities that matter most (for example calm, private, dependable). Link the document that defines the goal.>

## Read first

1. `docs/project_ops.md` and `.project_ops/config.json`
2. `docs/roadmap/roadmap.md` and the active request under `docs/roadmap/in_progress/`
3. `docs/architecture/README.md`
4. <Any other document an agent must read before changing behaviour>

## Layout

| Path | What lives there |
| --- | --- |
| `<dir>/` | <one line> |
| `docs/roadmap/` | Roadmap and request artifacts (Project Ops) |
| `docs/reports/changelog.md` | Request-level change history |
| `tests/` | <what the tests cover> |

## Which source wins

When two sources disagree, the higher one in this list is right, and the lower one gets fixed:

1. The user's explicit instruction in this session
2. `AGENTS.md` (this file)
3. The active request artifact's State Summary
4. `.project_ops/config.json`
5. `docs/roadmap/roadmap.md`
6. Architecture and contract docs under `docs/architecture/`
7. `README.md`
8. Comments in code
9. Generated files and reports (never edit these by hand; rerun the generator)

## Change classes

| Class | Examples | What it requires |
| --- | --- | --- |
| Docs only | Typos, clarifications, roadmap sync | Changelog line |
| Behaviour | Code paths, defaults, schemas | Request artifact, tests, changelog, roadmap parity |
| Data or migration | Schema migrations, stored formats | New migration file, never an edit to a shipped one; rollback noted |
| Process | Validation commands, CI, templates | Change in the shared repository first (`project_ops`), then adopt here by version |
| Secrets or access | Tokens, scopes, deploy credentials | Human does it; agents describe the step and stop |

## Rules

- Never commit secrets, local paths, build output, logs, or personal data.
- Read widely, write narrowly: change only the files the request names in its touch map.
- Prefer a new file or a new migration over editing something that has shipped.
- Do not copy shared files from another repository. Consume them by pinned version.
- Keep the request State Summary, the roadmap entry, and the changelog in step. The request audit checks parity.
- When unsure which of two readings is right, state the assumption in the request artifact and continue; stop only when proceeding under either reading would be unsafe.

## Validation

```sh
<project check command, for example: npm run check>
python <path-to-project_ops>/tools/project_ops_audit.py --repo .
python <path-to-project_ops>/tools/project_ops_roadmap.py --repo .
python <path-to-project_ops>/tools/project_ops_request_audit.py --repo . --request-id <request_id>
```

CI runs the same audits through the reusable workflows in `tensegrity-audio/project_ops`.

## Handoff

Every unattended run ends with a report in the request artifact: what changed, what was tested and what was not, what is blocked, and the exact command to resume.
