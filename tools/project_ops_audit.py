#!/usr/bin/env python3
"""Audit a project for Project Ops adoption readiness.

This tool is intentionally read-only. It reports whether a repository has the
configured Project Ops files, directories, privacy posture, and starter process
surfaces needed for a durable docs/execution workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(".project_ops/config.json")
REQUIRED_TOP_LEVEL = ("project", "paths", "scopeLabels", "requiredDocs", "privacy", "validation")
REQUIRED_PROJECT_KEYS = ("id", "name", "role")
REQUIRED_PATH_KEYS = ("roadmap", "inProgress", "completed", "reports", "changelog", "governance", "requestTemplate")
REQUIRED_PRIVACY_KEYS = ("defaultVisibility", "publicExamplesRequireSanitization")
REQUIRED_VALIDATION_KEYS = ("requireChangelog", "requireRoadmapParity", "dryRunByDefault")


def is_repo_relative(path: str) -> bool:
    candidate = Path(path)
    return not candidate.is_absolute() and ".." not in candidate.parts and path.strip() != ""


def as_repo_path(path: str) -> Path:
    if not is_repo_relative(path):
        raise ValueError(f"Path must be repo-relative: {path}")
    return Path(path)


def load_config(config_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not config_path.exists():
        return None, f"Missing Project Ops config: {config_path}"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {config_path}: {exc}"
    if not isinstance(data, dict):
        return None, f"Config root must be an object: {config_path}"
    return data, None


def require_object(config: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = config.get(key)
    if not isinstance(value, dict):
        errors.append(f"Missing object: {key}")
        return {}
    return value


def require_string_list(config: dict[str, Any], key: str, errors: list[str]) -> list[str]:
    value = config.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"Missing string array: {key}")
        return []
    return value


def audit_config_shape(config: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in config:
            errors.append(f"Missing top-level config key: {key}")

    project = require_object(config, "project", errors)
    for key in REQUIRED_PROJECT_KEYS:
        if not isinstance(project.get(key), str) or not project.get(key):
            errors.append(f"Missing project.{key}")

    paths = require_object(config, "paths", errors)
    for key in REQUIRED_PATH_KEYS:
        value = paths.get(key)
        if not isinstance(value, str):
            errors.append(f"Missing paths.{key}")
        elif not is_repo_relative(value):
            errors.append(f"paths.{key} must be repo-relative: {value}")
    for key, value in paths.items():
        if isinstance(value, str) and not is_repo_relative(value):
            errors.append(f"paths.{key} must be repo-relative: {value}")

    scope_labels = require_string_list(config, "scopeLabels", errors)
    if len(scope_labels) != len(set(scope_labels)):
        errors.append("scopeLabels must be unique")

    for path in require_string_list(config, "requiredDocs", errors):
        if not is_repo_relative(path):
            errors.append(f"requiredDocs entry must be repo-relative: {path}")

    privacy = require_object(config, "privacy", errors)
    for key in REQUIRED_PRIVACY_KEYS:
        if key not in privacy:
            errors.append(f"Missing privacy.{key}")
    if privacy.get("defaultVisibility") not in ("public", "internal", "local-private"):
        errors.append("privacy.defaultVisibility must be public, internal, or local-private")
    if privacy.get("defaultVisibility") == "public" and not privacy.get("publicExamplesRequireSanitization"):
        warnings.append("Public projects should keep privacy.publicExamplesRequireSanitization=true")
    private_paths = privacy.get("privateHistoryPaths", [])
    if private_paths is not None and (
        not isinstance(private_paths, list) or not all(isinstance(item, str) for item in private_paths)
    ):
        errors.append("privacy.privateHistoryPaths must be a string array when present")

    validation = require_object(config, "validation", errors)
    for key in REQUIRED_VALIDATION_KEYS:
        if not isinstance(validation.get(key), bool):
            errors.append(f"Missing boolean validation.{key}")
    if validation.get("dryRunByDefault") is False:
        warnings.append("Reusable Project Ops workflows should default to dry-run behavior")

    bootstrap = config.get("bootstrap", {})
    if bootstrap and not isinstance(bootstrap, dict):
        errors.append("bootstrap must be an object when present")
    if isinstance(bootstrap, dict):
        for list_key in ("requiredFiles", "recommendedFiles", "initialDirectories"):
            value = bootstrap.get(list_key, [])
            if value is not None and (
                not isinstance(value, list) or not all(isinstance(item, str) for item in value)
            ):
                errors.append(f"bootstrap.{list_key} must be a string array when present")

    commands = validation.get("commands", [])
    if commands is not None and (
        not isinstance(commands, list)
        or not all(isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("command"), str) for item in commands)
    ):
        errors.append("validation.commands must be an array of objects with string name and command")

    return errors, warnings


def audit_repo(root: Path, config: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required_docs = config.get("requiredDocs", [])
    for item in required_docs:
        try:
            path = root / as_repo_path(item)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.exists():
            errors.append(f"Missing required doc/file: {item}")

    paths = config.get("paths", {})
    directory_keys = {"inProgress", "completed", "reports", "governance", "templateRoot"}
    for key, raw in paths.items():
        if not isinstance(raw, str) or not is_repo_relative(raw):
            continue
        path = root / Path(raw)
        if not path.exists():
            warnings.append(f"Configured path does not exist: paths.{key}={raw}")
        elif key in directory_keys and not path.is_dir():
            errors.append(f"Configured path should be a directory: paths.{key}={raw}")
        elif key not in directory_keys and path.is_dir():
            errors.append(f"Configured path should be a file: paths.{key}={raw}")

    bootstrap = config.get("bootstrap", {})
    if isinstance(bootstrap, dict):
        for item in bootstrap.get("requiredFiles", []):
            if is_repo_relative(item) and not (root / Path(item)).exists():
                errors.append(f"Missing bootstrap required file: {item}")
        for item in bootstrap.get("initialDirectories", []):
            if is_repo_relative(item) and not (root / Path(item)).exists():
                warnings.append(f"Missing bootstrap directory: {item}")

    return errors, warnings


def print_text(project: str, root: Path, errors: list[str], warnings: list[str]) -> None:
    print(f"Project Ops audit: {project}")
    print(f"repo: {root}")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"Result: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
    else:
        print(f"Result: PASS (0 errors, {len(warnings)} warning(s))")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a repository for Project Ops adoption readiness.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Adopter repository root.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Config path relative to --repo.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    root = args.repo.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    config, load_error = load_config(config_path)
    errors: list[str] = []
    warnings: list[str] = []

    if load_error:
        errors.append(load_error)
        project_name = "<unknown>"
    else:
        assert config is not None
        shape_errors, shape_warnings = audit_config_shape(config)
        repo_errors, repo_warnings = audit_repo(root, config)
        errors.extend(shape_errors)
        errors.extend(repo_errors)
        warnings.extend(shape_warnings)
        warnings.extend(repo_warnings)
        project = config.get("project", {})
        project_name = project.get("name", project.get("id", "<unknown>")) if isinstance(project, dict) else "<unknown>"

    if args.json:
        print(json.dumps({"project": project_name, "repo": str(root), "errors": errors, "warnings": warnings}, indent=2))
    else:
        print_text(project_name, root, errors, warnings)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
