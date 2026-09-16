#!/usr/bin/env python3
"""Validate a project-relay run directory's blackboard state files.

Standard library only. Never clones, executes target code, or accesses the
network — it only checks local JSON/JSONL integrity, enum states, required
fields, and that every referenced artifact path stays inside the run root.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TASK_STATES = {"pending", "claimed", "done", "blocked", "failed"}
EVIDENCE_KINDS = {"code", "community", "doc", "inference"}
REQUIRED_MANIFEST_KEYS = ("schema_version", "skill_version", "run_id", "mode", "target", "tier", "status")

# 显式状态机转移表（模式D 借鉴点 B4：思路源自 aif-handoff stateMachine，仅理念不抄代码）。
# 规则：pending 未领取；claimed 单租约持有；blocked/failed 必须带 reason；done 为终态。
# 离开 blocked/failed 回到工作态时必须复位残留状态（reason 等）——复位纪律由协议与模板强制。
TASK_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"claimed", "blocked", "failed"},
    "claimed": {"done", "blocked", "failed"},
    "blocked": {"pending", "claimed"},
    "failed": {"pending", "claimed"},
    "done": set(),
}
# 结构化拒绝码（协议层枚举，与 stateMachine 的 denied code 思路同源）。
TRANSITION_DENIED_CODES = (
    "action_not_allowed",
    "status_conflict",
    "revision_conflict",
    "assignment_required",
    "blocked_status_missing",
)
# evidence-ledger 可选审计字段（模式D 借鉴点 B5：思路源自 audit.ts 的全字段快照，仅理念不抄代码）。
EVIDENCE_AUDIT_FIELDS = ("actor", "status_snapshot", "from_status", "to_status")


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(errors, f"missing file: {path.name}")
        return {}
    except json.JSONDecodeError as exc:
        fail(errors, f"{path.name}: invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        fail(errors, f"{path.name}: expected JSON object")
        return {}
    return payload


def inside_root(root: Path, candidate: Path) -> bool:
    try:
        resolved = candidate.resolve()
        root_resolved = root.resolve()
        return resolved == root_resolved or root_resolved in resolved.parents
    except OSError:
        return False


def check_manifest(root: Path, errors: list[str]) -> dict:
    manifest = load_json(root / "run-manifest.json", errors)
    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest or manifest.get(key) in (None, ""):
            fail(errors, f"run-manifest.json missing field: {key}")
    target = manifest.get("target")
    if isinstance(target, dict):
        if not target.get("commit_sha"):
            fail(errors, "run-manifest.json target.commit_sha missing — evidence must bind to a SHA")
    else:
        fail(errors, "run-manifest.json target must be an object")
    schema = str(manifest.get("schema_version", ""))
    if schema and not schema.startswith("2."):
        fail(errors, f"unsupported schema_version {schema!r}: refuse auto-resume, migrate first")
    return manifest


def check_tasks(root: Path, errors: list[str]) -> None:
    path = root / "task-ledger.json"
    if not path.exists():
        fail(errors, "missing file: task-ledger.json")
        return
    payload = load_json(path, errors)
    tasks = payload.get("tasks")
    if not isinstance(tasks, list):
        fail(errors, "task-ledger.json: 'tasks' must be a list")
        return
    seen: set[str] = set()
    for task in tasks:
        tid = str(task.get("id", ""))
        if not tid:
            fail(errors, "task missing id")
            continue
        if tid in seen:
            fail(errors, f"duplicate task id: {tid}")
        seen.add(tid)
        status = task.get("status")
        if status not in TASK_STATES:
            fail(errors, f"task {tid}: illegal status {status!r}")
        if status == "done":
            out = task.get("output_path")
            if not out:
                fail(errors, f"task {tid}: done without output_path")
            else:
                out_path = root / out
                if not inside_root(root, out_path):
                    fail(errors, f"task {tid}: output_path escapes run root: {out}")
                elif not out_path.exists():
                    fail(errors, f"task {tid}: output_path does not exist: {out}")
        if status in ("blocked", "failed") and not task.get("reason"):
            fail(errors, f"task {tid}: {status} without reason")
        check_task_transitions(task, tid, errors)


def check_task_transitions(task: dict, tid: str, errors: list[str]) -> None:
    """校验任务的状态机转移链（B4，借鉴 aif-handoff stateMachine 理念）。

    可选字段 `transitions`：前序转移链 `[{"from": ..., "to": ..., "by": ..., "at": ...}, ...]`。
    仅当存在时校验：每个转移的 from/to 组合必须合法；终态 done 之后不得再有转移；
    最后一条的 to 必须与当前 status 一致。旧 run（无该字段）向后兼容。
    """
    transitions = task.get("transitions")
    if not isinstance(transitions, list):
        return
    if not transitions:
        fail(errors, f"task {tid}: transitions present but empty")
        return
    for i, move in enumerate(transitions, 1):
        if not isinstance(move, dict):
            fail(errors, f"task {tid}: transitions[{i}] must be an object")
            continue
        frm = move.get("from")
        to = move.get("to")
        if frm not in TASK_STATES or to not in TASK_STATES:
            fail(errors, f"task {tid}: transitions[{i}] illegal state pair {frm!r} -> {to!r}")
            continue
        if to not in TASK_TRANSITIONS.get(frm):
            fail(errors, f"task {tid}: transitions[{i}] illegal transition {frm} -> {to}")
    last = transitions[-1]
    if isinstance(last, dict) and last.get("to") != task.get("status"):
        fail(errors, f"task {tid}: last transition to={last.get('to')!r} != current status {task.get('status')!r}")


def check_evidence(root: Path, errors: list[str]) -> int:
    path = root / "evidence-ledger.jsonl"
    if not path.exists():
        fail(errors, "missing file: evidence-ledger.jsonl")
        return 0
    count = 0
    ids: set[str] = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        count += 1
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, f"evidence-ledger.jsonl line {lineno}: invalid JSON: {exc}")
            continue
        eid = str(entry.get("id", ""))
        if not eid:
            fail(errors, f"evidence-ledger.jsonl line {lineno}: missing id")
        elif eid in ids:
            fail(errors, f"evidence-ledger.jsonl line {lineno}: duplicate id {eid}")
        else:
            ids.add(eid)
        kind = entry.get("kind")
        if kind not in EVIDENCE_KINDS:
            fail(errors, f"evidence {eid or lineno}: illegal kind {kind!r}")
        if not entry.get("ref"):
            fail(errors, f"evidence {eid or lineno}: missing ref")
        if kind == "community" and not str(entry.get("ref", "")).startswith("http"):
            fail(errors, f"evidence {eid}: community evidence ref must be a URL")
        if kind == "community" and not entry.get("accessed"):
            fail(errors, f"evidence {eid}: community evidence missing accessed date")
        check_evidence_audit_fields(entry, eid or lineno, errors)
    return count


def check_evidence_audit_fields(entry: dict, label, errors: list[str]) -> None:
    """evidence 可选审计字段（B5，借鉴 aif-handoff audit.ts 的全字段快照理念）。

    字段全部可选：actor（谁写的）、status_snapshot（当时状态快照）、
    from_status/to_status（审计流中的状态变迁标签）。存在时校验类型。
    """
    actor = entry.get("actor")
    if actor is not None and not isinstance(actor, str):
        fail(errors, f"evidence {label}: actor must be a string")
    snapshot = entry.get("status_snapshot")
    if snapshot is not None and not isinstance(snapshot, dict):
        fail(errors, f"evidence {label}: status_snapshot must be an object")
    for fkey in ("from_status", "to_status"):
        value = entry.get(fkey)
        if value is not None and value not in TASK_STATES:
            fail(errors, f"evidence {label}: {fkey} must be one of {sorted(TASK_STATES)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a project-relay run directory (stdlib only, offline).")
    parser.add_argument("run_dir", help="Run directory containing run-manifest.json etc.")
    args = parser.parse_args()

    root = Path(args.run_dir)
    errors: list[str] = []
    if not root.is_dir():
        print(json.dumps({"ok": False, "errors": [f"run dir not found: {root}"]}, ensure_ascii=False))
        raise SystemExit(2)

    manifest = check_manifest(root, errors)
    check_tasks(root, errors)
    evidence_count = check_evidence(root, errors)

    result = {
        "ok": not errors,
        "run_id": manifest.get("run_id"),
        "schema_version": manifest.get("schema_version"),
        "evidence_count": evidence_count,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    sys.exit(main())
