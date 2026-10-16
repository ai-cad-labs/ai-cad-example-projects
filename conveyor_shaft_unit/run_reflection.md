---
schema_version: 1
project: conveyor_shaft_unit
outcome: partial
started: 2026-10-08T14:17:38Z
ended: 2026-10-08T19:25:00Z
sessions:
  - {n: 1, end: completed}        # orchestrator, 15 spawns, all 4 gates passed, verdict ship
  - {n: 2, end: completed}        # verification + synthesis; re-measured everything, downgraded ship
parts_built: 3
repair_cycles: 2
conflicts: 0
tags: [bearings, shaft-support, casting, assembly, buy-part-envelopes,
       slow-finish-not-mute, abstraction-blind-spot, installability-blind,
       static-interference-gap, brief-contradiction, gate-baseline-corruption,
       process-misdetection, casting-rule-gap, fence-leak, timestamp-corruption,
       bearing-seating, chamfer-vs-corner-radius, self-review-caught-critical]
---

# Run Reflection: conveyor_shaft_unit (2026-10-08)

## 1. What happened

Two-bearing conveyor shaft support unit from a text brief with no input sketch:
3 Make parts (shaft, housing, cover), 22 purchased pieces, everything sized off the
40 mm shaft and the 6208 envelope.
All three parts designed first-try, all four validation gates passed, 2 repair cycles
(both housing, both one-constant), zero valid gate rejections, 6 exports, reviewer verdict `ship`.

**Then the DFM/DFA inspector finished — after the orchestrator had closed the run — with two
CRITICALs, both of which reproduced under independent measurement.
Then a critical-thinking pass over the verification session's own report found a third,
which no agent in the run had reported and which that report had explicitly dismissed.**
Outcome downgraded `complete` → `partial`.
Three blocking defects are known, measured and unfixed: the foot bolts cannot be washered
or socketed, the documented assembly sequence is impossible, and **neither bearing can seat
on its shoulder.**
Two of the three share a single root cause — `assembly.py` models catalogue parts as
idealised primitives — and all three were invisible to a clean 136-pair exact-boolean sweep.
The nominal geometry is right to three decimals; every defect lives in the gap between
nominal geometry and the real catalogue part.

## 2. Failures & frictions

- **`dfma_inspector` was SLOW, not mute — and the harness's own anti-mute doctrine
  converted that into a shipped miss.**
  The inspector ran ~53 min, produced its four machine reports (`dfma_report.json` ×3,
  `dfa_report.json`), and had not yet written `dfma_review.md`.
  The orchestrator applied the documented rule — *silent finish is the default,
  filesystem-verify the deliverable, the deliverable on disk is what counts* — found the
  machine reports present and the consolidated review absent, and correctly synthesised
  `dfma_review.md` itself at zero spawn cost rather than spend a 16th spawn.
  **The machine reports carried the scores; both CRITICALs lived in the reasoning,
  which existed only in the still-running agent.**
  The reviewer then saw a clean DFM/DFA record and returned `ship`.
  Cost: a `ship` verdict on a unit that cannot be bolted down.
  No signal existed to distinguish "died silently" from "still thinking".
- **Three independent threads confirmed the same wrong abstraction (the deepest failure
  of the run).**
  `ISSUE-005` (flange boss over the M12 bolt heads) was found, fixed by moving the foot
  bolts Z ±75 → ±55, and verified at **0.000 mm³ by three separate threads with three
  separate probes** — repair agent, orchestrator, re-validator.
  All three probed `M12_HEAD_D = 18.0`, the plain cylinder `assembly.py` models.
  Re-measured here against the envelopes the project's **own BOM** mandates:
  ISO 7089 washer OD 24 → **45.016 mm³** of cast iron; thin-wall socket Ø24 → **360.124**;
  standard socket Ø26 → **681.556**. Identical at all four stations.
  The fix traded one blocked position for another.
  Cost: a CRITICAL survived a fix, a gate, and triple verification.
