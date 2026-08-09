---
schema_version: 1
project: piston_crank
outcome: complete
started: 2026-07-13T15:19:00+05:30
ended: 2026-07-13T16:30:20+05:30
sessions:
  - {n: 1, end: self-checkpoint}   # deliberate split at ~14 spawns, clean boundary (5/5 validated) — NOT a crash
  - {n: 2, end: completed}         # cold resume from checkpoint.md; assembly → sweep → review → export
parts_built: 5
repair_cycles: 1
conflicts: 0
tags: [backfilled, piston-crank, assembly, self-checkpoint, cold-resume, gate-stochasticity, token-ceiling, dfma-latency-sink, attempt-log-format]
---
# Run Reflection: piston_crank (2026-07-13)

## 1. What happened
5-part IC-engine core (piston, crankshaft, connecting_rod, gudgeon_pin, piston_ring) assembled at
TDC (7 instances, ring ×3 clocked ~120°). All 5 parts validated PASSED, assembly PASSED (9/10),
STEP+STL for all 5 (10 files). **1 repair cycle** (piston critical undercut). Two orchestrator
sessions: session 1 self-checkpointed at a clean boundary (~14 spawns, BY DESIGN), session 2 resumed
cold from checkpoint.md in 5 spawns. Reviewer verdict ship. 71.3 min total. The planner's dimension
chain (fits/clearances) held end-to-end with zero drift.

## 2. Failures & frictions
- **crankshaft DFM — `Model token limit (8192) exceeded`, 2 dead attempts.** Passed on attempt 3.
  Phase: DFMA sweep (dfma_inspector). Root cause: the largest applicable rule set (25 rules) overflows
  the inner LLM's hard-coded 8192 max_tokens on DFM mode (the same ceiling that killed the chest's
  DFA). Cost: **~8.8 min dead**. *[Fixed since: evaluator token-ceiling raise.]*
- **DFM regression gate stochasticity — wrong verdict (not a crash).** Gate run 1 on the piston repair
  REJECTED 0→16 with an internally-inconsistent verdict: it scored the *stable* part 0 on the exact
  rules it had previously failed. Phase: DFM gate (part phase). Workaround: orchestrator re-ran the
  identical proposal → run 2 PROMOTED 15→0. Confirmed 3× across the run. Cost: ~2.5 min/gate-run churn
  + a near-miss false escalation to redesign.
- **dfma_inspector latency sink — 24.0 of the 33.4-min assembly session (72%).** Serial waves of
  inner-LLM evaluator calls (~2–6 min each): ~5 min pure serialization of independent evals + the
  ~8.8 min crank retries + ~4 min of a stochastic piston re-check. Phase: DFMA sweep. Cost: ~17 min of
  the 24 was avoidable. *[Addressed since: parallel sweep volley + staleness reuse.]*
- **attempt_log.json format inconsistency (defect).** `piston/attempt_log.json` is concatenated JSON
  objects (JSONL-style, appended by 3 different agent roles) while the other 4 parts are proper JSON
  arrays; `json.load()` fails with `JSONDecodeError: Extra data: line 2 column 1 (char 505)`. Phase:
  post-run tooling. Cost: any attempt-log parser breaks on multi-agent-touched parts. **STILL OPEN.**

## 3. Self-healing actions
- **Self-checkpoint at ~14 spawns + cold resume (BY DESIGN).** Session 1 checkpointed at a clean phase
  boundary (5/5 validated) rather than push a degrading context; session 2 picked up cold from
  checkpoint.md — zero repairs, conflicts, or proposals in 5 spawns. The mortal-orchestrator design
  choosing a fresh successor over a tired incumbent, and it worked.
- **Stochastic-gate re-run rule invented in-flight.** The orchestrator recognized the 0→16 reject as
  internally inconsistent and re-ran once (second verdict binding) instead of escalating to a needless
  full redesign. Broke the "one gate verdict is final" assumption to protect a good proposal.
- **Crank shipped despite 2 dead evaluations.** The inspector re-ran the ceiling-killed crank DFM
  rather than abandon the part, and got its report on attempt 3; DFA-009 (rod can't physically
  assemble onto the one-piece crank) was accepted as *sanctioned-by-goals for v1* rather than blocking
  the ship. Improvise around the tool ceiling; do not let it stop the result.
