# Constraints: shaft

## Functional Requirements
- Plain cylindrical shaft supporting one gear via its ⌀8mm bore.
- ONE part, instantiated twice in the assembly (one shaft per gear).

## Dimensions
- Overall: ⌀8 x 30 mm   ← revolved part (⌀D × L)
- Diameter: ⌀8 mm
- Length: 30 mm
- L/D ratio: 30/8 = 3.75:1 — well under the 8:1 unsupported turning limit; trivially
  fine for 3D printing.

## Features
- Plain solid cylinder — no holes, no features, NO fillets (deferred project-wide).

## Interfaces
- Connects to `pinion` and `gear` via ⌀8mm OD slip-fit into their ⌀8mm bores
  (nominal ⌀8 on both sides; any clearance handled on the gear bore side).

## Manufacturing
- Primary process: 3D_printing
- Material class: PLA / PETG (3D-print thermoplastic)
- Secondary processes: none

## Coordinate Convention
- Revolved part: axis of revolution = Z-axis; centre = origin (COOKBOOK Principle 0).

## Hard Rules
- NO FILLETS (deferred per project policy).
