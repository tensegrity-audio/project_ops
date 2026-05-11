# Agent Execution Contract

This document defines how an agent should execute a Project Ops request in a
step-by-step, resumable, and auditable way.

Project Ops is configurable, so this contract names default behavior. An
adopting project may tighten or relax gates in `.project_ops/config.json` or
`docs/governance/`, but the request artifact remains the durable source of
truth.

## Read First

Before changing files, the agent should read:

1. `docs/project_ops.md` in the adopter repo.
2. `.project_ops/config.json`.
3. The active request artifact, if one exists.
4. The configured roadmap and changelog paths.
5. The local prioritization policy if roadmap order is governed by one.
6. RFC-lite decisions linked by the request or roadmap entry.
7. Any architecture, governance, or validation docs listed in the request,
   config, roadmap, or local Project Ops contract.

If those docs disagree, prefer the project-local config for paths and prefer the
request artifact for current state. Record the conflict before proceeding.

## Non-Negotiable Rules

- Treat every meaningful request as a stateful artifact, not just a chat.
- Keep `Request ID` stable across request, roadmap, changelog, decision,
  handoff, and post-mortem artifacts.
- Do not expand scope beyond the request form, touch map, and approved plan.
- Do not guess missing intent, acceptance criteria, privacy posture, or
  validation requirements.
- Do not move into execution until Definition of Ready is met or an exception is recorded.
- Keep the State Summary current enough that another person or agent can resume
  from it.
- Keep request, roadmap, and changelog state aligned when the project requires
  parity.
- Verify command syntax before citing a command as validation evidence.
- Record validation that was not run, including the reason and waiver path.
- Stop when unknowns, blockers, destructive operations, privacy risk, or
  conflicting instructions appear.
- Preserve project-owned history. Do not rewrite or delete unrelated local
  files to make the process look clean.

## Execution Modes

| Mode | Meaning | Approval behavior |
| --- | --- | --- |
| Strict gated | Every phase and execution step pauses for human approval. | Use for high-risk, runtime, security, privacy, release, or multi-party work. |
| Assisted | The agent may batch low-risk work inside an approved plan, then reports the phase audit. | Use for ordinary implementation and docs work when the user has asked the agent to proceed. |
| Audit-only | The agent reads and reports gaps without changing adopter files. | Use for first adoption, migration, or CI dry runs. |
| Autonomous docs | The agent may update low-risk docs, templates, parity notes, and changelog breadcrumbs. | Use only when config/governance allows it and the touch map is narrow. |

When the mode is unclear, use Assisted for ordinary requested work and Strict
gated for risky or irreversible work. If the user explicitly asks for a plan,
review, or analysis only, do not move into execution.

## Request Lifecycle

Every request follows this lifecycle:

```text
INTAKE -> FORM -> ANALYSIS -> PLAN -> EXECUTION -> VALIDATION -> DOC_SYNC -> POST_MORTEM -> COMPLETE
```

Draft and locked are states within a phase. A phase is not complete until its
exit criteria are satisfied and the State Summary says what happens next.

| Phase | Agent job | Exit criteria |
| --- | --- | --- |
| `INTAKE` | Capture the user request, context, owner, and acceptance signal. | Request artifact exists and ambiguity is listed or resolved. |
| `FORM` | Define scope, non-goals, constraints, unknowns, and acceptance criteria. | Unknowns are empty or explicitly blocked with a next action. |
| `ANALYSIS` | Inspect affected docs, code, configs, schemas, interfaces, and active roadmap overlap. | Touch map, risks, alternatives, and complexity are recorded. |
| `PLAN` | Build an ordered task graph, validation contract, rollback path, and stop conditions. | Steps are reviewable and stay inside the touch map. |
| `EXECUTION` | Complete the approved steps without scope drift. | Step outcomes are recorded and the work slice is complete. |
| `VALIDATION` | Run required commands, manual checks, or record approved waivers. | Evidence is reproducible or the gap is explicit. |
| `DOC_SYNC` | Sync request, roadmap, changelog, architecture, governance, and related docs. | Durable docs match the actual work. |
| `POST_MORTEM` | Capture lessons, rework, residual risks, and follow-ups. | Lessons are actionable and linked to follow-up work when needed. |
| `COMPLETE` | Archive or close the request. | Completed path, roadmap, changelog, and final summary agree. |

