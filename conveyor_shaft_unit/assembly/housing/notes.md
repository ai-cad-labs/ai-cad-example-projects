# notes: housing (cast iron two-bearing body)

## Approach

One cast body, built in a strict order so the unions never poison the bores:

1. body cylinder dia 100, z = -95 .. +95
2. union dia 130 cover flange boss, z = +75 .. +95 (20 thick)
3. union pedestal box X -35..+35, Y -60..-40, Z -95..+95
4. union foot plate X -60..+60, Y -75..-60, Z -95..+95 (15 thick)
5. union the two dia 24 grease bosses (axis along Y at X = 0, z = +/-70, Y = +20 .. +70)
6. **then** cut the bore
7. 4 x M8 blind tapped holes, 8. 4 x foot bolt holes, 9. the two grease feeds

The bore is **one revolved cutting solid** whose 12-point (radius, z) profile carries
both dia 80 bores, the dia 72 passage, both bearing shoulders and **all four 1 x 45
chamfers as explicit geometry**. No edge is ever selected, so there is no `.chamfer()`
and no selector fragility anywhere in the part.

API trap avoided (flagged by a sibling agent): on `cq.Workplane("XZ")` the revolve axis
arguments are **local 2D**, so the call is `revolve(360.0, (0, 0), (0, 1))`.
`(0,0,0),(0,0,1)` would have revolved about global -Y.

Y-axis features (grease bosses, nipple ports, feed drillings, foot bolt holes) are built
with `cq.Solid.makeCylinder(r, h, pnt, Vector(0,1,0))` rather than a rotated workplane:
no plane-orientation sign errors, and `Workplane.union/.cut` take a `Solid` directly.

## Measured results (printed by part.py on every execution)

- bounding box **X 130.000 / Y 145.000 / Z 190.000**
  (X -65..+65, Y -75..+70, Z -95..+95) — exactly the expected numbers
- volume **1 282 021.4 mm^3** (~9.1 kg in EN-GJL-250 at 7.1 g/cm^3)
- **solids = 1** (single solid, all unions merged)
- section probes: dia 80 open at z = -80 and z = +80; dia 72 open at z = 0;
  material present just outside r = 36 at z = 0 and just outside r = 40 at z = +80

## Bearing seating

- **DE shoulder face at z = +66.0** — backs the drive-end 6208 outer ring (takes the
  ~1 kN thrust reaction). Shared plane with the shaft collar face.
- **FE shoulder face at z = -64.5**. The far-end outer ring sits at z = -84 .. -66, so
  the gap to its shoulder is **1.5 mm — the far-end bearing floats 1.5 mm axially**
  (brief: "free to float 1 to 2 mm"). Nothing clamps it at either side; the far-end bore
  mouth at z = -95 is left open, no step, no cover, no circlip.
- Both bores dia 80.000 nominal, **same axis = global Z**, line-bored in one setup.

## Minimum wall ledger (requirement: 8.0 mm everywhere)

| Section | Calculation | Result |
|---|---|---|
| body over the dia 80 bores | 50 - 40 | **10.0** |
| body over the dia 72 passage | 50 - 36 | **14.0** |
| M8 thread to bore | (52 - 4) - 40 | **8.0** |
| M8 thread to flange boss OD | 65 - (52 + 4) | **9.0** |
| grease boss wall around the M8 thread | 12 - 4 | **8.0** |
| foot bolt hole to foot edge | 60 - (45 + 7) | **8.0** |

Governing minimum = **8.0 mm**, at three places at once. There is no slack left in the
bolt circle (104), the boss diameter (24) or the foot width (120): moving any of them
inboard breaks the 8 mm rule.

## Grease access from above

Both boss top faces are at **Y = +70**. The next highest feature on the housing is the
dia 130 flange boss at **Y = +65**; the dia 100 barrel reaches Y = +50. Measured bbox
ymax = **+70.0**, so the nipple faces ARE the highest points on the part and a grease gun
coupler drops straight down onto either nipple with nothing in the way.

Each boss feeds **its own** bearing directly: M8 x 1 port (dia 7.0 tapping drill) 12 deep
from Y = +70 to +58, then a dia 4.0 feed from Y = +58 to Y = +38, breaking into the dia 80
bore whose crown is at Y = +40. No grease is routed through the dia 72 central passage.

## Fit and thread callouts (text only — the CAD is nominal)

- Both bearing bores: **⌀80 H7** (+0.030 / 0), CAD carries ⌀80.000. Coaxiality 0.020 TIR,
  both bores and both dia 72 steps line-bored in one setup.
- Cover fixing: **4 x M8 x 1.25**, bolt circle ⌀104, at 45/135/225/315 deg, **blind**,
  modelled at tapping-drill ⌀6.8 x 18 deep from the z = +95 face (hole bottoms at z = +77,
  inside the 20 mm boss). Usable thread ~16 deep = 2.0 x D.
- Grease nipples: **M8 x 1**, 12 deep, modelled at tapping drill ⌀7.0.
- Foot bolts: **⌀14 clearance for M12, NOT threaded**, 4 off at (X +/-45, Z +/-75).
- Drive-end face z = +95 perpendicular to the bore axis 0.025; DE shoulder face 0.015;
  foot underside flat 0.1; centre height 75 +/- 0.2.

## Discrepancies against constraints.md (task string wins, per dispatch)

