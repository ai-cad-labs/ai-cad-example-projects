---
schema_version: 1
project: spur_gear
outcome: complete
started: 2026-07-21T16:27:08+05:30
ended: 2026-07-21T17:16:54+05:30
sessions:
  - {n: 1, end: crash-dispatch}   # background-dispatched orchestrator, then ended turn (headless -p has no re-invoke)
  - {n: 2, end: completed}        # resume from filesystem; completed clean, no redesign
parts_built: 3
repair_cycles: 0
conflicts: 0
tags: [backfilled, gears, involute, dispatch-death, crash-resume, exporter-gap, single-pass, overfit-probe, reference-generalization]
---
# Run Reflection: spur_gear (2026-07-21)

## 1. What happened
Geometry-diversity probe #1 — first-ever gear-class (involute/module) geometry for this harness,
deliberately testing whether the prompt engineering is overfit to the bore-and-bolt class. Meshing
spur-gear pair (pinion 18T + gear 30T, m=2, 20° PA) + plain shaft ×2, 3D-print. **Verdict:
GENERALIZES** — shipped complete with exactly ONE in-design geometry adaptation, 0 hallucinations,
0 repairs, single-pass build. One runner death (background-dispatch in session 1) fully recovered by
filesystem resume, 0 work lost. ~49.8 min incl. death+resume; the gear *design* phase (~7.7 min) was
as fast as the chest's — gear complexity did not inflate the timeline, the death did.

