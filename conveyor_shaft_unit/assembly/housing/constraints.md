# Constraints: housing

Primary process: casting

> **AMENDED 2026-10-08 by orchestrator rulings R1-R4 (see `design_log.md`).**
> Four numbers in the original were defects against the brief's own hard requirements:
> the drive-end boss OD (124 left a 6.0 mm rim outboard of the M8 thread, under the hard
> 8 mm minimum wall -> now **130**); the boss thickness (a 16 mm M8 thread cannot fit a
> 10 mm boss with open air behind it -> now **20 mm**, z = +75…+95); the grease bosses
> (at Y = +58 they were buried by the taller boss, breaking "reachable from above" -> now
> **z = ±70, top face Y = +70**); and the foot length (174 mm left the dia-130 boss
> cantilevered -> now **190 mm**, the full housing length).
> Every number below is the AS-BUILT, post-amendment truth. Validate against THIS file.

## Coordinate convention

- **Shaft axis = global Z.** Up = **+Y** (grease nipples point up). Across = **X**.
  **Drive end = +Z.** The mounting foot is at the bottom, **-Y**.
- Global origin (0,0,0) is on the shaft axis, exactly midway between the two bearing centres.
- Bearing centres: **z = +75** (drive end), **z = -75** (far end). Span **150**.
- The housing is modelled directly in the global frame: **z = -95 … +95**, body cylinder
  concentric about Z, foot underside at **Y = -75**. Place with identity in the assembly.

## Functional Requirements

- **A SINGLE cast iron body carrying TWO IN-LINE BORES ON THE SAME AXIS** for two 6208
  bearings (OD 80, width 18), plus a **mounting foot with FOUR bolt holes**.
- Axially back the **drive-end** bearing outer ring against a bore step (this housing takes
  the ~1 kN thrust reaction).
- Let the **far-end** bearing outer ring **float 1.5 mm axially** for thermal growth.
- Present a machined drive-end face with **four M8 tapped holes** to receive the bolted
  cover, with wrench clearance.
- Feed grease to **each** bearing bore from a **tapped boss on the TOP of the housing**,
  reachable from directly above.
- Hold **minimum wall thickness 8 mm everywhere**.

## Dimensions

- Overall: **190 (Z) x 130 (X) x 145 (Y) mm** bounding box
  (z = -95 … +95, X = -65 … +65, Y = -75 … +70).

Numbered hard constraints — every one is final:

1. **Body**: cylinder **OD 100.000** about the Z axis, from z = **-95.0** to z = **+95.0**
   (overall length **190.0**). Wall over the dia 80 bores = **10.0 mm** (> 8 minimum).
2. **Drive-end bore**: dia **80.000** (H7), from the step face at z = **+66.0** out to the
   end face at z = **+95.0** — length **29.0**.
3. **Drive-end bore step**: the bore reduces to dia **72.000** inboard of z = **+66.0**.
   The annular face at z = **+66.0** **axially backs the DE bearing outer ring**
   (72 clears the 6208 outer-ring shoulder dia Da-max of ~73 and the cage).
4. **Far-end bore**: dia **80.000** (H7), from the end face at z = **-95.0** inboard to the
   step face at z = **-64.5** — length **30.5**.
5. **Far-end float**: the FE bearing outer ring nominally occupies z = -84.0 … -66.0, so the
   gap to the step face at z = -64.5 is **1.5 mm**. **The far-end outer ring is NOT clamped
   on either side — it is free to slide 1.5 mm axially.** This is a required functional gap.
6. **Central passage**: dia **72.000** through, z = **-64.5 … +66.0**, joining the two bores.
7. **Bearing span** between bore centres: **150.000** (z = -75.0 and z = +75.0).
8. **Drive-end boss**: dia **130.000**, from z = **+75.0** to z = **+95.0** (20.0 thick, proud of
   the dia 100 body). This is the cover mating pad; it makes the drive-end face
   **130 mm across**. The 20 mm thickness is REQUIRED: a 16 mm M8 thread does not fit in a
   10 mm boss, and at r 52 there is no body behind it (the body is only r 50), so a shallower
   boss would break the tapping drill out into open air.
