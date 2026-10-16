# Constraints: cover

Primary process: CNC_turning

> **AMENDED 2026-10-08 by orchestrator rulings R1 and R5 (see `design_log.md`).**
> This file previously specified a ⌀124 x 17 cover with a non-contacting 5 mm spigot and a
> dia-46 bore ahead of the seal pocket. Three of those numbers were defects:
> (R1) a ⌀124 flange left only a 6.0 mm rim outboard of the M8 thread on the housing side,
> breaking the brief's hard 8 mm minimum wall -> flange OD is now **130**;
> (R5) a 5 mm spigot left the "located" drive-end bearing's OUTER ring free to walk 6 mm,
> so the spigot is now **11 mm and bears on the outer ring**;
> (R5-corrected) the dia-46 bore made the ⌀62 seal physically **impossible to install** from
> either side, so the bore is now a straight ⌀62 to an outboard shoulder.
> Every number below is the AS-BUILT, post-amendment truth. Validate against THIS file.

## Coordinate convention

- **Shaft axis = global Z.** Up = **+Y**. Across = **X**. **Drive end = +Z.**
- Global origin (0,0,0) is on the shaft axis, exactly midway between the two bearing centres.
- The cover is a body of revolution about Z, modelled directly in the global frame:
  **z = +84.0 … +107.0**. Place with identity in the assembly (no rotation, no X/Y offset).
- Its **back face seats on the housing drive-end boss face at z = +95.0**;
  the spigot projects inboard (-Z) to z = +84.0; the flange projects outboard to z = +107.0.

## Functional Requirements

- **Close the drive end of the housing** and **carry a 40 x 62 x 10 radial lip seal**
  running on the shaft's dia 40 ground journal.
- **Axially locate the drive-end 6208 bearing**: the spigot front face clamps the bearing
  OUTER ring against the housing shoulder at z = +66. (The INNER ring is clamped between the
  shaft collar and the circlip. Both rings trapped = a true locating bearing.)
- **Be held by FOUR M8 hex-socket cap screws** into the housing drive-end boss,
  with **wrench clearance**.
- Pilot concentrically on the housing drive-end bore so the seal runs true to the shaft.
- Clear the shaft and the circlip without contact.

## Dimensions

- Overall: **⌀130 x 23 mm** (flange OD x total axial length, z = +84.0 … +107.0).

Numbered hard constraints — every one is final:

1. **Flange**: OD **130.000**, thickness **12.000**, from z = **+95.0** to z = **+107.0**.
   The face at z = +95.0 is the mating face against the housing boss.
2. **Spigot**: OD **80.000** (h8), length **11.000**, from z = **+84.0** to z = **+95.0**.
   It enters the housing drive-end bore (dia 80.000 H7) as a clearance pilot.
3. **Spigot front face BEARS on the drive-end bearing outer ring** at z = **+84.0**.
   The flat annulus runs r **32.0 … 39.0** (inboard of it is the 1 mm pocket-mouth chamfer);
   the 6208 outer ring face spans r 36.5 … 40.0, so the **contact band is r 36.5 … 39.0 =
   2.5 mm wide**. This contact is REQUIRED, not a clash.
4. **Seal pocket**: dia **62.000**, bored straight from the inboard face at z = **+84.0** to
   the shoulder at z = **+100.0** (16.0 long). The **40 x 62 x 10** lip seal is pressed in
   from the inboard (-Z) side and butts the shoulder, occupying z = **+90.0 … +100.0**.
   The leading **6.0 mm** of bore (z = +84.0 … +90.0) is the grease cavity ahead of the lip.
5. **Shaft clearance through-bore**: dia **42.000**, from z = **+100.0** to z = **+107.0**
   (7.0 long). Gives 1.0 mm radial clearance over the dia 40 shaft.
   Its inboard face at z = +100.0 is the seal's axial shoulder.
6. **Bolt holes**: **4 x dia 9.000** through the flange (z = +95.0 … +107.0),
   on a **bolt circle dia 104.000**, at **45 / 135 / 225 / 315 deg** —
   the identical clocking and circle used by the housing's 4 x M8 tapped holes.
7. **Seal-pocket wall**: between the pocket radius (31.0) and the spigot OD radius (40.0) =
   **9.0 mm**.
8. **Flange rim**: between the bolt-hole outer edge (r = 52.0 + 4.5 = 56.5) and the flange
   OD radius (65.0) = **8.5 mm**.
9. **Wrench clearance**: the bolt axes lie on r = 52.0 and the bolt heads sit on the flange
   outer face at **z = +107.0**. **Nothing on any part of the assembly rises above
   z = +107.0** (the housing tops out at z = +95.0; the only feature further out in +Z is the
   dia 35 shaft extension at r 17.5). Heads are **90 deg apart on r 52 = 73.5 mm
   centre-to-centre**, i.e. 60.5 mm of air between adjacent 13 mm heads. A 17 mm AF socket
   centred at r 52 sweeps r 43.5 … 60.5, which sits inside the flange OD (r 65) with
   **4.5 mm of flange still outboard of the socket** — that 4.5 mm is the governing number —
   and with wholly unobstructed open half-space above z = +107.0.
10. Total axial length **23.000** (11.0 spigot + 12.0 flange).

## Features

