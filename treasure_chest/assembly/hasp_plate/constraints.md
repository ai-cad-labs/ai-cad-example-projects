# Constraints: hasp_plate

## Functional Requirements
- Flat front latch plate, centered on the front face, straddling the lid–base seam.
- Bolt to the base below the seam; overlap the lid front edge above the seam.
- Provide a latch hole that aligns with the lid's latch hole so a pin/padlock secures the closed lid.

## Dimensions
- Overall: 40 x 4 x 50 mm   ← local bbox (X=width, Y=plate thickness, Z=height)
- Plate thickness: 4 mm
- Coordinate convention: prismatic — centered on XY, bottom at Z=0. Assembled on the front face (Y=−60), centered X=0, spanning the seam at Z=80.

## Features
- Flat plate 40 (X) × 4 (Y) × 50 (Z) mm. NO fillets.
- Latch hole: 1 through-hole ⌀6.0 mm near the top, centered X=0 (assembled Z≈95). NO fillets.
- Mount holes: 2 through-holes ⌀3.2 mm (M3 clearance) in the lower half at X=±14 (assembled Z=62). NO fillets.

## Interfaces
- Connects to base via the 2 ⌀3.2 mount holes over base front pilot holes (⌀2.5) at X=±14, Z=62, M3 self-tapping.
- Connects to lid via the ⌀6 latch hole aligning with the lid front ⌀6 latch hole in the closed position (pin/padlock shackle passes through both).

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA (or PETG)
- Secondary processes: none
- Minimum wall/plate thickness: 4 mm (above 0.8 mm plastic minimum).
