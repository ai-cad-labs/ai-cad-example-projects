---
schema_version: 1
project: treasure_chest
outcome: complete
started: 2026-07-21T14:23:22+05:30
ended: 2026-07-21T14:56:09+05:30
sessions:
  - {n: 1, end: completed}   # single session, 0 deaths, 0 salvage, 0 auth failures
parts_built: 4
repair_cycles: 0
conflicts: 1
tags: [backfilled, chest, assembly, de-gemini, evaluation-authority, staleness-reuse, single-pass, reuse-observability, deferred-majors, clean-baseline]
---
# Run Reflection: treasure_chest (2026-07-21)

## 1. What happened
First live E2E since the **de-Gemini migration** (keyless `claude`-CLI evaluator) and the **evaluation-authority
upgrade** (single-pass default, `--mode=sweep` parallel volley, staleness-cache reuse).
4 parts (base, lid, hinge_block ×2, hasp_plate) validated PASSED first-pass, **0 repairs**; assembly
composed + 1 conflict auto-resolved; DFMA sweep completed with **0 critical failures**; 8/8 exports.
**13 subagents, 0 died, 0 salvaged, 0 auth failures.** 32.8 min — 2.2× faster than the piston
baseline. Both never-before-observed subsystems worked on their first live run.

## 2. Failures & frictions
*A clean run — the frictions here are subtle observability gaps, not thrash.*
- **REUSED log marker undercounts actual reuse ~4:1.** The post-assembly sweep reused all 4 per-part
  evaluations (report timestamps prove it) but emitted exactly ONE explicit `REUSED` marker
  (hasp_plate); the other 3 reuses were silent. Phase: DFMA sweep #2. Cost: `grep -c REUSED` is a
  lying metric — reuse must be measured by report-timestamp stability. **The one substantive finding**
  (reuse *works*; the *log* under-reports it).
- **Per-part `overall_verdict=fail` vs validator `conditional_pass` split** (looked anomalous;
  diagnosed as working-as-designed). The failing rule on lid + hinge_block is DFM-3DP-002,
  severity=major, tier=active — a REAL failure, not a suppressed/probationary one. Reconciliation:
  `overall_verdict=fail` is the raw rule-rollup (any major fail → fail); the holistic gate verdict
  `conditional_pass` = 0 *critical* fails with majors deferred by rationale. Phase: DFMA sweep. Cost:
  warden diagnosis time only — not a defect. *[Since made deterministic: `_derive_verdict`.]*
- **Cosmetic: stale latch comment in `assembly/assembly.py`** (old Z=94 / 8 mm miss) left in place —
  self-noted by the run, deliberately NOT edited to avoid touching a PASSED assembly. Phase:
  post-conflict. Cost: cosmetic only (real code uses `latch_hole_z=34`).

## 3. Self-healing actions
- **CONFLICT-001 auto-resolution on the evaluation-authority stack.** Front hasp latch 8 mm misalignment (local
  `latch_hole_z` 42 → assembled Z=94 vs required Z=86) → assembly_resolver filed `part.proposal.py`
  (42→34) → DFM regression gate PROMOTED (0→0, no regression) → latch lands Z=86 → assembly
  re-validated PASSED. The conflict protocol running clean on the new keyless evaluator.
- **Vision honesty + ground-truth on a CRITICAL rule.** lid DFM-3DP-001 (wall thickness, severity
  *critical*) came back `uncertain` (not fail) because renders are scale-less; the run resolved it to
  PASS from source (`part.py` wall=3.0 mm; constraints.md 3 mm shell ≫ 0.8 mm FDM floor). Hedge-then-
  ground-truth instead of false-failing a good part — exactly right.
- **Mature DFMA self-governance — 3 MAJOR deferred with rationale, 0 thrash.** DFM-3DP-002
  (hinge_block, lid): horizontal bores = geometrically-unavoidable overhang (orthogonal bore groups →
  no single print orientation makes all bores vertical; horizontal is functionally mandatory).
  DFA-002: flat-mount + screws is conventional for a decorative 3DP chest, and the fix is a coordinated
  4-part change risking regression on a PASSED assembly. 0 critical → completion contract satisfied.
  Deferring-with-reasoning rather than repairing-on-reflex is the principle working at the strategy layer.

## 4. Tactical suggestions
- **Make sweep reuse self-describing** — emit a `REUSED` / `reused N of M` line for every skipped part
  (or a sweep-summary line) so reuse is measurable from the log, not only by diffing report
  timestamps. The one actionable item from this run. **NOT yet done.**
- Keep (confirmed working first-time): `_meta.engine=claude-cli`, `pass_label=single_pass`,
  `--mode=sweep` (0 serial `--part` calls), `ruleset_hash` staleness key — all fired correctly.

## 5. Strategic suggestions
- **A clean run is itself signal — the corpus needs control-group baselines, not only thrash.** This
  run's value is largely *negative space*: it proves de-Gemini + the evaluation-authority upgrade are production-healthy by NOT
  breaking, which no unit test establishes. A sweep that only surfaces failures cannot detect a
  regression *from* health. Tag clean runs (`clean-baseline`) so the self-improvement loop has a
  control group to diff future runs against.
- **"Sanctioned deferral" is a decision worth surfacing to the dev loop, not just an open_issues line.**
  This run deferred 3 MAJOR items with sound reasoning (geometrically-unavoidable overhang;
  conventional flat-mount). Those deferrals tell the harness *which rules routinely fire on
  correct-by-intent geometry* — candidates for context/orientation-aware suppression — a distinct
  signal from rules that catch real defects. The dev loop should mine deferrals, not just failures.
- **Observability is now the frontier, not throughput.** The evaluation-authority upgrade largely solved evaluator economics (2.2×
  faster than piston); the residual friction is that reuse/verdict internals are hard to read from
  outside (the 4:1 undercount; the fail-vs-conditional_pass confusion). The next leverage is a
  SELF-DESCRIBING pipeline (logs that state what they did and why) — a different discipline from speed.

## 6. Knowledge candidates
- **DFM-rule observation: DFM-3DP-002 (horizontal-bore overhang) fires on geometrically-unavoidable
  features** (orthogonal bore groups) — candidate for orientation-aware/intent-aware suppression, or a
  "functionally mandatory" annotation so it stops reading as a defect.
- **Pattern: uncertain-critical → resolve-from-source** — when the vision evaluator hedges `uncertain`
  on a scale-dependent CRITICAL rule (wall thickness), ground-truth from `part.py`/`constraints.md`
  rather than false-failing. Reusable across parts (also fired on the gear probe's tip-land).
- **DFA-rule note: DFA-002 (no self-locating features)** is conventional-and-acceptable for
  decorative/flat-mount assemblies — a blanket major may over-fire without context.

## 7. Unknowns
- **Probationary-rule governor NOT exercised** — this design proposed no new rule, so the
  propose→triage→promote path could not be confirmed live (also unexercised on the gear probe). Live
  confirmation still pending a run that trips a new rule.
- **Why staleness reuse fired comprehensively here (4 of 4)** but selectively on the gear probe (1 of 3
  unchanged parts) — the reuse-selectivity question is open across runs.
- **Whether the 2.2×-vs-piston speedup is attributable to the evaluation-authority upgrade specifically vs the zero-repair path.**
  This run had 0 repairs; the like-for-like control (vs chest #1, also 0 repairs) suggests ~1.75×, but
  clean attribution needs a repair-bearing run of the upgrade.
