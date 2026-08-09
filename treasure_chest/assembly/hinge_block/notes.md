# notes: hinge_block

## Approach
Solid prismatic block (30×25×30) minus three cutter families — printable bracket,
NOT a knuckle hinge (per constraints). Feature-decomposed (block_blank, pin_bore,
mount_holes). Coordinate convention: centered on XY, bottom at Z=0
→ X∈[-15,15], Y∈[-12.5,12.5], Z∈[0,30]. Verified bbox exactly 30×25×30.

## Key dimensions & rationale
- Pin bore ⌀4 along X (full width) at local Z=15 = block mid-height → assembled Z=80
  (rotation axle; receives the ⌀4 printed dowel).
- Mount holes ⌀3.2 (M3 clearance) along Y (through full 25 mm depth), X=±8 (16 mm spacing).
  - Lower pair Z=7  → assembled Z=72 (base rear pilots ⌀2.5).
  - Upper pair Z=23 → assembled Z=88 (lid rear pilots ⌀2.5).
- The assembled-Z mapping is local_Z + 65 (mid-height 15 → 80), which places the two
  flange hole rows exactly on the plan's 72 / 88 pilot rows.

## Assembly notes (for resolver / adjacent parts)
- ONE part, placed TWICE at assembly X=±50. Identical geometry; not duplicated.
- Cutters use `.extrude(..., both=True)` past the faces for clean through-cuts.
- No fillets (deferred). No chamfers needed — self-tapping M3 into printed walls.
- Pin bore and mount holes drill on ORTHOGONAL axes (X vs Y) so no interference.

## Trade-offs / potential issues
- Mount holes run the full 25 mm Y depth (simple through-holes), not counterbored —
  fine for M3 self-tap into printed base/lid walls.
- Block is fully solid apart from the bores (~21.3 cm³ PLA); acceptable for a small
  bracket. Could be lightened later if print time matters — not required.

## Validation Report — 2026-07-21
- **Score**: 9/10
- **Volume**: solid bracket less 5 bores (~21 cm^3, per design notes)
- **Bounding box**: -15..15 x -12.5..12.5 x 0..30 mm (30 x 25 x 30)

### DFMA Findings
- overall_verdict: conditional_pass, 0 failures, pass2 skipped
- DFM-3DP-002 [minor/warning]: orthogonal bore families mean at least one bore prints
  horizontal → upper-crown overhang/self-bridge. Inherent to a hinge; acceptable at
  ⌀4/⌀3.2 with correct print orientation. Not a blocker.

### Visual Observations
- FRONT_CLEAN: square face, 4 circular holes in a clean 2x2 pattern (mount holes exiting
  the Y face); no pin-bore opening on this face — correct.
- FRONT_WIREFRAME: same 4 circles + central hidden dashed band = pin bore behind the face.
- RIGHT_CLEAN: rectangular face with ONE centered circle = pin bore seen end-on (axis along
  view direction X) — confirms bore runs along X.
- RIGHT_WIREFRAME: central pin-bore circle + hidden vertical dashes = the 4 mount holes.
- TOP_CLEAN: blank rectangle — no hole exits the Z face (correct; neither family is vertical).
- TOP_WIREFRAME: 2 vertical dashed line-pairs (mount holes at X=+/-8) + horizontal dashed
  band (pin bore along X at Y=0) — matches geometry.
- ISO: box with 4 holes on the flange face + single pin bore on the side face.

### Findings
- [ok] Geometry: prismatic bracket, sharp edges, no fillets — matches spec.
- [ok] Dimensions: bbox 30x25x30 exact; dimension_checker deviations = none.
- [ok] Coordinate convention: prismatic, centered on XY, bottom at Z=0 — compliant.
- [ok] Pin bore: ⌀4 through full X at Z=15 (mid-height) — present and correct.
- [ok] Mount holes: 4x ⌀3.2 through Y at X=+/-8, Z=7 & 23 — all present, correct spacing.
- [ok] Placeholder check: real design.
- [minor] Manufacturability: horizontal-bore overhang warning (DFM-3DP-002), design-inherent.

### Recommendations
- None blocking. Optional: print with pin-bore axis vertical, or add teardrop/self-supporting
  hole profiles, to mitigate the horizontal-bore overhang if surface finish matters.

VALIDATION: PASSED
