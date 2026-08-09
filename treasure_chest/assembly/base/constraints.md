# Constraints: base

## Functional Requirements
- Hollow rectangular box with a solid floor and an OPEN top to receive the lid.
- Provide a flat top rim (Z=80) for the lid to seat on.
- Carry hinge mounting pilot holes on the rear face and hasp mounting pilot holes on the front face.

## Dimensions
- Overall: 180 x 120 x 80 mm   ← outer bounding box (X=length, Y=depth, Z=height)
- Wall thickness: 3 mm (all four side walls)
- Floor thickness: 3 mm
- Interior cavity: 174 x 114 x 77 mm (open top; cavity from Z=3 to Z=80)
- Coordinate convention: prismatic — centered on XY, bottom at Z=0. Front = −Y, rear = +Y.

## Features
- Open top (no top wall).
- Hinge pilot holes (rear face, Y=+60): 2 clusters at X=−50 and X=+50; each cluster = 2 holes ⌀2.5 mm × 2 mm deep at Z=72, X-spacing 16 mm (X ∈ {−58,−42} and {42,58}). NO fillets.
- Hasp pilot holes (front face, Y=−60): 2 holes ⌀2.5 mm × 2 mm deep at Z=62, X=±14. NO fillets.
- (Blind pilot holes 2 mm deep leave ~1 mm skin in the 3 mm wall — acceptable for self-tapping screws in printed plastic.)

## Interfaces
- Connects to lid via the top rim seat at Z=80 (footprint 180 × 120 mm matches lid outer ⌀120 width).
- Connects to hinge_block (×2) via rear pilot holes (⌀2.5) receiving the block's ⌀3.2 clearance holes with M3 self-tapping screws.
- Connects to hasp_plate via front pilot holes (⌀2.5) at X=±14, Z=62.

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA (or PETG)
- Secondary processes: none (self-tapping screws thread directly into printed walls)
- Minimum wall thickness: 3 mm (well above 0.8 mm plastic minimum).
