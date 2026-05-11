# Changelog

## Unreleased

- Added adopter integration guidance and subsystem connection docs for Project Ops.
- Restored a detailed agent execution contract with phase gates, rewind rules, validation discipline, and stronger request/roadmap template parity.
- Added prioritization policy templates, Definition of Ready checks, and a read-only roadmap parity checker.
- Added an artifact contract for stable Request IDs, Decision IDs, and RFC-lite readiness links across roadmap, changelog, handoff, and post-mortem artifacts.

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
