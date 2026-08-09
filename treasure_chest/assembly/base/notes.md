# base — design notes

## Approach
Hollow rectangular box built as `blank` (solid outer block, bottom at Z=0 via
`box(centered=(True,True,False))`) minus an `interior_cavity` cutter offset up by
the 3mm floor. Open top achieved naturally — the cavity cutter's top face sits at
Z=80, so no top wall remains and the rim at Z=80 is flat. Pilot holes are cut with
`cq.Solid.makeCylinder` cutters oriented along ±Y (drilled from the outer face
inward), which is deterministic and avoids face-local workplane coordinate math.

## Key dimensions / rationale
- Outer 180(X) × 120(Y) × 80(Z), spans X∈[-90,90], Y∈[-60,60], Z∈[0,80]. Front=-Y, rear=+Y.
- Walls 3mm, floor 3mm → cavity 174×114×77 (Z=3→80, open top). Verified bbox matches Overall spec exactly.
- Hinge pilots (rear Y=+60): ⌀2.5 × 2mm deep, Z=72, X∈{-58,-42,42,58} (2 clusters at X=±50, 16mm spacing).
- Hasp pilots (front Y=-60): ⌀2.5 × 2mm deep, Z=62, X=±14.
- All pilots blind, drilled outer-face-inward → leaves ~1mm skin in the 3mm wall (per spec, self-tapping screws).

## For adjacent parts
- Top rim seat at Z=80, footprint 180×120 — lid seats flat here.
- Rear pilots receive hinge_block ⌀3.2 clearance holes (M3 self-tapping); hole centers exactly at spec coords.
- Front pilots receive hasp_plate ⌀3.2 clearance holes at X=±14, Z=62.

## Trade-offs / notes
- No fillets (deferred project-wide).
- Volume ~200,569 mm³, consistent with solid-minus-cavity-minus-6-pilots hand calc.

## Validation Report — 2026-07-21
- **Score**: 10/10
- **Volume**: 200569.1 mm^3
- **Bounding box**: -90 to 90 x -60 to 60 x 0 to 80 mm

### DFMA Findings
- DFM 3D_printing [ok]: 5/5 rules passed, 0 failed, verdict=pass (pass2 skipped)

### Visual Observations
- ISO_CLEAN: open-top hollow box, solid floor visible at bottom, thin rim at Z=80; small dots on rear rim = hinge pilots seen from above.
- ISO_WIREFRAME: dashed hidden lines confirm interior cavity + solid floor; faint front-face pilot markers visible.
- TOP_CLEAN: double rectangle (outer 180x120 + inner cavity), confirming open top with thin (3mm) walls.
- TOP_WIREFRAME: 4 faint marks along rear (top) edge in two clusters + 2 marks along front (bottom) edge = 4 hinge + 2 hasp pilots.
- FRONT_WIREFRAME: 2 solid near-face holes + 4 dashed far-face holes = 6 pilots total (hasp near, hinge far).
- FRONT_CLEAN / RIGHT views: outer silhouette + pilot circles, no unexpected features.

### Findings
- [ok] Geometry: hollow rectangular box, solid floor, OPEN TOP — matches spec.
- [ok] Dimensions: bbox 180x120x80 exact (dimension_checker PASS); volume matches analytic solid-minus-cavity-minus-6-pilots.
- [ok] Features: 4 rear hinge pilots + 2 front hasp pilots present (6 total, confirmed in top + front wireframe).
- [ok] Coordinate convention: prismatic, centered on XY, bottom at Z=0 — correct.
- [ok] Manufacturability: 3mm walls (>0.8mm min), DFM 5/5 pass.

### Recommendations
- None. Part meets all constraints.

VALIDATION: PASSED