## Phase Exit Audit

Run this audit before moving phases, pausing, handing off, or closing:

```markdown
Phase Exit Audit
- Phase requirements satisfied: Yes / No
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
```

If any required item is `No`, resolve it or record an explicit exception before
asking for approval or continuing.

## State Summary Contract

Every active request should start with:

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
- Priority Lane: <Fast-Track, Standard, Review, Deferred, or N/A>
- Ready State: <Not Ready, Ready, Blocked, Deferred>
- Ready Gate: <one-line blocker, exception, or met>
- Project Ops / Roadmap Updates (timestamped): <YYYY-MM-DD> - <state sync note>
- Resume From: Phase <phase>, State <state>, Next Action <command/artifact>
```

The matching roadmap entry should paste the same State Summary block when
roadmap parity is required. The changelog should include the request ID for
meaningful lifecycle or behavior changes.

## Phase Details

### INTAKE

Goal: capture intent without over-interpreting it.

Agent actions:

- Create or locate the request artifact.
- Record the user request and relevant context.
- Identify the likely owner and scope labels.
- Record initial priority hints and obvious readiness blockers.
- Add a roadmap placeholder if the project tracks active work there.
- Add a changelog intake note if the project requires changelog parity.
- Ask clarifying questions when acceptance, scope, privacy, or risk is unclear.

Do not analyze or implement yet unless the request is explicitly trivial and the
project allows lightweight execution.

### FORM

Goal: define the work clearly enough to analyze it.

Record:

- Problem statement.
- User value or operational value.
- Non-goals.
- Constraints and must-not-change areas.
- Acceptance criteria.
- Unknowns.
- Dependencies and related active requests.
- Linked RFC-lite decisions, or `N/A`.
- Priority inputs, due date or timing driver, and any override reason.
- Execution mode: Strict gated, Assisted, Audit-only, or Autonomous docs.

Unknowns must be empty, explicitly blocked, or accepted as risk before leaving
FORM.

### ANALYSIS

Goal: determine scope and surface area.

Record a touch map:

```markdown
Touch Map
- Code:
- Docs:
- Config / schemas:
- Tests / validation:
- Public interfaces:
- Privacy-sensitive paths:
- Related requests:
```

If analysis reveals new surfaces, update FORM and the touch map before
continuing. If the new surfaces change the request's intent, rewind to FORM.

### Complexity Derivation

Use counts instead of a purely subjective band when the work is non-trivial:

```text
Predicted = A + B + C + D + E
```

- `A`: work item count.
- `B`: artifact count.
- `C`: dependency or overlap count.
- `D`: validation count.
- `E`: coordination checkpoint count.

Use the score to size the plan:

| Predicted score | Planning expectation |
| --- | --- |
| 1-3 | At least two reviewable steps unless the change is tiny. |
| 4-6 | Three to five steps, with validation separated from implementation. |
| 7+ | Consider sub-requests, staged rollout, or RFC Lite before execution. |

During POST_MORTEM, compare predicted complexity with actual complexity and
record why they differed.

### Prioritization And Ready Gate

Use the local policy, or start from
[`templates/prioritization_policy.md`](../../templates/prioritization_policy.md),
to compute:

- score inputs,
- Priority Score,
- Priority Lane,
- due date or timing driver,
- Sort Key,
- override reason when policy order is intentionally changed,
- Ready State.

Definition of Ready is satisfied only when acceptance criteria, scope
boundaries, owner or decision path, dependencies, touch map, validation plan,
privacy posture, priority fields, stop conditions, and blockers are recorded or
explicitly excepted. If the Ready State is `Not Ready`, `Blocked`, or
`Deferred`, do not enter EXECUTION until the next action is resolved or the
project records an exception.

If a request is blocked by a decision, link the RFC-lite `Decision ID` in the
request's Definition of Ready and keep `Ready State` out of `Ready` until the
decision is accepted, rejected, superseded, or explicitly excepted.

### PLAN

Goal: produce an ordered, reviewable execution plan.

Record:

- Task graph with dependencies and owner.
- Per-step scope and files likely touched.
- Validation contract.
- Rollback or stop conditions.
- Approval or autonomy boundary.
- Ready gate status and any exceptions.

Each execution step should be independently reviewable. No step may exceed the
touch map without a rewind to ANALYSIS.

### EXECUTION

Goal: do the planned work without scope drift.

For each step, record:

```markdown
Step Outcome
- Action Taken:
- Result:
- Files Touched:
- Issues:
- Docs Updated:
- Validation Added or Deferred:
```

Rules:

- Keep changes inside the planned step.
- Update the State Summary after meaningful progress.
- Record command discoveries, failed attempts, and deviations.
- If a helper command has drifted from documentation, verify the current command
  and update the relevant docs or validation note.
- If the next step depends on user or hardware action, create a handoff or manual
  test request.

### VALIDATION

Goal: prove the request is correct enough to hand off or close.

Use validation commands from `.project_ops/config.json` plus any request-specific
checks. For each check, record:

- Exact command or manual procedure.
- Working directory.
- Result.
- Artifact path or output summary.
- Not-run reason or waiver.

Manual test request template:

```markdown
Manual Test Request
1. Scenario / Goal:
2. Commands or Steps to Run:
3. Expected Result:
4. Data to Capture:
5. Environment or Hardware Checklist:
   - Devices or services needed:
   - Ports, credentials, or fixtures:
   - Special modes or setup:
