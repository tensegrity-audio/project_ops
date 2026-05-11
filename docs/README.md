# Documentation

- [Project Ops Model](concepts/project_ops_model.md)
- [Repo Component Map](concepts/repo_component_map.md)
- [Artifact Contract](concepts/artifact_contract.md)
- [Getting Started](adopters/getting_started.md)
- [Integration Guide](adopters/integration_guide.md)
- [Agent Execution Contract](adopters/agent_execution_contract.md)
- [Configuration](adopters/configuration.md)
- [Execution Process](adopters/execution_process.md)

Templates live in [`../templates`](../templates). Schemas live in [`../schemas`](../schemas).
Key operating templates include [`request.md`](../templates/request.md),
[`roadmap.md`](../templates/roadmap.md),
[`roadmap_entry.md`](../templates/roadmap_entry.md), and
[`prioritization_policy.md`](../templates/prioritization_policy.md).

Bootstrap and audit tools live in [`../tools`](../tools):

- `project_ops_bootstrap.py` plans or creates starter Project Ops docs.
- `project_ops_audit.py` checks adopter structure without rewriting files.
- `project_ops_request_audit.py` checks request, roadmap, and changelog parity.
- `project_ops_roadmap.py` checks all configured request artifacts against the roadmap.