## 2. Failures & frictions
- **Session-1 death — background-dispatch orphan-kill.** The entry session dispatched the orchestrator
  as a BACKGROUND agent, ran a criticalthink self-pass, and ended its turn ("will apply findings when
  it reports back"). Headless `claude -p` has NO re-invocation: turn-end exited the process and took
  the in-process orchestrator with it (terminal_reason=completed, stop_reason=end_turn — a *normal*
  turn-end, not overflow/auth/crash). Phase: post-design (3 parts coded, frozen at "Dispatching 3
  validators"). Root cause: **entry-prompt dispatch mode is NON-DETERMINISTIC** — cc2's identical
  prompt dispatched synchronously and survived; this run chose background-and-end. Workaround: resume
  session with synchronous dispatch mandated. Cost: ~14 min death+resume overhead (design untouched —
  part.py mtimes unchanged 16:31–16:34).
- **Golden `cylindrical_gear.py` arc-stitching FAILED on BOTH gears** for these params. NOT a
  hallucination — numerical fragility of the reference method. Phase: design (cad_designer). See §3.
  Cost: absorbed in a single design pass.
- **Exporter cannot export an assembly.** `tools.exporter` only targets `part.py`; the assembly had no
  export path. Phase: export. Workaround in §3. Cost: minor (one improvised exec).
- **gear validator `[validator]` design_log line never flushed.** Gear validation happened (assembly
  composed, gear report exists) but its summary line didn't reach design_log. Phase: validation. Cost:
  a logging gap, not a correctness gap.

## 3. Self-healing actions
- **Arc-stitch → point-sampled involute (the headline adaptation).** When the golden method failed,
  the designers did not stall — they switched to a robust point-sampled polyline involute (12–14
  samples/flank) and shipped BOTH gears in a single design pass, 0 repairs. The golden example was
  consulted **18×** and then correctly *rejected* as non-robust — reference consultation AND
  engineering judgment both fired. This is the single most important result of the probe.
- **Assembly export via direct exec.** With no exporter path for assemblies, the run exported by
  exec'ing `assembly.py` through the same `CadQueryExecutor` + `cq.exporters` path the tool uses
  internally. STEP/STL out; job done.
- **Quantitative mesh verification instead of trusting vision.** The resolver verified the half-tooth
  phase two independent ways: Z=0 section-interference (0°=18.04 mm² → −6°=0.00 mm²) AND full-face 3D
  boolean pinion∩gear (0.0000 mm³ @ −6° vs a 180.36 mm³ control @ 0°; the two agree — 18.04×10=180.36).
  Plus a volume-conservation invariant (39,739 mm³ = pinion 9,363.6 + gear 27,359.5 + 2×shaft 1,508.0,
  exact) confirming the assembly holds exactly the 4 intended bodies. Deterministic proof over
  false-positive-prone renders.
- **Gear-appropriate DFM ground-truth.** Tooth tip-land feature-size flagged `uncertain` (scale-less
  render) → resolved from geometry (1.36 mm ≥ 0.5 mm FDM floor) — the same uncertain-then-resolve
  discipline as cc2's wall thickness, generalized to a gear feature.
- **Planner pre-flagged the half-tooth phase as an assembly-time concern** up front — a positive no
  bore-and-bolt run had exercised.

## 4. Tactical suggestions
- **Exporter `--entry-file` flag** so assemblies (and any non-`part.py` entry) export through the tool
  instead of an improvised exec.
- **Entry-prompt MUST mandate synchronous dispatch** — "run the orchestrator to completion in THIS
  turn; never background-dispatch and end; headless has no re-invoke." (Baked into the resume prompt;
  worked.) *[Since encoded: CLAUDE.md runbook entry-prompt template.]*
- Flush the gear validator's `[validator]` design_log line (logging gap).
- **Reuse observability naming gap:** the sweep carries per-part `"reused": bool`, not the aggregate
  keys (`reused_parts`/`total_parts`/`dfa_reused`) the evaluation-authority upgrade named — either wire the aggregates or
  document the per-part boolean as the contract.

## 5. Strategic suggestions
- **Reference examples are candidates, not gospel — the harness needs a first-class "golden method
  failed, adapt" muscle, not a lucky improvisation.** This run consulted the golden gear example,
  detected its numerical fragility on THESE params, and adapted — but that judgment fired by luck of a
  capable designer. The paradigm shift: make "verify the reference method on your actual parameters
  before committing; fall back to a robustness-ranked alternative" an explicit design step. This
  dissolves a whole class ("the golden example doesn't fit my params") far beyond gears.
- **Runner robustness is a DIFFERENT AXIS from harness robustness — this is the through-line across all
  four runs.** Every death this run-class has seen is a *launcher/runner* failure, never a design
  failure: the chest died on auth, this run died on dispatch mode — the design pipeline never failed.
  A supervisor that owns dispatch-mode + resume as a contract retires the entire death class,
  independent of any design-quality work.
- **Overfit was the fear; generalization was the result — so invest in the knowledge layer, not
  per-class agent forks.** ONE new cookbook pattern (point-sampled involute + mesh-phase verify)
  captured the whole gear generalization; no per-class prompt re-engineering was needed. The
  prompt-engineering layer transfers across geometry classes; the leverage is growing the
  reference/cookbook layer, not branching the agents per class.

## 6. Knowledge candidates
- **Cookbook pattern: "point-sampled involute over arc-stitch"** — the robust involute-flank method
  (12–14 samples/flank) this run discovered. **HIGH-VALUE — the single pattern that captures the gear
  generalization.**
- **Cookbook assembly pattern: "gear mesh = half-tooth phase + section/boolean interference verify"** —
  the −6° = 360/(z·2) phase rule + the two-method quantitative mesh check + the volume-conservation
  invariant.
- **dfm-rules note:** tooth tip-land is a feature-size to ground-truth from geometry when the render is
  scale-less (1.36 mm ≥ 0.5 mm FDM floor) — optional feature-size guidance.
- **Anti-hallucination confirmation:** gear vocabulary (`.gear()` / `.involute()` etc.) triggered ZERO
  hallucination signals — the anti-hallucination watch is not gear-specific.

## 7. Unknowns
- **Why staleness-reuse fired on only 1 of 3 unchanged parts** (pinion reused; gear + shaft
  re-evaluated though also unchanged) — observed, not diagnosed. Directly contradicts cc2's comprehensive
  4-of-4 reuse; the reuse-selectivity question is open ACROSS runs, and the two disagree.
- **Whether the point-sampled sample count (12–14/flank) is optimal or merely sufficient** — it
  shipped; it was not swept for a minimum.
- **Whether the `reused_parts`/`total_parts`/`dfa_reused` aggregate keys are aspirational or derived** —
  the evaluation-authority upgrade named them; the run found only per-part booleans (naming gap, undiagnosed).