The orchestrator issued five post-constraints amendments. `constraints.md` was written
before them and disagrees; **the built geometry follows the amendments**:

| Item | constraints.md | BUILT |
|---|---|---|
| drive-end boss OD | 124.0 | **130.0** |
| drive-end boss thickness | 10.0 (z +85..+95) | **20.0 (z +75..+95)** |
| grease boss z positions | +/-75.0 | **+/-70.0** |
| grease boss top / port / feed | Y +58 / +58..+46 / +46..+40 | **Y +70 / +70..+58 / +58..+38** |
| nipple tapping drill | 6.8 | **7.0** (M8 x 1 drill) |
| foot plate length | Z -87..+87 (174) | **Z -95..+95 (190)** |
| pedestal length | Z -88..+88 | **Z -95..+95** |
| M8 tap drill depth | 20.0 | **18.0** |
| overall bbox | 190 x 120 x 133 | **190 (Z) x 130 (X) x 145 (Y)** |

Consequences worth knowing downstream: the min-wall ledger tightened from 8.6 to **8.0**
at three sections (still compliant, but zero margin), and the boss-to-bore ligament is now
exactly 8.0 rather than 8.6 because the bolt circle sits in a 130 boss, not a 124 one.

## For the adjacent parts

- **cover**: the mating pad is now **⌀130 at z = +95**, not ⌀124. A ⌀124 cover flange would
  leave a 3 mm exposed rim all round; match ⌀130 if a flush rim is wanted. Bolt circle is
  unchanged at **⌀104, clocked 45/135/225/315**. Spigot enters the ⌀80.000 H7 drive-end
  bore (use h8). The cover must not reach inboard past z = +84 (the DE bearing outer face).
- **shaft**: no contact with the housing. The shared planes are the DE bearing inboard face
  **z = +66.0** and the bearing span **150.0** (centres z = +/-75).
- **assembly**: place this part with an **identity transform**; it is already modelled in
  the global frame.

## Known, accepted deviations (project rule, do not "fix")

- **No fillets anywhere.** A real EN-GJL-250 casting would carry R5-R8 at the
  pedestal-to-body, boss-to-body and flange-to-body junctions. Deferred project-wide.
- **No draft.** 2 deg on as-cast vertical faces is a tooling requirement, deliberately
  not modelled. No core prints, no parting-line features either.

---

## Validation

**Date**: 2026-10-08 · **Score**: 7/10
**Volume**: 1282021.38 mm^3 (EN-GJL-250 @ 7.2 g/cc -> 9.23 kg)
**Bounding box**: X -65.0..+65.0 (130.000) x Y -75.0..+70.0 (145.000) x Z -95.0..+95.0 (190.000)
**Method**: all numbers below are MEASURED off the built solid — OCCT face
interrogation (radius / axis / bbox per face) plus a bisection "largest fully-open
disc" bore probe — not copied from part.py or constraints.md. Vision pass last.

### Numbered checks

1. **PASS — executes, ONE solid.** `cadquery_executor` success, 326 ms, no warnings.
   `result.val().Solids()` = **1**. The unions merged; this is not a compound.
2. **PASS — bounding box exact.** Measured 130.000 x 145.000 x 190.000,
   ranges X[-65.0,+65.0] Y[-75.0,+70.0] Z[-95.0,+95.0]. Zero deviation on all three axes.
3. **PASS — two in-line bores on the Z axis.** Bisection probe, largest fully-open
   coaxial disc:
   z = -80.000 -> **dia 79.9999** · z = +80.000 -> **dia 79.9999** · z = 0.000 ->
   **dia 72.0000**. Both bores are single OCCT cylinder faces of radius **40.0000**
   with axis direction (0,0,1) through axis location (0,0,·) — i.e. genuinely
   coaxial on global Z, not merely close. FE bore face spans z -94.0..-65.5,
   DE bore face spans z +67.0..+94.0. Passage face r 36.0000, z -64.5..+66.0.
4. **PASS — shoulders and the 1.5 mm float.** Measured planar annular faces
   (both r 36..39, area 706.9 mm^2 each):
   - DE shoulder, normal +Z, at **z = +66.000** — backs the DE outer ring with zero gap.
   - FE shoulder, normal -Z, at **z = -64.500**.
   FE outer ring inboard face is z = -66.0, so axial float =
   -64.500 - (-66.000) = **1.500 mm**, inside the brief's 1-2 mm band.
   Checked the corner clash too: the 1 x 45 shoulder relief reaches r 40.0 at
   z = -65.5, and a 6208's r_s min 1.1 corner chamfer puts the ring's face edge at
   r ~38.9 < 39.0, so the ring seats on the flat annulus and the full 1.5 mm is
   available. Not a 0.5 mm trap.
5. **PASS — exactly four foot bolt holes.** Four cylinder faces, radius **7.0000**
   (dia 14.000), axis +Y, at (x,z) = (+45,+75), (+45,-75), (-45,+75), (-45,-75),
   each spanning y -75.0..-60.0 — through the full 15 mm foot plate. Count is four,
   no strays, no doubles.
6. **PASS — four M8 tapped holes.** Four cylinder faces, radius **3.4000**
   (dia 6.800 tapping drill), axis +Z, centres at (+-36.77, +-36.77) ->
   bolt circle radius sqrt(2 x 36.77^2) = **52.000** (BC dia **104.000**) at
   45/135/225/315 deg. Each spans z +77.0..+95.0 -> depth **18.0**, blind
   (flat bottom faces measured at z = +77.0). Does not break into the bore.
