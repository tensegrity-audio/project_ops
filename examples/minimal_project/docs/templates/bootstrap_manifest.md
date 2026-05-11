# Bootstrap Manifest

Use this manifest to understand what `tools/project_ops_bootstrap.py` creates for a blank repository.

| Destination | Source | Level | First-fill instruction |
| --- | --- | --- | --- |
| `.project_ops/config.json` | generated from CLI arguments | Must-have | Review project id, visibility, scope labels, required docs, and validation commands. |
| `README.md` | generated starter | Must-have | Replace the placeholder quickstart with the real smallest useful setup. |
| `CONTRIBUTING.md` | generated starter | Must-have | Add project-specific validation and review rules. |
| `CHANGELOG.md` | generated starter | Must-have | Keep or replace with `docs/reports/changelog.md` as the canonical changelog. |
| `.gitignore` | `templates/gitignore` | Must-have | Add project build outputs, generated assets, and secret paths. |
| `.editorconfig` | `templates/editorconfig` | Recommended | Adjust only if the project has established formatting rules. |
| `docs/project_ops.md` | generated starter | Must-have | Add local operating notes if the project differs from the defaults. |
| `docs/architecture/README.md` | `templates/architecture_readme.md` | Recommended | Link architecture maps as they are created. |
| `docs/governance/README.md` | `templates/governance_readme.md` | Recommended | Add local decision, prioritization, approval, and validation policy. |
| `docs/governance/prioritization_policy.md` | `templates/prioritization_policy.md` | Recommended | Tune score inputs, priority lanes, and Definition of Ready gates. |
| `docs/roadmap/roadmap.md` | `templates/roadmap.md` | Must-have | Add the first active request or backlog item. |
| `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` | `templates/request.md` | Must-have | Customize scope labels and validation expectations. |
| `docs/roadmap/completed/.gitkeep` | empty generated file | Must-have | Keeps the completed request directory present. |
| `docs/reports/changelog.md` | `templates/changelog.md` | Must-have | Record meaningful administrative and product changes. |
| `docs/templates/**` | reusable Project Ops templates | Recommended | Local copies for offline/customized project use. |

`bootstrap --apply` never overwrites existing files. Existing project-owned files are skipped.
