# Cover (drive-end bolted end cover) - design notes

## Approach

ONE closed annular section revolved 360 deg about Z, then 4 drilled bolt holes.
Nothing else - no edge selection, no `.chamfer()`, no `.fillet()`.

Both required 1 x 45 chamfers (spigot leading edge, seal-pocket mouth) are
carried as EXPLICIT POINTS in the revolve profile.
That is deliberate: edge selection on a revolved body is the most brittle thing
in this part, and the chamfers are load-bearing for assembly
(press lead-in for the seal, pilot lead-in into the housing H7 bore),
so they must not depend on a selector resolving the way we hoped.

The section is an annulus - it never touches the axis - so the revolve yields the
hollow body directly and no bore has to be cut afterwards.

API trap paid for by two sibling agents and avoided here:
on a `cq.Workplane("XZ")` the `revolve()` axis arguments are LOCAL 2D coordinates,
not global 3D vectors.
`revolve(360, (0,0,0), (0,0,1))` revolves about the plane NORMAL (global -Y) and is wrong.
The correct call is `revolve(360.0, (0, 0), (0, 1))`.

Modelled DIRECTLY in the global frame, z = +84 .. +107.
Assembly places it with an identity transform - no rotation, no offset.

## Measured results (printed by part.py on every execution)

| Quantity | Value |
|---|---|
| Solids | **1** |
| Bounding box X, Y, Z | **130.000, 130.000, 23.000** |
| Z extent | **+84.000 .. +107.000** |
| Volume | **153 290.9 mm^3** (in the expected 1.4e5-1.8e5 band) |

`part.py` self-checks all of the above under an `if __name__ == "__main__":` guard,
so an assert can never break the renderer's execution of the module.

## The three jobs and the numbers that prove them

**1. Seal carrier.**
Seal pocket dia **62.000**, straight from z = +84 to the shoulder at z = +100
(16 mm of dia-62 bore for a 10 mm wide seal).
The 40 x 62 x 10 lip seal presses in from the INBOARD (-Z) face and butts the
dia-42 shoulder at z = +100, so it lands at z = +90 .. +100;
the leading 6 mm of dia-62 bore is the grease cavity ahead of the lip.
**Do not "optimise" the bore into a step.**
An earlier revision put a dia-46 bore ahead of the pocket and was rejected as
UNBUILDABLE: a 62 mm seal cannot pass a 46 mm bore from the inboard side, and the
dia-42 bore blocks it from the outboard side - the seal could never be installed.
The shoulder is on the OUTBOARD side on purpose: grease pressure arrives from -Z
and pushes the seal ONTO its shoulder rather than off it.

**2. Bearing clamp.**
The spigot front face at z = +84 bears on the drive-end 6208 OUTER ring and
axially locates it against the housing shoulder.
With the 1 mm pocket-mouth chamfer the flat annular band runs **r 32 .. r 39**;
the 6208 outer ring face spans r 36.5 .. r 40.
**Contact band = r 36.5 .. r 39 = 2.5 mm wide, fully flat.**
No chamfer or relief intrudes on it.

**3. Bolted joint.**
**4 x dia 9.000** through the flange (z = +95 .. +107), bolt circle **dia 104.000**,
at **45 / 135 / 225 / 315 deg** - identical clocking to the housing's 4 x M8
tapped holes. The angles are not negotiable; they are shared verbatim.

## Wrench clearance (computed, per hard constraint 2)

Bolt axes sit at r = 52. The cover outer face is z = +107 and **nothing anywhere
in this unit rises above z = +107** - the only thing further out in +Z is the
dia 35 shaft extension at r 17.5, which is 34.5 mm radially inboard of the bolt circle.
Each M8 socket-head screw therefore stands proud into completely open half-space.

- (a) Head-to-head: neighbouring heads are 90 deg apart on r 52
  -> **73.5 mm centre-to-centre** (2 x 52 x sin45). Head dia 13 -> 60.5 mm of air between heads.
