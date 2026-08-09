# Constraints: crankshaft

## Functional Requirements
- Single-throw crankshaft: convert the rod's reciprocating motion to rotation
- Two main journals on the main (rotation) axis; one offset crank pin carried between two webs
- Stroke 60.0 mm (crank pin offset / throw = 30.0 mm)

## Dimensions
- Overall: ⌀100 x 92 mm
  (axial stack along main axis: 25 journal + 10 web + 22 crank pin span + 10 web + 25 journal = 92 mm)
- Main journals: ⌀30.0 mm x 25.0 mm long, both coaxial on the main axis
- Webs / counterweight plates: 2x ⌀100.0 mm discs x 10.0 mm thick, centered on the main axis
  (v1: full discs — radius 50 covers crank pin outer extremity at 30 + 19 = 49 mm; counterweight cutouts deferred)
- Crank pin: ⌀38.0 mm x 22.0 mm long, axis parallel to main axis, offset 30.0 mm

## Features
- One-piece part: journal – web – crank pin – web – journal, all unioned
- Crank pin free length between web inner faces: 22.0 mm (accepts 20.0 mm rod big end with 1.0 mm clearance per side)
- NO fillets at journal/web junctions (deferred project-wide). NO threads, NO oil holes for v1.

## Interfaces
- Connects to connecting_rod via crank pin: pin ⌀38.0 ↔ big end bore ⌀38.0 (38.05) clearance, rotating
- Crank pin length 22.0 mm ↔ big end width 20.0 mm
- Throw 30.0 mm + rod center distance 95.0 mm → TDC gudgeon-pin axis at 125.0 mm from main axis
- Main journals ⌀30.0 x 25.0 are the external mounting interface (no bearing block in this project; journals left free)

## Manufacturing
- Primary process: CNC_turning
- Material class: Steel 304
- Secondary processes: CNC_milling for the offset crank pin (offset-turned or milled between centers); web OD turned
- Feasibility: overall L/D = 92/100 < 1 ✓; journal stickout 25/30 < 1 ✓; no thin walls (solid part)

## Coordinate convention
- Revolved-dominant part: MAIN axis = Z, centered at origin (Z = ±46.0)
- Crank pin axis parallel to Z through (30, 0, 0) — i.e., throw along +X; pin spans Z = ±11.0
