# Constraints: piston_ring

## Functional Requirements
- Rectangular-section piston ring seating in a piston ring groove (one part, quantity 3 in assembly)
- v1: single geometry shared by both compression rings and the oil ring
- Must sit in a 2.6 mm axial x 3.0 mm radial-deep groove with side and back clearance

## Dimensions
- Overall: ⌀60.5 x 2.5 mm
- Free (uncompressed) outer diameter: 60.5 mm
- Radial thickness: 2.5 mm (free ID = 55.5 mm)
- Axial height: 2.5 mm (0.1 mm side clearance in 2.6 mm groove)
- Compressed check (informational, not modeled): at working OD 60.0, ring ID = 55.0 > groove root ⌀54.0 → 0.5 mm back clearance ✓

## Features
- Rectangular cross-section (2.5 mm radial x 2.5 mm axial), no taper, no chamfer
- End gap: 1.0 mm straight radial cut through the section (split ring). Model as a simple angular gap cut
- NO fillets (deferred project-wide)

## Interfaces
- Connects to piston via ring groove: ring 2.5 x 2.5 mm section ↔ groove 2.6 mm axial height x 3.0 mm radial depth
  (ring OD faces outward; in assembly, seat ring concentric with piston axis at each groove mid-height)

## Manufacturing
- Primary process: CNC_turning
- Material class: Steel 304
- Secondary processes: gap cut by wire EDM or slitting saw
- Thin section 2.5 mm > 1.5 mm metal minimum ✓

## Coordinate convention
- Revolved part: ring axis = Z, section centered at origin (Z = ±1.25)
