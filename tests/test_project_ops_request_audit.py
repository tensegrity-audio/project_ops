from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import project_ops_request_audit as request_audit


def base_state_summary(phase: str = "EXECUTION", update_field: str = "Project Ops / Roadmap Updates (timestamped)") -> str:
    return f"""State Summary

- Request ID: example_request
- Phase: {phase}
- Status: In Progress
- Steps Complete: 1 / 2
- Progress: Fixture request is synchronized.
- Last Step Outcome: 2026-05-05 - Created request audit fixture.
- Next Step: Keep fixture green.
- Dependencies / Overlap: Project Ops request audit.
- Primary Scope: tools.
- Secondary Scopes: tests.
- Blocking Issues / Unknowns: None.
- Impact / Priority Notes: Proves downstream request audit tooling in CI.
- Priority Score: 9
- Priority Lane: Standard
- Ready State: Ready
- Ready Gate: met
- {update_field}: 2026-05-05 - Fixture request synchronized with roadmap and changelog.
- Resume From: Continue from fixture validation.
"""


READY_BODY = """
## Milestone Synthesis

- Milestone ID: request-audit-fixture
- Milestone Name: Request audit fixture
- Milestone Type: Validation Gate
- Source Requests: example_request
- Outcome Statement (Done When): The request audit fixture passes.
- KPI / Success Signal: Request audit returns Result: PASS.
- Target Window: 2026-05
- Dependency Gates: N/A
- Contract Surfaces: tools/project_ops_request_audit.py, tests
- Risk Posture: low - fixture-only coverage.
- Goal: Prove synchronized request audits.
- Non-Goals: N/A
- Owner: Project Ops tests.

## Roadmap Overlap Review

- Existing roadmap entries checked: docs/roadmap/roadmap.md
- Related active requests: N/A
- Duplicate risk: low
- Merge / split decision: Keep as independent fixture.
- Priority conflict: N/A

## Prioritization

- Policy Source: docs/governance/prioritization_policy.md
- Priority Score: 9
- Priority Lane: Standard
- Due Date / Timing Driver: N/A
- Sort Key: Standard:9:none:example_request
- Override: none

## Definition Of Ready

- Ready State: Ready
- Decision Links: N/A
- Ready Date: 2026-05-05
- Ready Owner: Project Ops tests.
- Ready Exceptions: none

## Complexity

- Level: low
- Predicted Count: 3
- Count Drivers: request doc, roadmap entry, changelog entry
- Drivers: validation fixture coverage
- Confidence: high

## Intake

- User Request: Keep request audit fixture green.
- Context: Unit tests need a synchronized request artifact.
- Acceptance Signal: Request audit passes.

## Form

- Problem Statement: Request audit fixtures need complete ready-state metadata.
- User / Operational Value: CI can catch request audit regressions.
- Change Type: test
- Execution Mode: Assisted
- Acceptance Criteria: Request audit returns Result: PASS.
- Constraints: Keep fixture local to the temp repo.
- Must Not Change: Production docs.
- Allowed To Change: Temp request, roadmap, and changelog fixtures.
- Inputs Needed: N/A

## Analysis

- Touch Map: tools/project_ops_request_audit.py and tests.
- Risks: N/A
- Alternatives Considered: N/A

## Plan

- Steps: Create synchronized temp request, roadmap, and changelog fixtures.
- Validation Plan: Run request audit against the temp repo.
- Rollback / Stop Conditions: N/A

## Task Graph

| Task ID | Description | Module Surface | Depends On | Owner | Status | Priority Lane | Priority Score | Ready State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-1 | Build synchronized fixture | tests | N/A | Project Ops tests | Complete | Standard | 9 | Ready |
"""


class ProjectOpsRequestAuditReadinessTests(unittest.TestCase):
    def write_repo(self, state_summary: str, readiness_body: str = READY_BODY) -> tuple[Path, dict[str, object], Path]:
        repo = self.tmp_path / "adopter"
        request_dir = repo / "docs" / "roadmap" / "in_progress"
        reports_dir = repo / "docs" / "reports"
        request_dir.mkdir(parents=True)
        reports_dir.mkdir(parents=True)
        repo.joinpath("docs", "roadmap").mkdir(parents=True, exist_ok=True)

        config = {
            "paths": {
                "roadmap": "docs/roadmap/roadmap.md",
                "inProgress": "docs/roadmap/in_progress",
                "completed": "docs/roadmap/completed",
                "changelog": "docs/reports/changelog.md",
            },
            "validation": {
                "requireChangelog": True,
                "requireRoadmapParity": True,
            },
        }
        request_path = request_dir / "example_request.md"
        request_path.write_text(f"# Example Request\n\n{state_summary}\n{readiness_body}", encoding="utf-8")
        repo.joinpath("docs", "roadmap", "roadmap.md").write_text(
            f"# Roadmap\n\n## Example Request\n\n{state_summary}\nRequest Doc: docs/roadmap/in_progress/example_request.md\n",
            encoding="utf-8",
        )
        reports_dir.joinpath("changelog.md").write_text(
            "# Changelog\n\n- 2026-05-05 - example_request fixture added.\n",
            encoding="utf-8",
        )
        return repo, config, request_path

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_execution_phase_flags_missing_readiness_field(self) -> None:
        readiness = READY_BODY.replace("- Acceptance Criteria: Request audit returns Result: PASS.\n", "")
        repo, config, request_path = self.write_repo(base_state_summary(), readiness)

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertEqual(warnings, [])
        self.assertIn(
            "Missing readiness field before EXECUTION: Form -> Acceptance Criteria",
            errors,
        )

    def test_execution_phase_flags_unresolved_readiness_placeholder(self) -> None:
        readiness = READY_BODY.replace(
            "- Validation Plan: Run request audit against the temp repo.",
            "- Validation Plan: <commands, reviews, manual checks>",
        )
        repo, config, request_path = self.write_repo(base_state_summary(), readiness)

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertEqual(warnings, [])
        self.assertIn(
            "Unresolved readiness field before EXECUTION: Plan -> Validation Plan",
            errors,
        )

    def test_plan_phase_does_not_require_ready_fields_yet(self) -> None:
        repo, config, request_path = self.write_repo(base_state_summary(phase="PLAN"), readiness_body="")

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_docops_roadmap_update_alias_still_passes(self) -> None:
        repo, config, request_path = self.write_repo(
            base_state_summary(update_field="DocOps / Roadmap Updates (timestamped)")
        )

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_request_id_must_match_filename(self) -> None:
        repo, config, request_path = self.write_repo(
            base_state_summary().replace("- Request ID: example_request", "- Request ID: other_request")
        )

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertIn(
            "No changelog entry found containing request id 'other_request'.",
            warnings,
        )
        self.assertIn(
            "Request ID mismatch: State Summary has 'other_request' but filename stem is 'example_request'",
            errors,
        )

    def test_ready_request_flags_unresolved_decision_blocker(self) -> None:
        readiness = READY_BODY.replace("- Decision Links: N/A", "- Decision Links: blocked by RFC PO-RFC-001")
        repo, config, request_path = self.write_repo(base_state_summary(), readiness)

        errors, warnings = request_audit.audit_request(repo, config, request_path)

        self.assertEqual(warnings, [])
        self.assertIn(
            "Definition of Ready not satisfied before EXECUTION: decision links still indicate a blocker",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
