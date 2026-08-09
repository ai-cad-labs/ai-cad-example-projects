---
schema_version: 1
project: impeller_assembly
outcome: complete
started: 2026-08-05T14:48:10+05:30
ended: 2026-08-05T17:00:00+05:30
sessions:
  - {n: 1, end: checkpoint-partial}   # 10 spawns, 7 children lost to context overflow, 0 work lost
  - {n: 2, end: completed}            # cold resume from checkpoint.md; 4 spawns, 4 survivors, 0 deaths
parts_built: 3
repair_cycles: 1
conflicts: 0
tags: [impeller, centrifugal, backswept-blades, assembly, context-overflow, auto-load-tax,
       vision-miscount, vision-stochasticity, ruleset-unreachable, empty-ruleset,
       process-declaration-vs-geometry, checkpoint-resume, guard-block, salvage-not-restart,
       manifest-as-testimony, sketch-input]
---
# Run Reflection: impeller_assembly (2026-08-05)

## 1. What happened

A small belt-driven centrifugal air compressor designed from a user's hand sketch: integrated
pulley-shaft, upright bearing housing, and a 6-blade backswept centrifugal impeller, sized around
three catalog Buy parts. Shipped complete across two orchestrator sessions — 3 Make parts designed,
validated, exported; assembly composed and validated; the headline 0.5–1.0 mm running clearance
delivered at **0.8000 mm** and realized structurally rather than as a drift-prone assembly gap.
Reviewer verdict `ship`, completeness 0.97.

The design work was never in trouble. Everything hard about this run was **infrastructure**:
S1 lost 7 of 10 children to context overflow (zero work lost — every death was salvaged), and the
run's most valuable output turned out to be a set of hard findings about the DFM evaluator's
reliability, culminating in the discovery that it miscounted the impeller's blades and would have
had a correct part destroyed to fix a defect that did not exist.

## 2. Failures & frictions

