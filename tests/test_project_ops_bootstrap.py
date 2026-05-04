from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "tools" / "project_ops_bootstrap.py"
AUDIT = ROOT / "tools" / "project_ops_audit.py"


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

            audit_result = run_tool(str(AUDIT), "--repo", str(repo))
            self.assertEqual(audit_result.returncode, 0, audit_result.stdout + audit_result.stderr)
            self.assertIn("Result: PASS", audit_result.stdout)

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


if __name__ == "__main__":
    unittest.main()
