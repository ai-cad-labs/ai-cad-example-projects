# Design Plan

## Overview
A meshing involute spur gear pair mounted on two parallel shafts. A small pinion
(18 teeth) drives a larger gear (30 teeth), both module 2mm / 20° pressure angle
/ 10mm face width, each with a ⌀8mm central bore. Both ride on identical plain
⌀8mm × 30mm shafts. The pair meshes at a centre distance of 48mm. Everything is
3D-printed, so every part is Make — there are no purchased/standard parts.

The gears are geometrically independent: each is modelled centred on its own
Z-axis at the origin. Meshing (centre distance + half-tooth-pitch phase offset)
is resolved entirely at ASSEMBLY time, not baked into the part files.

## Parts
### 1. pinion
- **Type**: Custom (make)
- **Description**: Involute spur gear, the smaller/driving member of the pair.
- **Key dimensions**: Module 2mm, 18 teeth, 20° PA, pitch ⌀36mm, outside ⌀40mm,
  root ⌀31mm, base ⌀33.83mm, 10mm face width, ⌀8mm through bore. Overall ~⌀40×10mm.
- **Interfaces**: ⌀8mm bore is a slip fit over a shaft (⌀8mm nominal). Meshes with
  `gear` at 48mm centre distance (assembly-time constraint).
- **parallel_safe**: true — all dimensions are fixed by standard involute formulas
  from module/teeth/PA; bore is a fixed ⌀8; no dependency on any other part's
  computed geometry.

### 2. gear
- **Type**: Custom (make)
- **Description**: Involute spur gear, the larger/driven member of the pair.
- **Key dimensions**: Module 2mm, 30 teeth, 20° PA, pitch ⌀60mm, outside ⌀64mm,
  root ⌀55mm, base ⌀56.38mm, 10mm face width, ⌀8mm through bore. Overall ~⌀64×10mm.
- **Interfaces**: ⌀8mm bore is a slip fit over a shaft (⌀8mm nominal). Meshes with
  `pinion` at 48mm centre distance (assembly-time constraint).
- **parallel_safe**: true — all dimensions are fixed by standard involute formulas;
  bore is a fixed ⌀8; no dependency on any other part's computed geometry.

### 3. shaft
- **Type**: Custom (make)
- **Description**: Plain cylindrical shaft. ONE part, instantiated twice in the
  assembly (one shaft per gear).
- **Key dimensions**: ⌀8mm × 30mm long. Overall ⌀8×30mm.
- **Interfaces**: ⌀8mm OD is a slip fit into a gear bore (⌀8mm nominal).
- **parallel_safe**: true — fixed ⌀8mm × 30mm cylinder, independent of everything.

## Interfaces
- **pinion ↔ shaft**: pinion ⌀8mm bore slip-fits over shaft ⌀8mm OD (nominal ⌀8
  both; ~0.2mm print clearance may be added on the bore by the designer if desired).
- **gear ↔ shaft**: gear ⌀8mm bore slip-fits over shaft ⌀8mm OD (same nominal ⌀8).
- **pinion ↔ gear (MESHING — ASSEMBLY-TIME ONLY)**: pitch diameters 36mm and 60mm
  → centre distance = (36+60)/2 = **48mm**. This is NOT a part-file constraint —
  both gears are modelled centred on their own Z-axis at the origin (COOKBOOK
  Principle 0). The assembly_resolver places them 48mm apart via `cq.Location` and
  rotates ONE gear by half a tooth pitch so the teeth interlock at the pitch line
  without interpenetration. Half-tooth-pitch angular offset on the gear = 360°/(2·N)
  = 360°/(2·30) = 6° (equivalently 10° on the pinion, 360°/(2·18)); rotating either
  member by its own half-tooth angle achieves interlock — resolver applies to one.

## Assembly Order
1. shaft (base reference cylinder)
2. pinion (bore over one shaft)
3. gear (bore over the other shaft)
4. Place pinion + gear at 48mm centre distance, coplanar (same axial Z position),
   with one gear phase-rotated half a tooth pitch to mesh.

## Make vs Buy
- **Buy**: NONE. Every part is 3D-printed in-house, including the shafts. There are
  no bearings, fasteners, or standard components. No sourcing agent / bom.md needed.
- **Make**: pinion, gear, shaft (all three).

## Assembly Structure
FLAT — no sub-assemblies. The assembly is 3 part instances of 2 distinct gear parts
plus 2 instances of the single shaft part: pinion + gear + shaft×2. Only 3 Make
parts total, no natural functional sub-grouping → flat structure per decision rules.
