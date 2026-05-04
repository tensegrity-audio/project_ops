# Configuration

Project Ops is configured per adopter. The framework should not hardcode project paths, scope labels, privacy rules, or validation commands.

Use `.project_ops/config.json` in the adopter repo. A standalone example lives at `examples/project_config.minimal.json`.

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
    "templateRoot": "templates",
    "projectAdminBaselineTemplate": "templates/project_admin_baseline.md"
  },
  "scopeLabels": [
    "governance",
    "docs",
    "runtime",
    "tests"
  ],
  "requiredDocs": [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "docs/roadmap/roadmap.md",
    "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
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
    "dryRunByDefault": true
  }
}
```

## Required Decisions

Before adopting Project Ops, decide:

- whether the project is public, internal, or local-private,
- what docs are required before work starts,
- which scope labels are meaningful,
- where request artifacts live,
- where private notes and local evidence are allowed,
- which validation command proves the repo is healthy,
- and when audits should warn versus fail.

## Public Examples

Keep examples generic. Do not copy an adopter's real roadmap, changelog, reports, private validation evidence, or product architecture into this repository.
