# notes: shaft

## Approach
Plain solid cylinder — single primitive, no feature decomposition needed (1 feature).
`Workplane("XY").circle(4).extrude(30).translate((0,0,-15))` so the part is centred
about Z=0 (Z = -15..+15) with the axis of revolution on Z, per COOKBOOK Principle 0.

## Key dimensions
- ⌀8mm OD (radius 4), 30mm length. L/D = 3.75:1.
- Parametric: `shaft_diameter`, `shaft_length` at top of part.py.

## Verification
Executor: success, volume 1507.96 mm³ (= π·4²·30, exact), bbox x/y ±4, z ±15. Matches spec.

## For adjacent parts (pinion, gear)
- Shaft OD is nominal ⌀8 with NO clearance applied on this side. Any slip-fit
  clearance must be taken on the gear/pinion bore side (their ⌀8mm bores).
- Shaft is centred on Z at origin, so mating a gear is a pure Z-offset via cq.Location.

## Trade-offs / issues
- None. NO fillets/chamfers per project policy (edges left sharp, deferred phase).

## Validation Report — 2026-07-21
- **Score**: 10/10
- **Volume**: 1507.96 mm^3 (= π·4²·30, exact)
- **Bounding box**: -4.0–4.0 x -4.0–4.0 x -15.0–15.0 mm

### DFMA Findings
- DFM (3D_printing, 6 applicable rules) [ok]: 6/6 passed, 0 failed, verdict=pass. Report written to dfma_report.json. Pass-2 skipped (no failures).

### Visual Observations
- FRONT_WIREFRAME: wide rectangle ~3.75:1 (30 long × 8 across), no internal hidden lines — clean side profile of a solid cylinder.
- FRONT_CLEAN: identical wide rectangle silhouette.
- TOP_WIREFRAME: single circular ring outline (the ⌀8 cross-section looking down the Z axis).
- TOP_CLEAN: same circle, no internal features (no bore).
- RIGHT_WIREFRAME/RIGHT_CLEAN: same wide rectangle as front — rotational symmetry confirmed.
- ISO_WIREFRAME: 3D cylinder with visible circular end face + dashed hidden-line arc for the far edge — correct cylinder topology.
- ISO_CLEAN: cylinder, sharp edges, no fillets/chamfers.

### Findings
- [ok] Geometry: plain solid cylinder, correct topology (circle in top view, rectangle in front/right, cylinder in iso).
- [ok] Dimensions: dimension_checker PASS — expected [8.0, 30.0], actual [8.0, 8.0, 30.0]; bbox ⌀8 × 30mm, 0 deviations.
- [ok] Features: no holes/slots/chamfers required; none present, per spec. NO fillets (correctly deferred).
- [ok] Coordinate convention (Principle 0): revolved part, axis of revolution on Z, cross-section centred at origin (bbox X/Y ±4, Z ±15 — symmetric protrusion). Correct.
- [ok] Manufacturability: L/D = 3.75:1, well under limits; DFM 6/6 pass for 3D printing.
- [ok] Constraints compliance: all constraints.md items satisfied (⌀8, L=30, plain cylinder, no features, no fillets, Z-centred).
- [ok] Not a placeholder: placeholder_detector reports real design.

### Recommendations
- None. Part is correct and complete; no repair needed.

VALIDATION: PASSED
