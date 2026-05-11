# Project Ops Model

Project Ops separates reusable operating structure from project-specific history.

## What Project Ops Owns

Project Ops owns reusable patterns:

- administrative baseline files,
- project config schema,
- request artifact template,
- roadmap entry template,
- prioritization policy template,
- changelog entry template,
- RFC Lite decision template,
- post-mortem template,
- handoff template,
- phase-exit audit template,
- public/private boundary rules,
- dry-run-first extraction habits,
- audit-only readiness checks,
- dry-run-first bootstrap behavior,
- and starter docs for blank repositories.

## What Adopters Own

Each adopter owns its actual work:

- product architecture,
- roadmap,
- changelog,
- request history,
- validation evidence,
- release notes,
- private reports,
- local scope labels,
- and project-specific governance overlays.

## The Boundary

The boundary is simple:

```text
Project Ops
  -> how to structure, validate, and operate project artifacts

Adopter repo
  -> the actual artifacts and project decisions
```

If a file only makes sense for one project, it belongs with that project.

If a file helps many projects create, validate, or maintain their own administrative structure, it may belong in Project Ops.

For a component-level view of this repository, see [Repo Component Map](repo_component_map.md).
For the ID and state fields that connect request, roadmap, changelog,
decision, handoff, and post-mortem artifacts, see [Artifact Contract](artifact_contract.md).

## The Integration Handshake

Project Ops connects to an adopter repo through a small set of explicit
contracts:

1. Templates seed human-readable operating artifacts.
2. `.project_ops/config.json` maps those artifacts to local paths and policies.
3. Request docs carry current task state.
4. Roadmap and changelog docs mirror planning and history.
5. Audit tools read the config and artifacts without rewriting them.

That handshake keeps Project Ops reusable while letting each adopter keep its
own architecture, governance, validation commands, and project history.

## Naming

Project Ops is the public umbrella name.

Request lifecycle mechanics can still use phrases like request state, phase exit, audit, and handoff, but public seed files should lead with Project Ops terminology.

Older adopter records may refer to `docops.md`. In Project Ops, the reusable
replacement surfaces are [Agent Execution Contract](../adopters/agent_execution_contract.md),
[Execution Process](../adopters/execution_process.md), and the local
`docs/project_ops.md` generated from `templates/project_ops_contract.md`.

## Request State Sidecars

The Markdown request template is the human-facing artifact. The request-state schema describes an optional machine-readable sidecar for tools.

Use `templates/request.md` for the durable document and `schemas/request_state.schema.json` for a JSON state file when automation needs phase, state, status, and history in a structured form.

See `examples/request_state.sidecar.json` for a synthetic sidecar example.

## Blank-Repo Bootstrap

Project Ops can start from an empty repository in two safe steps:

```powershell
python tools\project_ops_bootstrap.py --repo <repo> --project-name "<Project>"
python tools\project_ops_bootstrap.py --repo <repo> --project-name "<Project>" --apply
```

The first command prints a create/skip plan. The second command creates only missing files and never overwrites existing project-owned files.

After bootstrap, run:

```powershell
python tools\project_ops_audit.py --repo <repo>
```

Audit mode is read-only. It is the first reusable behavior every adopter should be able to trust.