- **Neither bearing can seat on its shoulder — and this was nearly buried by the
  verification session itself.** The interference sweep returned three bearing overlaps
  (124.617 / 63.879 / 63.879 mm³). The smoke report first dismissed all three as artifacts of
  `assembly.py` modelling bearings as sharp-cornered primitives, reasoning that a real 6208
  has an r1.1 corner and the catalogue gives `ra max` = 1.0 mm. **`ra max` governs a shoulder
  FILLET, not a 45° chamfer** — an invalid substitution that licensed a confident wrong
  conclusion. Re-measured with a realistic r1.1-cornered ring: housing overlap **59.255 mm³**,
  shaft overlap **30.590 mm³**, both rings seating **0.3556 mm proud**
  (closed form √2·(R − |c − 2R|/√2) = 0.3557; four decimals, two methods).
  Consequence: 17.644 mm of space for an 18.000 mm ring at the drive end, so **the circlip
  cannot be fitted and the located bearing is not located.** The run's most-celebrated number
  — "18.000 mm exactly, zero float" — holds as nominal geometry only.
  Caught only by the critical-thinking pass challenging the verification session's own report.
  Cost: nearly a shipped CRITICAL, in the document whose job was to catch CRITICALs.
- **The documented assembly sequence is physically impossible.**
  It presses both bearings onto the shaft and inserts the stack from the drive end,
  which needs an OD-80 bearing to traverse the Ø72 central passage.
  Swept r36–40 annulus over z −63.5…+67 = 124,633.3 mm³, of which **123,802.8 mm³ is
  cast iron — 99.3 % blocked.** The shaft alone passes freely (0.000 mm³).
  Static interference is blind to this: in the final pose nothing overlaps.
  Cost: prose + `add()` ordering, but it shipped as the build instruction.
- **DFM regression gate corrupted its own rollback baseline.**
  Gate run 3 wrote the **proposal's** content into `part.py.stable`, compared the proposal
  against itself, scored identical geometry 0 and then 1, and emitted a confident
  `REJECTED` naming `DFM-GEN-003` — which the surviving `dfma_report.json` for that exact
  geometry records as **pass**.
  It then deleted `part.proposal.py` on the rejection path, destroying the orchestrator's
  ability to follow the harness's own "re-run an inconsistent rejection once" rule.
  Two more gate failures on the same part: run 1 killed by the background time limit
  *after* a correct promotion but *before* printing its stdout verdict; run 2's inner
  evaluator CLI timed out at the 560 s default.
  Cost: ~40 min and an orchestrator override on four grounds.
- **`dfma_evaluator` ran the cover as `CNC_milling` though `constraints.md` says
  `CNC_turning`.**
  Root-caused to `.shared/tools/dfma_evaluator.py:372-394`: `_parse_manufacturing` ignores
  the `Primary process:` line and returns the first `_PROCESS_KEYWORDS` hit **in dict
  order**, where bare `"milling"` precedes `"cnc turning"`.
  The cover's section says `Primary process: **CNC_turning**` and two lines later
  `drill 4 x dia 9 on a milling station` — the secondary op wins.
  **No turning rule has ever been applied to this turned part.** Deterministic, reproduced.
- **Zero active casting rules exist.** No rule in `rules/dfm_rules.json` lists `casting` in
  its `manufacturing` field, so the housing — by far the most manufacturing-sensitive part
  in the unit — was graded against 2 generic rules out of 47. Its `pass` carries almost
  no information.
- **`rules_failed` counter reads 1/4/4 with zero active failures.** Every counted failure is
  a `PROPOSED-*` rule the evaluator wants *added* to the rulebook, not a rule the part was
  contracted against. An orchestrator reading the counter instead of the `results[]` array
  burns repair cycles on defects that do not exist. **It fails in the direction of
  manufacturing work that does not need doing.**
- **`spec_validator --query=state` under-reports.** Returns `open_issues: []` /
  `open_issues_count: 0` against an `open_issues.md` holding seven issues, one
  `NEEDS_HUMAN_INPUT`; and `assembly_executes: null` for an assembly that executes and
  renders. The one tool the process says to call first and often.
- **`design_log.md` timestamps are corrupt in the tail.** Early entries are real UTC
  (`2026-10-08T14:17:38Z`); later entries are local IST stamped `Z`
  (`2026-10-09T01:05Z` — **5h 43m in the future** relative to real UTC at synthesis).
  The frontend activity view and the operator timeline are built from this file.
- **`attempt_log.json` is JSONL, not JSON.** `json.load()` raises
  `JSONDecodeError: Extra data: line 2 column 1`; it needs line-by-line parsing.
  The extension promises a format the file does not hold.
- **`assembly.py` is not standalone-runnable.** It depends on a harness-injected global
  `__project_path__` (supplied by `cadquery_executor.py` / `exporter.py`); a bare
  `python assembly.py` raises `NameError`. Repo convention, but undocumented in the file.
