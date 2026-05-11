# Request Artifact Template

State Summary
- Request ID: <request_id>
- Phase: INTAKE
- Status: Draft
- Steps Complete: 0 / 0
- Progress: <one-sentence current state>
- Last Step Outcome: <date> - <what just happened>
- Next Step: <specific next action>
- Dependencies / Overlap: <related docs, requests, code areas, or N/A>
- Primary Scope: <project-config scope label>
- Secondary Scopes: <project-config scope labels or N/A>
- Blocking Issues / Unknowns: <none or list>
- Impact / Priority Notes: <why this matters or N/A>
- Priority Score: <integer or N/A>
- Priority Lane: <Fast-Track, Standard, Review, Deferred, or N/A>
- Ready State: <Not Ready, Ready, Blocked, Deferred>
- Ready Gate: <one-line blocker, exception, or met>
- Project Ops / Roadmap Updates (timestamped): <YYYY-MM-DD> - <state sync note>
- Resume From: Phase <phase>, State <state>, Next Action <command/artifact>

## Milestone Synthesis

- Milestone ID: <id>
- Milestone Name: <short name>
- Milestone Type: <Roadmap Phase | Contract Lock | Validation Gate | Custom>
- Source Requests: <request_id list or N/A>
- Outcome Statement (Done When): <testable outcome>
- KPI / Success Signal: <metric, threshold, or N/A>
- Target Window: <date, sprint, or N/A>
- Dependency Gates: <gates or N/A>
- Contract Surfaces: <docs, APIs, schemas, protocols, or N/A>
- Risk Posture: <low, medium, high and rationale>
- Goal: <outcome>
- Non-Goals: <what is intentionally out of scope>
- Owner: <human, agent, team, or N/A>

## Roadmap Overlap Review

- Existing roadmap entries checked: <paths or headings>
- Related active requests: <ids or N/A>
- Duplicate risk: <low, medium, high>
- Merge / split decision: <decision>
- Priority conflict: <higher-priority work displaced, or N/A>
- Decision Links: <decision_id list or N/A>

## Prioritization

- Policy Source: <docs/governance/prioritization_policy.md or N/A>
- Priority Score: <integer computed from score inputs>
- Priority Lane: <Fast-Track, Standard, Review, Deferred>
- Due Date / Timing Driver: <YYYY-MM-DD, event, or N/A>
- Sort Key: <lane>:<score>:<due-date-or-none>:<request_id>
- Override: <none, or owner/date/reason>

| Score Input | Value | Rationale |
| --- | --- | --- |
| Impact | <0-5> | <why> |
| Urgency | <0-5> | <why> |
| Risk Reduction | <0-5> | <why> |
| Dependency Unlock | <0-5> | <why> |
| Rework Reduction | <0-5> | <why> |
| Confidence | <0-5> | <why> |
| Effort | <0-5> | <why> |
| Coordination Cost | <0-5> | <why> |

## Definition Of Ready

- Ready State: <Not Ready, Ready, Blocked, Deferred>
- Ready Date: <YYYY-MM-DD or N/A>
- Ready Owner: <owner, team, agent, or N/A>
- Ready Exceptions: <none, or owner/date/reason>
- Decision Links: <accepted decision IDs, blocked-by decision IDs, or N/A>

| Ready Item | Evidence | Status |
| --- | --- | --- |
| Acceptance criteria are testable | <criteria, signal, or path> | <Met, Missing, Exception, N/A> |
| Scope boundaries are explicit | <in-scope, non-goals, allowed/must-not-change> | <Met, Missing, Exception, N/A> |
| Ownership or decision path is known | <owner/reviewer/path> | <Met, Missing, Exception, N/A> |
| Dependencies and overlap are checked | <request ids, docs, code areas, or N/A> | <Met, Missing, Exception, N/A> |
| Required decisions are resolved | <RFC Lite decision IDs, statuses, or N/A> | <Met, Missing, Exception, N/A> |
| Touch map is bounded | <files, docs, systems, or N/A> | <Met, Missing, Exception, N/A> |
| Validation plan is named | <commands, manual checks, or waiver path> | <Met, Missing, Exception, N/A> |
| Privacy and safety posture is checked | <public/private notes or N/A> | <Met, Missing, Exception, N/A> |
| Priority score and lane are computed | <score, lane, due date, override> | <Met, Missing, Exception, N/A> |
| Stop conditions are clear | <rollback, pause, escalation, or rewind triggers> | <Met, Missing, Exception, N/A> |
| Unknowns and blockers have next actions | <none, accepted risk, or next action> | <Met, Missing, Exception, N/A> |

## Complexity

- Level: <low, medium, high>
- Predicted Count: <A+B+C+D+E or N/A>
- Count Drivers: <work items, artifacts, dependencies, validation, coordination>
- Drivers: <risk, scope, validation, dependencies>
- Confidence: <low, medium, high>

## Intake

- User Request: <verbatim or summarized request>
- Context: <relevant background>
- Acceptance Signal: <how we will know this is done>

## Form

- Problem Statement: <what needs to change>
- User / Operational Value: <why it matters>
- Change Type: <feature, bugfix, refactor, investigation, docs-only>
- Execution Mode: <Strict gated, Assisted, Audit-only, Autonomous docs>
- Acceptance Criteria: <testable criteria>
- Constraints: <technical, product, privacy, or timing constraints>
- Must Not Change: <protected behavior, files, APIs, or N/A>
- Allowed To Change: <surfaces or N/A>
- Inputs Needed: <unknowns or N/A>

## Analysis

- Touch Map: <files, docs, tools, systems>
- Risks: <risks or N/A>
- Alternatives Considered: <alternatives or N/A>

## Plan

- Steps: <ordered implementation or documentation steps>
- Ready Gate Before Execution: <Ready State plus exceptions or blockers>
- Validation Plan: <commands, reviews, manual checks>
- Rollback / Stop Conditions: <conditions>

## Task Graph

| Task ID | Description | Module Surface | Depends On | Owner | Status | Priority Lane | Priority Score | Ready State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <TASK-1> | <description> | <docs, code, config, validation> | <task id or N/A> | <owner> | Planned | <Fast-Track, Standard, Review, Deferred> | <integer or N/A> | <Ready, Not Ready, Blocked, Deferred> |

## Execution

- <timestamp> - <what changed>

## Validation

- Passed: <commands or checks>
- Not Run: <commands and reason>
- Manual Evidence: <summary or N/A>
- Waivers: <approval path and reason or N/A>

## Doc Sync

- Roadmap updated: Yes / No / N/A
- Changelog updated: Yes / No / N/A
- Related docs updated: Yes / No / N/A
- Links checked: Yes / No / N/A

## Phase Exit Audit

- Phase requirements satisfied: Yes / No
- Definition of Ready satisfied before execution: Yes / No / N/A
- Request artifact updated: Yes / No / N/A
- State Summary updated: Yes / No / N/A
- Roadmap entry updated: Yes / No / N/A
- Changelog entry updated: Yes / No / N/A
- Related docs updated: Yes / No / N/A
- Validation evidence recorded: Yes / No / N/A
- Handoff context current: Yes / No / N/A
- Unknowns empty: Yes / No
- Blocking issues found: <None or list>
- Next phase ready: Yes / No

## Rewind Events

- <request_id-RW-### or N/A>

## Post-Mortem

Use `templates/post_mortem.md` when the request closes.

## Notes

- <freeform notes>

## Clarifications

- <question/answer history or N/A>