- (b) Socket swing: a socket of OD ~17 mm (r 8.5) centred at r 52 spans
  **r 43.5 .. r 60.5**, entirely inside the flange OD r 65, with free air above z = +107.

**Governing clearance number: the socket's outer sweep reaches r 60.5 against a
flange OD of r 65, i.e. 4.5 mm of flange still outboard of the socket, and the
swing radius in open space above z = +107 is unobstructed (well past the 15 mm
requirement).** No local relief needed anywhere.

## Walls recorded

- Seal pocket (r 31) to spigot OD (r 40) = **9.0 mm**.
- Bolt-hole outer edge (r 56.5) to flange OD (r 65) = **8.5 mm** rim.

Both are comfortable in machined steel; the 8.5 mm rim is a direct gain from the
post-amendment flange OD 130 (it was 5.5 mm at OD 124).

## Fit callouts (text only - the CAD is NOMINAL)

- Spigot **dia 80 h8** (0 / -0.046) into the housing **dia 80 H7** (+0.030 / 0):
  clearance pilot 0 .. 0.076. The model carries dia 80.000.
- Seal pocket **dia 62 H8**, Ra <= 1.6 um, for the press-fit elastomer-cased lip seal.
- Bolt holes **dia 9 H13** (M8 medium clearance, ISO 273).
- Seal pocket concentric to spigot OD **0.05 TIR** - turn the OD, spigot and both
  internal bores in ONE chucking; this is what keeps the lip true to the shaft.
- Flange back face perpendicular to the spigot axis **0.025**.
- Bolt circle **dia 104 +/- 0.2**, true position dia 0.4 MMC - matches the housing pattern.

## DISCREPANCY against constraints.md (read this)

`constraints.md` in this directory is **PRE-AMENDMENT and STALE**.
The orchestrator changed the design after it was written; the dispatch task string
supersedes it and is what was built. Differences:

| Item | constraints.md (stale) | AS BUILT |
|---|---|---|
| Flange OD | 124.000 | **130.000** |
| Axial extent | z = +90 .. +107 (17 long) | **z = +84 .. +107 (23 long)** |
| Spigot | 5.0 long, 6 mm clear of the bearing, NO contact | **11.0 long (z +84..+95), CLAMPS the 6208 outer ring at z = +84** |
| Flange rim | 5.5 mm | **8.5 mm** |
| Seal pocket | dia 62 x 10 deep (z +90..+100) | **dia 62 straight from z = +84 to the shoulder at z = +100** |

