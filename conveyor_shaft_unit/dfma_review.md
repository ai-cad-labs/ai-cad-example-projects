# DFM + DFA Review — conveyor_shaft_unit

The brief names "the manufacturability and assembly review" as a deliverable. This is it.

**Provenance note.** A `dfma_inspector` agent was dispatched to write this file and produced
all four machine reports it is built from, but had not written the consolidated document
after ~55 minutes. The orchestrator synthesised it directly from the agent's own artefacts
(`assembly/<part>/dfma_report.json` x3 and `assembly/dfa_report.json`) at zero additional
spawn cost. Every number below is read from those files, not restated from memory.

## Headline

**Zero active-rulebook DFM failures on all three Make parts. One active DFA failure, minor,
and it is a process recommendation with no geometry implication.**

| Target | Eval type | Verdict | Rules | Pass | Active failures | Uncertain |
|---|---|---|---|---|---|---|
| `shaft` | DFM (CNC_turning) | conditional_pass | 17 | 15 | **none** | 1 |
| `housing` | DFM (casting) | **pass** | 15 | 11 | **none** | 0 |
| `cover` | DFM | conditional_pass | 24 | 11 | **none** | 9 |
| `assembly` | **DFA** | conditional_pass | 10 | 2 | **DFA-004 (minor)** | 7 |

The raw `rules_failed` counters read 1 / 4 / 4 / 1. Every one of those on the three parts is a
`PROPOSED-*` rule — a rule the evaluator is *suggesting be added to the rulebook*, not a rule
the part was contracted against. Filtering to active-tier rules leaves **no part failure at
all**. This distinction matters: taken at face value the counters imply nine manufacturing
defects, and there are none.

## DFM summary, per part

**shaft — CNC_turning, 17 rules, no active failure.** Turning-specific rules pass. The single
`uncertain` is a vision-grounding limit, not a finding. Two earlier evaluator failures on this
part were refuted by measurement and are recorded in ISSUE-007: a `DFM-TURN-002` L/D of 8.6:1
computed by dividing total length (300) by the *smallest* diameter (35, a short overhung stub)
instead of the governing dia-45 body — the true ratio is **6.67:1**, inside the 8:1 limit —
and a "no circlip groove" finding on a 1.85 mm feature occupying roughly 7 render pixels.

**housing — casting, 15 rules, verdict `pass`, zero failures and zero uncertains.** The
cleanest report in the project, which is notable for the most feature-dense part. Its four
proposed-rule failures are all the documented draft/fillet/solid-wall compromises of
ISSUE-004.

**cover — 24 rules, no active failure, 9 uncertain.** The high uncertain count is image
grounding on a small part, not manufacturing risk. **Process-selection defect (ISSUE-007):
this part was evaluated as `CNC_milling` although its `constraints.md` declares
`Primary process: CNC_turning`, so no turning rules were applied to a turned part.** That is a
silent coverage hole — the report looks clean partly because the right rules never ran. The
cover is a simple single-chucking turned disc and the orchestrator does not consider it at
risk, but the gap is real and is filed upstream.

## DFA review

**DFA-004 (minor) — the one active failure. Assembly requires too many
held-against-gravity placements in the as-written sequence.**
Evaluator's recommendation, accepted verbatim as a *process* instruction:

> Sub-assemble vertically, install horizontally: stand the housing on its drive-end face so
> bearing, retainer, sleeve and cover all drop in along +Z under gravity and the 4 flange
> bolts torque from above, then rotate the finished unit once onto its base and drive the 4
> base bolts downward. That converts about ten held-against-gravity placements into a single
> fixture rotation.

**No CAD change is implied.** This is a build-sequence note for the assembly instruction, and
it is a good one. The seven `uncertain` DFA rules are image-grounding limits on a 17-component
scene; the hard access questions they bear on were each settled by direct measurement instead
(below).

**Measured DFA facts, all confirmed in the assembly validation rather than inferred:**
- **Part count 17**, of which 10 are threaded fasteners. Honest for a serviceable bearing unit
  with a bolted cover and a bolted-down foot; none of the ten is removable without losing a
  required function.