- **Write-fence leak.** Operator instruction 7 fenced `rules/` read-only. The orchestrator
  relayed the death-guard block verbatim to every child but **did not relay the write
  fence**, and the inspector retired 12 rules and proposed 2 through the evaluator's
  `--retire-rule` / `--propose-rule` CLI, which writes `rules/` as a side effect.
  All five files in `rules/` now carry mtime 2026-10-09 00:42; the lifecycle log is at 43 entries.
  Cost: an out-of-scope mutation to shared state, left in place for the operator to adjudicate.

## 3. Self-healing actions

- **The orchestrator wrote the consolidated DFM/DFA review itself when its inspector did not
  deliver.** Correct call on the information available: a 16th spawn to re-do finished work
  is worse than synthesising from the artifacts already on disk, and it labelled the
  provenance in the file. The doctrine was applied properly; it was the doctrine that was
  incomplete, not the judgment. **Keep this behaviour.**
- **Overrode a corrupt gate rejection on four explicit grounds, and substituted something
  stronger than the rule it could not follow.** The gate had deleted `part.proposal.py`,
  so "re-run once on an inconsistent rejection" was impossible. Instead of waiving the
  check, the orchestrator ran an **independent third-party measurement in its own thread
  with a self-checked probe envelope** — verifying the probe spanned y −60.00…−52.50 with
  volume 1908.518 = π·81·7.5 *before trusting it* — and reproduced the validator's
  6.437 mm³ figure and its asymmetry exactly, from different code. Convention broken,
  result protected, and the substitute was better evidence than the original rule.
- **Used asymmetry as a truth test.** The foot-bolt clash measured 6.437 mm³ at z = +75 and
  exactly 0.000 at z = −75 on a symmetric design. That asymmetry is what distinguished a
  real defect from a modelling convention. Promoted to a general heuristic in §6.
- **Probe self-checks became mandatory mid-run after one silently lied.** The orchestrator's
  own first interference probe measured the wrong half-space — `cq.Workplane("XZ")` extrudes
  along −Y, so a "bolt head above the foot" envelope was actually *inside* the foot plate —
  and returned a confident, plausible, wrong number. Caught only because the value equalled
  π(81−49)·7.5. Every subsequent probe was dispatched with a mandatory
  closed-form self-check of its own envelope before use. That guard then caught nothing
  else, which is the point.
