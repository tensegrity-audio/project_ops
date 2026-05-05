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
python tools\project_ops_audit.py --repo examples\minimal_project
python tools\project_ops_request_audit.py --repo ..\tensegrity --request-id docops_peel_off_plan
python tools\project_ops_request_audit.py --repo ..\synaptome --request-id project_ops_compatibility
python -m py_compile tools\project_ops_audit.py tools\project_ops_bootstrap.py tools\project_ops_request_audit.py
git diff --check
```
