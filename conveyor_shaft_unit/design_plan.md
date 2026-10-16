# Design Plan — conveyor_shaft_unit

## Overview

A two-bearing pillow-block style support unit for a 40 mm steel conveyor drive shaft
running at 1,500 rpm under ~4 kN radial / ~1 kN axial load, 20,000 h service interval.

Everything is sized outward from two catalogue anchors and nothing else:
the **6208 deep groove ball bearing envelope (bore 40 / OD 80 / width 18)**
and the **40 mm shaft diameter**.
The shaft seats, housing bores, cover and all spacing are derived from those two numbers;
no catalogue part is ever resized to suit a made part.

Three Make parts, strictly serial:
**shaft -> housing -> cover**.
The shaft fixes the axial station of every bearing face;
the housing is built around those stations;
the cover is built around the housing drive-end face.
No sub-assemblies: three parts with one shared axis is a flat structure.

## Coordinate convention

**THE RULING — all three parts and the assembly use this, without exception:**

- **The shaft axis is the global Z axis.** Every bore, seat, bearing and the seal are
  concentric about Z.
- **Up is +Y.** The mounting foot is at the bottom (-Y); the grease nipples point up (+Y).
- **Across is X.** The foot bolt pattern straddles X.
- **The DRIVE END is +Z.** The drive pulley extension, the circlip, the lip seal and the
  bolted cover are all at +Z. The FAR (floating) END is -Z.
- **Global origin (0,0,0) sits on the shaft axis, exactly midway between the two bearing
  centres.** Bearing centres are therefore at z = +75 (drive end) and z = -75 (far end).
- **Foot underside is the plane Y = -75** (centre height 75 mm).

Per-part modelling origins follow the house convention and resolve to the global frame by a
pure Z translation (no rotation, no X/Y offset):

| Part | Modelled about | Assembly placement |
|---|---|---|
| shaft | Z axis, z = -135 … +165 | identity (already in global frame) |
| housing | Z axis, z = -95 … +95, foot at -Y | identity |
| cover | Z axis, z = +90 … +107 | identity |

Because every part is modelled directly in the global frame, the assembly resolver needs
**zero** transforms. Keep it that way.

## Part decomposition

| # | Part | Make/Buy | Primary process | Material | parallel_safe | Reason |
|---|---|---|---|---|---|---|
| 1 | shaft | Make | CNC_turning | Steel C45 / EN8, through-hardened seats | **false** | Fixes every axial station (bearing faces at z = ±66/±84, collar, circlip groove). Housing and cover both derive from it. Must be designed FIRST. |
| 2 | housing | Make | casting | Grey cast iron EN-GJL-250 (machined bores) | **false** | Bore axial stations and the 1.5 mm float gap come from the shaft layout; the drive-end boss OD and tapped bolt circle are then consumed by the cover. Design SECOND. |
| 3 | cover | Make | CNC_turning | Steel S355 / 1.0570 | **false** | Spigot OD, bolt circle and axial start plane are all inherited from the housing drive-end face. Design LAST. |

Nothing is `parallel_safe: true` in this project. Every interface is a custom machined fit,
not a standard fastener pattern, and all three parts chain off one axial datum stack.
Design them in the order above, sequentially.

## Make vs Buy

**Buy (catalogue — sourcing agent writes `external/bom.md`):**

| Qty | Item | Spec | Mates with |
|---|---|---|---|
| 2 | Deep groove ball bearing | **6208**, bore 40 / OD 80 / width 18, C3 clearance, 2RS or open + grease | shaft seats (k6), housing bores (H7) |
| 1 | External retaining ring | **DIN 471 — 40 x 1.75**, groove dia 37.5, groove width 1.85 | shaft circlip groove at z = +84.0…+85.85 |
| 1 | Radial lip seal | **40 x 62 x 10**, type A/AS (NBR, spring-loaded) | cover seal pocket dia 62, shaft journal dia 40 |
| 4 | Hex socket head cap screw | **M8 x 30**, ISO 4762, property class 8.8 | cover dia 9 clearance holes -> housing M8 tapped holes, bolt circle 104 |
| 4 | Hex bolt | **M12 x 40**, ISO 4014, class 8.8, + washer + nut | housing foot dia 14 clearance holes (clearance only — no thread in the casting) |
| **2** | Straight grease nipple | **M8 x 1**, DIN 71412 form A | one per bearing bore, tapped boss on top of the housing |