- **Refused to silently redesign around a customer-fixed number.** The brief hard-fixes both
  the 6208 *and* 20,000 h and they are arithmetically incompatible (L10h = 14,094 h;
  required C = 34.5 kN vs the 6208's 30.7 kN). The orchestrator kept the specified bearing,
  reported the shortfall as `NEEDS_HUMAN_INPUT`, and costed three options rather than
  upsizing to a 6308 and moving the entire axial stack. The reviewer endorsed it and
  strengthened it: the ~1,300 h grease relube interval means a literal "20,000 h between
  services" fails for **any** bearing choice, so the requirement itself needs clarifying.
- **Ran 15 spawns against the ~12 guideline, deliberately and in the open.** Context was
  never the binding constraint; stopping at 12 would have left the assembly failing on an
  already-diagnosed defect with the DFM/DFA deliverable unwritten. Flagged in
  `checkpoint.md` rather than hidden. Right call, correctly surfaced.
- **Verification session re-measured everything rather than transcribing it.** Every figure
  in `smoke_report.md` is recomputed from the built solids in an independent thread. That is
  what surfaced the washer envelope: the claim "0.000 mm³, three independent threads" was
  true and the conclusion drawn from it was false.

## 4. Tactical suggestions

- **Gate guard, three lines**: hash-verify `part.py.stable` ≠ `part.proposal.py` before
  judging, and abort if they match. This single check kills the entire run-3 failure class.
- **Gate must retain `part.proposal.py` on rejection** until the orchestrator acknowledges.
  Deleting it makes the harness's own "re-run once on an inconsistent rejection" rule
  impossible to obey.
- **Gate must write its verdict to a FILE in the part dir, not only stdout.** A verdict that
  exists only on stdout is lost to any harness-level timeout (exactly what killed run 1
  *after* it had correctly done the work).
- **Gate should score the stable side twice and refuse to rule when its own two passes
  disagree.** A severity-weighted score is only meaningful if identical geometry scores
  deterministically; here it scored 0 and 1.
- **Fix `_parse_manufacturing` (`dfma_evaluator.py:372-394`)**: prefer an explicit
  `Primary process:` line; failing that, match the earliest keyword *in the text* and prefer
  the longest match, instead of first-in-dict-order.
- **Split the counter into `rules_failed_active` / `rules_proposed_failing`**, or exclude
  `PROPOSED-*` from `rules_failed` entirely.
- **Write casting rules.** Zero of 47 active DFM rules apply to `casting`, which is one of
  the six legal `Primary process` values.
- **Raise the default `CAD_EVALUATOR_TIMEOUT_S`** or scale it by part complexity: the housing
  needs ~540 s for a single pass, so a two-pass gate needs >1000 s against a 300 s default.
- **Model fastener *envelopes*, not fastener bodies, in `assembly.py`** — or at minimum ship
  washers and nuts when the BOM lists them. `M12_HEAD_D = 18.0` with no washer is what made
  the CRITICAL invisible to a 136-pair exact-boolean sweep.
- **Fix `spec_validator --query=state`** to parse the `VALIDATION:` markers and
  `open_issues.md` it documents as its contract.
- **Stamp `design_log.md` in UTC from a single clock**, and reject entries dated in the future.
- **Rename `attempt_log.json` → `.jsonl`**, or make it a real JSON array.
- **Relay write-fences to children the way the death-guard block is relayed.** The
  death-guard block reached every child verbatim; the `rules/` fence reached none.
  Fences should travel by the same mechanism, in the same prefix block.

## 5. Strategic suggestions

- **Agreement across threads is not agreement with reality — the harness needs envelope
  provenance, not more verifiers.** The run's worst miss had *three* independent
  confirmations. They agreed because they all measured the same abstraction
  (`M12_HEAD_D = 18.0`), and that abstraction was not the part the BOM specifies. Adding a
  fourth verifier would have produced a fourth 0.000 mm³.
  **One abstraction gap produced three separate defects in this run** — ISSUE-008 (washer
  omitted entirely), ISSUE-010 (bearings sharp-cornered), and the cover-spigot clash that
  falls out of ISSUE-010. Every one of them is a catalogue *detail* interacting with a Make
  part, and every one was invisible to a 136-pair exact-boolean sweep, because the sweep
  faithfully measured idealised stand-ins.
  The paradigm shift is to make **every Buy-part envelope carry a provenance link to its BOM
  row, with the catalogue's own detail dimensions** (corner radius, washer OD, across-corners
  hex), and to **fail the sweep when a BOM line item has no modelled envelope**. Then "the
  washer is not modelled" is a hard error, not a silence, and "the bearing has no corner
  radius" is a hard error too. This retires a whole class: *verification that is confidently
  correct about the wrong object.*
  The sharpest evidence that this is a class and not an incident: **the verification session
  diagnosed the abstraction blind spot, named it as the run's central strategic lesson, and
  then failed to apply it to the second idealised primitive in the same file.** Knowing about
  the trap did not prevent falling into it; only measuring the real part did.
- **Installability is a separate geometric question from interference, and the harness only
  asks one of them.** Static interference asks "does anything overlap in the final pose?"
  — always no, by construction, because the designer placed the parts. The run hit this
  class **twice**: once caught by luck (a Ø62 seal behind a Ø46 bore, spotted only because
  the orchestrator mentally walked the sequence before dispatching), once shipped (the
  bearing through the Ø72 passage). The paradigm is **swept-volume DFA as a first-class
  gate**: for each component, sweep its envelope along a candidate insertion path and
  require at least one path with zero material. Cheap, deterministic, zero-spawn, and it
  dissolves the entire "assembles on paper, not in a workshop" class — including the
  seal-lip step and the cover-extraction findings, which are the same question asked about
  removal.
- **"Silent finish is the default" needs a liveness channel, not a better heuristic.** The
  doctrine exists because dead agents look identical to slow ones, and it is right far more
  often than not. But here it converted a *slow* agent into a *lost* deliverable, and no
  amount of filesystem-verification could have helped: the artifact genuinely did not exist
  yet. The shift is to make long-running agents emit a cheap heartbeat the orchestrator can
  poll — a mtime-touched `*.inprogress` marker is enough — so "absent" and "not yet" become
  distinguishable states. The current doctrine optimises correctly for a two-state world
  that actually has three.
