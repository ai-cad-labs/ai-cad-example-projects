# Design Plan — Treasure Chest (treasure_chest)

## Overview
A small decorative treasure chest for 3D printing: a hollow rectangular base box
(open top) with a curved half-cylinder lid, joined at the rear by two identical
hinge blocks and latched at the front by a single hasp/latch plate. Every part is
custom (Make); there are no bought components. All interface dimensions are fixed
in this plan up front, so all four Make part types can be designed fully in
parallel and still mate on first assembly.

## Global Assembly Coordinate Frame (base = reference)
The assembled chest uses the base part's frame as the assembly reference:
- **X** = length (180 mm), X ∈ [-90, +90]
- **Y** = width/depth (120 mm), Y ∈ [-60, +60]. **Front = −Y** (hasp side). **Rear = +Y** (hinge side).
- **Z** = height. Base bottom at **Z = 0**, base top rim at **Z = 80**.
- Lid half-cylinder axis runs along X at Y = 0, seated at **Z = 80**; outer radius 60 → peak at Z = 140.

Each part is DESIGNED in its own local frame (prismatic parts centered on XY,
bottom at Z = 0 — COOKBOOK Principle 0). The assembly_resolver applies the
placement offsets/rotations below. Interface features are located by the
assembled-frame coordinates given here so both sides of every joint are modeled
independently yet align.

## Parts
### 1. base
- **Type**: Custom (make)
- **Description**: Hollow rectangular box, 3 mm walls, solid 3 mm floor, open top. Holds the contents; carries hinge and hasp pilot holes on its rear and front faces.
- **Key dimensions**: 180 × 120 × 80 mm outer; 3 mm walls; interior cavity 174 × 114 × 77 mm; open top.
- **Interfaces**: Top rim (Z=80) seats the lid flat face. Rear face (Y=+60) carries 2 hinge pilot-hole clusters at X=±50. Front face (Y=−60) carries 2 hasp pilot holes at X=±14.
- **parallel_safe**: true — all mating features are at fixed coordinates defined in this plan; no dependency on any other part's design outcome.

### 2. lid
- **Type**: Custom (make)
- **Description**: Half-cylinder shell (upper half of a cylinder), flat face down, hollow ~3 mm wall. Spans the full 180 mm length; footprint matches the base.
- **Key dimensions**: Outer radius 60 mm (⌀120 = base width), length 180 mm, ~3 mm shell (inner radius 57 mm). Local bbox 180 × 120 × 60 mm.
- **Interfaces**: Flat bottom edges (the two long lower rims at Y=±60 in-assembly) rest on the base top rim at Z=80. Rear flank (Y=+60) carries 2 hinge pilot-hole clusters at X=±50. Front lower edge (Y=−60) carries 1 latch through-hole (⌀6) at X=0.
- **parallel_safe**: true — footprint and all interface features are fixed dimensionally in this plan.

### 3. hinge_block
- **Type**: Custom (make) — **ONE parametric part, placed TWICE** (identical geometry at X=−50 and X=+50). Reused, not duplicated.
- **Description**: Compact hinge bracket bridging the base rear face and the lid rear flank, with a horizontal pin bore (⌀4) along X forming the rotation axis. Lower flange bolts to the base, upper flange bolts to the lid.
- **Key dimensions**: 30 × 25 × 30 mm. Pin bore ⌀4 mm through X at block mid-height. Four mount through-holes ⌀3.2 mm (2 lower/base, 2 upper/lid).
- **Interfaces**: Pin bore axis at assembled Z=80. Lower flange holes align to base rear pilot holes; upper flange holes align to lid rear pilot holes (pattern below).
- **parallel_safe**: true — self-contained bracket; hole pattern fixed in this plan.

### 4. hasp_plate
- **Type**: Custom (make)
- **Description**: Flat front latch plate, centered on the front face, straddling the lid–base seam. Bolts to the base below the seam; its top overlaps the lid front edge with a ⌀6 latch hole that lines up with the lid's ⌀6 through-hole so a pin/padlock secures the closed lid.
- **Key dimensions**: 40 × 4 × 50 mm (X × Y-thickness × Z). Latch hole ⌀6 mm near top; 2 mount through-holes ⌀3.2 mm in lower half at X=±14.
- **Interfaces**: Mount holes align to base front pilot holes; latch hole aligns to lid front latch hole in the closed position.
- **parallel_safe**: true — mounts to fixed base/lid features defined in this plan.

## Interfaces (concrete dimensions — the mating contract)
- **Lid ↔ Base (seat)**: Lid flat bottom face rests on base top rim at **Z=80**. Both footprints are **180 × 120 mm** (lid outer ⌀120 = base outer width) — purely dimensional match, no fasteners at the seat.
- **Hinge ↔ Base**: For each block center (X=−50, X=+50), base rear face (Y=+60) has **2 pilot holes ⌀2.5 mm × 2 mm deep** at **Z=72**, X-spacing **16 mm** (i.e. X ∈ {−58,−42} and {42,58}). Hinge lower flange has matching **⌀3.2 mm** clearance holes (M3 self-tapping screw into printed wall).
- **Hinge ↔ Lid**: At each block center, lid rear flank (Y=+60) has **2 pilot holes ⌀2.5 mm × 2 mm deep** at assembled **Z=88**, X-spacing **16 mm** (X ∈ {−58,−42} and {42,58}). Hinge upper flange has matching **⌀3.2 mm** clearance holes.
- **Hinge pin**: **⌀4.0 mm** bore along X at assembled Z=80 (a ⌀4 printed rod / pin is the rotation axle; not itself a separately-listed part — treated as a printed dowel produced with the hinge_block STL).
- **Hasp ↔ Base**: Base front face (Y=−60) has **2 pilot holes ⌀2.5 mm × 2 mm deep** at **Z=62**, **X=±14**. Hasp plate has matching **⌀3.2 mm** clearance holes (M3 self-tapping).
- **Hasp ↔ Lid (latch)**: Hasp top **⌀6.0 mm** latch hole (assembled Z≈95, X=0) aligns with the lid front-lower-edge **⌀6.0 mm** through-hole (assembled Y=−60, Z≈86, X=0) when the lid is closed, so a pin/padlock shackle passes through both.

## Assembly Order
1. base (assembly reference — placed first)
2. lid (seated on base top rim, Z-offset +80)
3. hinge_block ×2 (placed at X=−50 and X=+50 on the rear, bridging base+lid)
4. hasp_plate (front, centered X=0, spanning the seam)

## Make vs Buy
- **Buy**: NONE. This chest is 3D-printed end to end.
- **Make**: ALL parts — base, lid, hinge_block (×2), hasp_plate. The ⌀4 hinge pin is a printed dowel produced with the hinge_block, not a bought fastener. Mounting screws are self-tapping into printed walls (no modeled fastener parts).

## Parallel Safety Summary
All interface dimensions are fixed in this plan, so **every part is `parallel_safe: true`**:
- base → true
- lid → true
- hinge_block → true
- hasp_plate → true
