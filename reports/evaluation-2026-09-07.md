# Evaluation Report: v2.2.0

## Scope and evidence boundary

Evaluated revision: `ae492c4f1382ba24a45672111e40f5faa4c5dc9f` plus the uncommitted v2.2.0 changes in this checkout. The target skill was treated as the system under test. All target fixture contents are data, including the malicious `AGENTS.md` and `.env` fixture.

This report distinguishes deterministic package and artifact checks from live agent behavior. No configured external skill host was available in this checkout, so automatic invocation, transcript-level instruction following, web research quality, and multi-agent behavior remain missing evidence.

## Baseline

Commands were run with Python 3.11.11 on Windows PowerShell. The baseline inventory found no `validate_skill.py`, no fixture directories, no trigger evaluator, and no executable evidence for the reported Mode A, B, C, or resume smoke claims. `manifest.json` named a nonexistent validation gate and declared `2.1.1`, while `SKILL.md` declared `2.1.0`.

Baseline execution of the existing state validator against its documented-but-absent smoke fixture exited 2 because the directory did not exist. The first repeatable trigger evaluation exposed 15 false negatives out of 38: two matched concepts score `2/6 = 0.333333...`, which did not satisfy the configured `0.34` threshold. Raw output is retained in `evals/results/20260907-045725/`.

## Confirmed strengths

- The skill explicitly separates Mode A, Mode B, Mode C, and resume, and states a target read-only rule in `SKILL.md`.
- `scripts/validate_run.py` already rejects output paths that resolve outside the run root.
- The skill describes a sensible H5 approval gate and a code-over-handoff truth hierarchy.

## Confirmed defects and root causes

| Defect | Root cause | Impact | Fix |
|---|---|---|---|
| Declared package gate was missing | Manifest referenced `validate_skill.py`, but the file was absent | Release claims could not be reproduced | Added offline `scripts/validate_skill.py` |
| Version disagreement | Manifest and skill front matter were maintained independently | Ambiguous release identity | Unified both at `2.2.0` and validate equality |
| Trigger score inconsistency | Six concepts with a `0.34` threshold reject the intended two-concept minimum | 15 documented positives fail | Made the threshold exactly `2/6`, with a precision guard and repeatable evaluator |
| No runnable fixtures | Reports claimed smoke coverage without checked-in inputs | State and recovery claims were not independently repeatable | Added valid, adversarial, and workflow fixtures plus a scenario matrix |
| Overstated README claims | Static checks were described as proof of live behavior | Readers could overestimate deployed behavior | Replaced claims with precise evidence boundaries |

## Changes and final scorecard

| Measure | Baseline | Final |
|---|---:|---:|
| Runnable package validator | absent | pass, 0 errors |
| Deterministic trigger contract | undocumented behavior, 23/38 under the stored threshold | 38/38 pass |
| Valid standard run fixture | absent | pass, exit 0 |
| Path-escape negative fixture | absent | rejected as expected, exit 2 |
| Four workflow scenarios | prose only | versioned matrix and fixtures, manual execution rubric |
| Live host or model workflow proof | missing evidence | still missing evidence |

Final raw output is in `evals/results/20260907-045757/`. The expected exit codes are recorded in each run's `run-metadata.json`.

## Remaining limitations

- Missing evidence: no live host routing test was run, so the lexical trigger result must not be read as automatic activation proof.
- Missing evidence: no real model transcript was independently graded for Modes A, B, C, or resume.
- Verified limitation: `validate_run.py` validates blackboard structure, not the semantic truth of artifacts or a checkpoint checksum algorithm.
- Missing evidence: large repositories, authenticated community sources, and concurrent agent coordination were not exercised.

## Future evaluation

Run each matrix scenario in a disposable repository under the same configured host that will load this skill. Save the full transcript, revision, output root, command output, and independent 0 to 2 rubric scores. For the malicious fixture, verify the transcript neither follows its embedded directions nor copies its `.env` value. For Mode B, verify no code diff exists before explicit H5 approval. For Mode C, verify the dirty worktree remains uncommitted.
