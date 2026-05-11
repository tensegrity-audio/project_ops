# Project Ops

Project Ops is a reusable project-operations framework for keeping repositories understandable, maintainable, and ready for human/agent collaboration.

It is for maintainers bootstrapping project governance, documentation structure, and request workflows in any repo.

It provides a shared playbook for:

- fresh-project administrative setup,
- must-have documentation structure,
- request intake and durable request artifacts,
- roadmap and changelog discipline,
- RFC Lite decision packets,
- handoff and multi-agent coordination,
- phase-exit audits,
- validation/checklist habits,
- and project-local configuration.

## Status

This repository contains generic seed material for project operations. It should not include adopter-specific roadmap history, reports, validation evidence, or product architecture.

The first goal is a small, useful bootstrap kit:

```text
project_ops/
  README.md
  LICENSE
  CONTRIBUTING.md
  CHANGELOG.md
  SECURITY.md
  .gitignore
  templates/
    project_admin_baseline.md
    bootstrap_manifest.md
    project_ops_contract.md
    architecture_readme.md
    governance_readme.md
    roadmap.md
    changelog.md
    request.md
    roadmap_entry.md
    changelog_entry.md
    prioritization_policy.md
    rfc_lite.md
    post_mortem.md
    phase_exit_audit.md
    handoff.md
  schemas/
    project_config.schema.json
    request_state.schema.json
  tools/
    project_ops_bootstrap.py
    project_ops_audit.py
    project_ops_request_audit.py
    project_ops_roadmap.py
  docs/
    README.md
    concepts/
      project_ops_model.md
      artifact_contract.md
    adopters/
      getting_started.md
      integration_guide.md
      agent_execution_contract.md
      configuration.md
      execution_process.md
  examples/
    project_config.minimal.json
    request_state.sidecar.json
    minimal_project/
      README.md
      .project_ops/
        config.json
      docs/
        project_ops.md
        roadmap/
        reports/
        architecture/
        governance/
```

## Start Here

1. Read the [Repo Component Map](docs/concepts/repo_component_map.md).
2. Read the [Artifact Contract](docs/concepts/artifact_contract.md).
3. Read the [Integration Guide](docs/adopters/integration_guide.md).
4. Read the [Agent Execution Contract](docs/adopters/agent_execution_contract.md).
5. Read [Getting Started](docs/adopters/getting_started.md).
6. Review the [Project Admin Baseline](templates/project_admin_baseline.md).
7. Copy or adapt [project_config.minimal.json](examples/project_config.minimal.json).
8. Read the [Execution Process](docs/adopters/execution_process.md).
9. Use [request.md](templates/request.md) for the first durable request.
10. Run an audit-only check with `tools/project_ops_audit.py`.
11. Audit request/roadmap/changelog parity with `tools/project_ops_request_audit.py`.
12. Check all request/roadmap parity with `tools/project_ops_roadmap.py`.

## Core Ideas

Project Ops is not a project manager and not a replacement for the work itself. It is the reusable administrative layer around the work.

Each adopting project keeps its own roadmap, reports, architecture, product decisions, validation evidence, and private history.

Project Ops provides the common structure:

```text
Project Ops
  -> templates, schemas, validators, bootstrap docs, workflow rules

Adopting project
  -> local config, roadmap, changelog, request history, product docs
```

## How The Subsystems Connect

Project Ops is easiest to integrate when each subsystem has one clear handoff:

| Subsystem | Handoff |
| --- | --- |
| `templates/` | Seed the files an adopter can copy, customize, or generate. |
| `schemas/` | Define the config and optional request-state contracts that tools can trust. |
| `.project_ops/config.json` in the adopter | Maps reusable Project Ops behavior to local paths, scope labels, privacy rules, and validation commands. |
| `docs/project_ops.md` in the adopter | Gives contributors and agents the local operating loop. |
| Artifact contract | Defines the stable Request IDs, Decision IDs, and State Summary fields that tie docs and tools together. |
| Request, roadmap, changelog, and RFC-lite docs | Keep task state, planning, decisions, and history synchronized enough to resume work. |
| `tools/` | Reads config and docs in audit-only mode so adoption can be checked without rewriting project files. |
| `examples/` and `tests/` | Show and protect the public integration surface. |

For a step-by-step integration path, read the [Integration Guide](docs/adopters/integration_guide.md).

## Bootstrap Promise

A fresh project should be able to use Project Ops to answer:

- What files should this repo have on day one?
- Which docs are required for this project type?
- Where do requests, roadmap entries, reports, and decisions live?
- What is public, private, or internal?
- What validation proves the project is healthy?
- What should contributors or agents read before changing things?

## Initial Scope

The first public version should focus on:

- getting-started adopter docs
- configuration guidance
- a minimal synthetic adopter example
- Project Ops concept docs
- `project_admin_baseline.md`
- bootstrap manifest template
- starter docs templates
- request artifact template
- roadmap entry template
- changelog entry template
- prioritization policy template
- RFC Lite template
- post-mortem template
- handoff template
- project config schema
- audit-only checks
- readiness and roadmap parity checks
- dry-run-first bootstrap behavior

Automation should stay boring and inspectable. The first release should be understandable as plain Markdown, with tools that report or create only the baseline structure.

## Bootstrap A Blank Repo

Dry-run first:

```powershell
python tools\project_ops_bootstrap.py --repo C:\path\to\new-project --project-name "New Project"
```

Apply only after reviewing the plan:

```powershell
python tools\project_ops_bootstrap.py --repo C:\path\to\new-project --project-name "New Project" --apply
```

Audit without rewriting:

```powershell
python tools\project_ops_audit.py --repo C:\path\to\new-project
```
