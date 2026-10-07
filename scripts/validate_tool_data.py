"""Validate the central tool catalog and its cross-tool relationships."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "_data" / "tools.yml"

CATEGORIES = {"books", "text", "pronunciation", "speech", "audio", "infrastructure"}
LEVELS = {"workflow", "application", "component", "library", "infrastructure"}
WORKFLOWS = {
    "book-processing",
    "translation",
    "speech",
    "audiobook",
    "speech-development",
    "documentation",
}
STAGES = {"source", "structure", "normalize", "pronounce", "synthesize", "output"}
REQUIRED_FIELDS = {"name", "description", "docs_url", "repo_url"}
RELATION_FIELDS = ("depends_on", "used_by", "related")


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def validate_tool_data(path: Path = DATA_FILE) -> list[str]:
    """Return validation errors for a tool catalog YAML file."""
    try:
        with path.open(encoding="utf-8") as handle:
            tools = yaml.safe_load(handle)
    except OSError as error:
        return [f"{path}: {error}"]
    except yaml.YAMLError as error:
        return [f"{path}: invalid YAML: {error}"]

    if not isinstance(tools, list):
        return [f"{path}: expected a YAML list of tools"]

    errors: list[str] = []
    by_name: dict[str, dict[str, Any]] = {}
    for index, tool in enumerate(tools):
        location = f"tool[{index + 1}]"
        if not isinstance(tool, dict):
            errors.append(f"{location}: expected a mapping")
            continue
        name = tool.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{location}: missing non-empty name")
            continue
        if name in by_name:
            errors.append(f"{location} ({name}): duplicate tool name")
        else:
            by_name[name] = tool

        for field in REQUIRED_FIELDS:
            if not isinstance(tool.get(field), str) or not tool[field].strip():
                errors.append(f"{name}: missing non-empty {field}")

        category = tool.get("category")
        if not isinstance(category, str) or category not in CATEGORIES:
            errors.append(
                f"{name}: category must be one of {', '.join(sorted(CATEGORIES))}"
            )
        level = tool.get("level")
        if not isinstance(level, str) or level not in LEVELS:
            errors.append(f"{name}: level must be one of {', '.join(sorted(LEVELS))}")
        if not isinstance(tool.get("role"), str) or not tool["role"].strip():
            errors.append(f"{name}: missing non-empty role")

        workflows = tool.get("workflows")
        if not _is_string_list(workflows) or not workflows:
            errors.append(f"{name}: workflows must be a non-empty list of workflow IDs")
        else:
            for workflow in workflows:
                if workflow not in WORKFLOWS:
                    errors.append(f"{name}: unknown workflow '{workflow}'")
        stages = tool.get("stages")
        if not _is_string_list(stages):
            errors.append(f"{name}: stages must be a list of stage IDs")
        else:
            for stage in stages:
                if stage not in STAGES:
                    errors.append(f"{name}: unknown workflow stage '{stage}'")

        for field in (*RELATION_FIELDS, "inputs", "outputs"):
            value = tool.get(field, [])
            if not _is_string_list(value):
                errors.append(f"{name}: {field} must be a list of non-empty strings")

        if "start_here" in tool and not isinstance(tool["start_here"], bool):
            errors.append(f"{name}: start_here must be a boolean")

    for name, tool in by_name.items():
        for field in RELATION_FIELDS:
            refs = tool.get(field, [])
            if not _is_string_list(refs):
                continue
            for ref in refs:
                if ref not in by_name:
                    errors.append(f"{name}: {field} references unknown tool '{ref}'")
                elif ref == name:
                    errors.append(f"{name}: {field} must not reference itself")

        for dependency in (tool.get("depends_on", []) if _is_string_list(tool.get("depends_on", [])) else []):
            target = by_name.get(dependency)
            if target is not None and _is_string_list(target.get("used_by", [])) and name not in target.get("used_by", []):
                errors.append(
                    f"{name}: depends_on '{dependency}' but it does not list '{name}' in used_by"
                )
        for consumer in (tool.get("used_by", []) if _is_string_list(tool.get("used_by", [])) else []):
            target = by_name.get(consumer)
            if target is not None and _is_string_list(target.get("depends_on", [])) and name not in target.get("depends_on", []):
                errors.append(
                    f"{name}: used_by '{consumer}' but it does not list '{name}' in depends_on"
                )

    return errors


def main() -> int:
    errors = validate_tool_data()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Tool data validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    with DATA_FILE.open(encoding="utf-8") as handle:
        count = len(yaml.safe_load(handle))
    print(f"Tool data validation passed: {count} tools checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
