# pulley_shaft — notes

## Provenance
Designed by cad_designer (S1). The agent completed part.py AND rendered all 8 views,
then died of context overflow before writing its own notes. The orchestrator salvaged the
work and re-verified it by direct execution rather than re-dispatching a finisher.

## Verified by direct execution (orchestrator S1)
- Solids: 1 · valid: True · volume 28846.4 mm3
- Bounding box 48.0 x 48.0 x 118.0 mm (Ø48 pulley is the max diameter; 118 overall length)
- Z range -44.0 .. +74.0 about the datum

## Datum
Local Z = 0 is the CLAMP SHOULDER FACE (the Ø14 -> Ø10 annular face), per constraints.md.
The assembly resolver places this part by that datum (plan: local 0 -> global -14.0).

## Axial chain (checked against design_plan.md, adds up exactly)
Right of the shoulder: Ø10 impeller seat 45.0 + M10x1.5 nose thread 14.0 + Ø8 inlet-bearing
tail 15.0 = 74.0. Left of the shoulder: Ø14 mid-section + Ø48 pulley + Ø14 stub = 44.0.
Total 118.0. The lock nut face lands at 48.8 from the shoulder (L_IMP_GRIP), which sits inside
the thread region spanning 45.0..59.0 — consistent.

## Simplifications a validator should expect
- The M10x1.5 thread is modeled as a PLAIN Ø10 cylinder, not helical thread geometry.
  Intentional: modeled threads are slow and fragile in CadQuery and add nothing to a fit check.
- No fillets or chamfers anywhere, including the belt groove — fillets are deferred project-wide.
- The belt groove is cut with a torus (radius tool), leaving a ~6.9 mm U-opening in the Ø48 rim.
- The shaft deliberately has NO seat for the 6203; the impeller spigot is interposed per the spec.

## Validation Report: 2026-08-05
- **Score**: 9/10
- **Volume**: 28846.42 mm^3
- **Bounding box**: -24..24 x -24..24 x -44..74 mm (48 x 48 x 118)

### Re-execution
part.py re-executed clean in 55 ms: success=true, 1 solid, isValid=true,
volume 28846.42 mm^3, bbox 48.0 x 48.0 x 118.0 — identical to the S1 salvage figures.
`dimension_checker` PASS against the constraints `Overall:` spec (expected [48.0, 118.0]).

### Section probe (measured, not eyeballed)
Diameters measured by intersecting the solid with a 0.02 mm slab at each Z station and taking
both the bbox extent and 2*sqrt(area/pi). All 14 stations matched the locked segment table
to better than 0.001 mm:

| Station | Z | Expected Ø | Measured Ø |
|---|---|---|---|
| Left stub | -40.0 | 14.0 | 14.000 |
| Pulley rim, left of groove | -34.5 | 48.0 | 48.000 |
| Groove root | -30.0 | 40.0 | 40.000 |
| Pulley rim, right of groove | -25.5 | 48.0 | 48.000 |
| Mid-section | -12.0 | 14.0 | 14.000 |
| Just left of shoulder | -0.5 | 14.0 | 14.000 |
| Just right of shoulder | +0.5 | 10.0 | 10.000 |
| Impeller seat mid | +22.0 | 10.0 | 10.000 |
| Seat/thread boundary | +44.5 | 10.0 | 10.000 |
| Thread mid | +52.0 | 10.0 | 10.000 |
| Thread end | +58.5 | 10.0 | 10.000 |
| Tail start / mid / end | +59.5 / +66 / +73.5 | 8.0 | 8.000 |

The Ø14 -> Ø10 clamp shoulder is a sharp step exactly at Z=0 (14.000 at -0.5, 10.000 at +0.5),
so the assembly datum sits where the resolver expects it.

### Belt groove profile (verified as a true R3.5 round-belt U)
Swept the groove at 1 mm steps: 48.000 at Z=-34, then 43.428 / 41.269 / 40.298 / **40.000** at
the Z=-30 root, mirroring back to 48.000 at Z=-26. Symmetric about Z=-30, root Ø40.0.
The measured Ø43.428 at Z=-33 matches the analytic torus solution (Ø43.39) to 0.04 mm — the cut
is a true 3.5 mm radius torus, not an approximation. Rim opening
= 2*sqrt(3.5^2 - 0.5^2) = 6.93 mm, leaving a 2.535 mm flange land each side, so the "~6.9 mm
U-opening" recorded above is exact.

### DFMA Findings (existing dfma_report.json: conditional_pass, 17 rules, 14 pass / 3 fail)
No CRITICAL rule failed — DFM-CNC-008, DFM-TURN-003 and DFM-GEN-002 (the three critical rules)
all PASSED. The three failures are dispositioned as follows:

- **DFM-TURN-002 [major] slenderness** — PROCESS NOTE, not a geometry change. The rule measured
  L/Dmin ~13.6:1 by taking the 118 mm overall length against the Ø8 tail, the smallest diameter
  anywhere on the part. That is pessimistic: the Ø8 tail is only 15 mm long. Load-bearing
  slenderness on the main body is 118/14 = 8.4:1, ordinary for a turned part with tailstock
  support. Every diameter is locked to a catalog bearing bore (Ø8 = 688 bore, Ø10 = impeller
  bore), so none can move without reopening the whole design.
  Disposition: turn between centres with tailstock support; steady rest for the Ø8 tail.
