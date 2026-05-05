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
  docs/
    README.md
    concepts/
      project_ops_model.md
    adopters/
      getting_started.md
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

1. Read [Getting Started](docs/adopters/getting_started.md).
2. Review the [Project Admin Baseline](templates/project_admin_baseline.md).
3. Copy or adapt [project_config.minimal.json](examples/project_config.minimal.json).
4. Read the [Execution Process](docs/adopters/execution_process.md).
5. Use [request.md](templates/request.md) for the first durable request.
6. Run an audit-only check with `tools/project_ops_audit.py`.
7. Audit request/roadmap/changelog parity with `tools/project_ops_request_audit.py`.

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
- RFC Lite template
- post-mortem template
- handoff template
- project config schema
- audit-only checks
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
