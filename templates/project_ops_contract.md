# Project Ops

This project uses Project Ops for documentation structure and execution tracking.

Local operating files:

- `.project_ops/config.json` defines project paths, scope labels, privacy posture, and validation expectations.
- `docs/roadmap/roadmap.md` records active and completed work.
- `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` defines request artifacts.
- `docs/reports/changelog.md` records meaningful project changes.
- `docs/governance/README.md` explains local decision rules.

Project Ops provides reusable structure. This repository owns its product decisions, roadmap, reports, release notes, and validation evidence.

## Operating Loop

1. Open or create a request artifact from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.
2. Keep the request State Summary current.
3. Mirror active request state into `docs/roadmap/roadmap.md`.
4. Record meaningful outcomes in `docs/reports/changelog.md`.
5. Run the validation commands listed in `.project_ops/config.json`.
6. Close with doc sync and a post-mortem when the request is complete.
