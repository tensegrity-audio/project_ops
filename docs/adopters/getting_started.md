# Getting Started

Use Project Ops when you want a repository to start with clear administrative structure instead of accumulating process by accident.

## Start With The Baseline

For a new project, begin with:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `.gitignore`
- `.project_ops/config.json`
- `docs/roadmap/roadmap.md`
- `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`
- `docs/roadmap/completed/`
- `docs/reports/changelog.md`
- `docs/architecture/README.md`
- `docs/governance/README.md`

The template at `templates/project_admin_baseline.md` explains which files are must-have, recommended, or optional.

## Five-Minute Adoption Flow

1. Run `tools/project_ops_bootstrap.py --repo <project> --project-name "<Project>"` and review the dry-run plan.
2. Re-run with `--apply` only after the create/skip plan looks right.
3. Edit `.project_ops/config.json` for project-specific scope labels, required docs, privacy paths, and validation commands.
4. Read `docs/project_ops.md` and `docs/adopters/execution_process.md`.
5. Create the first request from `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md`.

Existing repos can still adopt manually by copying templates. New repos should prefer the dry-run bootstrap command because it does not overwrite project-owned files.

## Configure The Project

Each adopter should own its local config. Project Ops should not hardcode an adopter's paths, scope labels, privacy posture, or validation commands.

A minimal `.project_ops/config.json` should define:

- project id, name, and role,
- roadmap, changelog, request, and governance paths,
- scope labels,
- required docs,
- privacy rules,
- validation policy,
- bootstrap expectations.

Use `schemas/project_config.schema.json` as the contract for that config.

See `examples/project_config.minimal.json` for a standalone minimal config and `examples/minimal_project/.project_ops/config.json` for a tiny synthetic adopter layout.

## Create The First Request

Use `templates/request.md` for the first durable request artifact.

Good first requests include:

- project bootstrap,
- public/private boundary lock,
- validation baseline,
- documentation skeleton,
- first release plan.

## Keep History Local

Project Ops supplies structure. The adopter keeps the actual history:

- request docs,
- roadmap entries,
- changelog,
- reports,
- validation evidence,
- architecture decisions,
- and release notes.

Publish examples only after sanitizing them.
