# Assembly: conveyor_shaft_unit

Flat structure — three Make parts, no sub-assemblies.

## Coordinate convention (binding on every part)

- **Shaft axis = global Z.** Up = **+Y**. Across = **X**. **Drive end = +Z.**
- Origin (0,0,0) on the shaft axis, midway between the two bearing centres.
- Bearing centres at **z = +75** (drive, located) and **z = -75** (far, floating). Span **150**.
- Foot underside at **Y = -75** (centre height 75).
- **Every Make part is modelled directly in this global frame.** The assembly applies
  **identity transforms only** — no rotations, no offsets. Do not introduce any.

## Placement table

| Item | Make/Buy | Axial extent (Z) | Transform |
|---|---|---|---|
| shaft | Make | -135 … +165 | identity |
| housing | Make | -95 … +95 (foot to Y = -75) | identity |
| cover | Make | +90 … +107 | identity |
| 6208 far-end | Buy | -84 … -66 | identity |
| 6208 drive-end | Buy | +66 … +84 | identity |
| DIN 471 - 40 circlip | Buy | +84.0 … +85.75 | identity |
| lip seal 40x62x10 | Buy | +90 … +100 | identity |
| 4 x M8 x 30 cap screw | Buy | head at +107, into housing to +79 | BC 104, 45/135/225/315 deg |
| 4 x M12 foot bolt | Buy | through Y = -75 … -60 | X = +/-45, Z = +/-75 |
| 2 x M8x1 grease nipple | Buy | X = 0, Y = +58 up | Z = +75 and Z = -75 |

## Interface definitions

| # | Interface | Value | Between |
|---|---|---|---|
| I1 | Bearing seat dia | **40.000** (shaft k6) | shaft <-> 6208 bore (x2) |
| I2 | Housing bore dia | **80.000** (bore H7) | housing <-> 6208 OD (x2) |
| I3 | Bearing span | **150.000** | shaft seats <-> housing bores |
| I4 | DE bearing inboard face plane | **z = +66.0** | shaft dia-48 collar face <-> housing DE bore step face |
| I5 | DE bearing outboard face plane | **z = +84.0** | shaft circlip face — **zero float** (84.0 - 66.0 = 18.0 = 6208 width) |
| I6 | FE axial float | **1.5 mm** | FE outer ring face z = -66.0 <-> housing step z = -64.5 |
| I7 | Cover spigot pilot | **80.000** (cover h8 in housing H7) | cover <-> housing DE bore |
| I8 | Bolt circle | **104.000**, 45/135/225/315 deg | cover 4 x ⌀9 <-> housing 4 x M8 |
| I9 | Flange OD = boss OD | **124.000** | cover <-> housing DE boss |
| I10 | Cover mating plane | **z = +95.0** | cover flange back face <-> housing boss face |
| I11 | Seal pocket | **⌀62.0 x 10 deep** | cover <-> lip seal OD |
| I12 | Seal journal | **⌀40.0** at z = +90 … +100 | shaft <-> lip seal ID |
| I13 | Circlip groove | **⌀37.5 x 1.85** at z = +84.0 | shaft <-> DIN 471 - 40 |
| I14 | Foot clearance holes | **⌀14.0** at (X = +/-45, Z = +/-75) | housing <-> 4 x M12 |
| I15 | Grease thread | **M8 x 1** | housing bosses <-> 2 x nipple |

## Non-interference checks the assembly must prove

1. Cover spigot front face (z = +90.0) vs DE bearing outer face (z = +84.0): **6.0 mm gap**.
2. Circlip OD ~43.5 at z = +84.0 … +85.85 sits inside the ⌀80 housing bore: **18 mm radial clear**;
   4.15 mm inboard of the cover spigot face: **no contact**.
3. Cover ⌀42 through-bore vs ⌀40 shaft: **1.0 mm radial clearance**.
4. FE outer ring free both ways: 1.5 mm to the step at z = -64.5, 11 mm to the open mouth at z = -95.
5. Housing dia-72 central passage vs shaft dia 45 mid-body: **13.5 mm radial clearance**.
6. M8 bolt heads at z = +107, r = 52: **15 mm swing radius clear** — nothing on any part
   rises above z = +107.
7. Foot bolt holes (Z = +/-75) do not break into the pedestal or the bores:
   holes are at Y = -75 … -60, bores start at Y = -40.

## Assembly order

shaft -> press both 6208s -> fit circlip -> insert stack into housing from +Z ->
press seal into cover -> bolt cover with 4 x M8 -> fit 2 grease nipples -> bolt down with 4 x M12.
