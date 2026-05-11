# Prioritization Policy Template

Use this template as `docs/governance/prioritization_policy.md` or the local
equivalent. The goal is to make roadmap order explainable and computable while
leaving product judgment with the adopting project.

## Policy Metadata

- Policy Owner: <person, team, or role>
- Applies To: <roadmap, requests, releases, maintenance, or custom scope>
- Review Cadence: <weekly, per milestone, before release, or custom>
- Last Reviewed: <YYYY-MM-DD or N/A>

## Scoring Contract

Use integer values from 0 to 5. Use `0` for unknown only when the unknown is
listed in the request artifact.

```text
Priority Score =
  Impact
+ Urgency
+ Risk Reduction
+ Dependency Unlock
+ Rework Reduction
+ Confidence
- Effort
- Coordination Cost
```

| Field | Type | Scoring guide |
| --- | --- | --- |
| Impact | 0-5 | User, operational, compliance, or project value. |
| Urgency | 0-5 | Time sensitivity, external date pressure, active breakage, or release need. |
| Risk Reduction | 0-5 | Amount of technical, product, security, privacy, or delivery risk removed. |
| Dependency Unlock | 0-5 | Amount of downstream work unblocked by completing this request. |
| Rework Reduction | 0-5 | Likelihood this request prevents expensive rework or duplicated effort. |
| Confidence | 0-5 | Evidence quality, clarity of acceptance criteria, and certainty of approach. |
| Effort | 0-5 | Estimated implementation, documentation, validation, and review effort. |
| Coordination Cost | 0-5 | Number of owners, approvals, releases, or external dependencies involved. |

## Priority Lanes

| Lane | Default rule | Handling |
| --- | --- | --- |
| Fast-Track | Score >= 14 and Ready State is `Ready`. | Pull next unless a policy override says otherwise. |
| Standard | Score 7-13 and Ready State is `Ready`. | Plan in normal roadmap order. |
| Review | Score 1-6, high uncertainty, or missing policy input. | Clarify, split, or route through a decision process. |
| Deferred | Score <= 0, blocked, intentionally paused, or not currently valuable. | Keep visible, but do not schedule execution. |

Policy overrides are allowed, but record the override reason, owner, and date in
the request artifact and roadmap entry.

## Definition Of Ready

A request is ready for execution only when every required item is satisfied or
has an explicit exception.

| Ready item | Required evidence |
| --- | --- |
| Acceptance criteria | Testable criteria or a concrete acceptance signal. |
| Scope boundaries | In-scope, non-goals, allowed-to-change, and must-not-change surfaces. |
| Ownership | Owner, reviewer, or decision path. |
| Dependencies and overlap | Related active requests, blocked work, duplicate risk, and merge/split decision. |
| Touch map | Expected docs, code, config, schema, validation, and public interface surfaces. |
| Validation plan | Commands, manual checks, or waiver path. |
| Privacy and safety review | Public/private boundary and sensitive paths checked. |
| Priority contract | Score inputs, derived score, lane, due date or `N/A`, and override if any. |
| Stop conditions | Rollback, pause, escalation, or rewind triggers. |
| Unknowns and blockers | Empty, accepted as risk, or assigned a next action. |

Ready State values:

- `Ready`: all required items are satisfied or explicitly excepted.
- `Not Ready`: one or more required items need intake, form, or analysis work.
- `Blocked`: execution depends on an unavailable input, decision, owner, or external event.
- `Deferred`: the project intentionally chooses not to schedule the request now.

## Review Triggers

Recompute the score and Ready State:

- when a request is created,
- before it leaves FORM,
- before PLAN starts,
- when scope, dependencies, or validation change,
- when a blocker appears or clears,
- before roadmap closeout.

