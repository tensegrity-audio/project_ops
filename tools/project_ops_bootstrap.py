#!/usr/bin/env python3
"""Bootstrap a new repository with Project Ops docs and process files.

The command is dry-run by default. Pass --apply to create missing files. Existing
files are never overwritten.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_OPS_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ID = "https://raw.githubusercontent.com/tensegrity-audio/project_ops/main/schemas/project_config.schema.json"


@dataclass(frozen=True)
class PlannedFile:
    path: Path
    content: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-_")
    return slug or "new-project"


def render_config(project_id: str, project_name: str, role: str, visibility: str) -> str:
    config = {
        "$schema": SCHEMA_ID,
        "project": {
            "id": project_id,
            "name": project_name,
            "role": role,
            "description": f"Project Ops configuration for {project_name}.",
        },
        "paths": {
            "roadmap": "docs/roadmap/roadmap.md",
            "inProgress": "docs/roadmap/in_progress",
            "completed": "docs/roadmap/completed",
            "reports": "docs/reports",
            "changelog": "docs/reports/changelog.md",
            "governance": "docs/governance",
            "requestTemplate": "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
            "projectOpsContract": "docs/project_ops.md",
            "templateRoot": "docs/templates",
            "projectAdminBaselineTemplate": "docs/templates/project_admin_baseline.md",
        },
        "scopeLabels": ["governance", "docs", "runtime", "tests"],
        "requiredDocs": [
            "README.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            ".gitignore",
            ".project_ops/config.json",
            "docs/project_ops.md",
            "docs/roadmap/roadmap.md",
            "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
            "docs/reports/changelog.md",
            "docs/architecture/README.md",
            "docs/governance/README.md",
        ],
        "privacy": {
            "defaultVisibility": visibility,
            "publicExamplesRequireSanitization": visibility == "public",
            "privateHistoryPaths": ["docs/private/**", ".local/**"],
        },
        "validation": {
            "requireChangelog": True,
            "requireRoadmapParity": True,
            "allowEmptyRoadmap": True,
            "dryRunByDefault": True,
            "commands": [
                {
                    "name": "project-ops-audit",
                    "command": "python <path-to-project_ops>/tools/project_ops_audit.py --repo .",
                    "required": True,
                    "description": "Audit local Project Ops structure without rewriting files.",
                }
            ],
        },
        "bootstrap": {
            "requiredFiles": [
                "README.md",
                "CONTRIBUTING.md",
                "CHANGELOG.md",
                ".gitignore",
                ".project_ops/config.json",
                "docs/project_ops.md",
                "docs/roadmap/roadmap.md",
                "docs/roadmap/in_progress/_REQUEST_TEMPLATE.md",
                "docs/reports/changelog.md",
            ],
            "recommendedFiles": [".editorconfig", "LICENSE", "SECURITY.md"],
            "initialDirectories": [
                "docs/architecture",
                "docs/governance",
                "docs/roadmap/in_progress",
                "docs/roadmap/completed",
                "docs/reports",
                "docs/templates",
            ],
        },
        "adoption": {
            "mode": "bootstrap",
            "frameworkRepo": "https://github.com/tensegrity-audio/project_ops",
            "frameworkRepoName": "project_ops",
            "frameworkProductName": "Project Ops",
        },
    }
    return json.dumps(config, indent=2) + "\n"


def template(name: str) -> str:
    return (PROJECT_OPS_ROOT / "templates" / name).read_text(encoding="utf-8")


def simple_template(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def render_project_ops_doc(project_name: str) -> str:
    return simple_template(
        "Project Ops",
        f"""This project uses Project Ops for documentation structure and execution tracking.

Project: {project_name}

Local operating files:

- `.project_ops/config.json` defines project paths, scopes, privacy posture, and validation expectations.
- `docs/roadmap/roadmap.md` records active and completed work.
- `docs/roadmap/in_progress/_REQUEST_TEMPLATE.md` defines request artifacts.
- `docs/reports/changelog.md` records meaningful project changes.
- `docs/governance/README.md` explains local decision rules.

Project Ops provides reusable structure. This repository owns its own product decisions, roadmap, reports, and validation evidence.""",
    )


def render_readme(project_name: str) -> str:
    return simple_template(
        project_name,
        """Describe what this project is, who it is for, and how to get started.

## Quickstart

Add the smallest useful setup or run command here.

## Project Operations

This repo uses Project Ops. Start with `docs/project_ops.md` and `.project_ops/config.json`.""",
    )


def render_contributing() -> str:
    return simple_template(
        "Contributing",
        """Keep changes focused, documented, and validated.

Before changing behavior, check:

- `README.md`
- `docs/project_ops.md`
- `.project_ops/config.json`
- `docs/roadmap/roadmap.md`

