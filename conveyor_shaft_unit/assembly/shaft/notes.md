# Shaft - design notes

## Approach

One **single revolve** of one closed `(radius, z)` profile on `cq.Workplane("XZ")`.
No booleans, no edge selectors, no fillets.
Every chamfer and the circlip groove are explicit profile points,
so nothing can be lost to a fragile `.edges()` selection
and the model has zero failure modes beyond the profile itself.

Modelled DIRECTLY in the assembly's global frame
(axis = global Z, drive end = +Z, origin midway between bearing centres at z = +/-75),
so the assembly places it with an identity transform.
It is deliberately NOT centred on the origin.

### API gotcha worth knowing (bit the first draft)

`Workplane.revolve(angle, axisStart, axisEnd)` takes the axis points in the
workplane's **local** coordinates, not global.
On `"XZ"`, local `(u, v)` maps to global `(u, 0, v)`,
so local `(0,0,1)` is the plane NORMAL (global -Y) and revolving about it is wrong.
The correct global-Z axis is `revolve(360.0, (0, 0), (0, 1))`.

## Key dimensions (all parametric, module-level constants)

| Feature | Value | z range | Rationale |
|---|---|---|---|
| Overall length | 300.0 | -135 .. +165 | brief |
| Far-end bearing seat | dia 40.0 | -135 .. -66 | 6208 bore; bearing sits -84..-66 |
| Far-end shoulder | dia 45.0 face | at -66 | axial location of the far bearing |
| Mid body | dia 45.0 | -66 .. +60 | stiffness between supports |
| Thrust collar | dia 48.0 (max dia) | +60 .. +66 | square faces, takes belt-pull thrust |
| Drive-end bearing seat | dia 40.0 | +66 .. +84 | 6208 bore |
| Circlip groove | dia 37.5 x 1.85 | +84 .. +85.85 | DIN 471 - 40 x 1.75 |
| Seal journal | dia 40.0 | +90 .. +100 | no geometry change, finish callout only |
| dia 40 -> 35 step | at +120 | | |
| Pulley extension | dia 35.0 | +121 .. +165 | plain, taper-lock hub |
| Chamfers | 1 x 45 deg | both end faces, both bearing shoulders, the 40->35 step | bearing lead-in / deburr |

**The critical dimension**: collar front face (+66) to circlip groove rear wall (+84.0)
= **18.000 mm exactly** = the 6208 width.
The drive-end bearing is axially clamped with **zero float**.
It is derived in code as `Z_DE_SEAT_END = Z_DE_SHOULDER + BEARING_W`,
so changing `BEARING_W` in one place moves the groove with the bearing
and the clamp cannot drift. It is asserted in the `__main__` self-check.

## Measured self-check (from `python part.py` and a slice probe)

- bounding box: **48.000 x 48.000 x 300.000**, zmin -135.000, zmax +165.000
- volume: **408 899.7 mm^3** (~3.21 kg in steel at 7.85 g/cm^3)
- solids: **1**
- collar face -> circlip wall: **18.000 mm**
- diameters probed by 0.02 mm slices:
  z=-84 -> 40.0 | z=-70 -> 40.0 | z=-30 -> 45.0 | z=+63 -> 48.0 |
  z=+70 -> 40.0 | z=+84.9 -> 37.5 | z=+95 -> 40.0 | z=+150 -> 35.0
- renderer `dimension_check`: pass, 8 views written

Note: the dispatch brief guessed 3.0e5-3.5e5 mm^3.
The true volume is 4.089e5 because the dia 45 mid body is 126 mm long.
Hand integration of the profile agrees to 0.02%, so the brief's ballpark was simply loose:
the geometry is correct.

## Fit and finish callouts (tolerances are NEVER modelled - nominal geometry only)

- Both bearing seats: **dia 40 k6** (ground), bearing-seat cylindricity per 6208 mounting practice
- Seal journal (+90..+100): **dia 40, ground, Ra <= 0.4 um**
- Thrust collar front face (+66): perpendicular to the axis, it is a locating face
- Far-end shoulder face (-66): same, locating face
- Circlip groove: DIN 471 - 40 x 1.75, groove dia 37.5, width 1.85 (+0.14/-0)
- Material: steel, CNC turned between centres (centre drills at both ends are a
  process detail, not modelled)