7. **PASS — minimum wall 8.0 mm everywhere, re-derived from measured faces.**
   Three sit exactly at the limit; none is below it.

   | # | Section | Measured | vs 8.0 |
   |---|---------|----------|--------|
   | 1 | body OD r50.000 - dia-80 bore r40.000 | **10.000** | +2.000 |
   | 2 | body OD r50.000 - dia-72 passage r36.000 | **14.000** | +6.000 |
   | 3 | M8 thread major r48.000 (BC r52.000 - 4.0) - bore r40.000 | **8.000** | at limit |
   | 4 | boss OD r65.000 - M8 thread major r56.000 (BC r52.000 + 4.0) | **9.000** | +1.000 |
   | 5 | grease boss r12.000 - M8x1 thread major r4.000 | **8.000** | at limit |
   | 6 | foot edge x60.000 - foot hole outer edge x52.000 (45 + 7) | **8.000** | at limit |

   (#3/#4 use the finished M8 major dia 8.0, not the 6.8 drill — the conservative
   reading. On the as-modelled 6.8 drill they are 8.6 and 9.6.)
8. **PASS — grease nipples reachable from above, both feeds break through.**
   - Two boss top faces measured, normal +Y, at **Y = +70.000**, area 413.9 mm^2
     each (= pi x 12^2 - pi x 3.5^2, i.e. dia 24 boss less the dia 7 port).
   - **Y = +70.000 is the global ymax.** Next-highest features: flange OD r65
     -> Y = +65.0, barrel OD r50 -> Y = +50.0. Nothing reaches 70 but the bosses,
     so a grease gun drops straight down onto each nipple.
   - Boss centres z = **+70.0** and **-70.0**: inside DE bearing z +66..+84 and
     FE bearing z -84..-66 respectively — each boss sits over its own bearing.
   - **Feed break-through CONFIRMED for both.** Each dia 4 feed is a cylinder face
     of radius **2.0000**, axis +Y, at z = +-70.0, spanning y **39.95**..58.0.
     The 39.95 lower bound is the exact intersection of a dia-4 hole at x=0 with
     the r40 bore wall (sqrt(40^2 - 2^2) = 39.950): the drilling terminates ON the
     bore surface, so it is open to the bore, not blind in the wall.
     Nipple ports measured r 3.5000, y 58.0..70.0 -> 12.0 deep.
9. **FAIL — bore-mouth chamfers are half size and the wrong angle.**
   Shoulder chamfers are correct: conical faces of semi-angle **45.00 deg**
   at z +66.0..+67.0 (r 39->40) and z -64.5..-65.5 (r 39->40) — both true 1 x 45.
   Bore mouths are NOT. Measured conical faces at the end planes have semi-angle
   **26.57 deg**, and the bore probe reads:
   - z = -94.999 -> dia **80.989** · z = -94.000 -> dia 80.000
   - z = +94.999 -> dia **80.989** · z = +94.000 -> dia 80.000
   So each mouth chamfer is **0.500 mm radial x 1.000 mm axial @ 26.57 deg**,
   against the constraints.md requirement (line 99-101) of **1 x 45 deg**.
   Radial error **-0.500 mm**, angular error **-18.43 deg**.
   Root cause is in `bearing_bores()`: the mouth chamfer leg is drawn straight
   from `(BORE_R + CHAMFER, Z_END +- OVERSHOOT)` to `(BORE_R, Z_END -+ CHAMFER)`,
   i.e. from (41, -96) to (40, -94). That spreads 1 mm of radius over 2 mm of z and
   puts the chamfer's start plane 1 mm OUTSIDE the part, so the solid only keeps
   the inner half of it. The 1.0 mm `OVERSHOOT` was baked into the chamfer leg
   instead of being a separate flat run-out.
   Also missing: the 1 x 45 deburr named at constraints.md line 102 on the dia 130
   boss outer edge at z = +95 — the r 65.000 cylinder runs z 75.0..95.0 with no
   cone at its end, so that edge is sharp. (Minor; cosmetic deburr.)
10. **PASS — no fillets.** `.fillet(` count in part.py = **0**. All transitions are
    chamfers or sharp, per the project-wide deferral.

### 11. Vision pass (renders dated 22:03:23, 15 s newer than part.py — current)

Read `iso_clean.png` and `front_wireframe.png`. Everything below is what I SAW;
every suspicion raised here was then checked arithmetically against the solid.

- **ISO_CLEAN**: reads unambiguously as a **pillow block**. A horizontal cylindrical
  barrel runs left-to-right; a large flat disc flange caps the right-hand (+Z) end and
  clearly overhangs the barrel's silhouette all round. Four small circles sit in that
  disc's face near the rim, spaced diagonally (upper-left, upper-right, lower-left,
  lower-right of the bore) — the M8 pattern, and I count exactly four. Looking into
  the bore I can see concentric rings part-way down it (the step and its relief),
  so the bore is visibly not a plain through-hole. **Two** short cylindrical bosses
  stand proud of the top of the barrel, each with a small hole in its flat top face;
  one sits toward the far (-Z) end, one just behind the flange. Below, a rib drops
  from the barrel onto a flat rectangular foot plate that is wider than the rib, and
  oblong hole-openings are visible in both foot wings. Junctions are **hard creases** —
  no radii at the rib-to-barrel or boss-to-barrel meets — and the rib sides are
  parallel (no draft).