- **Self-location is good.** The cover spigot pilots in the dia-80 bore before any bolt is
  started; the shaft collar and circlip fix the bearing stack with no measurement at the
  bench; every press interface has a 1 x 45 lead-in (both shaft bearing shoulders, both
  housing bore mouths, the cover spigot nose, the seal pocket mouth).
- **Tool access, all measured:** the 4 M8 cover screws sit 73.5 mm apart on BC 104 with their
  heads in open half-space above z = +107, a 17 mm socket sweeping r 43.5..60.5 with 4.5 mm of
  flange still outboard; the 4 M12 foot bolts clear the drive-end boss by 8 mm of socket swing
  *after the ISSUE-005 fix*; both grease nipples stand at Y = +70..+82 as the highest geometry
  on the unit.
- **Error-proofing — one genuine risk, flagged for the work instruction:** the two 6208s are
  interchangeable and the cover has four valid 90-degree clockings (both harmless), but **the
  lip seal can be pressed in backwards.** Its lip must face inboard (-Z, toward the grease).
  Nothing in the geometry prevents reversal. Call it out on the drawing and in the build sheet.
- **Serviceability:** regrease via 2 nipples at roughly a 1,316 h interval, 7.2 g per bearing.
  Bearing replacement needs only the cover off at the drive end; the far end is open.

## Accepted, no action (recorded decisions — not re-raised as findings)

- **No fillets and no casting draft anywhere** (ISSUE-004). Project-wide deferral. A production
  drawing would carry R5-R8 at the pedestal-to-body and boss-to-body junctions and 2 deg draft.
- **Housing is solid-walled, not cored light** (~9 kg). Accepted for a static pillow block.
- **Three housing sections at exactly the 8.0 mm hard minimum wall.** At the limit passes.
  Zero margin: any future change to bolt circle 104, grease boss dia 24 or foot width 120
  breaks a brief requirement.
- **Far end deliberately open** — it is the floating end and the grease purge path (ISSUE-003).
- **Shaft dia-45 mid body gives 2.5 mm of shoulder** against the far-end inner ring where the
  catalogue wants da min 47. Deliberate: all thrust routes through the located drive-end
  bearing; this face is a creep stop only.
- **Cover dia-62 bore is 16 mm long for a 10 mm seal.** Deliberate — the seal enters from the
  inboard face and butts an outboard shoulder, so grease pressure seats it. A shorter lead bore
  made the part impossible to assemble.
- **Bearings modelled as sharp-cornered annuli** nominally overlap the 1 mm relief chamfers
  (63.9 mm^3 per end at the shaft shoulder, 124.6 mm^3 at the housing bore root — 0.1-0.2% of
  the ring). A real 6208's r_s 1.1 corner covers both.
- **ISSUE-005 closed**: the dia-130 boss overhanging the M12 foot bolt heads (6.437 mm^3 each)
  was fixed by moving the foot holes to Z = ±55 and independently re-measured at 0.000 mm^3 by
  three separate threads.

## Critical and major actions

**None.** No active-tier critical or major DFM failure exists on any part, and the single
active DFA failure is minor and process-only.

Two items for the drawing package rather than the model:
1. Add the lip seal orientation callout (lip faces inboard) to the build sheet — the only
   genuine assembly error-proofing gap.
2. Adopt the DFA-004 vertical sub-assembly sequence in the work instruction.

## Tool issues observed

1. **Process selection is wrong** — the cover evaluated as `CNC_milling` against a
   `CNC_turning` constraint, so turning rules never ran (ISSUE-007). Silent coverage hole.
2. **`rules_failed` counters conflate proposed rules with active ones**, implying nine
   manufacturing defects where the active rulebook finds none. Also seen reporting
   `rules_failed: 1` on the cover while the results array held no failure at all.
3. **Timeouts**: the evaluator needs `CAD_EVALUATOR_TIMEOUT_S=1800` on the housing; the 560 s
   default fails, sometimes emitting a `{"hooks":{}}` preamble before its JSON (ISSUE-006).
4. **The regression gate corrupted its own rollback baseline** by writing the proposal into
   `part.py.stable`, then scored identical geometry 0 and 1 on consecutive passes and emitted a
   spurious rejection (ISSUE-006, the serious one).