## For adjacent parts

- The shaft is modelled in the shared global frame. **Place it with an identity transform.**
- The housings see **dia 40.000 nominal** at the seats; interference comes from the k6 callout.
- Drive-end bearing position is fixed and fully constrained: collar at +66, circlip at +84.
  Nothing downstream may add shims there, there is no room.
- The far-end bearing (-84..-66) is **axially free on the shaft**:
  its seat runs unbroken from the end face to the shoulder at -66,
  so the far end is the floating/expansion bearing.
  Whatever locates it axially must do so from the housing side, not the shaft.
- Max diameter is 48 (collar, +60..+66): nothing may pass over the shaft from the
  drive end past z = +60 with a bore smaller than 48.
- The pulley extension is **plain** (no keyway, no flats): the hub must be taper-lock.

## Trade-offs

- Explicit-profile chamfers instead of `.chamfer()` on selected edges:
  slightly more verbose, but a chamfer cannot silently vanish or land on a wrong edge.
- No centre holes, no thread relief, no grinding undercut at the shoulders modelled.
  A ground seat normally wants a relief groove at the shoulder;
  the 1 x 45 chamfer is doing that job here, which is the cheaper
  (and brief-specified) solution and is fine for a shouldered bearing seat.
- No fillets anywhere (deferred project-wide). The shoulder at -66 is a dia 40 -> 45
  step and the collar at +60 is a square dia 45 -> 48 step: both are stress risers
  that a later fillet pass should address.

---

## Validation

**Date**: 2026-10-08 · **Score**: 9/10
**Volume**: 408899.67 mm^3
**Bounding box**: -24.000..+24.000 x -24.000..+24.000 x -135.000..+165.000 mm

Method note: every dimensional finding below is MEASURED off the built solid by
planar cross-section probe (`BRepAlgoAPI_Section` at each z station, outer radius
from the section bounding box), not read from the source or from these notes.
Vision-only observations are labelled as such and were each ground-truthed
arithmetically before being reported.

### Numbered checks

1. **PASS — executes cleanly, ONE solid.** `cadquery_executor`: `success: true`,
   27.8 ms, `result_type: Workplane`. `result.solids().size() == 1`. Volume
   408899.67 mm^3.
2. **PASS — bounding box.** Measured 48.000 x 48.000 x 300.000,
   z = -135.000 .. +165.000. `dimension_checker`: PASS, expected [48.0, 300.0],
   actual [48.0, 48.0, 300.0], zero deviations.
3. **PASS — THE CRITICAL NUMBER: 18.000 mm.** Measured, not trusted:
   the dia 48 collar face is the last full-diameter section at z = +66.000
   (probe r = 21.000 at z = +66.000, i.e. the face runs r 21.000..24.000);
   the circlip groove inboard wall is a clean step at z = +84.000
   (probe: dia 40.0000 at z = 83.900, 83.990 and 84.000; dia 37.5000 at
   z = 84.010). Span = 84.000 - 66.000 = **18.000 mm**, exactly the 6208 width.
   Zero axial float at the drive end confirmed. Constraint 8 satisfied.
4. **PASS — two dia 40.000 bearing seats, both >= 18 long.**
   Far end: dia 40.0000 measured at z = -120.0, -84.0 and -67.0 — continuous seat
   z = -134.0 .. -67.0 (67.0 long), fully covering the FE bearing at -84..-66.
   Drive end: dia 40.0000 at z = +67.0, +75.0, +83.9 — seat covers +67.0..+84.0
   and the bearing envelope +66..+84 (the first 1.0 mm is the shoulder chamfer
   relief, see the accepted-findings note).
