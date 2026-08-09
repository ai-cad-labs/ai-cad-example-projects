# Constraints: lid

## Functional Requirements
- Curved half-cylinder shell (upper half of a cylinder) forming the chest lid.
- Flat bottom face seats on the base top rim; footprint matches the base.
- Hollow shell (~3 mm) to keep the print light and match the box wall thickness.
- Carry hinge pilot holes on the rear flank and one latch through-hole on the front lower edge.

## Dimensions
- Overall: 180 x 120 x 60 mm   ← local bbox (X=length along cylinder axis, Y=⌀120 width, Z=radius height)
- Outer radius: 60 mm (⌀120 = base outer width)
- Inner radius: 57 mm (3 mm shell wall)
- Length: 180 mm (matches base length)
- Coordinate convention: designed flat-face-down in local frame, centered on XY, flat face at Z=0, arching to Z=60. Cylinder axis along X. Assembled with Z-offset +80.

## Features
- Half-cylinder shell, open along the flat bottom (mates onto the open base top). NO fillets.
- Hinge pilot holes (rear flank, assembled Y=+60): 2 clusters at X=−50 and X=+50; each = 2 holes ⌀2.5 mm × 2 mm deep at assembled Z=88, X-spacing 16 mm (X ∈ {−58,−42} and {42,58}). NO fillets.
- Latch through-hole (front lower edge, assembled Y=−60): 1 hole ⌀6.0 mm at X=0, assembled Z≈86 (through the shell wall). NO fillets.

## Interfaces
- Connects to base via the flat bottom face resting on the base top rim at Z=80 (footprint 180 × 120 mm match).
- Connects to hinge_block (×2) via rear pilot holes (⌀2.5) receiving the block's upper-flange ⌀3.2 clearance holes.
- Connects to hasp_plate via the ⌀6 front latch hole, which aligns with the hasp's ⌀6 latch hole when the lid is closed.

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA (or PETG)
- Secondary processes: none
- Minimum wall thickness: 3 mm shell (above 0.8 mm plastic minimum). Print orientation: flat face down on the bed (self-supporting arch).