- **ISO_CLEAN, chamfer impression**: the chamfer band at the bore mouth renders as a
  very thin sliver rather than a visible bevel. That is a vision impression only, but
  it agrees with the measurement — 0.5 mm radial, not 1.0.
- **ISO_CLEAN, suspected defect (DISMISSED by measurement)**: the far boss looks
  taller and fatter than the near boss. MEASURED: both top faces lie at Y = 70.000 and
  both outer cylinders have r = 12.000. Pure projection artefact — not a defect.
- **FRONT_WIREFRAME** (view down the Y axis; Z horizontal, X vertical): a long
  rectangle with a narrow strip at the left edge standing proud of the top and bottom
  outline — that is the dia 130 flange at +Z being wider in X than the 120 foot.
  **Four** heavy solid circles sit near the four corners, evenly placed about both
  centrelines — the foot bolt holes, and I count exactly four, no fifth, no doubles.
  **Two** grey dotted circles sit on the horizontal centreline, each with two smaller
  concentric dotted circles nested inside — the grease bosses with their nipple port
  and feed drilling, seen end-on. Both lie on the X = 0 centreline, mirrored about
  Z = 0. Long dotted horizontal line-pairs run the length of the view at a few
  different offsets from the centreline — the bore wall, the passage wall and the
  pedestal flanks, hidden behind the body.
- Nothing in either view contradicts a dimensional finding. The vision pass raised
  one suspicion (boss asymmetry); it was measured and dismissed.

### Known and accepted (NOT counted against the verdict)

- **No casting draft, no fillets/radii.** Sharp re-entrant corners at the
  pedestal-to-body and boss-to-body junctions, zero draft on as-cast faces.
  Confirmed present in the renders and in the source. Deliberate under the
  project-wide fillet deferral; already logged as accepted ISSUE-004. A production
  pattern would carry R5-R8 and 2 deg draft.
- **Solid-walled casting, not cored light.** 1 282 021 mm^3 -> ~9.23 kg in EN-GJL-250.
  Accepted for a static pillow block.
- **Three sections at exactly 8.0 mm.** At the limit is passing. None is below.
- **Far-end bore open to atmosphere** (no FE cover). Deliberate: floating end and
  grease purge path.
- **Nominal 80.000 bores**; the H7 fit is a text tolerance callout, not modelled.

### Separate findings (not part of the numbered checks)

- [minor] `constraints.md` line 39 still reads
  `Overall: 190 (Z) x 120 (X) x 133 (Y) mm` — the **pre-amendment** figures.
  The as-built and correct box is **190 (Z) x 130 (X) x 145 (Y)**
  (boss OD 124->130 drove X, grease bosses to Y = +70 drove Y). The amendment banner
  updated the body of the file but missed this summary line. Documentation only —
  the geometry is right and matches the amended intent.
- [minor] `dimension_checker` returned
  `"No parseable 'Overall:' line in .../constraints.md"` (pass = null) and so
  contributed no automated verdict. The bounding box was verified by direct
  measurement instead (check 2). Fixing the line above would also restore this tool.

### DFMA Findings

First invocation of `dfma_evaluator --mode=dfm --force` **malfunctioned** (tool fault,
not a part fault): the `claude` CLI hit the 300 s `CAD_EVALUATOR_TIMEOUT_S` on attempt 1
and attempt 2 returned a `{"hooks":{}}` preamble ahead of the JSON, so pydantic rejected
it (`Invalid JSON: trailing characters at line 1 column 13`). Re-ran with
`CAD_EVALUATOR_TIMEOUT_S=560`; it then completed and wrote `dfma_report.json`.

- **Overall verdict: `pass`** — 2 rules evaluated, 2 passed, 0 failed, 0 uncertain.
  (The casting rulebook only matched two generic rules; pass 2 was skipped.)
- `DFM-GEN-002` [critical] **pass**: tool access. Evaluator saw a
  pillow-block/plummer-style housing and found every feature reachable along a
  standard tool axis.
- `DFM-GEN-003` [minor] **pass**: symmetry. Evaluator found deliberate symmetry on
  every repeated feature with one tool approach direction each.
- **4 proposed rules** were emitted, and three of them restate the already-accepted
  casting compromises rather than new defects:
  `PROPOSED-001` [critical] mould-withdrawal draft · `PROPOSED-003` [major] as-cast
  internal corner radii — both are **accepted ISSUE-004**, deliberate under the
  project-wide fillet/draft deferral, and do **not** count against this verdict.
  `PROPOSED-002` [major] uniform wall / hot spots — the accepted solid-wall,
  not-cored-light decision.
  `PROPOSED-004` [major] fastener installation-tool swing — checked: the four M8
  taps open onto the fully exposed z = +95 flange face with the nearest obstruction
  (the z = +70 grease boss) 25 mm away in Z and below the flange rim, so socket
  swing is clear. No action.

### Verdict

**Nine of the ten dimensional checks pass, several of them exactly on nominal.**
One real, measured defect: **check 9, the two bore-mouth chamfers.**

