# Checkpoint — Session 2 (2026-07-13)

## Status: COMPLETE — goals met, reviewer verdict "ship", all exports produced

Session 1 ended at the parts-validated boundary; session 2 ran the entire assembly → inspection → validation → review → export tail with zero repairs, zero conflicts, zero proposals.

## What was done this session

1. **ASSEMBLY (assembly_resolver)**: `assembly/assembly.py` composed with direct `cq.Location` placements at the TDC pose from design_plan.md § Assembly Pose. 7 instances (piston_ring instanced 3x, end gaps clocked 0°/120°/240°). All 7 locked interfaces verified as-coded — zero mismatches, zero conflicts filed. Executes clean: Compound, volume 333,808.54 mm³ = exact sum of the 7 part volumes (no interpenetration), bbox X −50…157 / Y ±50 / Z ±46 exactly per plan. `assembly/assembly.md` updated (rings placed in as-built free state, superseding the planner draft's compressed-OD note).
2. **Assembly re-render**: 8 colored views + `color_legend.txt` refreshed via tools.renderer (7-part legend).
3. **DFMA INSPECTION (dfma_inspector)**: 5/5 parts DFM = 0 active failures (weighted score 0 each). DFA score 23 decomposes ENTIRELY into policy-deferred + goals-accepted items — 0 genuinely actionable v1 findings. Reports refreshed: per-part `dfma_report.json` x5 + `assembly/dfa_report.json`.
4. **ASSY-VALID (validator on assembly)**: PASSED 9/10 — `assembly/notes.md` ends `VALIDATION: PASSED`. TDC pose, all interface fits, ring clocking, and clearances visually confirmed across 8 renders; bbox exact to plan.
5. **REVIEW (reviewer)**: verdict **ship** — goals_met yes, converging, 0 consistency issues, 95% complete (export was the only gap).
6. **EXPORT (cad_designer export duty)**: all 5 parts exported STEP + STL — 10 files verified on disk in `assembly/<part>/exports/` (piston.step 132 KB … gudgeon_pin.step 14.6 KB; all `success: true`).

## Final state (verified via spec_validator at checkpoint time)

- 5/5 parts validated, 0 proposals (no orphans), 0 conflicts, 0 open issues
- `assembly/assembly.py` exists + validated PASSED; 8 assembly renders present
- 10 export files present (STEP + STL x 5 parts)
- Every goals.md deliverable traced and met

## v2 backlog (from DFMA sweep — do NOT act in v1)

1. **DFA-009 (headline)**: one-piece big end + one-piece crank = rod cannot physically be assembled onto the crank pin. Explicitly sanctioned by goals.md for v1. v2: split big end + bolted cap, or built-up pressed crank.
2. DFA-002: no gudgeon-pin axial retention — add circlip grooves + circlips in v2.
3. DFA-008 + ~18 probationary sharp-edge/chamfer warnings — fillet/chamfer optimization phase (project-wide deferral).
4. Bronze small-end bushing (external/bom.md, UNVERIFIED row) — catalog lookup + modeled bushing land in v2.

## Infrastructure notes for future sessions

- **DFM vision stochasticity confirmed 3x on this project** (piston gate run-1 rejection; inspector's piston run-1 fail describing pre-repair geometry; PROPOSED-FUNC-001 "no ring grooves" claim contradicted by renders). Standing rule that worked: re-run once when a verdict contradicts render evidence + history; second verdict binding.
- **dfma_evaluator inner-model 8192-token limit**: crankshaft DFM failed 2 consecutive attempts (`Model token limit (8192) exceeded`, tool exit 0 with success:false) before passing on attempt 3 — largest applicable rule set (25 rules). Recommend raising the inner eval model's max_tokens before any future part with ≥25 applicable rules.

## Spawn counts — session 2

| role | spawns |
|---|---|
| assembly_resolver | 1 |
| dfma_inspector | 1 |
| validator | 1 (assembly) |
| reviewer | 1 |
| cad_designer | 1 (export duty) |
| **total** | **5** |

Deterministic tool runs (not spawns): spec_validator x2, renderer (assembly) x1.
Project totals across both sessions: 19 spawns (14 + 5).

## Next steps

None — project complete. Any future session on this project should target the v2 backlog above as a fresh goals/plan cycle.
