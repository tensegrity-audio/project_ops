from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "tools" / "project_ops_bootstrap.py"
AUDIT = ROOT / "tools" / "project_ops_audit.py"
REQUEST_AUDIT = ROOT / "tools" / "project_ops_request_audit.py"
ROADMAP = ROOT / "tools" / "project_ops_roadmap.py"


def run_tool(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ProjectOpsBootstrapTests(unittest.TestCase):
    def test_bootstrap_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "blank"
            repo.mkdir()

            result = run_tool(str(BOOTSTRAP), "--repo", str(repo), "--project-name", "Blank Project")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("mode: dry-run", result.stdout)
            self.assertIn("create: .project_ops/config.json", result.stdout)
            self.assertFalse((repo / ".project_ops" / "config.json").exists())

    def test_bootstrap_apply_then_audit_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "blank"
            repo.mkdir()

            apply_result = run_tool(
                str(BOOTSTRAP),
                "--repo",
                str(repo),
                "--project-name",
                "Blank Project",
                "--apply",
            )
            self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
            self.assertTrue((repo / ".project_ops" / "config.json").exists())
            self.assertTrue((repo / "docs" / "roadmap" / "in_progress" / "_REQUEST_TEMPLATE.md").exists())
            self.assertTrue((repo / "docs" / "governance" / "prioritization_policy.md").exists())
            self.assertTrue((repo / "docs" / "templates" / "prioritization_policy.md").exists())

            audit_result = run_tool(str(AUDIT), "--repo", str(repo))
            self.assertEqual(audit_result.returncode, 0, audit_result.stdout + audit_result.stderr)
            self.assertIn("Result: PASS", audit_result.stdout)

            roadmap_result = run_tool(str(ROADMAP), "--repo", str(repo))
            self.assertEqual(roadmap_result.returncode, 0, roadmap_result.stdout + roadmap_result.stderr)
            self.assertIn("Result: PASS", roadmap_result.stdout)

    def test_bootstrap_never_overwrites_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "existing"
            repo.mkdir()
            readme = repo / "README.md"
            readme.write_text("# Existing\n\nKeep me.\n", encoding="utf-8")

            result = run_tool(
                str(BOOTSTRAP),
                "--repo",
                str(repo),
                "--project-name",
                "Existing Project",
                "--apply",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("skip existing: README.md", result.stdout)
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Existing\n\nKeep me.\n")

    def test_request_audit_passes_for_synchronized_request(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "adopter"
            request_dir = repo / "docs" / "roadmap" / "in_progress"
            reports_dir = repo / "docs" / "reports"
            config_dir = repo / ".project_ops"
            request_dir.mkdir(parents=True)
            reports_dir.mkdir(parents=True)
            config_dir.mkdir(parents=True)

            config_dir.joinpath("config.json").write_text(
                """{
  "paths": {
    "roadmap": "docs/roadmap/roadmap.md",
    "inProgress": "docs/roadmap/in_progress",
    "completed": "docs/roadmap/completed",
    "changelog": "docs/reports/changelog.md"
  },
  "validation": {
    "requireChangelog": true,
    "requireRoadmapParity": true
  }
}
""",
                encoding="utf-8",
            )
            state_summary = """State Summary

- Request ID: example_request
- Phase: EXECUTION
- Status: In Progress
- Steps Complete: 1/2
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
- Resume From: Continue from fixture validation.
- Project Ops / Roadmap Updates (timestamped): 2026-05-05 - Fixture request synchronized with roadmap and changelog.
"""
            readiness = """
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
            request_dir.joinpath("example_request.md").write_text(
                f"# Example Request\n\n{state_summary}\n{readiness}",
                encoding="utf-8",
            )
            repo.joinpath("docs", "roadmap", "roadmap.md").write_text(
                f"# Roadmap\n\n## Example Request\n\n{state_summary}\nRequest Doc: docs/roadmap/in_progress/example_request.md\n",
                encoding="utf-8",
            )
            reports_dir.joinpath("changelog.md").write_text(
                "# Changelog\n\n- 2026-05-05 - example_request fixture added.\n",
                encoding="utf-8",
            )

            result = run_tool(str(REQUEST_AUDIT), "--repo", str(repo), "--request-id", "example_request")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Result: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
