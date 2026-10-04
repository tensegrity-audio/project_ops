# Changelog

## Unreleased

## v0.2.0 - 2026-10-04

- Shipped `tools/project_ops_roadmap.py`, the read-only roadmap parity checker that adopters were already calling.
- Made the request Design Alignment section optional. Set `validation.requireDesignAlignment: true` in `.project_ops/config.json` to require it; when present it is audited either way. The explanation field is now `Plain-Language Explanation`; the older `Student-Facing Explanation` label is still accepted.
- Added reusable GitHub workflows: `reusable-project-ops-audit.yml` (structure audit plus roadmap parity) and `reusable-request-audit.yml` (audits every changed request artifact). Adopters call them with `uses: tensegrity-audio/project_ops/.github/workflows/<name>@v0.2.0`.
- Added a Pages workflow that publishes each tag's schemas at `https://tensegrity-audio.github.io/project_ops/schemas/<tag>/`, so `$schema` URLs resolve.
- Added `templates/AGENTS.md`, `templates/CLAUDE.md` (one line, `@AGENTS.md`), and `templates/dependabot.yml`; bootstrap now creates them.
- Moved the schema namespace to `v0.2.0`.
- CI compiles every tool, runs on Ubuntu and Windows, checks the minimal example's roadmap parity, and exercises the reusable audit workflow against the minimal example.
- Removed real adopter repositories from `CONTRIBUTING.md`; validation uses `examples/minimal_project` only. Reworded teaching-specific language in templates and docs to apply to any project.

- Added adopter integration guidance and subsystem connection docs for Project Ops.
- Restored a detailed agent execution contract with phase gates, rewind rules, validation discipline, and stronger request/roadmap template parity.
- Added prioritization policy templates, Definition of Ready checks, and a read-only roadmap parity checker.
- Added an artifact contract for stable Request IDs, Decision IDs, and RFC-lite readiness links across roadmap, changelog, handoff, and post-mortem artifacts.
- Added a design alignment log template and execution-process checkpoints so adopter projects can explain guiding principles, chosen systems/processes, and plain-language rationale.

## v0.1.2 - 2026-05-05

- Replaced raw GitHub schema identifiers with repo-owned, versioned Project Ops schema namespace IDs.
- Updated bootstrap-generated configs and minimal examples to consume the `v0.1.2` Project Ops schema namespace.

## v0.1.1 - 2026-05-05

- Pinned Project Ops schema IDs and bootstrap-generated config schemas to the `v0.1.1` tag so adopters can consume a release-stable schema URL.

## v0.1.0 - 2026-05-05

- Seeded Project Ops with public-safe templates, schemas, and adopter guidance.
- Added dry-run-first bootstrap and audit tooling for blank-repo adoption.
- Added execution-process guidance, starter docs templates, bootstrap manifest, and a fuller minimal adopter example.
- Added reusable request/roadmap/changelog parity auditing through `tools/project_ops_request_audit.py`.