- **7 of 10 S1 children died of context overflow. Root cause: the auto-load tax.** Every child
  inherits ~74K tokens of instruction stack (operator- and repo-level CLAUDE.md/AGENTS.md files,
  as sized in this operator's environment) *before reading a single project file*. Error classes seen: `Prompt is too long`
  and `Stream idle timeout - no chunks received`. Phase: design (4 cad_designers) and dfma
  (1 inspector), plus 2 others. **Every single death occurred AFTER the child completed its real
  work**, at the read-renders-back or write-notes stage. Cost: near zero in work (all salvaged),
  but ~7 dispatch rounds of overhead and the entire S1 spawn budget.
- **A misdiagnosis that cost one dispatch round.** S1 first attributed the deaths to parallel
  fan-out, having launched 3 cad_designers in one message and lost all three instantly. The
  hypothesis was plausible (nested teammate spawns starve the parent's stream) but wrong: the solo
  synchronous retry died identically. Recorded because the *correction* is the useful artifact —
  prompt length and dispatch mode were both red herrings; the constant was the inherited stack.
- **`dfma_evaluator` invoked without `--mode=dfm` exits 0 with an error payload.** S1's checkpoint
  handed S2 a literal command missing that flag. It returned in ~2 seconds instead of ~300, and
  because it exits 0, the background-job wrapper reported success. Phase: S2 dfma. Cost: one cycle
  and a moment of false confidence that the verdict had changed. Correct invocation:
  `uv run --frozen python -m tools.dfma_evaluator --mode=dfm --force --part-path <dir>`.
- **HARNESS BUG, confirmed: `5_axis_milling` is unreachable AND empty.** The alias map in
  `.shared/tools/dfma_evaluator.py` (~lines 88–92) defines three milling aliases — "cnc milling",
  "cnc machining", "milling" — all mapping to `CNC_milling`, and nothing maps to `5_axis_milling`.
  A part declaring 5-axis is silently flattened to the 3-axis rulebook. S2 then found the deeper
  half: across all `rules/*.json`, **exactly one rule lists `5_axis_milling` and it is
  `tier: retired`** — zero active 5-axis rules against 18 active CNC_milling rules. Consequence:
  any inherently 5-axis part (impeller, turbine wheel, blisk, propeller) is structurally
  un-passable. It cannot pass 3-axis rules, and the rulebook written for it is both unselectable
  and empty. Phase: dfma, both sessions. Cost: the hero part carries three open MAJOR findings that
  mean nothing. (ISSUE-005)
- **🚨 The DFM report asserts the impeller has FIVE blades. It has SIX.** Two separate rules
  (DFM-CNC-001, DFM-GEN-003) cite "clean 5-fold rotational symmetry" as evidence. The validator
  refuted it numerically — section cuts at r = 20, 28 and 34 each returned exactly six disjoint
  solids at 60.00° spacing, and `N_BLADES = 6` in source. Phase: S2 validate. Workaround: the
  validator probed geometry instead of deferring to the report. **Cost if undetected: catastrophic.**
  It would have failed a correct part for a missing blade that exists, and the obvious repair would
  have been to add a seventh. (ISSUE-010)
- **Gate stochasticity, measured cleanly.** The impeller was evaluated twice with byte-identical
  geometry — not one line of `part.py` touched between runs — and returned `fail` (20 rules
  evaluated, 7 failed) then `conditional_pass` (10 rules evaluated, 3 failed). Not only did the
  verdict move; **the number of rules the evaluator chose to apply halved.** Phase: dfma, S1 vs S2.
  (ISSUE-006)
- **Manifest-as-testimony caught in the wild.** The S1 assembly validator's summary claimed
  "exports present (3 per Make part)". Every `exports/` directory was empty. One `ls` caught it.
  Cost: near zero, but had the summary been trusted the run would have shipped missing a stated
  success criterion. (ISSUE-004)
- **Two evaluator vision misidentifications.** The DFA pass called the inlet_bearing a "washer"
  (invalidating its own DFA-001 finding) and the main_bearing a "bearing housing". (ISSUE-003)

## 3. Self-healing actions

- **The death-guard block, and its measured effect.** S1, after 4 of 6 dispatches died, began
  prefixing every dispatch with an explicit block naming *how the predecessors died*: save the
  deliverable early and incrementally, never read a rendered PNG back, do not read the sketch or
  part internals, all numbers pre-resolved for you, think in output tokens. Survival went **0/4 →
  3/3** in S1, and **4/4 in S2** with zero deaths. The single highest-value clause is
  *"never read rendered PNGs back"* — rasterized image reads were the fatal token in every death.
  S2 added one clause that appeared to help further: telling the agent that a **sibling had just
  succeeded on the same mission under the same rules**. Named consequences plus a proof of
  survivability beat polite instructions.
- **Salvage-not-restart, applied seven times, zero work lost.** Every S1 death was wreckage-mapped
  (`ls` + mtimes + grep for expected artifacts) rather than restarted. It cost ~30 seconds each and
  recovered three complete parts and three complete DFM reports that a restart would have rebuilt
  from scratch. Three of four dead cad_designers had produced complete, correct geometry before
  dying. **Deaths clustered at the finish line, which is exactly why salvage pays.**
- **The orchestrator as context filter.** S1 read the 4.7 MB sketch ONCE and handed children prose
  instead of making each pay for the image. S2 extended this into the dominant working mode: every
  validator received its full locked dimension table, its known non-defects, and its
  pre-dispositioned findings *inline*, so none of them opened `constraints.md`, `design_plan.md` or
  `part.py`. Three vision-heavy missions fit inside a budget that had killed seven agents.
- **Deterministic tools run in the main thread, costing zero spawns.** Exports, renders and the DFM
  gate are all bash-callable. S1 ran `tools.exporter` for all three parts itself rather than
  spending a `cad_designer` spawn on export duty as the process suggests; S2 ran the DFM
  re-evaluation the same way. In a session where children are dying, moving every deterministic
  step into the main thread is both cheaper and strictly more reliable.
- **🚨 The run REFUSED the evaluator's geometry advice, deliberately and twice.** The DFM report
  recommended cutting the impeller to 4 blades and straightening them into purely radial,
  vertically-extruded walls. `goals.md` specifies backswept blades and the user's sketch draws them
  curved. Acting on that advice would have let a mis-selected rulebook overwrite the user's stated
  design intent. S1 refused it and recorded the refusal loudly in `open_issues.md`; S2 carried the
  refusal into the impeller validator's prompt as an explicit do-not-comply block so no downstream
  agent could obey it by accident. **This is the most important judgment call in the run** — an
  obedient repair agent acting on that report would have destroyed the deliverable while appearing
  to improve it.
- **Frame-change over effort, twice.** Before dispatching any repair, S1 triaged each DFM finding
  as *geometry defect* versus *process-declaration defect*. Two of three parts' findings dissolved
  entirely on re-declaring the process (impeller → 5-axis; pulley_shaft → turn between centres with
  tailstock support). Only DFA-005 was a true geometry defect, and it repaired in two parameters.
  A frame change deleted more work than effort would have.
- **Anti-anchoring inside pre-resolved prompts.** Feeding validators their expected numbers risks
  confirmation bias. S2 mitigated by phrasing every ask as *"measure X and report the value"*
  rather than *"confirm X is true"* — and the impeller validator did contradict its own brief in
  one place (rim blade height 6.155 vs 6.0 nominal, correctly dispositioned as a sampling artifact),
  which is the evidence the mitigation held.

## 4. Tactical suggestions

- **Make `dfma_evaluator` exit non-zero when no action flag is given.** It currently exits 0 with an
  error payload, which reads as success to any background-job wrapper. One line.
- **Add the 5-axis aliases with longest-alias-wins** so `5_axis_milling` cannot be swallowed by the
  generic `milling` substring — but see the hard dependency below.
- **Make the evaluator REFUSE to emit a pass verdict when the selected ruleset resolves to zero
  active rules,** and say so loudly. Without this, the alias fix above is *actively harmful*: it
  would route 5-axis parts to an empty rulebook and the impeller would "pass" vacuously by being
  judged against nothing. A silent vacuous pass is worse than an honest wrong-ruleset failure.
  **These two fixes must ship together.**
- **Derive countable features analytically and hand them TO the vision pass as a given.** Blade,
  hole, boss and tooth counts are exactly computable from the solid — section-cut-and-count is ~15
  lines of CadQuery. Asking a vision model to count petals in a render is the wrong tool for an
  exactly-computable quantity, and it produced a five-versus-six error this run.
- **Report `rules_evaluated` as a first-class stability signal**, and treat a drop in coverage
  between runs on unchanged geometry as a tool-health alarm rather than a quieter result. This run
  saw 20 → 10 on byte-identical input.
- **Promote the death-guard block from orchestrator folklore into the agent instructions.** It is
  currently re-typed by hand on every dispatch and would be lost entirely if a session forgot it.
  Specifically: bake the produce/verify split into `cad_designer` and `repair` so "never read
  rendered PNGs back" is not orchestrator-optional. The validator is the only role that should read
  renders, because vision is its job.
- **Make children write `notes.md` and `attempt_log.json` as STUBS ON ARRIVAL** and fill them
  incrementally. Every one of S1's seven deaths lost exactly those two files and nothing else. One
  line per agent instruction turns seven expensive deaths into seven free ones.
- **Require a survival/death-mode section in the checkpoint template.** S1's was the highest-leverage
  artifact of the run — a cold successor was productive within two tool calls and inherited the
  death doctrine instead of re-learning it at the cost of seven more children.
- **When a checkpoint hands a successor a literal command, the writing session must have run that
  exact string at least once.** S1's did not, and S2 lost a cycle to it.
- **Flush the renderer's stale `dimension_check`** after a promoted repair — it still flags
  "expected ~80 vs actual 108" on the bearing_housing, which is the intentional repair delta. A
  stale check that contradicts current constraints trains agents to ignore checks.

## 5. Strategic suggestions

- **The harness has no concept of "the tool judging this part is the wrong tool." That is the
  paradigm gap this run exposes.** Every finding on the impeller was *correct* — a backswept
  centrifugal wheel genuinely is unmachinable in 3 axes — and every one of them was *irrelevant*,
  because real impellers are 5-axis milled. The harness had no way to represent "this verdict is
  well-formed but inapplicable", so a valid analysis of the wrong question arrived with the same
  authority as a valid analysis of the right one. The shift: **evaluation should carry an
  applicability precondition, and a part should be able to fail the PRECONDITION rather than the
  rules.** "No applicable ruleset exists for this part's declared process" is a different and far
  more useful verdict than `fail`, and it routes to a *product* backlog rather than a repair agent.
- **Agent obedience is a safety surface, and this run found the sharp edge of it.** The DFM report
  did not merely fail the part; it recommended a specific, actionable, plausible-sounding geometry
  change (4 straight radial blades) that would have destroyed the user's explicitly stated
  requirement. Two orchestrators had to spend real effort *defending the design from its own
  tooling*. The paradigm: **user intent should be a first-class constraint that automated advice is
  checked AGAINST, not an equal voice in a negotiation the tool usually wins.** A repair agent
  should be structurally unable to modify a feature that `goals.md` names explicitly without
  escalating. Today the only thing standing between "backswept blades" and "4 straight vanes" was
  an orchestrator noticing and typing a loud warning by hand.
- **Vision is being asked to do arithmetic, and this is a whole class of defect rather than a bug.**
  The evaluator miscounted blades (5 vs 6), misidentified a bearing as a washer, misidentified
  another as a housing, measured shaft slenderness "proportionally off the render", and returned
  two different verdicts and two different rule counts on byte-identical geometry. Every one of
  those is a question the *solid model* answers exactly and for free. The reframe: **vision should
  be reserved for questions that are genuinely perceptual (does this look like a sensible part, is
  anything visibly wrong) and structurally barred from questions that are metrical or countable.**
  The current architecture inverts this — it hands vision the exact questions where it is weakest
  and where a wrong answer is most actionable, and therefore most dangerous.
- **The bottleneck of this run was not intelligence but inheritance.** Seven children died before
  reading a project file, because ~74K tokens of doctrine arrive before the mission does. The
  orchestrator's successful workaround — read once, hand down prose — is the right instinct
  implemented by hand. The paradigm: **context inheritance should be a mission-scoped budget the
  dispatcher controls, not an unconditional broadcast.** A validator does not need the org's
  operator's org-level doctrine. Until that exists, the orchestrator-as-context-filter role should be
  promoted from an improvisation to the documented default for doc-heavy repos.
- **Deaths cluster at the finish line, so the bookkeeping should happen first.** Every one of the
  seven deaths came *after* the real work, while writing notes or reading renders back. The general
  pattern is that agents spend their last tokens on their least valuable output. Inverting the
  order — stub the record on arrival, fill it as you go, do the expensive verification last — would
  make the modal death free instead of merely cheap. This generalizes well beyond this harness.

## 6. Knowledge candidates

- **Cookbook pattern: backswept centrifugal impeller.** The method that worked first-try and is
  worth capturing verbatim: build the hub as a revolved contour; build ONE blade as a thin vertical
  profile swept along a plan-view spline path (θ(r) = K·(r − r_root)², r_root buried inside the hub
  so the blade foot is never a free-standing wall); intersect it with a revolved blade envelope to
  trim leading and trailing edges in one operation; then circular-pattern it N× and union onto the
  hub. The envelope-intersection trick is the load-bearing idea — it replaces per-blade edge
  trimming with a single revolved solid.
- **Cookbook pattern: clearance as a machined boss, not an assembly gap.** The 0.8 mm running
  clearance was realized as a Ø22 × 0.8 standoff boss bearing on the bearing's inner race, so the
  clearance is a dimension on a part rather than a stack-up that can drift. Generalizable: whenever
  a spec calls for a gap, ask which single part can *own* it.
- **Verification pattern: count features by section-cut-and-count.** Cut the solid at 2–3 radii and
  count disjoint solids; check angular spacing for symmetry. This is what refuted the evaluator's
  blade miscount, and it is cheap enough to run on every patterned feature.
- **Verification pattern: prove backsweep numerically.** Measure the plan-view angular shift of a
  blade's centroid between two radii (here 10.5° from r=20 to r=34). A radial blade shifts 0°. This
  turns "the blades look curved" into a number.
- **DFM rule gap: the 5-axis rulebook needs to be authored.** Candidate rules — tool-reach and
  tool-axis rules written for simultaneous 5-axis access; blade/vane thickness versus unsupported
  height for deflection; inter-blade passage width versus cutter reach and shank clearance;
  blend-radius accessibility.
- **DFM rule note: slenderness must be measured on the load-bearing section, not the global
  minimum diameter.** DFM-TURN-002 read 13.6:1 by comparing a 118 mm length to a 15 mm-long Ø8
  tail; the meaningful figure is 8.4:1 on the Ø14 body. The rule should either take the
  length-weighted minimum or explicitly consider each diameter over its own span.
- **Reference-doc gap: catalog bearing width traps.** Sourcing caught that the OPEN 688 is 4 mm
  wide, not 5 (the 2Z shielded variant holds the planned width), and that DIN 934 M10 overhangs a
  Ø18 hub nose by 0.8 mm/side where ISO 4032 stays within 0.24 mm/side. Both are the kind of fact
  a sourcing agent should find in a table rather than re-derive.

## 7. Unknowns

- **Why the second DFM run evaluated only 10 rules where the first evaluated 20**, on identical
  geometry. Observed, not diagnosed. It could be staleness-reuse interacting with `--force`, a
  different applicable-rule resolution, or non-determinism in rule selection itself — the run did
  not have the budget to instrument it. This is the single most important unknown here, because
  rule-coverage variance undermines every verdict the tool emits.
- **Whether the death threshold is a hard token ceiling or a variable one.** S1 observed that two
  early solo dispatches succeeded at 168K and 149K tokens while later ones died, and S2's three
  validators survived at 145–156K. That clusters suspiciously tightly, but the run never isolated
  whether the boundary is fixed, load-dependent, or affected by image reads specifically.
- **Whether the impeller would actually pass a properly authored 5-axis ruleset.** It cannot be
  known today — the ruleset does not exist. The refusal to straighten the blades rests on
  engineering judgment about how real impellers are made, which is sound, but it has not been
  *verified by the harness* and should not be described as if it had.
- **Whether 2.0 mm blade thickness is genuinely adequate** or merely satisfies the letter of a rule
  generated under the wrong process. It sits at the exact floor of the suggested 2.0–2.5 mm band,
  with no margin, and the suggestion came from a 3-axis deflection rule that may not transfer.
  Flagged in `smoke_report.md` for the human.
- **Whether the assembly's 7.5/10 validator score has any calibrated meaning.** It was accepted as
  a pass, but the run has no idea what a 6 or a 9 would represent, and no rubric was surfaced.
