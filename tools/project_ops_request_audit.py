#!/usr/bin/env python3
"""Audit Project Ops request artifacts against roadmap and changelog state.

This is the reusable counterpart to adopter-local request audits. It is
read-only and driven by the adopter's `.project_ops/config.json`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(".project_ops/config.json")
PHASES = {
    "INTAKE",
    "FORM",
    "ANALYSIS",
    "PLAN",
    "EXECUTION",
    "VALIDATION",
    "DOC_SYNC",
    "POST_MORTEM",
    "COMPLETE",
}
REQUIRED_KEYS = (
    "Phase",
    "Status",
    "Steps Complete",
    "Progress",
    "Last Step Outcome",
    "Next Step",
    "Dependencies / Overlap",
    "Blocking Issues / Unknowns",
    "Impact / Priority Notes",
    "Resume From",
)
UPDATE_FIELDS = (
    "Project Ops / Roadmap Updates (timestamped)",
    "DocOps / Roadmap Updates (timestamped)",
)
TIMESTAMP_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts or not str(path).strip():
        raise ValueError(f"Project Ops config path must be repo-relative: {candidate.as_posix()}")
    return candidate


def load_config(root: Path, config_path: Path) -> dict[str, Any]:
    path = config_path if config_path.is_absolute() else root / config_path
    if not path.exists():
        raise ValueError(f"Missing Project Ops config: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Project Ops config root must be an object: {path}")
    paths = data.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("Project Ops config missing object: paths")
    for key in ("roadmap", "inProgress", "completed", "changelog"):
        if not isinstance(paths.get(key), str):
            raise ValueError(f"Project Ops config missing paths.{key}")
    return data


def parse_state_summary(text: str) -> dict[str, str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip().lower() == "state summary":
            start = index + 1
            break
    if start is None:
        return {}

    summary: dict[str, str] = {}
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            if summary:
                break
            continue
        if not stripped.startswith("-"):
            if summary:
                break
            continue
        match = re.match(r"^-\s*([^:]+):\s*(.*)$", stripped)
        if match:
            summary[match.group(1).strip()] = match.group(2).strip()
    return summary


def find_roadmap_block(roadmap_text: str, request_rel: str) -> dict[str, str]:
    lines = roadmap_text.splitlines()
    marker = f"Request Doc: {request_rel}"
    marker_index = None
    for index, line in enumerate(lines):
        if marker in line:
            marker_index = index
            break
    if marker_index is None:
        return {}

    state_index = None
    for index in range(marker_index, max(-1, marker_index - 140), -1):
        if lines[index].strip().lower() == "state summary":
            state_index = index + 1
            break
    if state_index is None:
        return {}

    block: dict[str, str] = {}
    for line in lines[state_index : marker_index + 1]:
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        match = re.match(r"^-\s*([^:]+):\s*(.*)$", stripped)
        if match:
            block[match.group(1).strip()] = match.group(2).strip()
    return block


def update_field(summary: dict[str, str]) -> str | None:
    for field in UPDATE_FIELDS:
        if field in summary:
            return field
    return None


def resolve_request_path(root: Path, config: dict[str, Any], args: argparse.Namespace) -> Path:
    if args.request:
        request = Path(args.request)
        return request if request.is_absolute() else root / request
    if args.request_id:
        paths = config["paths"]
        in_progress = root / repo_path(paths["inProgress"]) / f"{args.request_id}.md"
        completed = root / repo_path(paths["completed"]) / f"{args.request_id}.md"
        if in_progress.exists():
            return in_progress
        return completed
    raise ValueError("Provide --request or --request-id")


def audit_request(root: Path, config: dict[str, Any], request_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not request_path.exists():
        return [f"Request doc not found: {request_path}"], warnings

    text = request_path.read_text(encoding="utf-8", errors="replace")
    summary = parse_state_summary(text)
    if not summary:
        return ["Missing State Summary block in request doc."], warnings

    for key in REQUIRED_KEYS:
        if key not in summary:
            errors.append(f"Missing required State Summary field: {key}")

    updates = update_field(summary)
    if updates is None:
        errors.append("Missing required State Summary field: Project Ops / Roadmap Updates (timestamped)")

    phase = summary.get("Phase", "").strip().upper()
    if phase and phase not in PHASES:
        errors.append(f"Invalid phase '{summary.get('Phase')}'. Expected one of: {', '.join(sorted(PHASES))}")

    for key in ("Last Step Outcome", updates):
        if key and summary.get(key) and not TIMESTAMP_RE.search(summary[key]):
            errors.append(f"Missing timestamp in field '{key}'.")

    paths = config["paths"]
    validation = config.get("validation", {})
    require_roadmap = bool(validation.get("requireRoadmapParity", True))
    require_changelog = bool(validation.get("requireChangelog", True))

    rel = request_path.relative_to(root).as_posix()
    roadmap = root / repo_path(paths["roadmap"])
    if not roadmap.exists():
        if require_roadmap:
            errors.append(f"Missing {paths['roadmap']}")
    else:
        roadmap_block = find_roadmap_block(roadmap.read_text(encoding="utf-8", errors="replace"), rel)
        if not roadmap_block:
            errors.append(f"Roadmap entry not found or missing State Summary block for Request Doc: {rel}")
        else:
            for key in (
                "Phase",
                "Status",
                "Steps Complete",
                "Progress",
                "Last Step Outcome",
                "Next Step",
                "Dependencies / Overlap",
                "Blocking Issues / Unknowns",
                "Impact / Priority Notes",
                "Resume From",
            ):
                if key in summary and key in roadmap_block and summary[key] != roadmap_block[key]:
                    errors.append(f"Roadmap parity mismatch for '{key}'.")
            if updates and updates in roadmap_block and summary[updates] != roadmap_block[updates]:
                errors.append(f"Roadmap parity mismatch for '{updates}'.")

    changelog = root / repo_path(paths["changelog"])
    if not changelog.exists():
        if require_changelog:
            errors.append(f"Missing {paths['changelog']}")
    else:
        changelog_text = changelog.read_text(encoding="utf-8", errors="replace")
        if request_path.stem not in changelog_text:
            warnings.append(f"No changelog entry found containing request id '{request_path.stem}'.")

    in_progress = repo_path(paths["inProgress"]).as_posix().rstrip("/")
    if phase == "COMPLETE" and rel.startswith(f"{in_progress}/"):
        errors.append("Path mismatch: COMPLETE phase doc still under in_progress/.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Project Ops request artifact.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Adopter repository root.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Config path relative to --repo.")
    parser.add_argument("--request", help="Request doc path relative to repo root.")
    parser.add_argument("--request-id", help="Request id / filename stem.")
    args = parser.parse_args()

    root = args.repo.resolve()
    try:
        config = load_config(root, args.config)
        request_path = resolve_request_path(root, config, args)
        errors, warnings = audit_request(root, config, request_path)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    rel = request_path.relative_to(root).as_posix() if request_path.exists() else str(request_path)
    print(f"Project Ops request audit: {rel}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Result: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"Result: PASS (0 errors, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
