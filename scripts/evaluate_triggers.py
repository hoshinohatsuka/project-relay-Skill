#!/usr/bin/env python3
"""Run the documented lexical trigger contract deterministically.

This is a regression check for the local rubric, not evidence of a host
router's semantic matching behavior.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def contains_any(text: str, words: list[str]) -> bool:
    normalized = text.casefold()
    return any(word.casefold() in normalized for word in words)


def score_case(text: str, concepts: dict[str, list[str]]) -> tuple[float, list[str]]:
    matched = sorted(name for name, words in concepts.items() if contains_any(text, words))
    return len(matched) / len(concepts), matched


def main() -> int:
    # PowerShell hosts may expose a legacy console encoding. The fixtures include
    # Chinese prompts, so the evaluator must be able to preserve raw evidence.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    spec = json.loads((ROOT / "evals/trigger_cases.json").read_text(encoding="utf-8"))
    concepts = spec["positive_concepts"]
    threshold = float(spec["recommended_threshold"])
    results = []
    failures = []
    for group, expected in (("should_trigger", True), ("should_not_trigger", False), ("near_neighbor", False)):
        for case in spec[group]:
            text = case["text"]
            score, matched = score_case(text, concepts)
            negative = next((item for item in spec["negative_patterns"] if item.casefold() in text.casefold()), None)
            # A two-concept prompt is the intended minimum positive signal.
            # Six concept groups make that score exactly 2/6, not 0.34.
            predicted = score + 1e-12 >= threshold and negative is None
            passed = predicted == expected
            record = {"family": case["family"], "expected_trigger": expected, "predicted_trigger": predicted, "passed": passed, "score": score, "matched_concepts": matched, "negative_pattern": negative}
            results.append(record)
            if not passed:
                failures.append(record)
    output = {"ok": not failures, "threshold": threshold, "total": len(results), "passed": len(results) - len(failures), "failures": failures, "results": results, "scope": "lexical contract only; host routing is not evaluated"}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
