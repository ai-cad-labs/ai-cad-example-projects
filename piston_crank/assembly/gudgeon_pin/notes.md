# Design Notes: gudgeon_pin

## Approach
Simplest possible construction: annulus profile (outer circle ⌀15.99 + coaxial inner
circle ⌀9.0 on the same Workplane stack) extruded symmetrically about Z=0 with
`extrude(25.0, both=True)`. One solid operation, no booleans needed. Inline code
(no feature functions) — this is a 1-feature part per the extraction rule.

## Key dimensions and rationale
- **OD 15.99 mm** — pin side of the ⌀16.0 nominal CLEARANCE fit. Both mating bores
  (piston bosses AND rod small end) are 16.02, giving 0.03 mm diametral clearance =
  full-floating (pin free to rotate in both piston and rod). Deliberately NOT
  interference — do not "fix" to 16.00/16.02 press dimensions.
- **Length 50.0 mm**, centered → Z = -25.0 .. +25.0 per the revolved-part convention.
  Spans the piston's AS-DESIGNED boss outer span of 48.0 with 1.0 mm protrusion per
  side into open cavity; half-length 25.0 < skirt inner radius 27.0 (⌀54 skirt inner
  wall), so the pin stays fully inside the piston with no retention needed in v1.
- **Bore ⌀9.0 through** — mass reduction; wall = 3.495 mm ≥ 1.5 mm min for turning.

## Verification results
- Executor: success; volume 6859.67 mm³ matches analytic π/4·(15.99²−9²)·50 = 6859.66 ✓
- Bbox: ±8.0 x ±8.0 x Z ±25.0 ✓ (renderer dimension_check pass vs "⌀16 x 50")
- All 8 renders visually confirmed: annulus cross-section, through bore (hidden
  lines full length), flat square ends, no chamfers/grooves.

## Constraints discovered
None new — all dimensions were fully locked by constraints.md / design_plan.md.

## What adjacent parts should know
- Pin axis = Z, centered at origin (Z ±25.0). Assembly resolver: at TDC the pin axis
  sits at (125, 0) parallel to global Z per design_plan.md — position with a single
  cq.Location; the rod small end and piston boss bores must land coaxial with it.
- NO circlip grooves exist — v1 retention relies on the ⌀54 skirt inner wall
  (pin half-length 25 < 27 skirt inner radius). If a future piston redesign narrows
  the skirt or opens the boss area, revisit retention.
- Ends are flat and square (no chamfers) — chamfers deferred with the project-wide
  fillet deferral; a real pin would get lead-in chamfers at the grind/assembly stage.

## Validation Report — 2026-07-13
- **Score**: 10/10
- **Volume**: 6859.67 mm^3
- **Bounding box**: -8.0-8.0 x -8.0-8.0 x -25.0-25.0 mm (bbox JSON rounds ±7.995 to ±8.0; volume confirms OD 15.99 — see Findings)

### DFMA Findings
- Overall verdict: conditional_pass (17 rules, 14 passed, 2 failed at rule level but 0 in failures list, 1 uncertain) — NO critical failures
- DFM-TURN-001 [minor/warning]: bore diameter >= 3mm could not be confirmed from unscaled images alone — pass per code (bore ⌀9.0 >= 3.0)
- PROPOSED-GEN-001 [minor/warning]: sharp 90° outer edges, no chamfers — INTENTIONAL per constraints.md ("NO fillets"; chamfers deferred with project-wide fillet deferral)
- PROPOSED-ASSY-003 [minor/warning]: no chamfered lead-in at bore entrances — same intentional v1 policy; constraints.md specifies "flat square ends"
- Placeholder detector: real design, not a stub

### Visual Observations
- FRONT_WIREFRAME: I see a wide horizontal rectangle of constant height across its full length, with two light dashed horizontal lines running end-to-end inside it (upper and lower bore walls). The dashed lines reach both ends — the bore is through with both ends open. A single vertical line at mid-length is the cylinder silhouette seam (tessellation edge), not a step: the outer profile height is identical on both sides of it.
- FRONT_CLEAN: plain rectangle silhouette, perfectly flat vertical ends, no chamfer breaks, no groove notches, no diameter steps anywhere along the length.
- TOP_WIREFRAME: two concentric circles centered in the view; the inner circle is a bit over half the outer circle's diameter, consistent with 9.0/15.99 ≈ 0.56. No eccentricity visible.
- TOP_CLEAN: identical two concentric circles — annulus cross-section confirmed.
- RIGHT_WIREFRAME / RIGHT_CLEAN: identical to the front views (as expected for an axisymmetric part): constant-height rectangle, through-running hidden bore lines, flat square ends.
- ISO_WIREFRAME: tube seen at an angle; near end shows the open bore circle, and dashed hidden circles/lines trace the far-end bore opening and the bore running the full length — through bore visible from geometry, not inferred.
- ISO_CLEAN: clean hollow cylinder, uniform OD along the whole length, open bore at the near end, no external features of any kind.
- NOT visible: no circlip grooves, no chamfers, no fillets, no steps in any of the 8 views.

### Findings
- [ok] Geometry: plain hollow cylinder (annulus extrusion), correct topology for a full-floating gudgeon pin
- [ok] OD = 15.99 mm (clearance side of ⌀16 nominal, NOT 16.00+): bbox JSON shows ±8.0 but that is 2-decimal display rounding of ±7.995 — measured volume 6859.67 mm³ matches the analytic value for OD 15.99 (π·(7.995²−4.5²)·50 = 6859.68 mm³) and does NOT match OD 16.00 (which would give 6872.23 mm³). part.py sets pin_od = 15.99 explicitly.
- [ok] Length = 50.0 mm, centered on Z: bbox zmin/zmax = -25.0/+25.0 exactly (Principle 0 satisfied: revolution axis on Z, cross-section centered at origin)
- [ok] Through bore ⌀9.0: code creates coaxial inner circle extruded with the outer over the full length; hidden bore lines run end-to-end in FRONT/RIGHT wireframes and both bore openings are visible in the ISO views — truly through, both ends open. Volume match further confirms ID 9.0.
- [ok] Plain tube: no chamfers, grooves, or steps in any view (v1 no-circlip policy per constraints.md)
- [ok] No fillets (deferred project-wide)
- [ok] Dimension check: PASS — expected [16.0, 50.0] vs actual [16.0, 16.0, 50.0] within tolerance
- [ok] Coordinate convention: revolved part, axis = Z, centered at origin
- [ok] Manufacturability: wall 3.495 mm >= 1.5 mm; L/D = 3.1; bore depth/dia = 5.6 — all within CNC turning limits; DFMA conditional_pass with zero critical failures

### Recommendations
- None required for v1. The three DFMA warnings (missing edge/bore chamfers) are the intentional project-wide deferral; revisit at the chamfer/fillet optimization phase together with circlip retention if the piston skirt design changes.

VALIDATION: PASSED
