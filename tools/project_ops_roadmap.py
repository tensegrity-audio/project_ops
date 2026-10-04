#!/usr/bin/env python3
"""Check Project Ops request artifacts against roadmap entries.

The command is read-only. It reads an adopter repository's
`.project_ops/config.json`, collects request docs from the configured
in-progress and completed request directories, and verifies that each request
has a matching roadmap entry with the same State Summary block.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(".project_ops/config.json")
REQUEST_PATH_KEYS = ("inProgress", "completed")
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
REQUEST_DOC_RE = re.compile(r"^\s*-?\s*Request Doc:\s*(?P<path>.+?)\s*$", re.IGNORECASE)
FIELD_RE = re.compile(r"^-\s*([^:]+):\s*(.*)$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S")


@dataclass(frozen=True)
class RequestDoc:
    path: Path
    rel: str
    bucket: str
    summary: dict[str, str]


@dataclass(frozen=True)
class RoadmapEntry:
    request_doc: str
    line: int
    summary: dict[str, str]


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts or not str(path).strip():
        raise ValueError(f"Project Ops config path must be repo-relative: {candidate.as_posix()}")
    return candidate


def as_posix_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


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
    for key in ("roadmap", *REQUEST_PATH_KEYS):
        value = paths.get(key)
        if not isinstance(value, str):
            raise ValueError(f"Project Ops config missing paths.{key}")
        repo_path(value)
    if isinstance(paths.get("requestTemplate"), str):
        repo_path(paths["requestTemplate"])

    return data


def is_state_summary_heading(line: str) -> bool:
    return line.strip().lstrip("#").strip().lower() == "state summary"


def is_markdown_heading(line: str) -> bool:
    return bool(HEADING_RE.match(line))


def parse_state_summary(text: str) -> dict[str, str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if is_state_summary_heading(line):
            return parse_state_summary_lines(lines, index + 1)
    return {}


def parse_state_summary_lines(lines: list[str], start: int) -> dict[str, str]:
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
        match = FIELD_RE.match(stripped)
        if match:
            summary[match.group(1).strip()] = match.group(2).strip()
    return summary


def state_summary_before(lines: list[str], marker_index: int) -> dict[str, str]:
    for index in range(marker_index, max(-1, marker_index - 160), -1):
        if is_state_summary_heading(lines[index]):
            return parse_state_summary_lines(lines, index + 1)
        if index != marker_index and is_markdown_heading(lines[index]):
            return {}
    return {}


def normalize_request_doc(value: str) -> str:
    normalized = value.strip().strip("`").strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.replace("\\", "/")


def collect_request_docs(root: Path, config: dict[str, Any]) -> tuple[list[RequestDoc], list[str]]:
    paths = config["paths"]
    errors: list[str] = []
    docs: list[RequestDoc] = []
    template_rel = None
    if isinstance(paths.get("requestTemplate"), str):
        template_rel = repo_path(paths["requestTemplate"]).as_posix()

    for key in REQUEST_PATH_KEYS:
        directory_rel = repo_path(paths[key])
        directory = root / directory_rel
        if not directory.exists():
            errors.append(f"Configured request path does not exist: paths.{key}={directory_rel.as_posix()}")
            continue
        if not directory.is_dir():
            errors.append(f"Configured request path is not a directory: paths.{key}={directory_rel.as_posix()}")
            continue

        for path in sorted(directory.rglob("*.md")):
            rel = as_posix_rel(path, root)
            if rel == template_rel or path.name.startswith("_") or path.name.startswith("."):
                continue
            docs.append(
                RequestDoc(
                    path=path,
                    rel=rel,
                    bucket=key,
                    summary=parse_state_summary(path.read_text(encoding="utf-8", errors="replace")),
                )
            )

    return docs, errors


def collect_roadmap_entries(roadmap_text: str) -> dict[str, list[RoadmapEntry]]:
    lines = roadmap_text.splitlines()
    entries: dict[str, list[RoadmapEntry]] = {}
    for index, line in enumerate(lines):
        match = REQUEST_DOC_RE.match(line)
        if not match:
            continue
        request_doc = normalize_request_doc(match.group("path"))
        if request_doc.lower() in {"n/a", "na", "<path or n/a>"}:
            continue
        entry = RoadmapEntry(
            request_doc=request_doc,
            line=index + 1,
            summary=state_summary_before(lines, index),
        )
        entries.setdefault(request_doc, []).append(entry)
    return entries


def short_value(value: str | None) -> str:
    if value is None:
        return "<missing>"
    if len(value) <= 96:
        return value
    return f"{value[:93]}..."


def compare_summaries(request: RequestDoc, roadmap: RoadmapEntry) -> list[str]:
    errors: list[str] = []
    if not request.summary:
        errors.append(f"Missing State Summary block in request doc: {request.rel}")
        return errors
    if not roadmap.summary:
        errors.append(
            f"Roadmap entry for Request Doc: {request.rel} is missing a State Summary block near line {roadmap.line}"
        )
        return errors

    for field in sorted(set(request.summary) | set(roadmap.summary)):
        request_value = request.summary.get(field)
        roadmap_value = roadmap.summary.get(field)
        if request_value == roadmap_value:
            continue
        errors.append(
            "State Summary mismatch for "
            f"{request.rel} field '{field}': "
            f"request='{short_value(request_value)}' roadmap='{short_value(roadmap_value)}'"
        )
    return errors


def audit_request_id(request: RequestDoc) -> list[str]:
    errors: list[str] = []
    request_id = request.summary.get("Request ID", "").strip()
    if not request_id:
        return [f"Missing Request ID in State Summary: {request.rel}"]
    if not REQUEST_ID_RE.match(request_id):
        errors.append(f"Request ID must be lowercase filename-safe text in {request.rel}: {request_id}")
    if request_id != request.path.stem:
        errors.append(f"Request ID mismatch in {request.rel}: State Summary has '{request_id}' but filename stem is '{request.path.stem}'")
    return errors


def project_name(config: dict[str, Any]) -> str:
    project = config.get("project", {})
    if isinstance(project, dict):
        value = project.get("name") or project.get("id")
        if isinstance(value, str) and value:
            return value
    return "<unknown>"


def check_roadmap(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    paths = config["paths"]
    errors: list[str] = []
    warnings: list[str] = []
    requests, request_errors = collect_request_docs(root, config)
    errors.extend(request_errors)

    roadmap_rel = repo_path(paths["roadmap"]).as_posix()
    roadmap_path = root / repo_path(paths["roadmap"])
    if not roadmap_path.exists():
        errors.append(f"Missing roadmap file: {roadmap_rel}")
        entries: dict[str, list[RoadmapEntry]] = {}
    elif not roadmap_path.is_file():
        errors.append(f"Configured roadmap path is not a file: {roadmap_rel}")
        entries = {}
    else:
        entries = collect_roadmap_entries(roadmap_path.read_text(encoding="utf-8", errors="replace"))

    request_refs = {request.rel for request in requests}
    for request in requests:
        if not request.summary:
            errors.append(f"Missing State Summary block in request doc: {request.rel}")
            continue
        errors.extend(audit_request_id(request))
        matches = entries.get(request.rel, [])
        if not matches:
            errors.append(f"Missing roadmap entry for Request Doc: {request.rel}")
            continue
        if len(matches) > 1:
            lines = ", ".join(str(entry.line) for entry in matches)
            errors.append(f"Duplicate roadmap entries for Request Doc: {request.rel} at lines {lines}")
            continue
        errors.extend(compare_summaries(request, matches[0]))

    for request_doc, roadmap_entries in sorted(entries.items()):
        if request_doc not in request_refs:
            lines = ", ".join(str(entry.line) for entry in roadmap_entries)
            warnings.append(f"Roadmap entry references missing request doc: {request_doc} at line(s) {lines}")

    counts = {key: sum(1 for request in requests if request.bucket == key) for key in REQUEST_PATH_KEYS}
    return {
        "project": project_name(config),
        "repo": str(root),
        "roadmap": roadmap_rel,
        "requestCount": len(requests),
        "requestBuckets": counts,
        "requests": [{"path": request.rel, "bucket": request.bucket} for request in requests],
        "errors": errors,
        "warnings": warnings,
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"Project Ops roadmap check: {result['project']}")
    print(f"repo: {result['repo']}")
    print(f"roadmap: {result['roadmap']}")
    buckets = result["requestBuckets"]
    print(
        "requests: "
        f"{result['requestCount']} "
        f"(inProgress: {buckets.get('inProgress', 0)}, completed: {buckets.get('completed', 0)})"
    )
    for warning in result["warnings"]:
        print(f"WARN: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    if result["errors"]:
        print(f"Result: FAIL ({len(result['errors'])} error(s), {len(result['warnings'])} warning(s))")
    else:
        print(f"Result: PASS (0 errors, {len(result['warnings'])} warning(s))")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Project Ops roadmap parity without modifying files.")
    parser.add_argument("mode", nargs="?", choices=("check",), default="check", help="Run the read-only check mode.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Adopter repository root.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Config path relative to --repo.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    root = args.repo.resolve()
    try:
        config = load_config(root, args.config)
        result = check_roadmap(root, config)
    except (ValueError, json.JSONDecodeError) as exc:
        if args.json:
            print(json.dumps({"errors": [str(exc)], "warnings": []}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
