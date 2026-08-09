# Checkpoint — impeller_assembly

**Status: COMPLETE.** The run reached terminal state on 2026-08-05. Reviewer verdict `ship`.
There is no pending work and no successor session is needed.

**Sessions**: S1 (partial, checkpointed at 10 spawns) → S2 (cold resume, completed at 4 spawns).
**Run total**: 14 spawns, 7 deaths (all in S1, all to context overflow), **zero work lost**.

If you are reading this looking for what to do next: nothing here. Read `smoke_report.md` for the
design outcome, `run_reflection.md` for the development feedback, and `open_issues.md` for the
three product defects this run found in the harness itself.

---

## Terminal state

- 3 Make parts (pulley_shaft, bearing_housing, impeller): designed, verified, rendered (8 views
  each), exported to STEP + STL, DFM-evaluated, and each `notes.md` ends `VALIDATION: PASSED`.
- 3 Buy parts specified in `external/bom.md` (6203 17×40×12, 688-2Z 8×16×5, ISO 4032 M10).
- `assembly/assembly.py` composes all 6 by pure Z translation. Assembly `VALIDATION: PASSED` (7.5/10),
  8 assembly renders present.
- `spec_validator --query=state`: parts_total 3 · parts_validated 3 · parts_failed 0 ·
  parts_with_proposals 0 · active_conflicts 0. Zero orphaned `part.proposal.py`.
- All artifacts verified on disk by direct inspection, not taken from child manifests.

**The user's headline requirement is met and measured**: impeller-backface-to-housing running
clearance = **0.8000 mm**, inside the required 0.5–1.0 mm window, confirmed by five independent
measurements across three agents and two orchestrators. It is realized structurally — a Ø22 × 0.8
standoff boss bearing on the 6203's inner-race face — so it is a machined dimension rather than a
stack-up that can drift.

```
component        global Z span        assembly bbox: X[-54,+54] Y[-60,+36] Z[-58,+60]
bearing_housing  -28.000 ..  12.000   total volume 207,148.16 mm³
main_bearing     -12.000 ..   0.000
impeller         -14.000 ..  34.800   running clearance to housing = 0.8000 mm  [PASS]
lock_nut          34.800 ..  43.200   impeller ∩ housing  = 0.0000 mm³ (no interference)
inlet_bearing     47.000 ..  52.000   shaft    ∩ housing  = 0.0000 mm³ (no interference)
pulley_shaft     -58.000 ..  60.000
```

## What S2 closed

1. **Impeller DFM re-run** — done. `conditional_pass` (up from S1's `fail`), but the process field
   still reads `CNC_milling`. ISSUE-005 confirmed, and found to be worse than S1 diagnosed.
2. **Per-part formal validation** — done. 3 dispatched one at a time, 3 survived, 3 PASSED.
3. **Reviewer pass** — done. Verdict `ship`, completeness 0.97.
4. **ISSUE-007** (pulley_shaft slenderness) — resolved as a process note, not a geometry change.
5. **ISSUE-009** (blade thickness) — checked and closed. `T_BLADE = 2.0` mm meets the suggested
   ≥ 2.0–2.5 mm band at its lower bound.
6. **ISSUE-010** — newly found: the DFM report miscounted the impeller's blades as 5 when it has 6.

## The three product defects this run found (all still OPEN — harness fixes, not CAD fixes)

- **ISSUE-005** — `5_axis_milling` is both unreachable (no alias maps to it) AND empty (its only
  rule is `tier: retired`; zero active rules vs 18 for CNC_milling). The alias fix must NOT ship
  alone: it would route 5-axis parts to an empty ruleset and produce a silent vacuous pass.
- **ISSUE-010** — the evaluator's vision miscounted 6 blades as 5, across two rules, citing
  "5-fold symmetry". Refuted by section cuts at three radii. Had it been trusted, a correct part
  would have been failed for a defect that does not exist.
- **ISSUE-006** — identical geometry evaluated twice returned `fail` (20 rules) then
  `conditional_pass` (10 rules). Verdict *and* rule coverage are non-reproducible.

## Standing warning, preserved

**Do not let any DFM output talk you into straightening the impeller's backswept blades.** The
report recommends cutting to 4 blades and making them purely radial. `goals.md` specifies backswept
blades and the user's sketch draws them curved. That recommendation is an artifact of the wheel
being judged under the 3-axis ruleset it was never meant to face. It was refused deliberately in
both sessions and the refusal is recorded in ISSUE-006.

## The death doctrine (kept because it is reusable, not because this run still needs it)

S1 lost 7 of 10 children to context overflow; S2 lost none. The difference was a guard block placed
at the top of every dispatch. Root cause is the **auto-load tax**: ~74K tokens of inherited
CLAUDE.md stack before a child reads a single project file.

The clauses that carry the weight:
- Save the primary deliverable to disk EARLY and incrementally; refine after.
- **Never read a rendered PNG back** — this was the fatal token in every death. Validators are the
  sole exception, because vision is their job; keep all their *other* reads minimal.
- Don't read `user_initial_sketch.jpeg` (4.7 MB), `part.py` in full, or `design_plan.md` in full.
  The orchestrator reads once and hands down prose.
- Pre-resolve every number the child needs into the prompt.
- Think in output tokens; the harness kills ~3 minutes of silence.
- Name the consequence explicitly ("your predecessors died of X"). S2 added: name that a sibling
  just succeeded on the same mission under the same rules.

Two more that paid off repeatedly:
- **Run deterministic tools yourself in the main thread.** `tools.exporter`, `tools.renderer` and
  `tools.dfma_evaluator` are bash-callable; using them cost zero spawns across both sessions.
- **Treat child manifests as testimony, not truth.** One `ls` caught a validator claiming exports
  that did not exist (ISSUE-004). Any claim of the form "artifact X exists" is worth a one-line
  filesystem check.

**Correct DFM invocation** (S1's checkpoint recorded this wrong and cost S2 a cycle — the tool
exits 0 with an error payload when the action flag is missing, so it looks like success):
```
uv run --frozen python -m tools.dfma_evaluator --mode=dfm --force --part-path <part-dir>
```

## Spawn ledger

| Role | S1 | S1 survived | S2 | S2 survived |
|---|---|---|---|---|
| planner | 1 | 1 | — | — |
| sourcing | 1 | 1 | — | — |
| cad_designer | 4 | 0 | — | — |
| assembly_resolver | 1 | 1 | — | — |
| validator | 1 | 1 | 3 | 3 |
| repair | 1 | 1 | — | — |
| dfma_inspector | 1 | 0 | — | — |
| reviewer | — | — | 1 | 1 |
| **total** | **10** | **4** | **4** | **4** |

Zero work lost across both sessions. Every S1 death occurred *after* the child completed its real
work and was recovered by wreckage-mapping rather than restarting.

## Files

`goals.md` · `design_plan.md` · `design_log.md` (262 lines) · `open_issues.md` (10 issues) ·
`smoke_report.md` · `run_reflection.md` · `reflection_notes.md` (121 lines) · this file ·
`external/bom.md` · `external/sourcing_notes.md` · `assembly/` (assembly.py, renders, 3 part dirs).