Constraints.md item 5 ("do not lengthen the spigot beyond 5.0 mm ... it would
strike the bearing") is exactly the behaviour now REQUIRED - the cover is the
drive-end bearing's axial retainer. Its constraint 3 (6 mm bearing gap) is void.

Consequence: the renderer's automatic `dimension_check` reports `pass: false`
because it parses the stale "dia 124 x 17" line out of constraints.md and compares
it to the as-built 130 x 23. **This is a stale-document artefact, not a geometry
defect** - the as-built numbers match the amended interface exactly.
Someone with ownership of constraints.md should refresh it; this agent owns only
the part dir contents it was told to write and left constraints.md untouched.

## For adjacent parts

- **Housing**: give me a dia 80.000 H7 drive-end bore at least 11 mm deep from
  z = +95 inward, a boss face at z = +95, boss OD 130 for a flush rim, and 4 x M8
  tapped holes on BC 104 at 45/135/225/315. The bearing outer-ring seat face must
  be positioned so the ring's outboard face lands at z = +84, or my spigot either
  misses it or over-clamps it. **This cover is what preloads the DE bearing:
  the housing must not also have an outboard shoulder there.**
- **Shaft**: the dia-42 bore clears the dia 40 journal by 1.0 mm radially out to
  z = +107. Keep the shaft at dia 40 through z = +84 .. +107 (step down to the
  dia 35 extension only beyond +107, as planned). The seal lip runs on z = +90..+100,
  which must be ground journal - no circlip groove, no step, no tool mark there.
- **Circlip** (DIN 471 - 40, free OD ~43.5, at z = +84 .. +85.85): sits inside my
  dia-62 seal pocket with 9.25 mm radial clearance. No interference, but note the
  seal face at z = +90 is only 4.15 mm outboard of the circlip - do not grow the
  circlip or move the seal inboard.
- **Fasteners**: M8 x 30 ISO 4762. Grip = 12 (cover flange) + ~16 thread engagement = 28 < 30.

## Trade-offs / known ceilings

- Chamfers are profile geometry, not `.chamfer()` operations. If someone later
  reparameterises CHAMFER to 0, the profile degenerates into duplicate points -
  the revolve would fail loudly rather than silently. Acceptable: chamfer 0 is not
  a valid state for this part anyway.
- The spigot front face is a plain flat annulus. No relief groove at the pocket
  corner; the 1 mm chamfer serves as the corner break, which is what keeps the
  bearing band flat out to r 39.
- NO FILLETS anywhere, per project-wide deferral.

---

## Validation

**Date**: 2026-10-08 · **Validator** · Score **10/10**

- **Volume**: 153290.87 mm^3 (independent hand-integration of the profile gives
  153292.0 mm^3; 7e-6 relative agreement -> the solid is the intended shape, not
  an accident that merely bounds correctly)
- **Bounding box**: -65.000..+65.000 x -65.000..+65.000 x **+84.000..+107.000** mm
- **Method**: every number below is MEASURED off the built B-rep via a face
  inventory probe (cylindrical/planar/conical face radii, axes, z-spans and
  areas), NOT read back from the script's own print statements and NOT inferred
  from a render. Vision was run last and is reported separately.

### Measured face inventory (ground truth)

| Face | Measured | Meaning |
|---|---|---|
| CYL r=4.500 x4 | axes (+/-36.770, +/-36.770), z 95.000..107.000 | 4 bolt holes |
| CYL r=21.000 | axis (0,0), z 100.000..107.000 | dia 42 shaft bore |
| CYL r=31.000 | axis (0,0), z 85.000..100.000 | dia 62 seal pocket |
| CYL r=40.000 | axis (0,0), z 85.000.. 95.000 | dia 80 spigot OD |
| CYL r=65.000 | axis (0,0), z 95.000..107.000 | dia 130 flange OD |
| PLANE z=84.000 | area 1561.372, r<=39.000 | spigot front / bearing face |
| PLANE z=100.000 | area 1633.628, r<=31.000 | seal shoulder |
| PLANE z=95.000 | area 7992.212, r<=65.000 | flange back / boss mating face |
| PLANE z=107.000 | area 11633.318, r<=65.000 | cover outer face |
| CONE z 84..85 | rmax 32.000, area 279.902 | pocket-mouth 1x45 chamfer |
| CONE z 84..85 | rmax 40.000, area 350.988 | spigot lead-in 1x45 chamfer |

No toroidal faces exist -> no fillets, confirmed topologically as well as by source grep.

### Numbered checks

1. **PASS - executes, ONE solid.** `success: true`, 51.8 ms, `solids = 1`,
   `result_type: Workplane`. No warnings, no exceptions.
2. **PASS - bounding box.** Measured **130.000 x 130.000 x 23.000**, z
   **+84.000 .. +107.000**. Exact to 3 dp on all six faces of the box.
3. **PASS - exactly FOUR bolt holes.** Probe counted **4** r=4.500 cylinders
   (dia **9.000**), no more and no fewer. Centres measured at r = **52.0006**
   (BC dia **104.001**, the 0.001 is float residue on the cos/sin, not a design
   error) at **45.00 / 135.00 / 225.00 / 315.00 deg**. Each runs z
   95.000..107.000, i.e. fully through the 12 mm flange and nowhere else - the
   1 mm cutter overshoot each side left no coincident faces and no stray
   material. Clocking is identical to the housing's 4 x M8 pattern.
4. **PASS - wrench clearance.** Measured, three ways:
   (a) bolt pitch = 2 x 52.0006 x sin45 = **73.539 mm** centre-to-centre, so
   73.539 - 13.0 = **60.54 mm of air between adjacent 13 mm M8 cap-screw heads**;
   (b) a 17 mm AF socket centred at r 52.0006 sweeps r 43.50..60.50, and the
   measured flange OD is r 65.000, leaving **4.50 mm of flange outboard of the
   socket** - *this is the governing number*;
   (c) overhead space: the measured model `zmax` is exactly **107.000**, which IS
   the flange outer face the heads bear on, so no feature of the cover rises above
   the bolt heads at all. The half-space above z = +107.0 is open.
5. **PASS - spigot.** OD measured **80.000** (CYL r 40.000). Full-diameter land
   runs z 85.000..95.000 with the 1x45 lead-in chamfer occupying z 84.000..85.000,
   so the spigot projects from z = **+84.0 to +95.0 = 11.000 mm** as specified.
6. **PASS - spigot front face is a real flat bearing contact face.** The planar
   face at z = 84.000 measures **area 1561.372 mm^2**; pi x (39^2 - 32^2) =
   1561.372 mm^2 to 3 dp, so the flat annulus runs **r 32.000 .. r 39.000**
   (7.000 mm wide), bounded inboard and outboard by the two chamfers. Against the
   6208 outer ring face at r 36.5..40.0 this gives a contact band of
   **r 36.5..39.0 = 2.500 mm**. Flat, square to the axis, and genuinely present -
   recorded as DESIGNED CONTACT, not interference.
7. **PASS - seal pocket.** Dia measured **62.000** (CYL r 31.000), running
   straight and unobstructed from the chamfer root at z = 85.000 to the shoulder
   at z = 100.000. With the 1 mm mouth chamfer the bore opens at the z = +84.0
   inboard face, so the pocket is 16.0 mm deep overall as specified. No bore
   smaller than dia 62 exists anywhere between z = +84.0 and z = +100.0 (the
   probe found no cylinder with r < 31 in that z range) - the dia-46 defect is
   confirmed ABSENT and the seal can be pressed in from -Z.
8. **PASS - shaft clearance bore.** Dia measured **42.000** (CYL r 21.000),
   z **100.000..107.000** (7.000 long). 1.000 mm radial clearance on the dia 40
   shaft.
9. **PASS - flange.** OD measured **130.000** (CYL r 65.000), z
   **95.000..107.000** = **12.000** thick.
10. **PASS - wall checks.** Seal pocket r31.000 -> spigot OD r40.000 =
    **9.000 mm**. Bolt-hole outer edge r(52.0006+4.500)=56.501 -> flange OD
    r65.000 = **8.499 mm** (nominal 8.5; the 0.001 is the same float residue).
    Both clear the brief's hard 8 mm minimum.
11. **PASS - both 1x45 chamfers present.** Two conical faces measured, both
    spanning z 84.000..85.000 (1.000 mm axial = 1.000 mm radial = 45 deg):
    pocket mouth rmax **32.000**, area 279.902 (pi x 63 x sqrt2 = 279.902 exact);
    spigot leading edge rmax **40.000**, area 350.988 (pi x 79 x sqrt2 = 350.988
    exact). Built as profile geometry rather than `.chamfer()` edge selection,
    which is why they survived the revolve.
12. **PASS - no fillets.** `grep -n fillet part.py` returns nothing, and the face
    inventory contains **zero toroidal/BSpline blend faces**. Confirmed twice.

### `dimension_check` - the stale-document artefact is RESOLVED

Both the standalone `dimension_checker` and the renderer's embedded check now
report **`pass: true`**, expected `[23.0, 130.0]` vs actual `[23.0, 130.0,
130.0]`, zero deviations. The earlier `pass: false` was purely a parse of the
pre-amendment "dia 124 x 17" line; constraints.md now reads "**dia 130 x 23 mm**"
and agrees with the model. **Neither side is wrong - the document caught up to
the metal.** Nothing to fix.

### Coordinate convention (Principle 0)

Deliberately and correctly OFF-origin. The cover is modelled in the global frame
at z = +84..+107 with its axis of revolution on **Z** and both bores concentric
on **(0.000, 0.000)** (measured: every internal cylinder axis is exactly
(0,0)). constraints.md mandates identity placement in the assembly, so this is
compliant, not an origin defect. All four bolt-hole axes are parallel to Z.

### Known-and-accepted findings (NOT defects)

- **dia 62 pocket is 16 mm long for a 10 mm seal** - deliberate grease cavity
  (z +84..+90) ahead of the lip; seal seats z +90..+100. Any DFMA
  "tighten the pocket to 10 mm" recommendation is REJECTED: it re-creates the
  unbuildable condition.
- **Seal shoulder on the outboard side** - correct; grease pressure from -Z
  pushes the seal onto its shoulder.
- **Spigot front face touching the 6208 outer ring** - the intended axial
  location feature, not interference.
- **Missing radii / sharp internal corners in DFMA output** - fillets deferred
  project-wide; expected and accepted.
- **Nominal-only diameters** (80 h8, 62 H8, 9 H13) - fits are drawing callouts
  in constraints.md section "Fit callouts"; modelling nominal is correct.

### Real defects

**None.** No measured value deviates from constraints.md by more than 1 micron of
floating-point residue on the bolt circle (104.001 vs 104.000), which is two
orders of magnitude inside the stated +/- 0.2 bolt-circle tolerance.

### DFMA Findings (`--mode=dfm --force`, confirmed it really evaluated)

Headline: **`conditional_pass`** — and on the per-rule evidence, **nothing failed**.

- **Counter discrepancy, reported for honesty**: the summary block claims
  `rules_passed: 5, rules_failed: 1, rules_uncertain: 4`, but tallying the
  `results` array gives **7 pass / 3 uncertain / 0 fail**, and the `failures`
  array is **empty**. No rule in the report carries a `fail` verdict. The
  summary counters are a tool-side miscount, not a part defect. The part has
  **zero DFM failures**.
- **Process mis-detection [minor, tool-side]**: the evaluator ran as
  `manufacturing_process: CNC_milling`, but constraints.md declares
  **CNC_turning**. It therefore applied the milling rulebook and never applied
  the turning-specific rules (L/D slenderness, tool access, single-chucking
  concentricity). The part is unaffected — constraints.md already records the
  turning case (130 x 23 disc, no L/D concern, 1.3:1 deepest drilling) — but the
  DFM pass is less relevant than it looks and should not be read as turning
  clearance.

| Rule | Severity | Verdict | Note |
|---|---|---|---|
| DFM-CNC-001 min wall | critical | uncertain | **Resolved by measurement: PASS.** Evaluator said "no absolute dimension, no scale bar" in the renders. Measured: flange plate **12.000** thick, thinnest wall anywhere **8.499 mm** (flange rim) — both far above any CNC limit in steel. Its worry about "an internal stepped recess thinning the plate" is the dia 62 pocket, whose floor is the dia-42-bore annulus at z=100, **7.000 mm** thick. Fine. |
| DFM-CNC-002/004/005/006 | major | pass | — |
| DFM-CNC-007 | minor | pass | — |
| DFM-CNC-008 tapped-hole depth | critical | uncertain | **Resolved: rule does not apply.** The evaluator correctly noted it cannot tell a tapped hole from a clearance hole in a render. These are **clearance** holes (plain dia 9.000 straight through, no thread feature); the M8 threads live in the mating housing. Its hypothetical "critical failure if tapped" branch is moot. |
| DFM-GEN-002 | critical | pass | — |
| DFM-GEN-003 | minor | pass | — |
| PROPOSED-ASSY-004 split ring | major | uncertain | **Resolved: assembles fine.** The evaluator worried an unsplit bore cannot pass a captive shaft. The cover slides on over the shaft END from +Z: its smallest bore is **dia 42.000**, which clears both the dia 40 journal and the dia 35 outboard shaft extension. No split needed. |

4 rules were auto-staged as proposals; none bears on this part's acceptance.
**No DFMA recommendation to tighten the dia 62 pocket was issued** — and had one
been, it would have been rejected per the accepted-findings list above.

### Visual Observations (run LAST, after every number above was already measured)

- **TOP_CLEAN**: I see one large outer circle, one concentric circle at roughly a
  third of its diameter, and **four** small equal circles sitting at the four
  diagonal clock positions — upper-left, upper-right, lower-left, lower-right —
  evenly spaced and all the same size. Scaling off the outer circle (~900 px for
  the known 130 mm = 6.92 px/mm): the central circle reads **~43 mm** (model
  42.000), the small circles **~9.8 mm** (model 9.000) on an apparent bolt circle
  of **~103.5 mm** (model 104.001). Pixel-level agreement.
  Notably the dia 62 pocket and dia 80 spigot are **absent** from this view —
  correct, both are occluded behind the solid z=+107 outer face, which also
  confirms the camera sits on the +Z (outboard) side.
- **FRONT_WIREFRAME**: I see the part in profile as two rectangles of different
  heights, butted. The tall slim one measures ~902 x 87 px = **130 x 12.5 mm**
  (the flange); the shorter one projecting from its side measures ~562 x 75 px =
  **81 x 10.8 mm** (the spigot). So the stepped two-diameter turned profile is
  really there and in the right proportion. +Z points left in this view.
  Hidden (dotted) horizontals sit at apparent radii **±41.4, ±31.8, ±21.2 mm**
  against the modelled 40 / 31 / 21. A dotted vertical crosses at **z ≈ 100.9**
  (the modelled seal shoulder at z=100). At the spigot's free end I can see a
  **doubled vertical line about 1 mm apart** — the 1x45 chamfer at z=+84.
- **FRONT_WIREFRAME — vision-only ambiguity, flagged deliberately**: the bolt
  holes project into this view at an apparent radius band of
  52.0 x sin45 ± 4.5 = **32.3 .. 41.3 mm**, which lands almost exactly on top of
  the r31 pocket and r40 spigot hidden lines. The front wireframe therefore
  **cannot** separate bolt-hole edges from bore edges here. I did not try to read
  the bolt pattern from it; the pattern was established by face-probe measurement
  and corroborated by TOP_CLEAN. Recorded so no later reader mistakes those
  overlapping dotted lines for a defect.
- **ISO_CLEAN**: reads unmistakably as a **flanged, bored, turned disc**. Each of
  the four bolt holes shows a crescent of its own inner cylindrical wall, which
  is what a genuine **through**-hole looks like in iso — not a blind dimple. The
  central bore shows a double edge (the z=+107 bore mouth with the z=+100
  shoulder visible behind it through the opening) and the rim shows a double edge
  (flange OD at z=+107 and at z=+95). The spigot is hidden behind the flange from
  this +Z viewpoint, as it should be.
- **Nothing in any view contradicts the dimensional findings.** No stray solids,
  no missing or extra holes, no asymmetry, no self-intersection artefacts.

### Which findings are measured vs vision-only

- **Measured (B-rep probe / executor / dimension_checker)**: checks 1-12 in full,
  every diameter, every z station, hole count, hole positions, both chamfers,
  all wall thicknesses, the wrench-clearance arithmetic, the absence of fillets.
- **Vision-only**: the overall "does it read as the right kind of object" gestalt,
  and the ISO confirmation that the bolt holes are through rather than blind.
  Both agree with the measurements; neither was used to override one.
- **Vision rejected as unreliable**: reading the bolt pattern off FRONT_WIREFRAME
  (overlapping hidden lines, see above).

### Verdict

All 12 commissioned checks **PASS** on measured geometry. Zero DFM rules fail.
Both `dimension_check` instances now agree with the model. The three DFMA
uncertainties are all image-grounding limitations that the measurements resolve
in the part's favour. No defect of any severity was found in the part; the only
two issues recorded are tool-side (the DFMA counter miscount and the
CNC_milling/CNC_turning process mis-detection), and neither is the designer's to
fix.

VALIDATION: PASSED