**Grease nipple quantity note for sourcing:** the seed BOM listed 1.
Two in-line bearing bores separated by the central dia-72 passage each need their own feed
to guarantee grease reaches both rolling elements, so the housing carries **two** tapped
M8x1 bosses and the BOM must carry **qty 2**. This is a deliberate uplift, not a typo.

**Make:** shaft, housing, cover. Nothing else.

## Interfaces

Every number below is stated identically in both of the `constraints.md` files that share it.
If one side changes, both change.

| # | Shared dimension | Value | Part A | Part B / catalogue item | Nature |
|---|---|---|---|---|---|
| I1 | Bearing seat diameter | **40.000** (shaft **k6**) | shaft | 6208 bore | interference, light press |
| I2 | Housing bore diameter | **80.000** (bore **H7**) | housing | 6208 OD | transition / locating |
| I3 | Bearing span, centre to centre | **150** | shaft (seats) | housing (bores) | axial datum |
| I4 | Drive-end bearing inboard face plane | **z = +66** | shaft collar face | housing DE bore step face | both bear on the same plane |
| I5 | Drive-end bearing outboard face plane | **z = +84** | shaft circlip face | — | zero axial float |
| I6 | Far-end bearing float gap | **1.5 mm** | housing FE bore step at z = -64.5 | 6208 outer ring face at z = -66 | sliding clearance |
| I7 | Cover spigot OD into housing DE bore | **80.000** (spigot **h8**) | cover | housing | pilot clearance ~0.05 mm |
| I8 | Cover / housing bolt circle | **104** | cover (4 x dia 9 thru) | housing (4 x M8 tapped) | fastener pattern |
| I9 | Cover flange OD = housing DE boss OD | **124** | cover | housing | flush rim, no overhang |
| I10 | Cover mating plane (housing DE face) | **z = +95** | cover flange back face | housing DE boss face | axial datum |
| I11 | Seal pocket bore | **62** x 10 deep | cover | lip seal OD | press fit |
| I12 | Seal running journal | **40** | shaft (z = +90…+100) | lip seal ID | dynamic seal |
| I13 | Circlip groove | dia **37.5** x width **1.85** | shaft | DIN 471 - 40 | retaining |
| I14 | Foot bolt clearance holes | dia **14** (M12) | housing | foundation / M12 bolts | clearance |
| I15 | Grease feed thread | **M8 x 1** | housing boss | grease nipple | threaded |

## Resolved dimension spine

**Every number here is final. All three `constraints.md` files repeat these verbatim.**

### Global
- Shaft axis = **global Z**; up = **+Y**; drive end = **+Z**; origin midway between bearings.
- Bearing centres: **z = +75** (drive end) and **z = -75** (far end). Span **150**.
- Bearing envelope (both): **40 x 80 x 18** (6208).
- Drive-end bearing occupies **z = +66 … +84**. Far-end bearing occupies **z = -84 … -66**.
- Centre height, foot underside to shaft axis: **75**.

### Shaft — total length 300, z = -135 … +165, CNC_turning
| Seg | z from | z to | Length | Dia | Purpose |
|---|---|---|---|---|---|
| S1 | -135 | -66 | 69 | **40** | far-end stub + FE bearing seat (bearing at -84…-66), k6 over the seat |
| S2 | -66 | +60 | 126 | **45** | mid-shaft body; the step face at z = -66 backs the FE inner ring |
| S3 | +60 | +66 | 6 | **48** | drive-end thrust collar (shoulder). 48 > 6208 da-min 47 |
| S4 | +66 | +120 | 54 | **40** | DE bearing seat (66…84, k6) + circlip groove + seal journal |
| S5 | +120 | +165 | 45 | **35** | drive pulley extension — **plain, no keyway** (shrink-disc / taper-lock hub) |

