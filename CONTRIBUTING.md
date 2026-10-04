# Contributing

Project Ops is intended to stay small, readable, and reusable across different kinds of repositories.

## Contribution Goals

Prefer changes that make project administration clearer for many projects:

- better templates,
- clearer bootstrap guidance,
- safer public/private boundaries,
- stronger dry-run behavior,
- simple schemas,
- and plain-language adoption docs.

Avoid changes that make Project Ops depend on one adopter's product architecture, roadmap history, private reports, or local validation evidence.

## Public-Safety Rules

Before contributing examples or docs, verify that they do not include:

- real private roadmap history,
- local filesystem paths,
- secrets or tokens,
- raw conversation logs,
- adopter-specific product strategy,
- validation evidence from a private machine,
- or project names used as hidden assumptions.

Examples should be synthetic unless the owning project has explicitly approved publication.

## Template Rules

Templates should:

- use placeholders where adopters must provide local details,
- avoid hardcoded scope labels except in clearly marked examples,
- keep file paths relative,
- make public/private posture explicit,
- and stay useful when copied into a fresh unrelated repository.

## Validation

For this seed stage, validate by checking:

```powershell
python -m compileall -q tools
python -m unittest discover -s tests
python tools\project_ops_audit.py --repo examples\minimal_project
python tools\project_ops_roadmap.py --repo examples\minimal_project
git diff --check
```

Do not validate against a real adopter repository from this repo's docs or CI. Use `examples/minimal_project`, and add a synthetic fixture when a check needs new shapes.

## Releasing

1. Update `CHANGELOG.md` and move the `Unreleased` notes under the new version.
2. Bump the schema namespace (`schemas/*.json` `$id`, `SCHEMA_ID` in `tools/project_ops_bootstrap.py`, `examples/project_config.minimal.json`) and the default `project-ops-ref` in `.github/workflows/reusable-*.yml`.
3. Tag `vX.Y.Z` on `main`. The Pages workflow publishes that tag's schemas at `https://tensegrity-audio.github.io/project_ops/schemas/vX.Y.Z/`.
4. Adopters move by changing the `@vX.Y.Z` on their `uses:` lines and the `$schema` in `.project_ops/config.json`.

```text
```
