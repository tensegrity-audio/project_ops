from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


def state_summary(
    *,
    phase: str = "EXECUTION",
    status: str = "In Progress",
    note: str = "Fixture",
    request_id: str = "example_request",
) -> str:
    return f"""State Summary

- Request ID: {request_id}
- Phase: {phase}
- Status: {status}
- Steps Complete: 1 / 2
- Progress: {note} request is synchronized.
- Last Step Outcome: 2026-05-07 - Created roadmap fixture.
- Next Step: Keep roadmap parity green.
- Dependencies / Overlap: Project Ops roadmap check.
- Primary Scope: docs
- Secondary Scopes: governance
- Blocking Issues / Unknowns: None.
- Impact / Priority Notes: Validates roadmap sync behavior.
- Project Ops / Roadmap Updates (timestamped): 2026-05-07 - Request and roadmap state match.
- Resume From: Phase {phase}, State {status}, Next Action validate roadmap check.
"""


def write_adopter_config(repo: Path) -> None:
    (repo / ".project_ops").mkdir(parents=True)
    (repo / "docs" / "roadmap" / "in_progress").mkdir(parents=True)
    (repo / "docs" / "roadmap" / "completed").mkdir(parents=True)
    (repo / ".project_ops" / "config.json").write_text(
        """{
  "project": {
    "id": "roadmap-fixture",
    "name": "Roadmap Fixture",
    "role": "test"
  },
  "paths": {
    "roadmap": "docs/roadmap/roadmap.md",
    "inProgress": "docs/roadmap/in_progress",
    "completed": "docs/roadmap/completed",
    "requestTemplate": "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md"
  }
}
""",
        encoding="utf-8",
    )


def write_request(repo: Path, rel: str, summary: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {path.stem}\n\n{summary}", encoding="utf-8")


class ProjectOpsRoadmapTests(unittest.TestCase):
    def test_roadmap_check_passes_for_synchronized_request_collection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "adopter"
            repo.mkdir()
            write_adopter_config(repo)
            (repo / "docs" / "roadmap" / "in_progress" / "_REQUEST_TEMPLATE.md").write_text(
                "# Template\n\nNo live request here.\n",
                encoding="utf-8",
            )

            active_summary = state_summary(note="Active", request_id="active_request")
            completed_summary = state_summary(
                phase="COMPLETE",
                status="Done",
                note="Completed",
                request_id="completed_request",
            )
            write_request(repo, "docs/roadmap/in_progress/active_request.md", active_summary)
            write_request(repo, "docs/roadmap/completed/completed_request.md", completed_summary)
            (repo / "docs" / "roadmap" / "roadmap.md").write_text(
                f"""# Roadmap

## In Progress

### Active Request

{active_summary}
Request Doc: docs/roadmap/in_progress/active_request.md

## Completed

### Completed Request

{completed_summary}
Request Doc: docs/roadmap/completed/completed_request.md
""",
                encoding="utf-8",
            )

            result = run_tool(str(ROADMAP), "check", "--repo", str(repo))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("requests: 2 (inProgress: 1, completed: 1)", result.stdout)
            self.assertIn("Result: PASS", result.stdout)

    def test_roadmap_check_reports_missing_roadmap_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "adopter"
            repo.mkdir()
            write_adopter_config(repo)
            write_request(repo, "docs/roadmap/in_progress/example_request.md", state_summary())
            (repo / "docs" / "roadmap" / "roadmap.md").write_text(
                "# Roadmap\n\n## In Progress\n\nNo active requests yet.\n",
                encoding="utf-8",
            )

            result = run_tool(str(ROADMAP), "--repo", str(repo))

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(
                "Missing roadmap entry for Request Doc: docs/roadmap/in_progress/example_request.md",
                result.stdout,
            )
            self.assertIn("Result: FAIL", result.stdout)

    def test_roadmap_check_reports_state_summary_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "adopter"
            repo.mkdir()
            write_adopter_config(repo)
            request_summary = state_summary(status="In Progress")
            roadmap_summary = state_summary(status="Blocked")
            write_request(repo, "docs/roadmap/in_progress/example_request.md", request_summary)
            (repo / "docs" / "roadmap" / "roadmap.md").write_text(
                f"""# Roadmap

## In Progress

### Example Request

{roadmap_summary}
Request Doc: docs/roadmap/in_progress/example_request.md
""",
                encoding="utf-8",
            )

            result = run_tool(str(ROADMAP), "check", "--repo", str(repo))

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(
                "State Summary mismatch for docs/roadmap/in_progress/example_request.md field 'Status'",
                result.stdout,
            )
            self.assertIn("request='In Progress' roadmap='Blocked'", result.stdout)


if __name__ == "__main__":
    unittest.main()