- **Circlip groove**: dia **37.5**, width **1.85**, z = **+84.0 … +85.85**.
  DE inner ring is clamped between the collar face (z=+66) and the circlip (z=+84): **zero float**.
- **Seal journal**: dia 40, z = **+90 … +100**, ground. 4.15 mm clear of the circlip groove.
- Chamfers **1 x 45 deg**: both shaft ends; the dia 48->40 collar faces at z=+60 and z=+66;
  the dia 45->40 step at z=-66; the dia 40->35 step at z=+120.
- L/D = 300 / 45 = **6.7:1** — inside the 8:1 unsupported turning limit.

### Housing — overall length 190, z = -95 … +95, casting
- Body: cylinder **OD 100** about Z (wall 10 mm over the dia 80 bores — exceeds the 8 mm minimum).
- **Drive-end bore**: dia **80.000 H7**, z = **+66 … +95**, length **29**.
  Terminated inboard by a step down to dia **72**, whose face at z = +66 **axially backs the
  DE bearing outer ring**.
- **Far-end bore**: dia **80.000 H7**, z = **-95 … -64.5**, length **30.5**.
  Step down to dia 72 at z = -64.5, leaving **1.5 mm axial float** against the FE outer
  ring face at z = -66. No outboard retention: the FE outer ring is free to slide.
- Central passage: dia **72** through, z = -64.5 … +66 (clears the 6208 outer-ring shoulder
  dia of ~73 at both ends and carries grease between the bores).
- **Bore mouth chamfers 1 x 45 deg** at dia 80 on both end faces (z = +95 and z = -95).
- **Drive-end boss**: dia **124**, z = **+85 … +95** (10 mm proud of the dia-100 body),
  carrying **4 x M8 tapped holes, 16 deep (6.8 drill x 20 deep), on a 104 bolt circle**,
  at 45/135/225/315 deg so no hole sits over the foot pedestal.
- **Grease bosses**: **2 off**, dia **24**, on top (+Y) at X = 0, z = **+75** and **z = -75**,
  rising to Y = +58. Tapped **M8 x 1 x 12 deep**, then a dia **4** feed drilling down to
  break into the dia-80 bore at Y = +40. Reachable from directly above.
- **Foot plate**: X = -60 … +60 (120 wide), Z = -87 … +87 (174 long), Y = **-75 … -60**
  (thickness **15**).
- **Foot bolt pattern**: 4 x dia **14** through holes at **(X = +/-45, Z = +/-75)** —
  i.e. **150 along the axis x 90 across**. Edge distance 12 (Z) / 15 (X).
- **Pedestal**: solid rib X = -35 … +35 (70 wide), Y = -60 … -40, Z = -88 … +88, unioned
  into the body cylinder.

### Cover — flange OD 124 x 12 thick + 5 spigot, z = +90 … +107, CNC_turning
- **Spigot**: OD **80** (h8), z = **+90 … +95**, 5 mm long, entering the housing DE bore.
  Front face clears the DE bearing outer face (z=+84) by **6 mm**.
- **Flange**: OD **124**, thickness **12**, z = **+95 … +107**. Back face seats on the
  housing DE boss face at z = +95.
- **Seal pocket**: dia **62** x **10 deep**, z = **+90 … +100**, for the 40 x 62 x 10 lip seal.
- **Shaft clearance through-bore**: dia **42**, z = **+100 … +107**.
- **Bolt holes**: 4 x dia **9** through the flange on a **104** bolt circle, at 45/135/225/315 deg.
- Chamfers **1 x 45 deg** on the spigot leading edge and the seal pocket mouth.
- Wall between seal pocket (r 31) and spigot OD (r 40): **9 mm**.
- Rim between bolt hole edge (r 56.5) and flange OD (r 62): **5.5 mm**.
- **Wrench clearance**: bolt axes on r = 52. Nothing on any part rises above the cover outer
  face (z = +107) anywhere, so each M8 socket head has a full **unobstructed 15 mm swing
  radius** in the half-space z > +107, and the 8.6 mm hemisphere of the head itself sits
  clear of the flange rim. Verified: largest obstruction radius = 62 (flange OD) at
  z <= +107, bolt swing envelope = r 52 +/- 15 = 37…67 but only above z = +107 where there
  is air.

