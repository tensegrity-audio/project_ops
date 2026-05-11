# Project Ops

This project uses Project Ops for documentation structure and execution tracking.

Local operating files:

- `.project_ops/config.json` defines project paths, scope labels, privacy posture, and validation expectations.
- `docs/roadmap/roadmap.md` records active and completed work.
- `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` defines request artifacts.
- `docs/reports/changelog.md` records meaningful project changes.
- `docs/governance/README.md` explains local decision rules.
- `docs/governance/prioritization_policy.md` explains roadmap scoring and readiness gates when used.
- Stable `Request ID` and `Decision ID` values connect requests, roadmap entries, changelog notes, RFC-lite decisions, handoffs, and postmortems.

Project Ops provides reusable structure. This repository owns its product decisions, roadmap, reports, release notes, and validation evidence.

## Local Subsystem Connections

| Local file or folder | Connects to | Why it matters |
| --- | --- | --- |
| `.project_ops/config.json` | Project Ops audit tools and local docs. | Keeps paths, scope labels, privacy posture, and validation commands explicit. |
| `docs/project_ops.md` | README, roadmap, governance, and contributors. | Gives people and agents the local operating map. |
| `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` | Request artifacts. | Gives every request the same state, risk, validation, and resume fields. |
| `docs/roadmap/roadmap.md` | Request artifacts, prioritization policy, RFC-lite decisions, and changelog. | Makes active and completed work visible in one planning surface. |
| `docs/reports/changelog.md` | Roadmap, releases, request IDs, and closeout notes. | Records meaningful outcomes after the work changes. |
| `docs/architecture/` | Requests and implementation work. | Holds project-specific system maps and contracts. |
| `docs/governance/` | Config, prioritization, validation, and review policy. | Explains local decision rules, readiness gates, and ownership boundaries. |

## Agent Start Checklist

Before changing files, an agent should read:

1. This document.
2. `.project_ops/config.json`.
3. The active request artifact, if one exists.
4. `docs/roadmap/roadmap.md`.
5. `docs/reports/changelog.md`.
6. `docs/governance/prioritization_policy.md` if the project uses one.
7. Any RFC-lite decisions linked by the request or roadmap.
8. Any architecture, governance, or validation docs named by the request.

Use the Agent Execution Contract from the installed Project Ops version as the detailed step-by-step protocol. Adopter repos may keep a local copy or reference the version they consume.

## Operating Loop

1. Open or create a request artifact from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.
2. Set the Request ID to match the request filename stem.
3. Keep the request State Summary current.
4. Compute priority and Ready State before moving from planning to execution.
5. Resolve or explicitly except linked RFC-lite decision blockers.
6. Mirror active request state into `docs/roadmap/roadmap.md`.
7. Record meaningful outcomes in `docs/reports/changelog.md`.
8. Run the validation commands listed in `.project_ops/config.json`.
9. Close with doc sync and a post-mortem when the request is complete.