Record meaningful work in the roadmap and changelog.""",
    )


def render_changelog(project_name: str) -> str:
    return simple_template(
        "Changelog",
        f"""All meaningful changes to {project_name} should be recorded here.

## Unreleased

- Bootstrapped Project Ops structure.""",
    )


def planned_files(project_id: str, project_name: str, role: str, visibility: str) -> list[PlannedFile]:
    return [
        PlannedFile(Path(".project_ops/config.json"), render_config(project_id, project_name, role, visibility)),
        PlannedFile(Path("README.md"), render_readme(project_name)),
        PlannedFile(Path("CONTRIBUTING.md"), render_contributing()),
        PlannedFile(Path("CHANGELOG.md"), render_changelog(project_name)),
        PlannedFile(Path(".gitignore"), template("gitignore")),
        PlannedFile(Path(".editorconfig"), template("editorconfig")),
        PlannedFile(Path("docs/project_ops.md"), render_project_ops_doc(project_name)),
        PlannedFile(Path("docs/architecture/README.md"), template("architecture_readme.md")),
        PlannedFile(Path("docs/governance/README.md"), template("governance_readme.md")),
        PlannedFile(Path("docs/roadmap/roadmap.md"), template("roadmap.md")),
        PlannedFile(Path("docs/roadmap/in_progress/_REQUEST_TEMPLATE.md"), template("request.md")),
        PlannedFile(Path("docs/roadmap/completed/.gitkeep"), ""),
        PlannedFile(Path("docs/reports/changelog.md"), template("changelog.md")),
        PlannedFile(Path("docs/templates/project_admin_baseline.md"), template("project_admin_baseline.md")),
        PlannedFile(Path("docs/templates/bootstrap_manifest.md"), template("bootstrap_manifest.md")),
        PlannedFile(Path("docs/templates/project_ops_contract.md"), template("project_ops_contract.md")),
        PlannedFile(Path("docs/templates/architecture_readme.md"), template("architecture_readme.md")),
        PlannedFile(Path("docs/templates/governance_readme.md"), template("governance_readme.md")),
        PlannedFile(Path("docs/templates/roadmap.md"), template("roadmap.md")),
        PlannedFile(Path("docs/templates/changelog.md"), template("changelog.md")),
        PlannedFile(Path("docs/templates/request.md"), template("request.md")),
        PlannedFile(Path("docs/templates/roadmap_entry.md"), template("roadmap_entry.md")),
        PlannedFile(Path("docs/templates/changelog_entry.md"), template("changelog_entry.md")),
        PlannedFile(Path("docs/templates/rfc_lite.md"), template("rfc_lite.md")),
        PlannedFile(Path("docs/templates/post_mortem.md"), template("post_mortem.md")),
        PlannedFile(Path("docs/templates/phase_exit_audit.md"), template("phase_exit_audit.md")),
        PlannedFile(Path("docs/templates/handoff.md"), template("handoff.md")),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a repository with Project Ops starter docs.")
    parser.add_argument("--repo", type=Path, required=True, help="Repository root to inspect or bootstrap.")
    parser.add_argument("--project-name", required=True, help="Human-facing project name.")
    parser.add_argument("--project-id", help="Machine-friendly project id. Defaults to a slug of project name.")
    parser.add_argument("--role", default="project-ops-adopter", help="Project role label.")
    parser.add_argument(
        "--visibility",
        choices=("public", "internal", "local-private"),
        default="public",
        help="Default project visibility posture.",
    )
    parser.add_argument("--apply", action="store_true", help="Create missing files. Existing files are skipped.")
    args = parser.parse_args()

    root = args.repo.resolve()
    if root == root.anchor or root.parent == root:
        print(f"ERROR: refusing to bootstrap filesystem root: {root}")
        return 3
    if not root.exists():
        print(f"ERROR: repo path does not exist: {root}")
        return 3
    if not root.is_dir():
        print(f"ERROR: repo path is not a directory: {root}")
        return 3
    project_id = args.project_id or slugify(args.project_name)
    files = planned_files(project_id, args.project_name, args.role, args.visibility)

    print("Project Ops bootstrap")
    print(f"repo: {root}")
    print(f"mode: {'apply' if args.apply else 'dry-run'}")

    created = 0
    skipped = 0
    planned = 0
    for item in files:
        destination = root / item.path
        if destination.exists():
            skipped += 1
            print(f"skip existing: {item.path.as_posix()}")
            continue
        planned += 1
        print(f"create: {item.path.as_posix()}")
        if args.apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(item.content, encoding="utf-8", newline="\n")
            created += 1

    if args.apply:
        print(f"Result: APPLIED ({created} created, {skipped} skipped)")
    else:
        print(f"Result: DRY-RUN ({planned} planned, {skipped} skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