### Deliberate deviations from the seed spine (with arithmetic)

| Seed value | Shipped value | Why |
|---|---|---|
| Housing bore length 22 each | **29 (DE) / 30.5 (FE)** | 22 is geometrically impossible here. With span 150 the DE bearing's outboard face is at z = +84; the cover spigot needs 5 mm of bore plus clearance, so the DE face must sit at z >= +91. Housing length 190 puts it at +95, which makes the DE bore 95 - 66 = 29. Shortening the bore to 22 would force a 176 mm housing and the spigot would hit the bearing. |
| Cover/housing bolt circle 102 | **104** | On BC 102 the ligament between an M8 tapping drill (6.8, r 3.4) and the dia 80 bore is 51 - 3.4 - 40 = **7.6 mm**, which breaks the hard 8 mm minimum wall. BC 104 gives 52 - 3.4 - 40 = **8.6 mm**. The hard requirement outranks the seed number. |
| Cover flange OD 120 | **124** | Follows from BC 104: a 120 OD would leave only 60 - 56.5 = 3.5 mm of rim outboard of a dia 9 hole. 124 gives 5.5 mm. Still satisfies "at least 120 mm across". |
| Grease boss dia 20 (implied) | **24** | (20 - 6.8)/2 = 7.6 mm wall, under the 8 mm minimum. (24 - 6.8)/2 = **8.6 mm**. |
| 1 grease nipple | **2** | One per bearing bore (see Make vs Buy note). |

## Assembly order

1. Press the **FE 6208** onto the shaft dia-40 seat up to the dia-45 step at z = -66.
2. Press the **DE 6208** onto the shaft dia-40 seat up to the dia-48 collar face at z = +66;
   fit the **DIN 471 - 40 circlip** into the groove at z = +84.0 so the inner ring is clamped.
3. Drop the shaft-and-bearings sub-stack into the housing from the drive end:
   the DE outer ring lands on the dia-72 step face at z = +66; the FE outer ring floats with
   1.5 mm clearance to its step at z = -64.5.
4. Press the **40 x 62 x 10 lip seal** into the cover pocket (dia 62, 10 deep), lip facing
   inboard (-Z, toward the bearing).
5. Fit the cover: spigot into the DE bore, flange on the boss face at z = +95; fasten with
   **4 x M8 x 30** on the 104 bolt circle, torque 25 Nm.
6. Fit **2 x M8 x 1 grease nipples** into the two top bosses; charge both bearings.
7. Bolt the unit down through the 4 x dia 14 foot holes with **M12** hardware.

## Risks

1. **Far-end inner-ring shoulder is undersized against the catalogue.**
   The dia-45 mid-body gives only 2.5 mm of radial contact against the 6208 inner ring,
   where SKF recommends da min = 47. Accepted deliberately: the brief routes **all** axial
   thrust through the located drive-end bearing (collar + circlip), so the FE inner-ring face
   is a creep stop only, not a thrust face. The k6 interference carries the duty.
   If a later revision passes thrust through the far end, raise the mid-body to dia 48.
2. **Casting draft is not modelled.** The housing carries no draft angles in the CAD; 2 deg
   draft on all as-cast vertical faces is a tooling note in `constraints.md`. The DFM
   evaluator will flag this; it is intentional, consistent with the project-wide
   fillet deferral.
3. **No fillets anywhere, project-wide.** A real cast iron housing needs generous radii at
   the pedestal-to-body and boss-to-body junctions for stress and casting soundness. These
   are deferred by project rule. The model therefore has sharp re-entrant corners that a
   production drawing would radius at R5–R8.
4. **Housing is modelled as a solid-walled casting, not cored light.** Mass is around 11 kg.
   Acceptable for a static pillow block; a weight-driven revision would core the pedestal.
5. **Bore concentricity between the two in-line bores** is the single hardest machining
   requirement (both must be line-bored in one setup to hold the 150 mm span coaxial).
   Called out in the housing manufacturing notes, not a geometry risk.
6. **The dia-72 central passage is open between the bearings**, so grease can migrate.
   Both bores are fed independently (2 nipples) to guarantee each bearing is charged.