- **Orchestrator rulings are a change class with no regression gate.** Both real defects in
  this run were caused by the orchestrator's own mid-run rulings, and the serious one by two
  rulings *interacting* (R2 thickened the boss; R4 placed the foot bolts; neither conflicts
  with the brief, together they put cast iron over the bolt heads). Every ruling was checked
  against the brief; none was checked against the other rulings. A ruling is a design change
  and should re-trigger whatever gate a repair would — **including the interference sweep
  against already-placed neighbours.** "Check the ruling against the hard requirements" is
  necessary and demonstrably not sufficient.
- **The sell-side risk in this harness is confident, well-evidenced wrongness.** This run
  produced exceptionally good evidence — exact boolean volumes, closed-form probe
  self-checks, reproduced positive controls, asymmetry reasoning — and used it to certify a
  defect as fixed. The quality of the measurement culture is exactly what made the wrong
  conclusion credible. Any future "certification" concept in this product needs to pin
  **what was measured** alongside the result, not just the result and its confidence.

## 6. Knowledge candidates

- **Cookbook pattern — orchestrator-resolved profile tables for turned parts.** The
  orchestrator read `design_plan.md` once and handed each designer a complete `(radius, z)`
  point list inline. All three parts executed first-try with zero fix cycles, on a part
  family where chamfers and grooves are normally the main source of churn. Revolving a
  closed profile makes every chamfer, groove, bore step and shoulder relief an explicit
  point, so nothing depends on fragile edge selection. **Strictly stronger than prose
  constraints for anything axisymmetric.**
- **Anti-hallucination entry — `revolve()` axis args on a non-XY workplane are LOCAL 2D.**
  On `cq.Workplane("XZ")`, `revolve(360, (0,0,0), (0,0,1))` is wrong (local `(0,0,1)` is the
  plane normal); correct is `revolve(360.0, (0,0), (0,1))`. The orchestrator seeded the wrong
  idiom and the designer caught it rather than cargo-culting it. Worth adding verbatim.
- **Heuristic — asymmetric findings on symmetric designs are real; symmetric ones are
  suspect.** The same bolt measured 6.437 mm³ at z = +75 and exactly 0.000 at z = −75. That
  asymmetry is what ruled out a modelling convention. Conversely, the three bearing-chamfer
  overlaps in this run (124.617 / 63.879 / 63.879 mm³) are perfectly mirrored — and are
  indeed artifacts of a sharp-cornered catalogue primitive.
- **Heuristic — every probe carries a closed-form self-check of its own envelope before it
  is trusted.** Verify bbox and volume against an analytic value first. The cheapest possible
  guard against a whole class of silent measurement error, and it caught a real one here
  (`Workplane("XZ")` extruding along −Y).
- **Pattern — the interference sweep as a BOM cross-check.** The four
  `cap_screw ∩ housing` overlaps measured 181.333 mm³ each. A Ø8 screw in a Ø6.8
  tapping-drill hole gives π(4² − 3.4²) = 13.94 mm²/mm, so 181.333 mm³ = **exactly 13.0 mm**
  of engagement — precisely the figure the BOM derives independently (25 mm screw − 12 mm
  flange). A "designed" overlap whose volume reproduces the BOM's arithmetic is a free
  two-way consistency check. Worth doing deliberately rather than noticing by accident.
- **DFM rule, fully derived and checkable — bearing-shoulder chamfer clearance band.**
  A 45° shoulder chamfer of leg *c* clears a rolling-element bearing's corner radius *R*
  **only when *c* ≤ *R*(2 − √2) ≈ 0.586·*R* or *c* ≥ *R*(2 + √2) ≈ 3.414·*R*.**
  Between those bounds the chamfer ramps through the corner's swept space and the ring seats
  proud by √2·(*R* − |*c* − 2*R*|/√2). For a 6208 (*R* = 1.1) the forbidden band is
  **0.644 … 3.76 mm**, and the intuitive "1 mm chamfer" sits almost dead centre in it.
  This is arithmetic on two numbers already present in every BOM row and every constraints
  file — no render, no vision, no spawn. It would have caught ISSUE-010 at plan time.
  **Counter-intuitive and therefore worth encoding**: a *smaller* chamfer clears where a
  larger one does not, which is why "add a generous chamfer" is the wrong instinct here.
- **Cookbook pattern — model catalogue parts with their corner radii when they touch a
  shoulder.** A sharp-cornered primitive is fine for envelope reservation and actively
  misleading for seating. Build the ring by revolved profile with sampled arc points
  (`.fillet()` on `%OD` edge selectors fails; `%Circle`/`%OD` is not valid selector syntax).
