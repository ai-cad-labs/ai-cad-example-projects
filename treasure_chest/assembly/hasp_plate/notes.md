# notes: hasp_plate

## Approach
Flat prismatic latch plate, 40(X) × 4(Y-thick) × 50(Z) mm, centered on XY, bottom at Z=0
(COOKBOOK Principle 0). Built as `.box()` + `.translate((0,0,25))`. Three through-holes cut
along the Y (thickness) axis via explicit `Solid.makeCylinder` cutters oriented along +Y —
unambiguous placement vs face-workplane local-coord juggling.

## Holes (local frame)
- Latch: ⌀6.0 at X=0, Z=42 (near top; assembled Z≈95, aligns to lid front ⌀6).
- Mount ×2: ⌀3.2 at X=±14, Z=10 (lower half; assembled Z=62, over base front pilots ⌀2.5, M3 self-tap).
- All holes bore fully through Y (cutter length 8mm > 4mm plate).

## Verification
`tools.cadquery_executor` → success, volume 7822.56 mm³, bbox exactly 40×4×50
(X∈[-20,20], Y∈[-2,2], Z∈[0,50]). No fillets (deferred).

## For adjacent parts / assembly_resolver
- Local frame matches design_plan: assembled on front face Y=−60, centered X=0, straddling seam at Z=80.
  Local Z=42 latch → assembled ≈95; local Z=10 mounts → assembled 62 (consistent w/ plan §Interfaces).
- Holes run along Y = the mounting/latch axis once placed on the front face. No rotation needed beyond
  the resolver's front-face placement offset.

## Validation Report — 2026-07-21
- **Score**: 10/10
- **Volume**: 7822.6 mm^3
- **Bounding box**: -20 to 20 (X) x -2 to 2 (Y) x 0 to 50 (Z) mm

### DFMA Findings
- DFM 3D_printing: 5/5 rules PASS, 0 failed, 0 warnings (verdict=pass, dfma_report.json written).

### Visual Observations
- FRONT_CLEAN/WIREFRAME: flat rectangular plate with 3 through-holes — one larger circle and two smaller circles. Front view is rendered rotated (model Z→horizontal), so the larger latch hole sits at one short-axis end and the two smaller mount holes cluster at the opposite end, symmetric about the long axis. Wireframe shows the holes fully bored through (dashed hidden circle).
- TOP_CLEAN/WIREFRAME: thin long bar (40 x 4) — the 4mm plate thickness; wireframe dashes mark the 3 bores passing through the thickness.
- RIGHT_CLEAN/WIREFRAME: thin bar edge view; wireframe dashes confirm through-holes exit both faces.
- ISO: flat plate; 3 through-holes visibly bored top-to-bottom, one clearly larger than the other two.

### Findings (ground-truthed against geometry, not vision alone)
- [ok] Geometry: flat plate, correct prismatic topology.
- [ok] Dimensions: bbox 40 x 4 x 50 mm — dimension_checker PASS (expected [4,40,50] = actual).
- [ok] Coordinate convention (Principle 0): prismatic — centered on XY (X -20..20, Y -2..2), bottom at Z=0. Correct.
- [ok] Latch hole: ⌀6.0 at X=0.0, Z=42.0, Y-axis through-hole. Matches constraint (near top, X=0).
- [ok] Mount holes: two ⌀3.2 at X=-14.0 and X=+14.0, Z=10.0, Y-axis through-holes. Matches constraint (lower half, X=±14, M3 clearance).
- [ok] All three holes bore along Y (through 4mm thickness), exit both faces.
- [ok] No fillets present (correctly deferred).

### Recommendations
- None. Part meets all constraints.

VALIDATION: PASSED
