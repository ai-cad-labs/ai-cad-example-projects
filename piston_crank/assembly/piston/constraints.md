# Constraints: piston

## Functional Requirements
- Reciprocating piston for a single-cylinder engine core (no cylinder bore modeled)
- Carry 3 piston rings in rectangular grooves near the crown
- Transmit gas load to the connecting rod through a full-floating gudgeon pin in two pin bosses
- Flat crown (no dome, no valve pockets)

## Dimensions
- Overall: ⌀60 x 55 mm
- Skirt OD: 60.0 mm (constant, no barrel/ovality for v1)
- Overall height: 55.0 mm (crown top to skirt bottom)
- Crown thickness: 8.0 mm (solid, flat top)
- Skirt wall thickness: 3.0 mm (interior hollowed below crown; skirt inner ⌀54.0 mm)
- Compression height (crown top to gudgeon-pin axis): 32.0 mm
  (pin axis therefore 23.0 mm above skirt bottom)

## Features
- THREE rectangular ring grooves, turned into the OD near the crown (2 compression + 1 oil; identical geometry for v1):
  - Groove axial height: 2.6 mm (accepts 2.5 mm ring with 0.1 mm side clearance)
  - Groove radial depth: 3.0 mm (groove root ⌀54.0 mm; 0.5 mm back clearance behind 2.5 mm ring)
  - Top land: 5.0 mm (crown top to top edge of groove 1)
  - Inter-groove lands: 3.0 mm (grooves at 5.0–7.6, 10.6–13.2, 16.2–18.8 mm below crown top)
- TWO pin bosses inside the skirt, coaxial, on the gudgeon-pin axis (perpendicular to piston axis, through piston centerline):
  - Through bore: ⌀16.0 mm (clearance for full-floating pin; bore 16.02 mm, i.e., clearance direction, NOT interference)
  - Boss inner faces spacing: 22.0 mm (accepts 20.0 mm rod small end with 1.0 mm clearance per side)
  - Boss outer faces span: 48.0 mm (each boss 13.0 mm long; boss OD ~26 mm blending into skirt)
  - Pin bore does NOT break through skirt OD (bore ends inside skirt inner wall; 50 mm pin sits fully inside ⌀54 inner skirt)
- NO fillets (deferred project-wide). NO threads.

## Interfaces
- Connects to gudgeon_pin via boss through-bore: bore ⌀16.0 mm clearance (16.02), pin ⌀16.0 (15.99) — full-floating
- Connects to connecting_rod small end (indirectly): boss inner face spacing 22.0 mm ↔ small end width 20.0 mm
- Connects to piston_ring via ring grooves: groove 2.6 mm axial x 3.0 mm radial ↔ ring section 2.5 x 2.5 mm

## Manufacturing
- Primary process: CNC_milling
- Material class: Aluminum 6061
- Secondary processes: ring grooves may be finish-turned (grooving insert); pin bore line-bored in one setup for coaxiality
- 3 mm minimum wall thickness everywhere (skirt, boss webs)

## Coordinate convention
- Revolved-dominant part: piston axis = Z, centered at origin (crown at Z=+27.5, skirt bottom at Z=-27.5)
- Gudgeon-pin bore axis along X through (0, 0, -4.5) (i.e., 32.0 mm below crown top)
