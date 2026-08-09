# Assembly: piston_crank (flat, 5 parts, TDC pose) — RESOLVED

**Status (2026-07-13, assembly_resolver)**: assembly.py composed with direct `cq.Location` placements, executed clean (Compound, 337.7 ms), rendered, all 8 colored views visually verified. **ZERO interface conflicts** — no proposals filed, open_issues.md untouched (empty).

Single-cylinder piston-crank core. Flat structure — no sub-assemblies. piston_ring is one part instanced 3x. All clearances positive (rotating/floating fits); no interference found in the posed compound.

## Global frame

Per design_plan.md § Assembly Pose:
- Crank main axis = global Z; crankshaft centered at origin; throw at TDC = +X
- Piston reciprocation axis = global X; all pin/bore axes parallel to Z
- Plane of motion Z = 0 (rod, big end, crank pin, gudgeon pin all Z-centered)

## Interfaces checked (code = ground truth, per-part part.py values)

| Interface | As-coded A | As-coded B | Result |
|---|---|---|---|
| gudgeon_pin ↔ piston bosses | pin_od 15.99 | pin_bore_dia 16.02 | ✓ 0.03 diametral clearance, full-floating |
| gudgeon_pin ↔ rod small end | pin_od 15.99 | small_end_bore_dia 16.02 | ✓ 0.03 diametral clearance, full-floating |
| crank pin ↔ rod big end | ⌀38.0, free span 22.0 (Z ±11) | bore 38.05, width 20.0 (Z ±10) | ✓ 0.05 dia clearance, 1.0 mm/side axial |
| rod small end ↔ piston boss gap | width 20.0 | boss_inner_gap 22.0 (faces x=±11) | ✓ 1.0 mm/side |
| pin length ↔ piston boss span | 50.0 (Z ±25) | boss_outer_span 48.0; skirt inner r 27 | ✓ 1.0 mm protrusion/side, fully inside skirt |
| piston_ring ↔ grooves | section 2.5×2.5, FREE OD 60.5 | groove 2.6 axial × 3.0 radial, root ⌀54, mids 6.3/11.9/17.5 below crown | ✓ 0.1 axial clearance; free ring renders 0.25 mm proud of piston OD 60 — BY DESIGN (uncompressed free state), not interference |
| kinematic closure | throw 30 + center distance 95 | gudgeon axis X=125; crown top X=125+32=157 | ✓ (stroke 60; BDC pin axis would be X=65) |
| swing/clearance | piston skirt bottom X=102 | web disc radius 50 | ✓ 52 mm gap; rod I-beam max radial 12.8 < skirt inner r 27 where it enters the skirt |

Note vs the earlier draft of this file: rings are placed in their as-built FREE state (OD 60.5), NOT re-modeled at compressed working OD 60.0 — per piston_ring/notes.md and orchestrator direction, the 0.25 mm proud condition is an accepted static-render artifact.

Piston accepted deviations honored (stepped interior ⌀47/⌀54; boss web merging into skirt wall — see assembly/piston/notes.md): no conflicts filed on these.

## Mate relationships (as placed in assembly.py)

| Part | Location | Derivation |
|---|---|---|
| crankshaft | identity | local frame already = global (main axis Z at origin, crank pin at (30,0), free span Z ±11) |
| connecting_rod | translate (30, 0, 0) | big-end bore is local Z through origin, long axis +X, width Z ±10 → pure translation seats the big end on the crank pin; small end lands at (125, 0, 0) = 30 + 95. No rotation needed. |
| gudgeon_pin | translate (125, 0, 0) | pin local axis = Z, centered at origin → pure translation onto the gudgeon axis; spans Z ±25 |
| piston | rotate +90° about Y, then translate (129.5, 0, 0) | rotation maps piston local +Z → global +X (crown faces +X) and the local-X pin bore → global Z; pin bore center local (0,0,−4.5) rotates to (−4.5,0,0), so tx = 125 − (−4.5) = **129.5**. Checks: crown top 129.5+27.5 = 157 ✓; skirt bottom 129.5−27.5 = 102 ✓ |
| piston_ring ×3 | pre-rotate about own axis 0°/120°/240°, then rotate +90° about Y, translate (X_seat, 0, 0) | X_seat = 157 − groove mid-depth {6.3, 11.9, 17.5} = **{150.7, 145.1, 139.5}**; ring section is Z-centered locally so seat X is the translation directly. Pre-rotation clocks the three +X end gaps ~120° apart about the ring axis. |

## Verification

- Executor: success, `Compound`, volume 333,808.54 mm³ = exact sum of the 7 part volumes (217,373.08 + 37,260.78 + 6,859.67 + 68,917.28 + 3×1,132.58) → all solids present, zero boolean loss
- Bbox: X −50…157 (web OD → crown top, matches plan), Y ±50, Z ±46 — exactly as predicted
- All 8 renders read against the color legend: TOP shows big end concentric on the crank pin at X=30 and pin circles concentric in the small end at X=125; RIGHT shows the pin symmetric Z ±25, big end centered in the 22 mm web gap with visible clearance, rings concentric and slightly proud (expected), gaps clocked apart; FRONT/ISO show the full chain with no floating parts and no interpenetration

## Conflicts opened

None.

## Sub-assembly structure

Flat — 5 parts (piston_ring instanced 3x), no sub-assemblies.

## Outputs

- `assembly.py` — loads all 5 parts via `load_part()` (ring instanced 3x), direct `cq.Location` placements, `result = assy.toCompound()`
- Renders: `assembly/renders/{front,top,right,iso}_{clean,wireframe}.png` + `color_legend.txt`