- [ok] Execution, single solid, bounding box, both coaxial dia 80.000 bores,
  dia 72.000 passage, both shoulders, the 1.500 mm far-end float, four dia 14.000
  foot holes, four M8 taps on BC 104.000 x 18 deep, all six minimum-wall sections
  at or above 8.000, both grease bosses at the global ymax Y = 70.000 with both
  dia 4 feeds breaking through to their own bore, no fillets.
- [major] **Bore-mouth chamfers are 0.500 x 1.000 @ 26.57 deg instead of the required
  1 x 45 deg**, at both z = +95.0 and z = -95.0. Radial error -0.500 mm per side
  (mouth dia 80.989 where it should be 82.000 at the face). These are the bearing-entry
  lead-ins and are explicitly named in the brief and in constraints.md lines 98-101.
- [minor] The 1 x 45 deburr on the dia 130 boss outer edge at z = +95
  (constraints.md line 102) is absent — that edge is sharp.
- [minor] `constraints.md` `Overall:` line is stale (see Separate findings above).

### Recommendations

1. **Fix the mouth chamfers in `bearing_bores()`** — the profile currently folds the
   1.0 mm `OVERSHOOT` into the chamfer leg, halving it. Add a flat run-out point at
   each end so the chamfer spans exactly 1 mm of z inside the part. Replace

   ```python
   (0.0, Z_END_FE - OVERSHOOT),
   (BORE_R + CHAMFER, Z_END_FE - OVERSHOOT),
   (BORE_R, Z_END_FE + CHAMFER),
   ```

   with

   ```python
   (0.0, Z_END_FE - OVERSHOOT),
   (BORE_R + CHAMFER, Z_END_FE - OVERSHOOT),
   (BORE_R + CHAMFER, Z_END_FE),              # flat run-out to the face
   (BORE_R, Z_END_FE + CHAMFER),              # now a true 1 x 45
   ```

   and symmetrically at the drive end, replacing

   ```python
   (BORE_R, Z_END_DE - CHAMFER),
   (BORE_R + CHAMFER, Z_END_DE + OVERSHOOT),
   ```

   with

   ```python
   (BORE_R, Z_END_DE - CHAMFER),
   (BORE_R + CHAMFER, Z_END_DE),              # true 1 x 45
   (BORE_R + CHAMFER, Z_END_DE + OVERSHOOT),  # flat run-out past the face
   ```

   Acceptance test: bore dia at z = +-94.999 must measure **81.998** (not 80.989),
   and the two end cones must report semi-angle **45.00 deg** (not 26.57).
   Nothing else moves; the bounding box is unchanged because the chamfer is internal.
2. Add the 1 x 45 deburr on the dia 130 boss outer edge at z = +95
   (a 1 mm cone from r 65 to r 64, or a matching revolved cutter leg).
3. Fix `constraints.md` line 39 to
   `Overall: **190 (Z) x 130 (X) x 145 (Y) mm** bounding box` — this also unblocks
   `dimension_checker`, which currently cannot parse it.
4. Nothing else needs touching. Do not add fillets or draft, and do not "correct"
   the three 8.000 mm walls; all are accepted as-is.

VALIDATION (superseded): FAILED

## Repair attempt 1 (repair agent, 2026-10-08)

**Defect**: both bore-mouth chamfers measured 0.5 radial x 1.0 axial (26.57 deg),
not the briefed 1 x 45.

**Root cause** (as diagnosed by the validator, confirmed on inspection of
`bearing_bores()`): the 1 mm cutter OVERSHOOT was folded into the chamfer leg.
The profile ran `(BORE_R + CHAMFER, Z_END_FE - OVERSHOOT) -> (BORE_R, Z_END_FE + CHAMFER)`
= `(41, -96) -> (40, -94)`: 1 mm of radius spread over 2 mm of z, with the chamfer's
notional start plane 1 mm OUTSIDE the part, so half the chamfer was consumed by the
overshoot before reaching the z = -95 face.

**Change** (the only edit; +2 lines in `bearing_bores()`, nothing else in the file
differs from `part.py`): inserted a FLAT RUN-OUT point at the overshoot radius at each
mouth, so the overshoot travels in z only and the chamfer leg is a clean 1 x 1:

```python
(BORE_R + CHAMFER, Z_END_FE - OVERSHOOT),   # overshoot, outer radius
(BORE_R + CHAMFER, Z_END_FE),               # FLAT RUN-OUT to the face   <- inserted
(BORE_R, Z_END_FE + CHAMFER),               # FE mouth chamfer, true 1x45
...
(BORE_R, Z_END_DE - CHAMFER),
(BORE_R + CHAMFER, Z_END_DE),               # DE mouth chamfer, true 1x45
(BORE_R + CHAMFER, Z_END_DE + OVERSHOOT),   # FLAT RUN-OUT past the face <- inserted
```

Named constants preserved (`BORE_R + CHAMFER`, `CHAMFER`); nothing hard-coded.

**Measured on the proposal** (thin-disc binary search + exact circular-edge query):

| probe | before | after |
|---|---|---|
| bore dia @ z = -94.999 | 80.989 | **81.997** |
| bore dia @ z = +94.999 | 80.989 | **81.997** |
| bore dia @ z = -93.999 | — | **80.000** |
| bore dia @ z = +93.999 | — | **80.000** |

