# Constraints: connecting_rod

## Functional Requirements
- Link the gudgeon pin (small end) to the crank pin (big end) at a fixed center distance
- One-piece big end for v1 (NO bolted cap, no split line, no bolts)
- I-beam shank between the two eyes
- Small end includes a bronze-bushing land (v1 geometry: plain ⌀16 bore; bushing is a Buy item, not modeled)

## Dimensions
- Overall: 134 x 52 x 20 mm
  (length = big-end boss radius 26 + center distance 95 + small-end boss radius 13)
- Center distance (small end bore axis to big end bore axis): 95.0 mm
- Small end: bore ⌀16.0 mm (clearance 16.02 for full-floating pin); boss OD 26.0 mm; width 20.0 mm
- Big end: bore ⌀38.0 mm (clearance 38.05 on crank pin); boss OD 52.0 mm; width 20.0 mm
- Shank (I-beam): overall section 16.0 mm wide x 20.0 mm deep; flange thickness 4.0 mm,
  web thickness 5.0 mm (pocket each side: 5.5 mm wide x 12 mm — depth/width = 5.5/12 ≈ 0.5 ≤ 4 ✓)

## Features
- Two coaxial-bored eyes (bores parallel, both perpendicular to rod long axis)
- I-beam shank formed by milling a pocket into each side of a rectangular blank
- Uniform width 20.0 mm across both eyes (single thickness plate blank)
- NO fillets (deferred project-wide). NO threads, NO bolt holes (one-piece big end).

## Interfaces
- Connects to gudgeon_pin via small end bore: ⌀16.0 (16.02) clearance ↔ pin ⌀16.0 (15.99), full-floating
- Connects to piston (indirectly): small end width 20.0 mm ↔ piston boss inner face spacing 22.0 mm (1.0 mm clearance per side)
- Connects to crankshaft via big end bore: ⌀38.0 (38.05) clearance ↔ crank pin ⌀38.0
- Big end width 20.0 mm ↔ crank pin axial length 22.0 mm between webs (1.0 mm clearance per side)
- Center distance 95.0 mm + crank throw 30.0 mm sets TDC pin-axis position at 125.0 mm from crank main axis

## Manufacturing
- Primary process: CNC_milling
- Material class: Steel 304
- Secondary processes: bores finish-bored/reamed for fit; bronze bushing (Buy) pressed into small end in a later revision
- Minimum wall: small end 5.0 mm, big end 7.0 mm, I-beam web 5.0 mm — all ≥ 1.5 mm metal minimum ✓

## Coordinate convention
- Part with a primary bore: BIG END bore axis = Z through origin; rod long axis along +X
  (small end bore axis = Z-parallel line through (95, 0, 0)); width centered Z = ±10.0
