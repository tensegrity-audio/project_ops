# Execution Process

Project Ops gives a project a durable operating loop. The loop is intentionally simple: write down the request, keep state current, validate before closing, and leave enough context for the next person or agent to resume.

## Phases

| Phase | Purpose | Exit signal |
| --- | --- | --- |
| `INTAKE` | Capture the request and context. | The request artifact exists and has an acceptance signal. |
| `FORM` | Shape the problem and constraints. | The work has a clear scope and non-goals. |
| `ANALYSIS` | Inspect affected files, docs, systems, and risks. | The touch map and risks are explicit. |
| `PLAN` | Choose steps, validation, and stop conditions. | The task graph is executable. |
| `EXECUTION` | Make the change. | The implementation or documentation slice is complete. |
| `VALIDATION` | Run checks and record results. | Pass/fail/not-run evidence is recorded. |
| `DOC_SYNC` | Update roadmap, changelog, and related docs. | The durable docs match the work. |
| `POST_MORTEM` | Capture lessons, residual risks, and follow-ups. | The closeout notes are useful. |
| `COMPLETE` | Archive or close the request. | The request can be resumed historically without guessing. |

## Operating Loop

1. Create a request from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.
2. Fill in the State Summary first.
3. Check the roadmap for overlap before starting.
4. Work the task graph in small slices.
5. Record meaningful execution notes as the work changes.
6. Run the validation commands in `.project_ops/config.json`.
7. Update the roadmap and changelog before closeout.
8. Use `templates/phase_exit_audit.md` before moving phases or handing off.
9. Use `templates/handoff.md` when another person or agent needs to resume.
10. Use `templates/post_mortem.md` when the work closes or reveals a durable lesson.

## Required Sync Points

| Event | Update |
| --- | --- |
| Request starts | request artifact, roadmap entry |
| Scope changes | request State Summary, roadmap overlap review |
| Meaningful behavior changes | changelog, validation plan, related docs |
| Validation runs | request Validation section |
| Work pauses | request Resume From field, optional handoff |
| Work completes | roadmap status, changelog, post-mortem |

## Audit-Only First

For a new adopter, run Project Ops in audit-only mode before adding CI enforcement. Audit-only mode should report missing files, risky config, and missing validation commands without rewriting the repo.

```powershell
python <path-to-project_ops>\tools\project_ops_audit.py --repo .
```

When the audit is quiet, the project can decide whether to add assisted state-machine tooling, CI checks, or stricter roadmap/changelog parity.