Exact circular edges: r = 41.000 at z = +/-95.000 and r = 40.000 at z = +/-94.000 on both
mouths -> 1.000 mm of radius over 1.000 mm of z = a true 1 x 45 deg.
(81.997 vs the ideal 81.998 is binary-search resolution, not geometry: the edge query is
exact at r 41.000.)

**Constraints re-verified after the change** (executor output, unchanged from the stable
part): bbox X = 130.000 / Y = 145.000 / Z = 190.000, ranges X[-65,65] Y[-75,70] Z[-95,95];
solids = 1; both dia 80 bores open on the Z axis (probes at z = +/-80 open, material at
r 40.1); dia 72 passage open at z = 0 with material at r 36.1; DE shoulder z = +66.0 and
FE shoulder z = -64.5 with the 1.5 mm float gap; all min-wall asserts pass. Volume moved
1282021.4 -> 1281894.1 mm^3 (-127.2), which matches the closed-form extra material the
two now-full-size chamfer cones remove: 2 x pi x 20.25 = 127.2 mm^3. Nothing else touched: no fillets, no draft, no change to the
shoulder reliefs, the dia 130 boss, the bolt circle, the foot, the grease bosses or feeds,
and no dia-130 deburr chamfer added.

---

## Re-validation (post-repair): 2026-10-08

**Scope**: narrow re-validation of the ONE defect that failed the first pass
(bore-mouth chamfer angle),
plus a no-regression sweep of the other nine checks.

**The earlier validation marker higher up this file
(now rewritten to `VALIDATION (superseded): FAILED`)
refers to the PRE-REPAIR geometry.**
It has been rewritten to `VALIDATION (superseded): FAILED` and is resolved by this section.
`part.py` now carries the repaired geometry promoted by the DFM regression gate
(stable 0 / proposal 0 / delta 0, zero new failures).

**Method**: every number below is MEASURED from the built OCCT solid --
an exact circular-edge query (edge geomType `CIRCLE`, adaptor radius, centre on the bore axis)
plus 40-iteration binary-search section probes --
not read off the renders.
Two renders were inspected for corroboration only,
in line with this project's ground-truth rule
(three vision false positives on record).

- **Score**: 10/10
- **Volume**: 1281894.1 mm^3
- **Bounding box**: -65.000..+65.000 x -75.000..+70.000 x -95.000..+95.000 mm
  (130.000 x 145.000 x 190.000)
- **Solids**: 1

### Check 1: the fix -- both bore mouths are now a true 1 x 45 [PASS]

Exact circular edges on the bore axis (centre X = Y = 0):

| z | radius | diameter |
|---|---|---|
| -95.000 | 41.000 | **82.000** |
| -94.000 | 40.000 | **80.000** |
| +94.000 | 40.000 | **80.000** |
| +95.000 | 41.000 | **82.000** |

Independent section probes (binary search on material onset):

| probe z | measured bore dia | required | verdict |
|---|---|---|---|
| -94.999 | **81.993** | 81.99x | PASS |
| -93.999 | **79.996** | 80.00x | PASS |
| +93.999 | **79.996** | 80.00x | PASS |
| +94.999 | **81.993** | 81.99x | PASS |

r = 41.000 at each z = +/-95.000 end face tapering to r = 40.000 exactly one millimetre inboard:
**1.000 radial over 1.000 axial = 45.000 deg at BOTH mouths.**
Pre-repair both measured 0.500 radial x 1.000 axial = 26.57 deg.
The defect is fixed.
The residual 0.005 mm in the probe column is the probe's own 0.002 mm annulus half-width
on a 45 deg taper, not a geometry error;
the edge query above is the authoritative measurement.

### Check 2: no regression

| # | Item | Measured | Verdict |
|---|---|---|---|
| a | One solid; bbox X/Y/Z | 1 solid; 130.000 / 145.000 / 190.000, X -65..+65, Y -75..+70, Z -95..+95 | UNCHANGED |
| b | Two in-line dia-80 bores on global Z; dia-72 passage at z = 0 | open at r 39.9 / z -80.0 and +80.0; passage open at r 35.9 / z 0, material at r 36.1 and at r 40.1 / z +80 | UNCHANGED |
| c | Shoulders at z +66.0 / -64.5, far-end float | DE +66.0, FE -64.5, float gap **1.5 mm** (brief 1-2) | UNCHANGED |
| d | Both bearing-shoulder relief chamfers 1 x 45 | FE: r 39.000 @ z -64.500 to r 40.000 @ z -65.500. DE: r 39.000 @ z +66.000 to r 40.000 @ z +67.000. Both 1.000 x 1.000 = 45 deg | UNDISTURBED |
| e | Six minimum walls >= 8.0 | all six source asserts pass: 10.0 body/bore, 14.0 body/passage, 8.0 thread-to-bore, 9.0 thread-to-OD, 8.0 boss wall at M8, 8.0 foot edge. Three at exactly 8.0 = at the limit = passing | UNCHANGED |
| f | 4x foot bolt holes dia 14 at (X +/-45, Z +/-75); 4x M8 tapped, 6.8 drill, 18 deep, blind, BC 104 | dia **14.000** at (-45,-75), (-45,+75), (+45,-75), (+45,+75), axis Y, through the foot plate (Y -75..-60). dia **6.800** at (+/-36.77, +/-36.77) = radius **52.000** = BC **104.000** at 45/135/225/315 deg, axis Z, z-span **77.0..95.0 = 18.0 deep, blind** | UNCHANGED |
| g | Grease boss tops at Y +70.0 = global ymax; dia-4 feeds break into their bore | two dia-24 bosses at z +/-70, both top faces planar at **Y = +70.000** = bbox ymax. Nipple tap dia 7.0 from Y 70.0 to 58.0; dia **4.000** feed from Y 58.0 down to **Y 39.95**, i.e. past the bore wall at r 40 -- **breakthrough confirmed at both ends** | UNCHANGED |
| h | Volume ~1,281,894 mm^3; no fillets | **1281894.1 mm^3**; `.fillet(` occurrences in part.py: **0** | UNCHANGED |