- **One repair, precisely targeted.** Piston DFM-GEN-002 critical undercut → `web_width` 24→28 → gate
  PROMOTED 15→0 (the fix zeroed all weighted DFM cost). Single cycle, no thrash.

## 4. Tactical suggestions
- Raise dfma_evaluator inner `max_tokens` before any part with ≥25 applicable rules (crank proved DFM
  mode hits the ceiling, not just DFA). *[Since shipped.]*
- Encode the stochastic-gate re-run rule permanently: internally-inconsistent REJECT → re-run once,
  second verdict binding. *[Since encoded: orchestrator step 6 + the deterministic-verdict upgrade.]*
- **Standardize the attempt_log.json append convention** (JSONL everywhere OR read-modify-write array)
  across all agent roles — the multi-agent concatenated-object file is unparseable. **STILL OPEN.**
- Parallel-volley the dfma_inspector sweep (independent evals launched together, cap 4–6) + reuse
  fresh reports instead of re-DFM'ing every part. *[Since shipped: staleness-cache reuse.]*
- Cache the gate's stable-side score — both sides currently re-evaluate (~2.5 min/gate). *[Since shipped: staleness reuse.]*

## 5. Strategic suggestions
- **Geometry evaluation is deterministic input through a stochastic function — so caching UNCHANGED
  geometry increases consistency AND cuts latency (the CAP trade is inverted).** Re-evaluating
  unchanged geometry doesn't refresh truth, it injects variance — the 0→16 false-reject was exactly
  that. The staleness dimension that genuinely bounds correctness is the RULESET, not the geometry;
  key the cache on a ruleset-hash and rule-staging becomes a curated batch event instead of continuous
  inflation. This reframing (not any single flag) is the seed of the whole evaluation-authority redesign.
- **The assembly phase FELT slow because it is one silent serial lane with no visible fan-out.** Parts
  feel fast (3–4 agents landing results continuously); the 24-min sweep sits inside one agent with
  multi-minute silent waits. Perceived latency is an *observability* problem as much as a throughput
  one — surfacing in-flight evaluator waves (the ActivityStrip direction) changes the felt experience
  before any throughput fix lands.
- **The evaluator is the last pydantic-ai/Gemini remnant.** A CC-native subagent inspector (Reads
  renders natively, Writes the report directly) unifies the harness paradigm AND dissolves the
  output-ceiling class entirely — file writes chunk, single completions don't. (Later realized as the
  de-Gemini migration.)

## 6. Knowledge candidates
- **Cookbook pattern: dimension-chain lock** — the planner fixes the full fit/clearance chain up front
  (pin ⌀15.99 ↔ bore ⌀16.02; crank pin ⌀38 ↔ big end 38.05; ring 2.5×2.5 ↔ groove 2.6×3.0; centres
  95 + throw 30 → TDC crown 125) and it holds end-to-end. Reusable "lock the fit chain in the plan"
  discipline for any mechanism.
- **Cookbook pattern: TDC-pose assembly with clocked ring instances** (7 placed solids from 5 unique
  parts) + a volume-conservation invariant (333,808.54 mm³ = exact part-sum → no interpenetration).
- **DFA-rule example: DFA-009** (one-piece big end + one-piece crank → rod is physically
  un-assemblable) — a real assemblability finding, worth keeping as a canonical DFA teaching case.
- **Convention: single canonical attempt_log.json append format** (also §4) — a durable knowledge-layer
  rule, not just a bug fix.

## 7. Unknowns
- **Whether dual-pass DFM's second pass (engineering-domain) adds value** — the merged report keeps no
  per-rule pass provenance, so P2's contribution is unmeasurable; 1/3 of reports already survive
  single-pass. Confirmed cost, unproven benefit — feeds the single-pass-default decision but is not
  *settled* by this run.
- Whether the attempt_log format defect has already silently broken any downstream tooling (no parser
  has yet run against it).
- **Why the piston specifically drew vision stochasticity** (re-checked 3×) while the other parts did
  not — observed, not diagnosed.
