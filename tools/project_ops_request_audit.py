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
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
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
READY_PHASES = {
    "EXECUTION",
    "VALIDATION",
    "DOC_SYNC",
    "POST_MORTEM",
    "COMPLETE",
}
REQUIRED_KEYS = (
    "Request ID",
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
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
UNRESOLVED_RE = re.compile(
    r"^(?:tbd|todo|unknown|unresolved|pending|needs?\s+clarification|not\s+(?:set|filled)|missing)\b",
    re.IGNORECASE,
)
READINESS_SUMMARY_KEYS = (
    "Primary Scope",
    "Secondary Scopes",
    "Priority Score",
    "Priority Lane",
    "Ready State",
    "Ready Gate",
)
READINESS_SECTION_FIELDS = {
    "Milestone Synthesis": (
        "Milestone ID",
        "Milestone Name",
        "Milestone Type",
        "Source Requests",
        "Outcome Statement (Done When)",
        "KPI / Success Signal",
        "Target Window",
        "Dependency Gates",
        "Contract Surfaces",
        "Risk Posture",
        "Goal",
        "Non-Goals",
        "Owner",
    ),
    "Roadmap Overlap Review": (
        "Existing roadmap entries checked",
        "Related active requests",
        "Duplicate risk",
        "Merge / split decision",
        "Priority conflict",
    ),
    "Prioritization": (
        "Policy Source",
        "Priority Score",
        "Priority Lane",
        "Due Date / Timing Driver",
        "Sort Key",
        "Override",
    ),
    "Definition Of Ready": (
        "Ready State",
        "Ready Date",
        "Ready Owner",
        "Ready Exceptions",
        "Decision Links",
    ),
    "Complexity": (
        "Level",
        "Predicted Count",
        "Count Drivers",
        "Drivers",
        "Confidence",
    ),
    "Intake": (
        "User Request",
        "Context",
        "Acceptance Signal",
    ),
    "Form": (
        "Problem Statement",
        "User / Operational Value",
        "Change Type",
        "Execution Mode",
        "Acceptance Criteria",
        "Constraints",
        "Must Not Change",
        "Allowed To Change",
        "Inputs Needed",
    ),
    "Analysis": (
        "Touch Map",
        "Risks",
        "Alternatives Considered",
    ),
    "Plan": (
        "Steps",
        "Validation Plan",
        "Rollback / Stop Conditions",
    ),
}


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


def parse_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items()}


def parse_bullet_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        match = re.match(r"^-\s*([^:]+):\s*(.*)$", stripped)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def is_unresolved_value(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    if PLACEHOLDER_RE.search(stripped):
        return True
    if "??" in stripped:
        return True
    return bool(UNRESOLVED_RE.search(stripped))


def is_blocked_decision_value(value: str | None) -> bool:
    if not value:
        return False
    lowered = value.strip().lower()
    if lowered in {"n/a", "na", "none"}:
        return False
    return "blocked" in lowered or "draft" in lowered or "proposed" in lowered or "pending" in lowered


def add_readiness_field_error(errors: list[str], label: str, value: str | None) -> None:
    if value is None:
        errors.append(f"Missing readiness field before EXECUTION: {label}")
    elif is_unresolved_value(value):
        errors.append(f"Unresolved readiness field before EXECUTION: {label}")


def audit_task_graph_readiness(section: str | None, errors: list[str]) -> None:
    if section is None:
        errors.append("Missing readiness section before EXECUTION: Task Graph")
        return

    data_rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        first_cell = cells[0].lower()
        if first_cell == "task id" or all(set(cell) <= {"-", " "} for cell in cells):
            continue
        data_rows.append(cells)

    if not data_rows:
        errors.append("Missing readiness task graph before EXECUTION: Task Graph has no task rows")
        return

    for row_index, cells in enumerate(data_rows, start=1):
        for cell in cells:
            if is_unresolved_value(cell):
                errors.append(f"Unresolved readiness task graph before EXECUTION: row {row_index}")
                return


def audit_definition_of_ready(summary: dict[str, str], text: str, errors: list[str]) -> None:
    phase = summary.get("Phase", "").strip().upper()
    if phase not in READY_PHASES:
        return

    for key in READINESS_SUMMARY_KEYS:
        add_readiness_field_error(errors, f"State Summary -> {key}", summary.get(key))
    if summary.get("Ready State", "").strip().lower() != "ready":
        errors.append("Definition of Ready not satisfied before EXECUTION: State Summary -> Ready State must be Ready")

    sections = parse_markdown_sections(text)
    definition_fields: dict[str, str] = {}
    for section_name, fields in READINESS_SECTION_FIELDS.items():
        section = sections.get(section_name)
        if section is None:
            errors.append(f"Missing readiness section before EXECUTION: {section_name}")
            continue
        section_fields = parse_bullet_fields(section)
        if section_name == "Definition Of Ready":
            definition_fields = section_fields
        for field in fields:
            add_readiness_field_error(errors, f"{section_name} -> {field}", section_fields.get(field))
        if section_name == "Definition Of Ready" and section_fields.get("Ready State", "").strip().lower() != "ready":
            errors.append("Definition of Ready not satisfied before EXECUTION: Definition Of Ready -> Ready State must be Ready")
    if summary.get("Ready State", "").strip().lower() == "ready" and is_blocked_decision_value(
        definition_fields.get("Decision Links")
    ):
        errors.append("Definition of Ready not satisfied before EXECUTION: decision links still indicate a blocker")

    audit_task_graph_readiness(sections.get("Task Graph"), errors)


def audit_request_id(summary: dict[str, str], request_path: Path, errors: list[str]) -> None:
    request_id = summary.get("Request ID", "").strip()
    if not request_id:
        return
    if not REQUEST_ID_RE.match(request_id):
        errors.append("Request ID must be lowercase filename-safe text")
    if request_id != request_path.stem:
        errors.append(f"Request ID mismatch: State Summary has '{request_id}' but filename stem is '{request_path.stem}'")


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
    audit_request_id(summary, request_path, errors)

    updates = update_field(summary)
    if updates is None:
        errors.append("Missing required State Summary field: Project Ops / Roadmap Updates (timestamped)")

    phase = summary.get("Phase", "").strip().upper()
    if phase and phase not in PHASES:
        errors.append(f"Invalid phase '{summary.get('Phase')}'. Expected one of: {', '.join(sorted(PHASES))}")

    for key in ("Last Step Outcome", updates):
        if key and summary.get(key) and not TIMESTAMP_RE.search(summary[key]):
            errors.append(f"Missing timestamp in field '{key}'.")

    audit_definition_of_ready(summary, text, errors)

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
                "Request ID",
                "Phase",
                "Status",
                "Steps Complete",
                "Progress",
                "Last Step Outcome",
                "Next Step",
                "Dependencies / Overlap",
                "Primary Scope",
                "Secondary Scopes",
                "Blocking Issues / Unknowns",
                "Impact / Priority Notes",
                "Priority Score",
                "Priority Lane",
                "Ready State",
                "Ready Gate",
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
        request_id = summary.get("Request ID", request_path.stem)
        if request_id not in changelog_text:
            warnings.append(f"No changelog entry found containing request id '{request_id}'.")

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
