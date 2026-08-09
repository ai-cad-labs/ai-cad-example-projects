# Design Notes: piston_ring

## Approach
Simple 2-feature part, kept inline (per the 3+ feature extraction rule):
1. **Annular body** — `circle(30.25).circle(27.75).extrude(1.25, both=True)`: rectangular-section ring, no taper, no chamfer, no fillets (project-wide deferral).
2. **End gap** — 1.0 mm straight radial slot cut with a box cutter along +X (Y-centered), spanning radially and axially past the section with 1.0 mm overshoot on all cut directions. Represents the wire-EDM/slitting-saw split; gap faces are parallel planes 1.0 mm apart.

## Key dimensions (all locked from constraints.md — zero drift)
- Free OD 60.5 / free ID 55.5 (radial thickness 2.5)
- Axial height 2.5 → 0.1 mm side clearance in the piston's 2.6 mm groove
- End gap 1.0 mm, located on +X
- Coordinate convention: ring axis = Z, section centered at origin, Z = -1.25 .. +1.25

## Verification
- Executor: success, volume 1132.58 mm³ (hand-calc π(30.25²−27.75²)×2.5 − gap ≈ 1132.6 ✓), bbox exactly (±30.25, ±30.25, ±1.25)
- Renderer dimension check: PASS (expected [2.5, 60.5] vs actual [2.5, 60.5, 60.5])
- All 8 renders visually verified: annulus + gap present, uniform section, no unexpected features
- Compressed-state back clearance (informational, not modeled): working OD 60.0 → ID 55.0 > groove root ⌀54.0 → 0.5 mm ✓

## Constraints discovered
None new — the piston's AS-DESIGNED grooves (2.6 axial × 3.0 radial, root ⌀54.0) match the plan exactly, so the ring section 2.5 × 2.5 fits with the intended 0.1 axial / 0.5 radial clearances.

## For adjacent parts / assembly resolver
- One geometry, instanced 3x — seat each instance concentric with the piston axis at each groove mid-height (ring section is Z-centered, so `cq.Location` offset = groove mid-height directly).
- Gap is at +X in part frame; the assembly may rotate instances about Z to clock the gaps (standard practice ~120° apart) — free choice, no interference either way.
- Ring is modeled in FREE state (OD 60.5). At the piston's working OD 60.0 the ring would be sprung closed ~0.5 mm on diameter; a static assembly render will show the free ring standing 0.25 mm proud of the ⌀60 piston OD — expected, not an error.

## Trade-offs
- v1 shares one geometry between compression and oil rings (no oil drainage slots) per constraints.
- Gap modeled as parallel-face slot (chord cut), not a true wedge angular cut — per constraints' "simple angular gap cut" allowance; difference is negligible at 1.0 mm width on ⌀60.5.

## Validation Report — 2026-07-13
- **Score**: 10/10
- **Volume**: 1132.58 mm^3
- **Bounding box**: -30.25-30.25 x -30.25-30.25 x -1.25-1.25 mm

### DFMA Findings
- DFM (CNC_turning, 17 rules): verdict conditional_pass — 16 passed, 0 critical/major failures
- PROPOSED-GEN-001 [warning]: "inner and outer edges of the ring, as well as the edges at the gap, are perfectly sharp 90-degree angles" — expected and per spec: constraints.md mandates "no taper, no chamfer" and fillets are deferred project-wide. Not a defect.
- Placeholder detector: not a placeholder — real implementation.

### Visual Observations
- TOP_CLEAN: I see two concentric circles forming a thin annulus, with a single narrow radial break at the 3 o'clock (+X) position that interrupts BOTH the outer and inner circle — the gap severs the full radial section. Annulus wall looks visually thin relative to the ~60 mm diameter, consistent with a 2.5 mm wall on a 30.25 mm radius.
- TOP_WIREFRAME: same annulus + gap; the short parallel edges of the two gap faces are visible at the break. No other features (no slots, holes, or steps) anywhere on the circumference.
- FRONT_CLEAN: a very thin, tall rectangle — the ring edge-on (height ≈ diameter, width ≈ axial 2.5 mm). Flat top and bottom, straight parallel sides: rectangular section, no taper or chamfer discernible.
- FRONT_WIREFRAME: same silhouette; two small light-gray hidden-line marks near the top and bottom ends — internal edges of the far side/gap region seen through the part. Nothing unexpected.
- RIGHT_CLEAN: thin tall rectangle with a small dark notch/break at mid-height of the strip — this is the +X end gap facing the viewer (right view looks along X; the Z-centered gap projects at strip center). Confirms the gap passes fully through the axial height.
- RIGHT_WIREFRAME: visible split line across the strip at mid-height (the two gap faces), strip otherwise continuous and uniform in width.
- ISO_CLEAN: circular ring seen obliquely; gap visible as a clean break on the right side; uniform rectangular section all around.
- ISO_WIREFRAME: hidden (dashed gray) far-side edges follow the same two concentric circles — uniform section, no internal features besides the gap.

### Findings
- [ok] Geometry: split annular ring, rectangular cross-section — matches description
- [ok] Focus check 1 — section 2.5 radial x 2.5 axial: radial = (60.5−55.5)/2 = 2.5 (bbox X/Y span 60.5, code ID 55.5); axial = bbox Z span 2.5 ✓
- [ok] Focus check 2 — free OD 60.5 / ID 55.5: bbox 60.5 across X and Y; ID 55.5 derived in code (free_od − 2×2.5); volume hand-calc π(30.25²−27.75²)×2.5 − gap ≈ 1132.6 matches executor's 1132.58 exactly, confirming the ID is real ✓
- [ok] Focus check 3 — 1.0 mm end gap fully through: cutter spans radially 26.625–31.125 (covers 27.75–30.25 with 1.0 overshoot) and axially ±2.25 (covers ±1.25); TOP views show both circles interrupted at +X; RIGHT views show the break through the full strip ✓
- [ok] Focus check 4 — centered on Z at origin: bbox symmetric (±30.25, ±30.25, ±1.25); revolved part, axis = Z, section centered at origin — Principle 0 satisfied ✓
- [ok] Focus check 5 — no fillets/chamfers/taper: none in code; renders show sharp rectangular section throughout (DFMA sharp-edge warning confirms sharpness, which is per spec) ✓
- [ok] Dimensions: dimension_checker PASS — expected [2.5, 60.5] vs actual [2.5, 60.5, 60.5], zero deviations
- [ok] Free-state note honored: OD 60.5 (0.25 mm proud of ⌀60 piston) is by design per task directive — NOT flagged as failure
- [ok] Manufacturability: 2.5 mm section > 1.5 mm turning minimum; gap cut = wire EDM/slitting saw per constraints

### Recommendations
- None required. Optional future (v2): oil-ring drainage slots if the shared-geometry simplification is lifted; gap clocking (~120° apart) is an assembly-level choice already documented above.

VALIDATION: PASSED
