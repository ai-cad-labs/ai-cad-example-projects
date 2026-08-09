# Constraints: hinge_block

## Functional Requirements
- ONE parametric part, placed TWICE in the assembly (identical geometry at X=−50 and X=+50). Reused, not duplicated.
- Bridge the base rear face and the lid rear flank, providing a horizontal pin bore (rotation axis) so the lid can pivot open.
- Lower flange fastens to the base; upper flange fastens to the lid.

## Dimensions
- Overall: 30 x 25 x 30 mm   ← local bbox (X=width along hinge axis, Y=stand-off depth, Z=height)
- Pin bore: ⌀4.0 mm through-hole along X at block mid-height (assembled Z=80).
- Coordinate convention: prismatic — centered on XY, bottom at Z=0.

## Features
- Pin bore ⌀4.0 mm through the full 30 mm width along X (hinge rotation axis). NO fillets.
- Lower flange (base side): 2 mount through-holes ⌀3.2 mm (M3 clearance), X-spacing 16 mm, positioned to align with base rear pilot holes (assembled Z=72). NO fillets.
- Upper flange (lid side): 2 mount through-holes ⌀3.2 mm (M3 clearance), X-spacing 16 mm, positioned to align with lid rear pilot holes (assembled Z=88). NO fillets.

## Interfaces
- Connects to base via lower-flange ⌀3.2 holes over base rear pilot holes (⌀2.5), M3 self-tapping.
- Connects to lid via upper-flange ⌀3.2 holes over lid rear pilot holes (⌀2.5), M3 self-tapping.
- Pin bore ⌀4.0 receives a ⌀4 printed dowel (produced with this part's STL) forming the hinge axle at assembled Z=80.

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA (or PETG)
- Secondary processes: none
- Note: the ⌀4 hinge pin is a printed dowel (not a bought fastener); print it alongside the block.
