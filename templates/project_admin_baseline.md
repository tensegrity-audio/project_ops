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
| `docs/roadmap/roadmap.md` | Must-have for active projects | Gives the current roadmap, active requests, completed work, and backlog. |
| `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` | Must-have for Project Ops adopters | Defines the durable request artifact shape. |
| `docs/reports/` | Must-have for Project Ops adopters | Holds changelog, audits, release notes, and post-mortems. |
| `docs/architecture/` | Recommended | Holds system maps, boundary docs, contracts, and design decisions. |
| `docs/governance/` | Recommended for multi-person or agent-assisted projects | Holds decision policy, RFC Lite rules, autonomy boundaries, ownership rules, and roadmap topology. |
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
    architecture/
      README.md
    governance/
      README.md
    roadmap/
      roadmap.md
      in_progress/
        _REQUEST_TEMPLATE.md
      completed/
    reports/
      changelog.md
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
    "requestTemplate": "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md"
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

## Bootstrap Checklist

- Project identity recorded.
- License posture recorded.
- README has a quickstart.
- Contribution path recorded.
- Roadmap exists.
- Changelog exists.
- Request template exists.
- `.project_ops/config.json` exists.
- Required docs are listed in project config.
- Ignore rules cover generated files and local state.
- First validation command is documented.
- Public/private boundary is explicit.
- First request artifact can be created without adding project-specific Project Ops code.