The -127.2 mm^3 volume delta the repair agent reported is confirmed as closed-form exact:
two full-size chamfer cones at 2 x pi x 20.25 = 127.235 mm^3.

### DFMA Findings

`dfma_report.json` is post-repair (same mtime as the promoted `part.py`) and was read rather than
re-run, since the regression gate already scored this exact geometry.

- Summary: 2 rules evaluated, **1 passed, 0 FAILED**, 1 uncertain; overall verdict `conditional_pass`.
- DFM-GEN-002 (tool access) [critical severity, verdict **uncertain**, not a failure]:
  the observation records straight-line access for the through bore, the flange bolt holes
  and the base holes;
  its recommendation is explicitly a **RULEBOOK** action (widen the mould draft / wall-variation
  rules to cover casting), not a part change.
  This is the accepted no-draft deferral, ISSUE-004.
- DFM-GEN-003 (prefer symmetric features) [minor]: **pass**.

### Visual Observations (corroboration only, 2 renders)

- RIGHT_WIREFRAME: looking along X, so horizontal is Z and vertical is Y.
  I see one long rectangular body silhouette spanning the full view width,
  a raised band across the top carrying two short dotted-bore stacks near each end
  (the grease bosses),
  a foot plate at the bottom with two arched legs, each with a dotted vertical pair through it
  (the foot bolt holes),
  and a tall narrow flange standing proud at the right-hand end with two dotted pockets in it.
  Internally, hidden lines draw a continuous bore running face to face with a step inward
  near each end -- consistent with the measured shoulders at z -64.5 and +66.0.
  The 1 mm mouth chamfers are roughly 8 px at this scale and are NOT individually resolvable here;
  they were judged arithmetically, above.
- ISO_CLEAN: a cylindrical body sitting on a rectangular foot plate via a vertical web.
  Two cylindrical bosses stand on top, each with a small concentric hole in its top face,
  and both tops read at the same height.
  The near end face is an annulus with FOUR small circular holes spaced evenly about the bore
  at roughly 45/135/225/315 deg.
  At the bore mouth there is a distinct narrow concentric ring between the flange face and the
  bore wall -- the chamfer band.
  Further inside the bore a second, offset ellipse is visible: the bearing shoulder step.
  Foot bolt holes are visible as ellipses in the foot plate.
  No stray slivers, no doubled faces, no visible artefacts from the repair.
  (Vision cannot discriminate a 26.57 deg band from a 45 deg band at this scale -- this view
  confirms the chamfer EXISTS and the part is otherwise intact; it is not the angle evidence.)

### Findings

- [ok] Check 1, bore-mouth chamfers: measured 1.000 x 1.000 = 45 deg at both mouths. The sole
  first-pass defect is RESOLVED.
- [ok] Checks 2a-2h: all eight no-regression items measured UNCHANGED. Nothing else moved.
- [ok] Coordinate convention (Principle 0): bore axis on global Z through the origin,
  bores centred at X = Y = 0, central passage at z = 0. Compliant.
- [ok] DFMA: 0 rule failures; the single critical-severity entry is `uncertain` and resolves to a
  rulebook gap, not a part defect.
- [accepted] No casting draft, no fillets, no junction radii (ISSUE-004, project-wide deferral).
  A production drawing would carry R5-R8 and 2 deg draft.
- [accepted] Solid-walled casting (~9 kg), three walls at exactly 8.0 mm, far-end bore open to
  atmosphere. All previously adjudicated.

### Recommendations

None blocking.
The part is released for assembly.
Carry ISSUE-004 (draft and radii) into the production-drawing stage;
the three 8.0 mm walls have zero margin,
so any future wall-thickness change must be re-checked against the 8.0 minimum.

## Repair attempt 2 (repair agent, 2026-10-08) — foot bolt hole Z station

### What was wrong

Nothing in this part *in isolation*: it passed validation on every check and DFMA reports
zero rule failures. The defect was found only by an ASSEMBLY-level interference sweep
between the housing and a purchased M12 foot bolt.

The two DRIVE-END foot bolts could not physically be fitted. The dia-130 drive-end flange
boss (r 65, z = +75 … +95) hangs down over the two foot bolt holes at Z = +75, so cast iron
occupies the space the M12 bolt head needs. Measured `housing ∩ M12 bolt head envelope`
(a cylinder r 9.0 about Y at the hole centre, spanning Y = -60.0 … -52.5):