9. **Cover fixing**: **4 x M8 tapped holes**, **bolt circle dia 104.000**, at
   **45 / 135 / 225 / 315 deg** in the XY plane (clocked so no hole falls over the foot
   pedestal). Tapped depth **16.0**, tapping drill **6.8** x **20.0** deep, entering from
   the z = +95.0 face. Ligament to the dia 80 bore = 52.0 - 3.4 - 40.0 = **8.6 mm** (> 8).
   Thread engagement 16 / 8 = **2.0 x D** (> the 1.5 x D minimum).
10. **Foot plate**: X = **-60.0 … +60.0** (120 wide), Z = **-95.0 … +95.0** (190 long,
    the full housing length, so it supports the dia-130 drive-end boss, which hangs to
    Y = -65 and would otherwise be cantilevered in air),
    Y = **-75.0 … -60.0** (thickness **15.0**).
11. **Foot bolt holes**: **4 x dia 14.000** through the plate (M12 clearance, **no thread**)
    at **(X = +/-45.0, Z = +/-55.0)** — pattern **110.0 along the axis x 90.0 across**.
    Edge distance **33.0 (Z)** (foot plate ends at Z = +/-95, hole edge at 55 + 7) /
    **8.0 (X)** (plate edge at X = 60, hole edge at 45 + 7 = 52). The old "12.0 (Z) / 15.0 (X)"
    was ungrounded against either the hole centreline or its edge; these are measured.
12. **Centre height**: foot underside (Y = -75.0) to shaft axis (Y = 0) = **75.000**.
13. **Pedestal**: solid rib X = **-35.0 … +35.0** (70 wide), Y = **-60.0 … -40.0**,
    Z = **-88.0 … +88.0**, unioned into the body cylinder (which reaches Y = -50).
14. **Grease bosses — 2 off**, cylindrical dia **24.000**, axis along Y at **X = 0**,
    one at **z = +70.0** (over the DE bearing, which spans z = +66…+84) and one at
    **z = -70.0** (over the FE bearing, which spans z = -84…-66), rising from inside the body
    to **Y = +70.0** (20.0 proud of the dia-100 top). Y = +70 is REQUIRED: the dia-130
    drive-end boss reaches Y = +65, so a lower boss would bury the nipple and break the
    brief's "reachable from above". Y = +70 is the global ymax of the part.
15. **Grease feed**: each boss is tapped **M8 x 1**, **12.0 deep** from Y = +70.0 down to
    Y = +46.0 (tapping drill **6.8**), then a dia **4.000** feed drilling continues from
    Y = +46.0 down to **Y = +40.0**, breaking into the dia 80 bore. Boss wall around the
    6.8 drill = (24.0 - 6.8)/2 = **8.6 mm** (> 8).
16. **Minimum wall thickness 8.0 mm everywhere.** Governing sections: body over bore 10.0,
    boss-to-bore ligament 8.6, grease boss wall 8.6, foot plate 15.0, pedestal 20.0.

## Features

- Two in-line dia 80 H7 bores on the common Z axis, each with its outer step (dia 72).
- Dia 72 central through passage.
- Dia 130 x 20 thick drive-end boss with 4 x M8 tapped holes on a 104 bolt circle.
- Foot plate with 4 x dia 14 clearance holes.
- 2 x dia 24 top grease bosses, M8x1 tapped, each with a dia 4 feed drilling to its bore.
- **Chamfers — 1 x 45 deg, required, these SHIP:**
  - **Mouth of the drive-end bore**, dia 80 at z = **+95.0**.
  - **Mouth of the far-end bore**, dia 80 at z = **-95.0**.
  - (Both are bearing-entry lead-ins and are explicitly named in the brief.)
  - (1 x 45 deg on the dia 130 boss outer edge at z = +95.0: DELETED 2026-10-08 after
    validation. A cosmetic deburr, not a functional chamfer and not named in the brief;
    the as-built part has a square corner there. The four chamfers above - both bore
    mouths and both bearing shoulders - are the required set.)
- **NO fillets anywhere**, including at the pedestal-to-body and boss-to-body junctions.
  Production drawings would carry R5-R8 there; deferred project-wide.

## Interfaces

- **-> 6208 bearings (Buy, x2)**: bore **80.000 nominal**, fit **H7**. Model carries
  **nominal 80.000**. The DE outer ring seats on the step face at **z = +66.0**;
  the FE outer ring floats with **1.5 mm** clearance to its step at z = -64.5.
