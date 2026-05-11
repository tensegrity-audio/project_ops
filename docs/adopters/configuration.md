# Configuration

Project Ops is configured per adopter. The framework should not hardcode project paths, scope labels, privacy rules, or validation commands.

Use `.project_ops/config.json` in the adopter repo. A standalone example lives at `examples/project_config.minimal.json`.

The config is the adapter between Project Ops and the adopter. Templates and
docs can use defaults, but tools should discover the real roadmap, request,
changelog, governance, privacy, and validation surfaces from this file.

## Minimal Shape

```json
{
  "$schema": "../../schemas/project_config.schema.json",
  "project": {
    "id": "example-project",
    "name": "Example Project",
    "role": "example-adopter"
  },
  "paths": {
    "roadmap": "docs/roadmap/roadmap.md",
    "inProgress": "docs/roadmap/in_progress",
    "completed": "docs/roadmap/completed",
    "reports": "docs/reports",
    "changelog": "docs/reports/changelog.md",
    "governance": "docs/governance",
    "requestTemplate": "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
    "projectOpsContract": "docs/project_ops.md",
    "templateRoot": "docs/templates",
    "projectAdminBaselineTemplate": "docs/templates/project_admin_baseline.md",
    "prioritizationPolicy": "docs/governance/prioritization_policy.md"
  },
  "scopeLabels": [
    "governance",
    "docs",
    "runtime",
    "tests"
  ],
  "requiredDocs": [
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".gitignore",
    ".project_ops/config.json",
    "docs/project_ops.md",
    "docs/roadmap/roadmap.md",
    "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
    "docs/architecture/README.md",
    "docs/governance/README.md",
    "docs/reports/changelog.md"
  ],
  "privacy": {
    "defaultVisibility": "public",
    "publicExamplesRequireSanitization": true,
    "privateHistoryPaths": [
      "docs/private/**",
      ".local/**"
    ]
  },
  "validation": {
    "requireChangelog": true,
    "requireRoadmapParity": true,
    "allowEmptyRoadmap": true,
    "dryRunByDefault": true,
    "commands": [
      {
        "name": "project-ops-audit",
        "command": "python <path-to-project_ops>/tools/project_ops_audit.py --repo .",
        "required": true,
        "description": "Audit local Project Ops structure without rewriting files."
      },
      {
        "name": "request-audit",
        "command": "python <path-to-project_ops>/tools/project_ops_request_audit.py --repo . --request-id <request_id>",
        "required": true,
        "description": "Audit one request artifact against local roadmap and changelog state."
      },
      {
        "name": "roadmap-check",
        "command": "python <path-to-project_ops>/tools/project_ops_roadmap.py --repo .",
        "required": true,
        "description": "Check roadmap entries against local request artifacts without rewriting files."
      }
    ]
  },
  "bootstrap": {
    "requiredFiles": [
      "README.md",
      "CONTRIBUTING.md",
      "CHANGELOG.md",
      ".gitignore",
      ".project_ops/config.json",
      "docs/project_ops.md",
      "docs/roadmap/roadmap.md",
      "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
      "docs/reports/changelog.md"
    ],
    "recommendedFiles": [
      ".editorconfig",
      "LICENSE",
      "SECURITY.md",
      "docs/governance/prioritization_policy.md"
    ],
    "initialDirectories": [
      "docs/architecture",
      "docs/governance",
      "docs/roadmap/in_progress",
      "docs/roadmap/completed",
      "docs/reports",
      "docs/templates"
    ]
  }
}
```

## Required Decisions

Before adopting Project Ops, decide:

- whether the project is public, internal, or local-private,
- what docs are required before work starts,
- which scope labels are meaningful,
- where request artifacts live,
- where prioritization policy and Ready gate rules live,
- where private notes and local evidence are allowed,
- which validation command proves the repo is healthy,
- which files and directories bootstrap must create,
- and when audits should warn versus fail.

## Validation Commands

Use `validation.commands` for the commands a contributor or agent should run before closeout. Project Ops does not decide the full command list for the adopter. It records the local truth and provides reusable checks that adopters can call.

Each command has:

- `name`: stable machine-readable name,
- `command`: command text to run from the repo root,
- `required`: whether it is part of the normal gate,
- `description`: short human explanation.

## Bootstrap Expectations

Use `bootstrap.requiredFiles`, `bootstrap.recommendedFiles`, and `bootstrap.initialDirectories` to make the starter structure auditable. `tools/project_ops_bootstrap.py` creates a default version of this structure; `tools/project_ops_audit.py` checks whether it still exists.

Use `tools/project_ops_request_audit.py` when a repository wants Project Ops to verify request state, roadmap parity, and changelog breadcrumbs from outside the adopter repo. The adopter still owns its roadmap and history; Project Ops owns the reusable audit behavior.

Use `tools/project_ops_roadmap.py` when a repository wants a read-only check
across all configured request artifacts. It verifies that each request has a
roadmap entry and that State Summary fields match.

## Public Examples

Keep examples generic. Do not copy an adopter's real roadmap, changelog, reports, private validation evidence, or product architecture into this repository.