- **PROPOSED-TURN-001 [minor] axial retention** — FALSE POSITIVE. The rule reports the nose end
  as "a plain square-ended cylinder with no threads". It is in fact the M10x1.5 nose thread,
  modeled deliberately as a plain Ø10 cylinder at annotation level, so the vision evaluator could
  not see it. Axial retention is the clamp stack: the impeller is trapped between the Z=0
  shoulder face and a lock nut landing at Z=+48.8, well inside the 45..59 thread span. No
  retaining-ring groove is wanted here.
- **PROPOSED-TURN-006 [major] thin-wall pulley flange** — MISAPPLIED METRIC. The rule scores a
  48:2.5 "diameter-to-thickness" ratio as if each flange were an unsupported disc. It is not:
  each flange is a rim land 2.535 mm thick projecting only 4.0 mm radially (Ø40 root to Ø48 rim),
  fully backed by the solid Ø40 x 12 mm pulley body. The governing aspect ratio for a rim land is
  projection/thickness = 4.0/2.535 = 1.6:1, which is stocky. Both failing PROPOSED-* rules are
  candidate rules, not ratified rulebook entries.

### Visual Observations
- **FRONT_CLEAN**: a horizontal turned part, axis left-right. Reading the silhouette left to
  right: a short small-diameter square-ended stub (~88 px tall), a step up to a long slender
  cylinder (~116 px, the longest run), a step up to a shorter thicker cylinder (~153 px), then a
  large disc (~495 px tall) with clear semicircular U-notches cut into both top and bottom of its
  rim, then a short square-ended stub (~153 px) past the disc. Ratios read 88/153 = 0.58
  (Ø8/Ø14 = 0.571) and 495/153 = 3.2 (Ø48/Ø14 = 3.43). At ~10.8 px/mm the axial runs read ~13.6,
  ~55, ~22, 12 and ~6.9 mm against the specified 15, 59, 24, 12 and 8. The pulley sits at one end
  with the long thin shaft and stepped nose extending away from it, as designed.
- **FRONT_CLEAN, orientation**: the view is MIRRORED relative to the segment table (+Z renders to
  the left, so the pulley appears on the right). Camera convention, not geometry — the axial
  ordering is preserved.
- **FRONT_CLEAN, thread region**: no step is visible anywhere inside the long Ø10 run, confirming
  the seat and the thread are one continuous Ø10 cylinder (annotation-level thread), as intended.
- **FRONT_WIREFRAME**: same silhouette with hidden lines shown, and no hidden circles, bores,
  cross-holes, keyway or cavity lines appear anywhere. The only internal edges are the two
  vertical tangent lines inside the pulley where the torus meets the rim lands. Confirms a single
  solid body with no through-bore and no secondary features.
- **TOP_CLEAN**: looking down the axis, one large circle (the Ø48 rim, ~905 px) with a tight group
  of concentric inner circles at its centre (the Ø14, Ø10 and Ø8 journals nested). Outer-circle
  centre ~(497, 491) vs inner group ~(497, 497) — coincident to under 1% of the rim diameter, so
  all sections are concentric on one axis. Every circle is perfectly round: no lobes, no chords,
  no flats or keyway notch.
- **Edges**: every visible edge in both elevations is square. No fillets or chamfers, as expected.
- **Not discernible in these views**: the groove root Ø40 is hidden behind the flange lands in the
  top view, and the thread form is by definition invisible (plain cylinder). Both were confirmed
  numerically by the section probe instead.

### Findings
- [ok] Build: 1 solid, isValid=true, re-executes in 55 ms with no warnings.
- [ok] Dimensions: bbox 48 x 48 x 118 mm exact; volume 28846.42 mm^3; dimension_checker PASS.
- [ok] Geometry: all 14 probed stations match the locked segment table to <0.001 mm.
- [ok] Datum: sharp Ø14 -> Ø10 shoulder exactly at Z=0, so the assembly datum is correct.
- [ok] Coordinate convention (Principle 0): revolved part with its axis of revolution on Z and
  cross-sections centred on (0,0) — confirmed concentric in TOP_CLEAN. Z=0 is the mating datum
  rather than the mid-plane, which is the correct choice for a clamp-stack shaft.
- [ok] Belt groove: true R3.5 torus, root Ø40.0 centred at Z=-30, 6.93 mm rim opening.
- [ok] Topology: single body, no bore, no keyway, no cross-holes, no flats — all deliberate.
- [ok] Clamp-stack closure: lock nut face at Z=+48.8 sits inside the 45..59 thread span.
- [minor] Manufacturing process note (DFM-TURN-002): turn between centres with tailstock support
  and use a steady rest for the Ø8 tail. No geometry change required.
- [minor] Deferred by project doctrine, NOT defects: no fillets, no chamfers (including the belt
  groove), no undercut relief grooves; thread modeled without helix; no 6203 seat on the shaft
  (the impeller spigot is interposed, per spec).

### Recommendations
- No geometry changes. Do not modify part.py.
- Carry the DFM-TURN-002 slenderness item into the process sheet, not the model: turn between
  centres, steady rest for the Ø8 tail, and finish the Ø10 seat in one setup with the Ø14
  shoulder to hold seat-to-shoulder perpendicularity.
- Consider retiring or re-scoping PROPOSED-TURN-006: applying a thin-disc diameter/thickness
  metric to a rim land backed by solid material produces false positives on any V or U-groove
  pulley. A rim land is better judged on radial-projection/thickness.
- PROPOSED-TURN-001 will keep mis-firing on any annotation-level thread. If that rule is promoted,
  it needs a way to be told a plain cylinder is a thread (or to read the part's constraints).
- At fillet-reinstatement time (post-deferral), add a small radius at the Ø14 -> Ø10 shoulder
  root for fatigue, and break the sharp corners on the Ø8 tail and nose end for assembly.

VALIDATION: PASSED
