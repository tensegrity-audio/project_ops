# Artifact Contract

Project Ops connects its subsystems through stable IDs and shared state blocks.
The goal is simple: a person or agent should be able to follow one request from
intake through roadmap priority, decision records, validation evidence,
changelog history, handoff, post-mortem, and closeout.

## Stable IDs

Use stable, lowercase, filename-safe IDs:

```text
request_id: project-bootstrap
decision_id: project-bootstrap-architecture
task_id: project-bootstrap-T1
rewind_id: project-bootstrap-RW-001
```

Recommended pattern:

- `request_id`: matches the request artifact filename stem.
- `decision_id`: starts with the related `request_id` when a decision blocks or
  unlocks that request.
- `task_id`: starts with the related `request_id` or milestone ID.
- `rewind_id`: starts with the related `request_id`.

Do not rename IDs for presentation. Change titles freely, but keep IDs stable.

## Shared State Summary

The State Summary is the cross-subsystem state contract. Request artifacts and
roadmap entries should carry the same State Summary when roadmap parity is
required.

Required fields:

```markdown
State Summary
- Request ID: <request_id>
- Phase: <current phase>
- Status: <Draft | In Progress | Blocked | Planned | Complete | Rewind Active>
- Steps Complete: <complete> / <total>
- Progress: <one-sentence current state>
- Last Step Outcome: <YYYY-MM-DD> - <what just happened>
- Next Step: <specific next action>
- Dependencies / Overlap: <related docs, requests, code areas, or N/A>
- Primary Scope: <project-config scope label>
- Secondary Scopes: <project-config scope labels or N/A>
- Blocking Issues / Unknowns: <none or list>
- Impact / Priority Notes: <why this matters or N/A>
- Priority Score: <integer or N/A>
- Priority Lane: <Fast-Track | Standard | Review | Deferred | N/A>
- Ready State: <Not Ready | Ready | Blocked | Deferred>
- Ready Gate: <one-line blocker, exception, or met>
- Project Ops / Roadmap Updates (timestamped): <YYYY-MM-DD> - <state sync note>
- Resume From: Phase <phase>, State <state>, Next Action <command/artifact>
```

## Traceability Chain

| Artifact | Required link back |
| --- | --- |
| Request artifact | `Request ID` in State Summary. |
| Roadmap entry | Same State Summary plus `Request Doc`. |
| Changelog entry | `Request ID`, request doc path, and roadmap entry reference. |
| RFC Lite decision | `Decision ID`, related `Request IDs`, and whether it blocks readiness. |
| Handoff | `Request ID`, current phase/state, files touched, validation, and resume action. |
| Post-mortem | `Request ID`, outcome, lessons, and follow-up IDs. |

## RFC Lite Readiness Link

RFC-lite is the decision packet for unresolved tradeoffs. If a request is not
ready because a decision is open, make that explicit:

```markdown
- Ready Gate: blocked by RFC <decision_id>
- Decision Links: <decision_id or N/A>
```

The request can enter `EXECUTION` only when decision blockers are accepted,
rejected, superseded, or explicitly excepted in the Definition of Ready.

## Audit Expectations

Project Ops tools should prefer IDs over fuzzy text when possible:

- request audits should check that `Request ID` exists and matches the request
  filename stem;
- roadmap checks should compare State Summary fields across request and roadmap;
- changelog checks should look for the stable `Request ID`;
- future decision checks should use `Decision ID` and `Request ID` links rather
  than searching for titles.
