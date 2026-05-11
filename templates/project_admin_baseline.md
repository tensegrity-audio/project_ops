# Project Admin Baseline Template

Use this template as the default administrative skeleton for a fresh project. The goal is not to force every project into the same product shape; the goal is to make the basic operating surface explicit on day one.

## Baseline Files

| File | Level | Purpose |
| --- | --- | --- |
| `README.md` | Must-have | Explains what the project is, who it is for, how to install or run it, and where to start. |
| `LICENSE` | Must-have for public projects | States reuse rights. Private/internal projects should still record license posture. |
| `CHANGELOG.md` or `docs/reports/changelog.md` | Must-have | Records meaningful changes, lifecycle milestones, releases, and administrative decisions. |
| `CONTRIBUTING.md` or `docs/contributing.md` | Must-have for collaborative projects | Explains contribution flow, validation expectations, coding/doc standards, and review norms. |
| `.gitignore` | Must-have | Keeps generated files, local state, secrets, and build outputs out of version control. |
| `.editorconfig` | Recommended | Establishes portable whitespace, line-ending, and final-newline behavior. |
| `docs/project_ops.md` | Must-have for Project Ops adopters | Explains the local operating loop and points to the config, roadmap, changelog, and request template. |
| `docs/roadmap/roadmap.md` | Must-have for active projects | Gives the current roadmap, active requests, completed work, and backlog. |
| `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` | Must-have for Project Ops adopters | Defines the durable request artifact shape. |
| `docs/reports/` | Must-have for Project Ops adopters | Holds changelog, audits, release notes, and post-mortems. |
| `docs/architecture/` | Recommended | Holds system maps, boundary docs, contracts, and design decisions. |
| `docs/governance/` | Recommended for multi-person or agent-assisted projects | Holds decision policy, RFC Lite rules, autonomy boundaries, ownership rules, and roadmap topology. |
| `docs/governance/prioritization_policy.md` | Recommended for roadmap-driven projects | Defines scoring inputs, priority lanes, and Definition of Ready gates. |
| `docs/templates/` | Recommended | Holds local copies of Project Ops templates for offline or project-specific adaptation. |
| `.project_ops/config.json` | Must-have for Project Ops adopters | Defines project-local paths, scopes, privacy policy, validation gates, and adoption mode. |
| `.github/pull_request_template.md` | Recommended for GitHub projects | Gives reviewers a consistent validation and documentation checklist. |
| `.github/workflows/` | Recommended once validation stabilizes | Runs audit, tests, formatting, or release checks in CI. |
| `SECURITY.md` | Recommended for public software | Explains how to report vulnerabilities or sensitive issues. |
| `CODE_OF_CONDUCT.md` | Recommended for community projects | Establishes participation norms. |

## Baseline Directory Shape

```text
<project>/
  README.md
  LICENSE
  CHANGELOG.md
  CONTRIBUTING.md
  .gitignore
  .editorconfig
  .project_ops/
    config.json
  docs/
    project_ops.md
    architecture/
      README.md
    governance/
      README.md
      prioritization_policy.md
    roadmap/
      roadmap.md
      in_progress/
        _REQUEST_TEMPLATE.md
      completed/
    reports/
      changelog.md
    templates/
```

## First Project Questions

- What is the project called?
- Is it public, private, or internal?
- What license posture applies?
- Who is the intended user or adopter?
- What is the smallest useful quickstart?
- What files are generated and should be ignored?
- What validation command proves the project still works?
- What docs must an agent or contributor read before making changes?
- What priority scoring and Definition of Ready gates decide roadmap order?
- What lifecycle artifacts should be local-private?
- What release/versioning pattern will the project use?

## Project Config Defaults

```json
{
  "project": {
    "id": "<project-id>",
    "name": "<Project Name>",
    "role": "<project role>"
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
    "projectAdminBaselineTemplate": "docs/templates/project_admin_baseline.md"
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
      }
    ]
  }
}
```

## Bootstrap Checklist

- `.project_ops/config.json` exists and names the project.
- `README.md` exists and has a quickstart placeholder or real quickstart.
- `CONTRIBUTING.md` exists or the config explicitly says the project is solo/private.
- `.gitignore` exists and covers generated files plus local/private Project Ops state.
- `docs/project_ops.md` exists and links the local operating files.
- `docs/roadmap/roadmap.md` exists.
- `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` exists.
- `docs/roadmap/completed/` exists.
- `docs/reports/changelog.md` exists.
- `docs/architecture/README.md` exists or the project records why architecture docs are deferred.
- `docs/governance/README.md` exists or the project records why governance docs are deferred.
- `docs/governance/prioritization_policy.md` exists or the project records why prioritization policy is deferred.
- Required docs are listed in `.project_ops/config.json`.
- Validation commands are listed in `.project_ops/config.json`.
- Public/private boundary is explicit in `.project_ops/config.json`.
- `python <path-to-project_ops>/tools/project_ops_audit.py --repo .` passes or every warning is intentionally accepted.
