# Execution Process

Project Ops gives a project a durable operating loop. The loop is intentionally simple: write down the request, keep state current, validate before closing, and leave enough context for the next person or agent to resume.

The loop connects the subsystems directly: request artifacts hold the active
state, roadmap entries make the state visible in the plan, changelog entries
record durable outcomes, the design alignment log explains why the project is
built this way, and validation commands prove the repository is ready to hand
off or close. The shared Request ID from the
[Artifact Contract](../concepts/artifact_contract.md) is the thread through
all of those artifacts.

For the fuller agent-facing protocol, including approval modes, phase gates,
complexity derivation, priority scoring, Definition of Ready gates, controlled
rewinds, manual validation requests, autonomy boundaries, and multi-agent
ownership, read
[Agent Execution Contract](agent_execution_contract.md).

## Phases

| Phase | Purpose | Exit signal |
| --- | --- | --- |
| `INTAKE` | Capture the request and context. | The request artifact exists and has an acceptance signal. |
| `FORM` | Shape the problem and constraints. | The work has clear scope, non-goals, and initial priority inputs. |
| `ANALYSIS` | Inspect affected files, docs, systems, design principles, and risks. | The touch map, risks, and design-alignment impact are explicit. |
| `PLAN` | Choose steps, validation, and stop conditions. | The task graph is executable and the Ready State is resolved. |
| `EXECUTION` | Make the change. | The implementation or documentation slice is complete. |
| `VALIDATION` | Run checks and record results. | Pass/fail/not-run evidence is recorded. |
| `DOC_SYNC` | Update roadmap, changelog, design alignment log, and related docs. | The durable docs match the work. |
| `POST_MORTEM` | Capture lessons, residual risks, and follow-ups. | The closeout notes are useful. |
| `COMPLETE` | Archive or close the request. | The request can be resumed historically without guessing. |

## Operating Loop

1. Create a request from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.
2. Set the Request ID to match the request filename stem.
3. Fill in the State Summary first.
4. Check the roadmap for overlap before starting.
5. Compute the priority score, lane, sort key, and Ready State.
6. Link RFC-lite decisions if any unresolved tradeoff blocks readiness.
7. Fill the request's Design Alignment section with affected principles, systems, elements, processes, and explanation impact.
8. Work the task graph in small slices only after the Ready gate is satisfied or excepted.
9. Record meaningful execution notes as the work changes.
10. Run the validation commands in `.project_ops/config.json`.
11. Update the roadmap, changelog, and design alignment log before closeout.
12. Use `templates/phase_exit_audit.md` before moving phases or handing off.
13. Use `templates/handoff.md` when another person or agent needs to resume.
14. Use `templates/post_mortem.md` when the work closes or reveals a durable lesson.

## Prioritization And Readiness

Use `templates/prioritization_policy.md` as the starter for
`docs/governance/prioritization_policy.md`. The request artifact should record
the numeric score inputs, derived Priority Score, Priority Lane, due date or
timing driver, Sort Key, and any override.

Definition of Ready is the gate between planning and execution. A request is
Ready only when acceptance criteria, scope boundaries, owner or decision path,
dependencies, touch map, design and teaching impact, validation plan, privacy
posture, priority fields, stop conditions, and blockers are recorded or
explicitly excepted.
If a decision is still draft, proposed, pending, or blocking, the request stays
Not Ready or Blocked until the decision is resolved or deliberately excepted.

## Design Alignment

Use `docs/architecture/design_alignment_log.md` as the human-readable rationale
surface. The request artifact records the local Design Alignment checkpoint; the
log keeps the project-wide version that any reader can follow later.

Update it when work changes:

- guiding principles,
- major systems, elements, tools, libraries, patterns, or workflows,
- architecture or process decisions that explain why the project is shaped this
  way,
- plain-language notes or common misconceptions.

## Step Discipline

Each execution step should be small enough to review on its own:

1. Confirm the step is inside the locked touch map.
2. Make the change.
3. Record the files touched and outcome in the request artifact.
4. Run or defer the relevant validation with an explicit reason.
5. Recompute priority and Ready State if scope, blockers, timing, or dependencies changed.
6. Update State Summary, roadmap, changelog, and design alignment notes if meaningful state changed.
7. Run the phase-exit audit before moving on or handing off.

## Required Sync Points

| Event | Update |
| --- | --- |
| Request starts | request artifact, roadmap entry |
| Scope changes | request State Summary, roadmap overlap review |
| Priority or readiness changes | request Prioritization and Definition of Ready sections, roadmap queue |
| Decision blocks or unlocks work | request Decision Links, RFC-lite decision, roadmap Ready Gate |
| Meaningful behavior changes | changelog, validation plan, related docs |
| Design principle, system, element, process, or explanation changes | request Design Alignment section, `docs/architecture/design_alignment_log.md`, related architecture docs |
| Validation runs | request Validation section |
| Work pauses | request Resume From field, optional handoff |
| Work completes | roadmap status, changelog, post-mortem |

## Audit-Only First

For a new adopter, run Project Ops in audit-only mode before adding CI enforcement. Audit-only mode should report missing files, risky config, and missing validation commands without rewriting the repo.

```powershell
python <path-to-project_ops>\tools\project_ops_audit.py --repo .
```

When the audit is quiet, the project can decide whether to add assisted state-machine tooling, CI checks, or stricter roadmap/changelog parity.