- Turned flange + spigot (two outside diameters: 130 and 80).
- Internal bore: dia 62 straight through to the shoulder at z = +100, then dia 42 through.
- 4 x dia 9 drilled through-holes on BC 104.
- **Chamfers — 1 x 45 deg, required, these SHIP:**
  - **Spigot leading edge**, dia 80 at z = **+84.0** (entry lead-in into the housing bore).
  - **Seal pocket mouth**, dia 62 at z = **+84.0** (press lead-in for the lip seal).
- **NO fillets anywhere.** Deferred project-wide.

## Interfaces

- **-> housing (Make)**:
  - Spigot **⌀80.000** (h8) pilots in the housing drive-end bore **⌀80.000** (H7).
  - Flange back face seats on the housing boss face at **z = +95.0**.
  - **4 x dia 9 holes on bolt circle ⌀104.000** align with the housing's **4 x M8 tapped
    holes on bolt circle ⌀104.000**, same 45/135/225/315 deg clocking.
  - Flange OD **130.000** equals the housing drive-end boss OD **130.000** — flush rim.
- **-> 40 x 62 x 10 radial lip seal (Buy)**: pocket **⌀62.000**, seal butts the shoulder at
  z = +100.0; lip faces inboard (-Z, toward the bearing). Grease pressure arrives from -Z and
  pushes the seal ONTO its shoulder, so the shoulder is correctly on the outboard side.
- **-> shaft (Make)**: no metal-to-metal contact. The seal lip runs on the shaft's dia
  **40.000** ground journal at z = +90.0 … +100.0. The dia 42 through-bore gives 1.0 mm
  radial shaft clearance.
- **-> drive-end 6208 bearing (Buy)**: **DESIGNED CONTACT** on the outer ring face at
  z = +84.0, contact band r 36.5 … 39.0 (constraint 3).
- **-> circlip (Buy)**: no contact. The DIN 471 - 40 ring (OD ~43.5, r 21.75) sits at
  z = +84.0 … +85.85 inside the dia 62 bore (r 31) — **9.25 mm radial clearance**.
- **-> 4 x M8 x 25 ISO 4762 cap screws (Buy)**: dia 9 clearance holes, head bears on the
  flange outer face at z = +107.0. Grip = 12 (cover) + 13 (thread engagement) = 25.

## Fit callouts (text only — the model is NOMINAL)

- Spigot: **⌀80 h8** (0 / -0.046) into the housing **⌀80 H7** (+0.030 / 0) —
  clearance pilot, 0 to 0.076. **The CAD carries ⌀80.000.**
- Seal pocket: **⌀62 H8**, Ra <= 1.6 um, for a press-fit elastomer-cased lip seal.
- Bolt holes: **⌀9 H13** (M8 medium clearance per ISO 273).
- Seal pocket concentric with the spigot OD: **0.05 TIR** (both machined in one chucking —
  this is what keeps the seal lip true to the shaft).
- Flange back face perpendicular to the spigot axis: **0.025**.
- Spigot front face (the bearing clamping face) perpendicular to the axis: **0.025**.
- Bolt circle **⌀104 +/- 0.2**, true position **⌀0.4 MMC** — matches the housing pattern.

## Manufacturing

- Primary process: **CNC_turning**
- Material class: **Steel S355JR (1.0045)** or **C22**, as-rolled plate / disc stock
- Secondary processes: turn the OD, spigot and both internal bores in **one chucking**
  (protects the seal-to-spigot concentricity); drill 4 x dia 9 on a milling station or
  live-tool turret; deburr all edges; zinc plate or paint for corrosion protection.
- Stock: dia 136 x 26 disc or plate blank.
- Disc proportions (130 dia x 23 long) — no L/D concern; short, stiff, single-setup part.
- Deepest drilling: dia 9 x 12 deep = 1.3:1, far inside the 10:1 limit.
- Minimum wall in the part: 8.5 mm (flange rim) — steel, machined, far above any limit.

## Must NOT

1. **No `.fillet()` anywhere.** Fillets are deferred project-wide. Chamfers only.
2. **Do not change ⌀62.000** on the seal pocket — catalogue-locked by the 40 x 62 x 10
   lip seal.
3. **Do not change the spigot to anything other than ⌀80.000** — it must match the housing
   drive-end bore, which is catalogue-locked by the 6208 OD.
4. **Do not move the bolt circle off ⌀104.000.** It is shared verbatim with the housing;
   ⌀102 would drive the housing's bolt-to-bore ligament to 7.6 mm and break the hard 8 mm
   minimum wall.
5. **Do not shorten the spigot below 11.0 mm** (z = +84.0 … +95.0). Its front face is what
   axially traps the drive-end bearing OUTER ring. This REVERSES the pre-amendment rule.
6. **Do not insert any bore smaller than ⌀62 between z = +84.0 and the seal shoulder at
   z = +100.0.** The ⌀62 seal must pass through to reach its seat; a ⌀46 lead bore made the
   part impossible to assemble and was rejected for exactly this reason.
7. **Do not shrink the flange OD below 130.000** — it must match the housing boss OD, and the
   housing's own 8 mm minimum wall depends on that boss diameter.
8. **Do not reduce the dia 42 through-bore** — it must clear the dia 40 shaft with margin.
9. **Do not add a grease groove, breather, lip or dust flinger** — not in scope.
10. **No obstruction may be added above z = +107.0** anywhere near r = 52, or the wrench
    swing at each M8 bolt is lost.