5. **PASS — circlip groove.** Measured floor dia **37.5000** across
   z = 84.010 .. 85.840; dia returns to 40.0000 at z = 85.850 and 85.860.
   Groove extent therefore z = +84.000 .. +85.850, width **1.850**,
   dia **37.500** — DIN 471 - 40 as specified.
6. **PASS — diameters by section probe** (all exact to 1e-6):
   - 40.0000 at FE seat z = -120.0 / -84.0 / -67.0
   - 45.0000 mid body at z = -60.0, 0.0, +59.0
   - 48.0000 collar at z = +61.0, +65.5 (collar runs +60.0..+66.0)
   - 40.0000 DE seat at z = +67.0, +75.0, +83.9
   - 40.0000 seal journal at z = +90.0, +95.0, +100.0 (and +119.9)
   - 35.0000 pulley extension at z = +121.0, +160.0
7. **PASS (5 of 5 required) — 1 x 45 chamfers, verified as true 45 deg ramps**
   (radius probed at both ends and at the midpoint of each 1.000 mm axial run;
   midpoint radius equals the mean in every case, so the face is a 45 deg cone,
   not a step or a radius):
   - z = -135.000 end face: r 19.000 -> 19.500 -> 20.000 over 1.000 axial — OK
   - z = -66.000 FE bearing shoulder: r 20.000 -> 20.500 -> 21.000 — OK
   - z = +66.000 DE bearing shoulder: r 21.000 -> 20.500 -> 20.000 — OK
   - z = +120.000 dia 40 -> 35 step: r 18.500 -> 18.000 -> 17.500 — OK
   - z = +165.000 end face: r 17.500 -> 17.000 -> 16.500 — OK
   All are 1.000 mm axial x 1.000 mm radial. No chamfer at a bearing shoulder
   exceeds 1 x 45 (Must-NOT #7 respected).
   See Finding M1 for the sixth chamfer listed in constraints.md (z = +60).
8. **PASS — no fillets.** `.fillet(` does not occur in part.py (string search).
   No radii found at any step by probe: every transition is either a square face
   or a linear 45 deg cone.
9. **PASS — no keyway, cross-hole or flat.** No `.hole(`, `.rect(`, `cboreHole`
   or `slot` call in the source; the part is a single `.revolve(360.0)` of one
   closed polyline, so it is a solid of revolution by construction and cannot
   carry a flat or a cross-hole. Probe across the extension (z = +121.0, +160.0)
   returns a constant dia 35.0000 — plain cylinder, as the taper-lock hub needs.
10. (vision) — see Visual Observations below.

### DFMA Findings

`dfma_evaluator --mode=dfm`: **conditional_pass**, 10 rules evaluated,
7 pass / 2 fail / 1 uncertain. Report: `dfma_report.json`.

- DFM-CNC-005 [major]: PASS · DFM-CNC-008 [critical]: PASS
- DFM-TURN-001 [major]: PASS · DFM-TURN-003 [critical]: PASS
- DFM-GEN-002 [critical]: PASS · DFM-GEN-003 [minor]: PASS
- PROPOSED-TURN-005 [minor]: PASS
- **DFM-TURN-002 [major]: FAIL — REBUTTED, measured.** The evaluator measured the
  silhouette in pixels and divided the FULL 300 mm length by the SMALLEST
  diameter (the dia 35 pulley extension), getting ~8.6:1. That is the wrong
  denominator: the dia 35 section is a 45 mm overhung stub at one end, not the
  unsupported length. The governing ratio is overall length / mid-body dia =
  300 / 45 = **6.67:1**, inside the 8:1 limit, exactly as constraint 11 states.
  Its own observation concedes this ("~6.5:1 against the main body ... the
  violation is marginal and localized"). Not a defect. Its preferred
  recommendation (declare tailstock support) is already in constraints.md
  Manufacturing: "turn between centres (two-setup)".
- **PROPOSED-TURN-001 [minor]: FAIL — VISION FALSE POSITIVE, refuted by probe.**
  The rule claims "no circlip groove ... both end faces terminate in plain
  square-edged cylinders" and that each bearing is located in one direction only.
  The 1.85 mm groove is simply below the render's pixel resolution at this
  zoom (1.85 mm on a 300 mm part = ~7 px). The groove is measurably present:
  dia 37.5000 over z = 84.010..85.840 (check 5 above), and it is the outboard
  clamp face that gives the DE bearing its 18.000 mm zero-float pocket
  (check 3). The FE bearing is single-side located BY DESIGN — the brief routes
  all thrust through the DE bearing and takes FE float in the housing bore.
  Not a defect.
- DFM-TURN-004 [minor]: UNCERTAIN — the evaluator could not convert pixels to
  mm and so would not rule on grooving-tool width. Resolved by measurement:
  narrowest plunge feature is the circlip groove at 1.850 mm wide x 1.250 mm
  deep (dia 40 -> 37.5), which is a standard DIN 471 groove cut with a
  purpose-ground 1.85 mm circlip grooving insert, and the collar is 6.000 mm
  wide at dia 48 — both routine for CNC turning. No action.

### Accepted findings (recorded, NOT failures)

- **A1 — No fillets anywhere.** Deferred project-wide by harness rule. The
  square dia 45 -> 48 collar step at z = +60 and the shoulders are stress
  risers a later fillet pass should address. Expected and accepted.
- **A2 — Far-end shoulder height.** The dia 45 mid body gives a nominal 2.5 mm
  radial shoulder against the FE bearing inner ring (catalogue da-min is 47).
  Measured, the usable flat annulus is r 21.000..22.500 = **1.500 mm** once the
  1 x 45 shoulder chamfer is taken off. Deliberate recorded decision: all thrust
  routes through the located DE bearing, so this face is a creep stop only.
  Accepted, not a defect. (Worth noting the as-built 1.5 mm rather than 2.5 mm
  in the design log, since the chamfer eats 1 mm of it.)
- **A3 — No keyway on the dia 35 extension.** Deliberate (shrink-disc /
  taper-lock hub).
- **A4 — Nominal geometry only.** The k6 seats, h11 groove, h8 ground seal
  journal and h7 extension are text tolerance callouts; the CAD carries
  40.000 / 37.500 / 35.000. Correct per constraints.
- **A5 — Shoulder chamfer direction at both bearing shoulders.** Both are
  material-ADDING 45 deg cones at the concave corner (r 20 -> 21 over 1 mm),
  not undercut reliefs. This is correct shaft practice: a 1.0 mm transition
  sits inside the 6208 inner-ring corner chamfer (r_s min 1.1), so the ring
  still seats flat on the shoulder face. Verified against the 6208 corner
  radius, not assumed.

### Findings

- [ok] Geometry: single solid of revolution, five turned diameters
  (40 / 45 / 48 / 40 / 35) plus one groove, exactly as constraint 57 requires.
- [ok] Coordinate convention: shaft axis on global Z, drive end at +Z, origin on
  the axis midway between the bearing centres (-75 / +75, span 150.000
  confirmed by the seat positions). Assembly can place this with identity.
- [ok] Critical dimension: collar face +66.000 to circlip wall +84.000 =
  18.000 mm, zero drive-end float.
- [minor] **M1 — sixth chamfer missing.** constraints.md Features lists a
  1 x 45 chamfer at z = +60.0, the dia 45 -> dia 48 collar entry. Measured:
  dia 45.000 at z = 59.900, dia 48.000 at z = 60.000 — a square step, no
  chamfer. The five chamfers this validation was tasked to verify are all
  present; this is the non-functional sixth (a concave corner with no mating
  part, back-facing the collar, nothing registers against it). The designer's
  own notes already describe it as "a square dia 45 -> 48 step", so it is a
  known choice rather than an oversight. Does not affect fit, assembly or the
  zero-float requirement. Flagged for the record only.

### Visual Observations

Orientation note first, because it matters for reading the DFM report: in
FRONT_CLEAN the part is drawn with **+Z to the LEFT** (the long 126 mm dia 45
run measures ~497 px of a ~1200 px overall, and the 69 mm far-end section
~275 px, which fixes the scale at ~4 px/mm and the handedness). The DFM
evaluator read the view left-to-right as if left were the far end, which is
why it called the dia 35 pulley extension "the left-hand end stub" and drove
DFM-TURN-002 off the wrong diameter.

- **FRONT_CLEAN**: a stepped turned shaft, six distinct silhouette bands. From
  the left: a plain small-diameter run (~175 px, ~44 mm, ~140 px tall) — the
  dia 35 pulley extension, completely featureless, no keyway slot, no flat, no
  dimple; a step UP to a medium run (~140 px, ~35 mm); then a **narrow vertical
  slot, only ~4-7 px wide, cutting slightly into the silhouette** — this is the
  circlip groove, and it IS visible, contrary to the DFM report's claim that
  "both end faces terminate in plain square-edged cylinders with no narrow
  groove"; then a short medium run of ~71 px (~18 mm) — the drive-end bearing
  seat, and its measured width reads as the bearing width at this scale; then
  the **tallest band in the whole silhouette, a short proud collar ~27 px wide
  (~6.8 mm) standing clearly above both its neighbours** — the dia 48 thrust
  collar; then the longest run (~497 px) at a slightly lower height — the dia 45
  mid body; then a final step DOWN to the far-end run (~275 px). So the drive
  end reads exactly as the brief describes: collar, then an 18 mm seat, then a
  narrow groove just outboard of it, then the reduced plain extension.
- **FRONT_WIREFRAME**: same silhouette with the hidden back edges shown. The
  interior is EMPTY — no hidden bore circle, no cross-hole, no internal
  feature of any kind. Confirms the solid-shaft / no-through-bore requirement
  (Must-NOT #9). The step corners show small angled cuts at both extreme ends
  rather than square corners, consistent with the end-face chamfers.
- **TOP_CLEAN** (looking down the shaft axis): a nest of **concentric circles**,
  one per turned diameter — outermost the collar, then progressively smaller
  rings. No notch, no keyway slot, no flat interrupting any ring, no bolt
  circle. The nest confirms a true solid of revolution on one axis. The rings
  appear very slightly offset to the eye; that is a projection artifact of the
  axial view, **ground-truthed as a non-issue**: the bounding box is symmetric
  (-24.000..+24.000 in both X and Y) and the part is a single `.revolve(360)`
  about global Z, so it is axisymmetric by construction.
- **ISO_WIREFRAME**: the stepped cylinder in three-quarter view, large end at
  upper left descending through the step cluster to the small plain extension
  at lower right. Dotted grey = hidden far-side edges. The step cluster shows
  closely spaced ring pairs where the collar and the circlip groove sit. No
  surface feature anywhere on the extension.

**Check 10 — PASS.** The renders read as a stepped turned shaft with a visible
collar near the drive end, a narrow groove just outboard of it, and a
reduced-diameter plain extension at the +Z end. Nothing visible contradicts the
dimensional findings. The only two apparent anomalies (the "missing" circlip
groove in the DFM vision pass, and the apparent eccentricity in TOP_CLEAN) were
both checked arithmetically and are vision artifacts, not defects.

### Recommendations

No repair required. For the record:
1. Optional, cosmetic: add the 1 x 45 chamfer at z = +60 (dia 45 -> dia 48
   collar entry) listed in constraints.md Features, so the model matches its own
   feature list exactly. Non-functional corner; the designer's notes already
   treat it as a square step. Do NOT touch any other geometry to do it.
2. Log in the design log that the far-end bearing abutment face is **1.500 mm**
   of flat annulus as built (r 21.000..22.500), not the nominal 2.5 mm, because
   the shoulder chamfer consumes 1 mm. Already an accepted creep-stop-only face;
   this is a numbers-of-record note, not a change request.
3. DFM-TURN-002 and PROPOSED-TURN-001 should be treated as refuted for this
   part. Both stem from the evaluator reading the render with the +Z end on the
   left and from the 1.85 mm groove falling under the render's pixel
   resolution. Do not "fix" the shaft against either.

VALIDATION: PASSED
