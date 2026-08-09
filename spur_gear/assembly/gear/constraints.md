# Constraints: gear

## Functional Requirements
- Involute spur gear (driven/larger member) that meshes cleanly with `pinion`.
- Transmit rotation via a slip-fit ⌀8mm bore over the shaft.

## Dimensions
- Overall: ⌀64 x 10 mm   ← revolved/rotational part (outside diameter × face width)
- Module (m): 2 mm
- Number of teeth (z): 30
- Pressure angle: 20°
- Pitch diameter: 60 mm (= m·z = 2·30)
- Base circle diameter: 56.38 mm (= pitch_dia·cos20° = 60·0.9397)
- Root (dedendum) diameter: 55 mm (= pitch_dia − 2·1.25·m = 60 − 5)
- Outside (addendum) diameter: 64 mm (= pitch_dia + 2·m = 60 + 4)
- Face width: 10 mm
- Central bore: ⌀8 mm, through (full 10mm face width)

## Features
- 30 involute teeth around the pitch circle — NO fillets (deferred project-wide).
- ⌀8mm central through-bore on the Z-axis.
- Wall between bore and root circle = (55 − 8)/2 = 23.5mm — ample for 3D printing.

## Interfaces
- Connects to `shaft` via ⌀8mm bore slip-fit over ⌀8mm OD (nominal ⌀8; designer may
  add ~0.2mm print clearance on the bore for a functional slip fit).
- Meshes with `pinion` at 48mm centre distance — this is an ASSEMBLY-TIME constraint
  (resolved by assembly_resolver via cq.Location + half-tooth phase rotation), NOT a
  part-file dimension. Model this part centred on its own Z-axis at the origin. The
  half-tooth phase offset for this 30-tooth gear = 360°/(2·30) = 6°.

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA / PETG (3D-print thermoplastic)
- Secondary processes: none
- Minimum wall thickness (plastic): ≥ 0.8mm — satisfied everywhere.

## Coordinate Convention
- Revolved part: axis of revolution = Z-axis; centre = origin; bore axis = Z through
  origin (COOKBOOK Principle 0).

## Hard Rules
- NO FILLETS (deferred per project policy).

## DOMAIN NOTE — building involute teeth
- CadQuery has NO `.gear()` and NO `.involute()` method — THEY DO NOT EXIST. Do not
  hallucinate them.
- Involute tooth profiles MUST be built from point math (involute parametric
  equations) via `parametricCurve` / `polyline` + `close` + `extrude`, arrayed around
  the gear with `polarArray`.
- Before writing code: READ `reference/cadquery-contrib/examples/cylindrical_gear.py`
  (the golden involute-gear example) and INVOKE the `cadquery-cookbook` skill.
