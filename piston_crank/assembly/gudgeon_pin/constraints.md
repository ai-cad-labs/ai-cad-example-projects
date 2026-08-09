# Constraints: gudgeon_pin

## Functional Requirements
- Full-floating wrist pin joining the piston bosses and the connecting rod small end
- Hollow to reduce reciprocating mass
- Free rotating (clearance) fit in BOTH the piston boss bores and the rod small end bore

## Dimensions
- Overall: ⌀16 x 50 mm
- Outer diameter: 16.0 mm nominal (pin side of clearance fit: 15.99 mm — clearance direction, NOT interference)
- Length: 50.0 mm (spans piston boss outer span of 48.0 mm with 1.0 mm protrusion per side;
  half-length 25.0 mm < piston skirt inner radius 27.0 mm → pin stays fully inside the piston)
- Inner (bore) diameter: 9.0 mm, through

## Features
- Plain hollow cylinder: through ⌀9.0 mm bore, flat square ends
- NO circlip grooves for v1 (retention deferred; pin cannot escape past the ⌀54 skirt inner wall in this model)
- NO fillets (deferred project-wide). NO threads.

## Interfaces
- Connects to piston via boss bores: pin ⌀16.0 (15.99) ↔ boss bore ⌀16.0 (16.02) clearance, full-floating
- Connects to connecting_rod via small end bore: pin ⌀16.0 (15.99) ↔ small end bore ⌀16.0 (16.02) clearance, full-floating
- Length 50.0 mm ↔ piston boss outer span 48.0 mm (must clear rod small end width 20.0 mm centered between bosses)

## Manufacturing
- Primary process: CNC_turning
- Material class: Steel 304
- Secondary processes: OD ground for fit (represented as turned for v1); gun-drill/drill ⌀9 through
- Feasibility: L/D = 50/16 = 3.1 ≤ 8 ✓; bore depth/dia = 50/9 = 5.6 ≤ 10 ✓; wall = 3.5 mm ≥ 1.5 mm ✓

## Coordinate convention
- Revolved part: pin axis = Z, centered at origin (Z = ±25.0)
