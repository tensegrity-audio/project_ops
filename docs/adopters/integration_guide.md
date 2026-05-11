# Integration Guide

Project Ops integrates with another codebase as a repository-local operating
layer. It does not need to become a runtime dependency. An adopter can copy the
starter files, point `.project_ops/config.json` at local paths, and run the
read-only audit tools from a Project Ops checkout, submodule, vendored copy, or
future package.

## Integration Model

```text
Project Ops templates
  -> starter adopter docs
  -> local config
  -> request, roadmap, changelog, governance, and architecture surfaces
  -> read-only audits
  -> contributor or agent closeout evidence
```

The important handoff is the config file. Project Ops owns reusable templates,
schemas, and validators. The adopter owns the actual paths, decisions, roadmap,
history, and validation commands.

## Subsystem Handshakes

| Subsystem | Project Ops provides | Adopter provides | Integration contract |
| --- | --- | --- | --- |
| Entry docs | README and adopter guidance. | Local `README.md` and `docs/project_ops.md`. | A contributor can find the operating files before changing code. |
| Config | `schemas/project_config.schema.json` and generated defaults. | `.project_ops/config.json`. | Tools discover local paths, privacy posture, scopes, validation commands, and bootstrap expectations without hardcoded assumptions. |
| Templates | Copyable Markdown and baseline files in `templates/`. | Local copies under `docs/templates/` when useful. | Human artifacts keep a stable shape while staying editable by the adopter. |
| Requests | `templates/request.md` and optional request-state schema. | Request docs under the configured in-progress or completed paths. | The State Summary gives humans and tools the same phase, status, resume point, and risk picture. |
| Roadmap | A starter roadmap template, prioritization fields, and request parity rules. | The actual project roadmap. | Active work has a visible index, computable sort order, and links back to request docs. |
| Changelog | A starter changelog template and changelog requirement flag. | The actual change history. | Meaningful outcomes leave a durable breadcrumb for releases and handoffs. |
| Architecture | Starter architecture index guidance. | Project-specific maps, interfaces, and decisions. | System knowledge stays in the adopter repo, not in Project Ops. |
| Governance | Starter governance index guidance and `templates/prioritization_policy.md`. | Local ownership, approval, priority, readiness, privacy, and validation rules. | The operating policy is explicit instead of implied. |
| Audits | Read-only structure and request parity checks. | Files and config for the tools to inspect. | Adoption can be verified without rewriting project-owned files. |
| Examples and tests | Synthetic fixtures and regression tests. | Real usage feedback from adopter repos. | Project Ops can evolve while keeping the public integration surface understandable. |

## Existing Codebase Adoption

1. Read the [Repo Component Map](../concepts/repo_component_map.md) to identify
   the reusable Project Ops pieces.
2. Decide whether the adopter will use Project Ops from a sibling checkout,
   submodule, vendored copy, or future packaged install.
3. Create or adapt `.project_ops/config.json` from
   `examples/project_config.minimal.json`.
4. Map config paths to the adopter's real docs instead of moving files just to
   match Project Ops defaults.
5. Add `docs/project_ops.md` as the local bridge document for contributors and
   agents.
6. Link the local bridge document to the Project Ops Agent Execution Contract
   or keep a local copy if the adopter needs stricter rules.
7. Add or map the request template, roadmap, changelog, governance,
   prioritization policy, and architecture surfaces.
8. Run `tools/project_ops_audit.py --repo <adopter>` and fix missing required
   files or intentional config mistakes.
9. Create one request artifact for the integration work itself, then run
   `tools/project_ops_request_audit.py` once roadmap and changelog parity exist.
10. Add audit commands to local validation or CI only after the read-only checks
   are useful and quiet enough for the team.

## Blank Repo Adoption

For a fresh repository, start with bootstrap:

```powershell
python tools\project_ops_bootstrap.py --repo C:\path\to\project --project-name "Project Name"
python tools\project_ops_bootstrap.py --repo C:\path\to\project --project-name "Project Name" --apply
```

The first command explains what would be created. The second creates only
missing files. Existing project-owned files are skipped.

## Integration Checklist

- `.project_ops/config.json` points to real repo-relative paths.
- `docs/project_ops.md` explains the local operating loop.
- Agents know whether to follow the upstream Agent Execution Contract or a
  stricter local copy.
- Request artifacts, roadmap entries, and changelog entries can reference one
  another without guesswork.
- The roadmap can be sorted by Ready State, Priority Lane, Priority Score, and
  due date or timing driver.
- `validation.commands` names the checks a contributor or agent should run.
- Private or local-only paths are listed in `privacy.privateHistoryPaths`.
- Architecture and governance docs describe the adopter's own system and
  decision rules.
- Project Ops audits run read-only before any CI gate depends on them.

When in doubt, keep the adopter's real project truth local and use Project Ops
only for the reusable structure that helps people find, validate, and resume
that truth.