```

If validation cannot be run, record the gap instead of implying success.

### DOC_SYNC

Goal: make durable docs match the actual work.

Check:

- Request artifact State Summary and execution notes.
- Roadmap entry and request path.
- Changelog entry.
- RFC-lite decision links when decisions affected readiness, scope, or plan.
- Architecture docs for system behavior changes.
- Governance docs for process or decision rule changes.
- README, contributing docs, or examples when user-facing setup changed.
- Links to moved request docs.

For major work, include at least a text-first diagram or flow sketch when it
would make the change easier to resume.

### POST_MORTEM

Goal: capture useful lessons before they evaporate.

Record:

- Delivered and not delivered.
- Predicted versus actual complexity.
- Rework, failed assumptions, or validation gaps.
- What worked.
- What should change in Project Ops or the adopter overlay.
- Follow-up request IDs or roadmap entries.

If there were no issues, say so explicitly.

### COMPLETE

Goal: close the loop without losing context.

Before closing:

- Move the request artifact to the configured completed path when applicable.
- Ensure the roadmap points to the final request path.
- Ensure the changelog includes the request ID and final status.
- Ensure linked decision IDs still resolve or are recorded as historical.
- Record final validation status.
- Leave a final summary with rollback guidance and open follow-ups.

## Controlled Rewind

When execution hits a wall, do not continue ad hoc. Rewind to the minimum prior
phase that can repair the problem.

| Trigger | Rewind to |
| --- | --- |
| Intent, scope, or acceptance criteria changed. | `FORM` |
| Touch map, dependency, or complexity assumption was wrong. | `ANALYSIS` |
| Step order or validation plan was wrong. | `PLAN` |
| Local implementation defect inside the locked plan. | Stay in `EXECUTION` |

Record every rewind:

```markdown
Rewind Event
- Rewind ID: RW-###
- Triggered At: <YYYY-MM-DD>
- From: Phase <phase>, Step <step>
- To: Phase <phase>
- Reason Type: Scope shift | Analysis miss | Plan failure | Execution defect | External blocker
- What Changed:
- Approval:
- Impact:
- Next Checkpoint:
```

When a rewind is active, the State Summary status should say `Rewind Active` and
the Resume From field should identify the repaired phase and next action.

## Autonomy Boundaries

Agents may usually self-approve low-risk documentation parity, typo fixes,
template alignment, and audit-only reporting when the adopter allows it.

Escalate to RFC Lite or human approval when:

- Multiple viable approaches have meaningful tradeoffs.
- Runtime behavior, public API, UX semantics, privacy, or security posture may
  change.
- Work is destructive or hard to reverse.
- The plan would cross the touch map.
- Validation requires a waiver.
- Two agents or contributors conflict on implementation direction.

Any autonomous decision should be logged in the request artifact with why it was
safe, which files changed, and how to roll back.

## Multi-Agent Coordination

Use one owner agent per request artifact. Parallel agents may work only on
bounded subtasks with explicit ownership.

Every delegated or parallel task should name:

- Owned files or module boundary.
- Inputs and expected output.
- Validation responsibility.
- Write conflicts to avoid.
- Handoff format.

The owner agent is responsible for final synthesis, request state, roadmap
parity, changelog parity, and closeout.