| station | before | after |
|---|---|---|
| (X = +45, Z = +75) | **6.437 mm³** | n/a (hole moved) |
| (X = -45, Z = +75) | **6.437 mm³** | n/a (hole moved) |
| (X = ±45, Z = -75) | 0.000 mm³ | n/a (hole moved) |
| (X = ±45, Z = ±55) | — | **0.000 mm³ (all four)** |

The far-end pair measuring exactly 0 is the proof it was real geometry, not a modelling
convention: only the drive end carries the boss. Arithmetic agrees — at the bolt-head top
plane Y = -52.5 the r 65 boss reaches X = ±sqrt(65² - 52.5²) = ±38.32 while the M12 head
(dia 18) edge sits at ±36.00: a 2.32 mm overlap.

### Root cause

A clearance omission, not a modelling error. `FOOT_HOLE_Z` was set to 75.0 to line the foot
bolts up with the two bearing centres (z = ±75) — a sound instinct for load paths, but
z = +75 is also exactly where the drive-end boss starts. The bolt pattern was never checked
against the *fastener envelope* (head + socket), only against the hole itself, which does
clear. The housing-side hole is fine; the space above it is not.

### What changed — ONE constant

```
FOOT_HOLE_Z = 75.0   ->   FOOT_HOLE_Z = 55.0
```

That is the entire diff against the stable `part.py`: line 52, one number plus a short
inline comment. Verified with `diff` — every other byte is identical. No feature function
was touched; `foot_bolt_holes()` already read the constant, so the four holes relocate
together and stay four holes, dia 14.0, at X = ±45, cut along Y from Y = -75 to Y = -60.

Why ±55: an M12 socket of r 12 centred at Z = 55 sweeps z = +43 … +67, clearing the boss
that starts at z = +75 by 8 mm. The X edge distance is untouched at 8.0 mm (the hard
minimum, and the subject of a `__main__` assert). The foot-plate Z edge distance improves.
Resulting pattern: 110 (along the axis) x 90 (across) on a 190 mm foot.

### Measured verification (proposal, not assumed)

- **M12 bolt-head envelope, r 9.0 about Y, Y = -60.0 … -52.5, at all four new stations:
  0.000 mm³. Total 0.000 mm³.** The same probe re-measures 6.437 mm³ at the two old
  Z = +75 stations and 0.000 at Z = -75, reproducing the assembly sweep's numbers exactly,
  so the measurement is apples-to-apples with the finding.
- Four dia-14 holes confirmed material-free at (±45, ±55): 0.000 mm³ each.
- No hole remains at Z = ±75: each old station now measures 2309.071 mm³ of solid foot
  plate (= π·7²·15, a completely filled hole footprint).
- Volume **1,281,894.1 mm³ — unchanged** to 0.1 mm³. Expected: both the old and the new
  stations pass through nothing but the 15 mm foot plate (the pedestal is X ±35, clear of
  X = ±45), so the holes remove identical material. Mass is unaffected.

### No-regression checks (all re-measured on the proposal)

- bbox X = 130.000 / Y = 145.000 / Z = 190.000; ranges X[-65,65] Y[-75,70] Z[-95,95].
- ONE solid.
- Shoulders z = +66.0 and z = -64.5; float gap 1.5 mm.
- Six minimum walls — `ALL ASSERTS PASS` from the `__main__` ledger: body over bore 10.0,
  body over passage 14.0, thread-to-bore 8.0, thread-to-OD 9.0, grease boss wall 8.0,
  foot edge 8.0. The three at exactly 8.0 are untouched (none depends on `FOOT_HOLE_Z`;
  the foot edge assert is driven by `FOOT_HOLE_X`, which did not move).
- All four 1 x 45 chamfers intact, attempt 1's repair preserved: open radius 40.998 at
  z = ±94.999 and 40.000 at z = ±93.999 — the true 1 x 45 lead-ins.
- FOUR foot holes clear, FOUR tapped holes clear (dia 6.8, BC 104, 45/135/225/315).
- Drive-end boss dia 130 x 20 thick, grease bosses at z = ±70 with tops at Y = +70,
  foot plate outline, pedestal: all produced by byte-identical code.
- NO fillets, no draft added. ISSUE-004 stands as already-accepted.
- Coordinate convention (Principle 0) unchanged: bore axis on global Z through the origin.

### constraints.md amendment

Constraint 11's station line was superseded by this repair and has been updated in place:
`(X = ±45.0, Z = ±75.0)` / `150.0 along the axis x 90.0 across`
-> `(X = ±45.0, Z = ±55.0)` / `110.0 along the axis x 90.0 across`.
That one line is the only edit to constraints.md.

**Flagged, deliberately NOT edited** (outside the authorised scope of this repair): the next
sub-clause still reads `Edge distance 12.0 (Z) / 15.0 (X).` The Z figure is now stale — but
note it was already ungrounded before this change, matching neither the centre-to-edge
convention (95 - 75 = 20.0) nor the hole-edge convention (95 - 75 - 7 = 13.0) that the
X figure (60 - 45 = 15.0, centre-based) implies. At Z = ±55 the hole-edge distance is
33.0 and the centre-to-edge distance is 40.0. Someone who owns constraints.md should pick a
convention and fix both numbers; I did not want to invent one.

### Not re-validated here

Renders were regenerated from the proposal (8 views). Per this repair's dispatch rules the
PNGs were not read back — vision is the validator's job. Everything above is arithmetic
measurement on the solid, not a look at a picture.

VALIDATION: PASSED
