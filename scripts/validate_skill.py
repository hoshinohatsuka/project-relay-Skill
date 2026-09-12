#!/usr/bin/env python3
"""Offline structural validation for the project-relay package.

This validates only packaged, machine-checkable contracts. It deliberately
does not claim to execute an agent, trigger a host router, or validate an
untrusted target repository.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "SKILL.md", "manifest.json", "agents/interface.yaml",
    "evals/trigger_cases.json", "scripts/validate_run.py",
    "scripts/validate_skill.py", "scripts/evaluate_triggers.py",
    "evals/EVALUATION_PLAN.md", "evals/scenario_matrix.json",
)
REQUIRED_MODE_MARKERS = ("模式A", "模式B", "模式C", "续跑")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return payload


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    manifest = load_json(ROOT / "manifest.json", errors)
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").is_file() else ""
    interface = (ROOT / "agents/interface.yaml").read_text(encoding="utf-8") if (ROOT / "agents/interface.yaml").is_file() else ""
    trigger_cases = load_json(ROOT / "evals/trigger_cases.json", errors)
    scenarios = load_json(ROOT / "evals/scenario_matrix.json", errors)

    frontmatter = re.search(r"^---\s*$([\s\S]*?)^---\s*$", skill, re.MULTILINE)
    version = re.search(r'^\s*version:\s*["\']?([^"\'\s]+)', frontmatter.group(1) if frontmatter else "", re.MULTILINE)
    if not frontmatter:
        errors.append("SKILL.md has no YAML front matter")
    if not version:
        errors.append("SKILL.md front matter has no version")
    elif version.group(1) != manifest.get("version"):
        errors.append("SKILL.md and manifest.json versions differ")
    for marker in REQUIRED_MODE_MARKERS:
        if marker not in skill:
            errors.append(f"SKILL.md missing workflow marker: {marker}")
    for token in ("display_name:", "modes:", "- id: teardown", "- id: handoff", "- id: freeze", "- id: resume"):
        if token not in interface:
            errors.append(f"interface.yaml missing declared interface token: {token}")
    gates = manifest.get("release_gates")
    if not isinstance(gates, dict):
        errors.append("manifest.json release_gates must be an object")
    elif "validate_skill.py" not in str(gates.get("validate_skill", "")):
        errors.append("manifest validate_skill gate does not name validate_skill.py")
    for section in ("should_trigger", "should_not_trigger", "near_neighbor"):
        if not isinstance(trigger_cases.get(section), list) or not trigger_cases[section]:
            errors.append(f"trigger_cases.json missing nonempty {section}")
    cases = scenarios.get("cases")
    modes = {case.get("mode") for case in cases} if isinstance(cases, list) else set()
    if not {"A", "B", "C", "resume"}.issubset(modes):
        errors.append("scenario matrix does not cover modes A, B, C, and resume")

    result = {"ok": not errors, "errors": errors, "version": manifest.get("version")}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
