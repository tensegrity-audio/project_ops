# Roadmap

This roadmap is the durable index for active, completed, and planned work.

## Roadmap Generation Contract

- Use request artifacts as the source of truth for phase, status, priority, readiness, validation, and resume state.
- Keep each request's `Request ID` stable and reuse it in roadmap entries, changelog entries, RFC-lite decisions, handoffs, and postmortems.
- Copy the request State Summary into each active roadmap entry when roadmap parity is required.
- Derive roadmap order from the configured prioritization policy, not from chat order or file creation time.
- Recompute priority and readiness when scope, dependencies, due dates, validation, or blockers change.
- Keep `Not Ready`, `Blocked`, and `Deferred` work visible so missing inputs do not get rediscovered later.

Default sort order:

1. `Ready` items before `Not Ready`, `Blocked`, or `Deferred` items.
2. Priority Lane: `Fast-Track`, then `Standard`, then `Review`, then `Deferred`.
3. Higher Priority Score before lower Priority Score.
4. Earlier due date or timing driver before later or `N/A`.
5. Older request creation date before newer request creation date.

Policy template: copy `templates/prioritization_policy.md` to
`docs/governance/prioritization_policy.md` or link the local equivalent.

## Priority Queue

| Rank | Request | Request ID | Ready State | Priority Lane | Priority Score | Due Date / Driver | Owner | Next Step | Request Doc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | <title> | <request_id> | <Ready, Not Ready, Blocked, Deferred> | <Fast-Track, Standard, Review, Deferred> | <integer or N/A> | <YYYY-MM-DD, event, or N/A> | <owner> | <next action> | <path> |

## In Progress

No active requests yet.

## Completed

No completed requests yet.

## Backlog

- Create the first request from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.
- Add validation commands to `.project_ops/config.json` once they exist.