- **-> shaft (Make)**: no direct contact. Shared via the bearings. The DE bearing inboard
  face plane **z = +66.0** is common to the housing step face and the shaft collar face.
  Bearing span **150** is common to both parts.
- **-> cover (Make)**:
  - Cover spigot dia **80.000** (h8) enters the **drive-end bore** (dia 80.000 H7).
  - Cover flange back face seats on the boss face at **z = +95.0**.
  - **4 x M8 tapped holes on bolt circle 104.000** receive the cover's 4 x dia 9 holes.
  - Boss OD **130.000** equals the cover flange OD **130.000** — flush rim, no overhang.
  - The cover spigot (⌀80 x 11 long, z = +84…+95) pilots in the drive-end bore and its front
    face CLAMPS the drive-end bearing outer ring against the z = +66 shoulder. Designed
    contact, not a clash.
- **-> 4 x M8 x 25 cap screws (Buy)**: tapped M8 x 14 deep (6.8 drill x 18 deep, ending at
  z = +77 inside the 20 mm boss), BC 104. Engagement 25 - 12 cover = 13 mm in 14 mm of thread.
- **-> 4 x M12 foot bolts (Buy)**: dia 14 clearance holes, no thread in the casting.
- **-> 2 x M8 x 1 grease nipples (Buy)**: tapped M8 x 1, 12 deep, in the two top bosses at
  z = ±70, boss top face Y = +70.

## Fit callouts (text only — the model is NOMINAL)

- Both bearing bores: **⌀80 H7** (ES/EI +0.030 / 0). Transition/locating for the 6208 OD
  with a rotating inner-ring load. **The CAD carries ⌀80.000.**
- Both bores line-bored in **one setup**; coaxiality of the two bores **0.020 TIR**.
- Drive-end face (z = +95) perpendicular to the bore axis: **0.025**.
- Drive-end bore step face (z = +66) perpendicular to the bore axis: **0.015**.
- Foot underside flat within **0.1** over the 190 x 120 footprint.
- Centre height 75 **+/- 0.2**.
- Cover spigot location: housing bore **⌀80 H7** / cover spigot **⌀80 h8** = clearance pilot.

## Manufacturing

- Primary process: **casting**
- Material class: **Grey cast iron EN-GJL-250 (GG25)**
- Secondary processes: stress relieve after casting; line-bore both dia 80 H7 bores and both
  dia 72 steps in one setup; face the drive-end boss; drill and tap 4 x M8; drill 4 x dia 14
  foot holes; drill and tap 2 x M8x1 grease bosses plus the dia 4 feeds; machine the foot
  underside.
- **Minimum wall 8 mm everywhere** (actual minimum in this design: 8.6 mm).
- **Draft 2 deg on all as-cast vertical faces is a tooling requirement and is NOT modelled**
  (consistent with the project-wide deferral of cast radii). Machined faces carry no draft.
- Approximate mass: 11 kg.
- Deepest drilling: dia 6.8 x 20 deep = 2.9:1, and dia 4 x 6 deep = 1.5:1 — both well inside
  the 10:1 limit.

## Must NOT

1. **No `.fillet()` anywhere.** Fillets are deferred project-wide. Chamfers only.
2. **No feature may reduce any wall below 8.0 mm.** Specifically: do not move the cover bolt
   circle inboard of 104 (at BC 102 the ligament to the bore is 7.6 mm — a violation), and
   do not shrink the grease bosses below dia 24.
3. **Do not change ⌀80.000** on either bore — catalogue-locked by the 6208 OD.
4. **Do not clamp the far-end outer ring.** The 1.5 mm gap at z = -64.5 is a required
   function, not slop. Do not "fix" it by moving the step to z = -66.
5. **Do not add a step, shoulder, cover or circlip at the far-end bore mouth** (z = -95) —
   the FE outer ring must stay free to slide outboard.
6. **Do not thread the foot holes.** Dia 14 clearance only.
7. **Do not move the drive-end bore step off z = +66.0** — it shares that plane with the
   shaft collar face and sets the bearing span.
8. **Do not reduce the drive-end boss below dia 130** or the cover rim loses its seat AND
   the rim outboard of the M8 thread falls under the hard 8 mm minimum wall.
9. **Do not route the grease feed through the central dia 72 passage** — each bore gets its
   own direct dia 4 drilling from its own boss.
10. No as-cast draft, no core prints, no parting-line features in the CAD model.