- **DFM/DFA rule idea — swept insertion path.** For every component, require at least one
  straight (or documented multi-stage) path from outside the assembly to its seat with zero
  material intersection. Would have caught both the Ø62-seal-behind-Ø46-bore case and the
  bearing-through-Ø72-passage case.
- **DFM/DFA rule idea — extraction provision on serviceable closures.** A press-fit closure
  that is flush with its mating face, pilots on a spigot, and grips a shaft through a seal
  has no purchase for removal. Require a pry notch, jacking thread or step.
- **Sourcing doctrine — always demand explicit duty arithmetic, never just part numbers.**
  Sourcing returned three findings no geometry check in the pipeline could ever surface
  (bearing capacity shortfall, a screw bottoming in its tapped hole, a grease purge path with
  no outlet). DFM, DFA and vision all look only at shape. This single instruction is why the
  run's most important open issue exists at all.
- **Doctrine gap the orchestrator had to invent — brief-vs-brief contradictions.** When a
  brief hard-fixes two mutually incompatible requirements, the default should be: *obey the
  stated part, compute and report the shortfall, never silently redesign around a
  customer-fixed number.* It was invented mid-run and endorsed by the reviewer; it should be
  written down.
- **Design heuristic — dispatch hard minima with headroom.** Three housing sections landed at
  **exactly** the 8.0 mm minimum wall with zero margin. Any later repair that nudges the bolt
  circle, grease boss diameter or foot width silently breaks a brief requirement. Aim 9,
  floor 8.
- **Sub-pixel features must never be vision-judged.** A "missing circlip groove" finding
  fired on a 1.85 mm feature occupying ~7 px of render. A 1 mm chamfer on a 300 mm part is
  ~4 px. Both need analytics, not vision — the evaluator even states its own confidence
  limit while failing the part.

## 7. Unknowns

- ~~Whether the 1 mm bearing-shoulder chamfers are correct against the 6208's r1.1 corner.~~
  **RESOLVED — they are not. Promoted to ISSUE-010; see §2.** This entry is kept rather than
  deleted because the sequence is the lesson: it was first written as a *confident claim*
  ("standard-correct, the ring seats flat"), demoted to an *honest unknown* on review, and
  only then measured. Two of those three states were wrong, and the one that cost nothing
  was admitting the gap.
- **Why `dfma_inspector` verdicts flipped on byte-identical geometry across two sweeps
  15 minutes apart.** Three documented flips (shaft DFM-TURN-002 fail → uncertain; shaft
  PROPOSED-TURN-001 pass → fail; housing DFM-GEN-003 fail → pass) and the DFA swinging
  `conditional_pass` (1 failure) → `fail` (4 failures). Vision stochasticity is the obvious
  candidate, but the magnitude — a verdict flip on an unchanged solid — was not diagnosed.
  A regression gate on this signal is noise-limited.
- **Whether `rules/` should be reverted.** Twelve rules retired and two proposed outside the
  operator's fence. Several retires were re-reasoned by the inspector and look substantively
  correct (notably `PROPOSED-SHAFT-003`, kept probationary against a triage that flagged it
  on the words "corner radius" in a project that *requires* chamfers and defers only
  fillets). Reverting would discard that judgment; keeping it ratifies a fence breach.
  Not this run's call.
- **Whether the inspector's washer figure (135.047 mm³) or this session's (45.016 mm³) is
  the right number to quote.** Both are non-zero at all four stations and the defect is not
  in doubt; the difference is probe depth (a 7.5 mm swept column vs the washer's own 2.5 mm
  seated thickness). Which envelope the fix should be dimensioned against was not resolved.
- **Whether `FOOT_X` 120 → 130 / `FOOT_HOLE_X` 45 → 50 actually clears everything.** It is
  the inspector's proposed fix and the arithmetic is plausible (15 mm to the pedestal wall,
  outboard edge distance exactly 8.0 mm, no bbox growth since the flange is already Ø130),
  but it was neither applied nor measured. Note the 8.0 mm edge distance reproduces the
  zero-margin pattern flagged in §6.
- **How much of the housing's manufacturability is actually unknown.** It passed DFM against
  2 applicable rules out of 47, with zero casting rules in the book. The `pass` is close to
  uninformative, and this run has no way to say whether the casting is good.
