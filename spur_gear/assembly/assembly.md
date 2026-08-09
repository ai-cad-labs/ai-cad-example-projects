# Assembly: spur_gear

## Structure
FLAT assembly — no sub-assemblies. 3 distinct Make parts, 4 instances total:
- `pinion` × 1
- `gear` × 1
- `shaft` × 2  (one shaft per gear — the single shaft part is instantiated twice)

## Parts & Coordinate Frames
All parts are modelled centred on their own Z-axis at the origin (COOKBOOK
Principle 0). The assembly_resolver composes them via `cq.Location` transforms.

| Part   | Frame at origin                       | Axis |
|--------|---------------------------------------|------|
| pinion | pitch ⌀36, outside ⌀40, centred XY, Z axis | Z  |
| gear   | pitch ⌀60, outside ⌀64, centred XY, Z axis | Z  |
| shaft  | ⌀8 × 30 cylinder, centred, Z axis     | Z    |

## Interfaces

### Gear ↔ shaft (slip fit)
- Each gear's ⌀8mm bore slip-fits over a shaft's ⌀8mm OD (nominal ⌀8 both).
- Shaft passes through the full 10mm face width; the shaft (30mm) is longer than the
  gear face (10mm) so it protrudes on both sides.
- Assembly: place each shaft coaxial with its gear (same Z-axis line), gear centred
  along the shaft length.

### Pinion ↔ gear (MESHING — resolved here, not in part files)
- Pitch diameters 36mm and 60mm → **centre distance = (36+60)/2 = 48mm**.
- Both gears sit at the SAME axial position (coplanar faces).
- Resolver places the two gear axes 48mm apart on parallel Z-axes via `cq.Location`
  (e.g. pinion at X=0, gear at X=48, or symmetric ±24).
- **Phase offset for mesh**: rotate ONE gear by half a tooth pitch so teeth interlock
  at the pitch line without interpenetration. Half-tooth angle = 360°/(2·N):
  - gear (30T): 6°
  - pinion (18T): 10°
  Apply to exactly one member (either works). This is the key meshing move.

## Assembly Order
1. Establish shaft axes: pinion axis and gear axis parallel along Z, 48mm apart.
2. Place shaft on each axis.
3. Place pinion on its shaft (bore coaxial), centred axially.
4. Place gear on its shaft (bore coaxial), coplanar with pinion, phase-rotated half
   a tooth pitch to mesh.

## Notes for assembly_resolver
- No fasteners, no press fits — all bore↔shaft joints are nominal-⌀8 slip fits.
- Meshing correctness = correct 48mm centre distance + correct half-tooth phase
  offset on one gear. Verify teeth interlock without overlap in the assembly render.

## RESOLVED — composed by assembly_resolver (2026-07-21)

`assembly.py` written and executor-verified (Compound, volume 39,739 mm³,
bbox X[-19.99,79.89] Y[-32,32] Z[-15,15]). Direct `cq.Location` placement only
(constraint solver banned). No part modified — all 3 parts loaded via `load_part()`.

### Interfaces checked (against the coded part.py dimensions, ground truth)
- **pinion/gear ↔ shaft**: gear bores are ⌀8.2 (nominal ⌀8 + 0.2 print clearance,
  in both pinion & gear part.py); shaft OD ⌀8.0 → 0.2mm diametral slip-fit. MATCH.
- **pinion ↔ gear centre distance**: pinion pitch r=18 + gear pitch r=30 = 48mm.
  Placed 48mm apart on +X → pitch circles tangent at x=18. MATCH.
- **Coplanarity**: both gears centred on Z (faces Z=-5..+5); no Z offset applied → coplanar.
- **Shaft protrusion**: shaft ⌀8×30 centred (Z=-15..+15) through 10mm gears → protrudes
  ±10mm each side. As specced (fine).

### Mate relationships (each derived from part dimensions above)
| Instance | cq.Location | Derivation |
|----------|-------------|-----------|
| pinion | (0,0,0) | reference part, no transform |
| gear | translate (48,0,0), rotate −6° about Z | centre distance 48; half-tooth phase 360/(2·30) |
| shaft_pinion | (0,0,0) | coaxial with pinion bore (pinion centre = origin) |
| shaft_gear | (48,0,0) | coaxial with gear bore (gear centre) |

### Meshing verification (VISUAL + GEOMETRIC)
- **Visual**: top_clean + iso_clean renders show teeth interleaved, pitch circles
  tangent, shafts running coaxially through both bores.
- **Geometric (Z=0 section-interference test)**: phase 0° → 18.04 mm² tooth-on-tooth
  overlap (would interpenetrate); phase −6° → **0.00 mm² overlap (clean mesh)**.
  +6° equivalently clean by tooth symmetry; **−6° used**.

### Colour legend (from renderer)
pinion → red · gear → blue · shaft_pinion → green · shaft_gear → orange

### Conflicts
NONE. All interfaces matched in the code; no part.proposal.py written, no CONFLICT opened.
