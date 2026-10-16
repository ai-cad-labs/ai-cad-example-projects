# Constraints: shaft

Primary process: CNC_turning

## Coordinate convention

- **Shaft axis = global Z.** Up = **+Y**. Across = **X**. **Drive end = +Z.**
- Global origin (0,0,0) is on the axis, exactly midway between the two bearing centres.
- Bearing centres: **z = +75** (drive end), **z = -75** (far end). Span **150**.
- The shaft is modelled directly in the global frame: **z = -135 … +165**.
  No rotation, no X/Y offset in the assembly. Place with identity.

## Functional Requirements

- Support a 1,500 rpm conveyor drive carrying ~4 kN radial at the overhung drive pulley and
  ~1 kN axial thrust, 20,000 h between services.
- Carry two **6208** deep groove ball bearings (bore 40 / OD 80 / width 18) on dia 40 seats.
- **Drive-end bearing axially located between a shaft SHOULDER and a CIRCLIP** — zero float.
- **Far-end bearing inner ring located by a step on one side only**; that bearing floats
  1.5 mm axially in the housing bore (float is taken in the housing, not on the shaft).
- Provide a ground dia 40 journal for a 40 x 62 x 10 radial lip seal running in the cover.
- Provide a plain dia 35 drive pulley extension at the drive end — **no keyway**
  (hub is a shrink-disc / taper-lock type).
- Take **all** axial thrust through the drive-end bearing.

## Dimensions

- Overall: **⌀48 x 300 mm** (largest turned diameter x total length), z = -135 … +165.

Numbered hard constraints — every one is final:

1. Total length **300.0**, from z = **-135.0** to z = **+165.0**.
2. Segment S1: z = **-135.0 … -66.0** (69.0 long), dia **40.000** — far-end stub and
   **far-end bearing seat**. The FE 6208 occupies z = -84.0 … -66.0.
3. Segment S2: z = **-66.0 … +60.0** (126.0 long), dia **45.000** — mid-shaft body.
   The step face at z = **-66.0** backs the FE bearing inner ring.
4. Segment S3: z = **+60.0 … +66.0** (6.0 long), dia **48.000** — **drive-end thrust
   collar (the shoulder)**. 48 clears the 6208 inner-ring shoulder diameter da-min of 47.
5. Segment S4: z = **+66.0 … +120.0** (54.0 long), dia **40.000** — **drive-end bearing
   seat**. The DE 6208 occupies z = **+66.0 … +84.0**, butted against the collar face at
   z = +66.0.
6. Segment S5: z = **+120.0 … +165.0** (45.0 long), dia **35.000** — drive pulley
   extension, plain cylindrical, **no keyway, no thread, no flat**.
7. **Circlip groove**: diameter **37.500**, width **1.850**, from z = **+84.000** to
   z = **+85.850**. Per **DIN 471 - 40 x 1.75**. Its inboard wall at z = +84.0 is the
   outboard clamping face for the DE bearing inner ring.
8. **Zero axial float at the drive end**: collar face z = +66.0 to circlip face z = +84.0 =
   **18.000**, exactly the 6208 width. This is a hard check.
9. **Seal journal**: dia **40.000** over z = **+90.0 … +100.0**, ground, Ra <= 0.4 um.
   It sits 4.15 mm outboard of the circlip groove end (z = +85.85) — no overlap.
10. Bearing span, seat centre to seat centre: **150.000** (z = -75.0 to z = +75.0).
11. L/D ratio: 300 / 45 = **6.7:1**, inside the 8:1 unsupported CNC turning limit.
    No steady rest required.

## Features

- Five turned diameters only (40 / 45 / 48 / 40 / 35) plus one groove. Nothing else.
- **Circlip groove** dia 37.5 x 1.85 wide at z = +84.0 (see constraint 7).
- **Chamfers — 1 x 45 deg, required, these SHIP:**
  - z = **-135.0** shaft end face (lead-in for the FE bearing press).
  - z = **-66.0**, the dia 45 -> dia 40 step (bearing shoulder).
  - (z = **+60.0**, the dia 45 -> dia 48 collar entry: DELETED 2026-10-08 after validation.
    This one was listed in error. It is a step UP into the back of the collar, not a bearing
    shoulder and not an assembly lead-in, so it carries no chamfer and needs none. The
    as-built part has a square corner there. The five chamfers above are the required set.)
  - z = **+66.0**, the dia 48 -> dia 40 step (**the drive-end bearing shoulder**).
  - z = **+120.0**, the dia 40 -> dia 35 step.
  - z = **+165.0** shaft end face.
- **NO fillets. NO undercut radii. NO keyway. NO centre holes modelled.**

## Interfaces

- **-> 6208 bearings (Buy, x2)**: seat diameter **40.000 nominal**, fit **k6**
  (+0.002 / +0.018 on a 40 mm shaft). Model carries **nominal 40.000**.
- **-> DIN 471 - 40 circlip (Buy)**: groove dia **37.500**, width **1.850**,
  located at z = +84.000.
- **-> 40 x 62 x 10 lip seal (Buy, carried in the cover)**: journal dia **40.000**,
  z = +90.0 … +100.0.
- **-> housing (Make)**: no direct contact. Shared via the bearings only.
  The DE bearing inboard face plane **z = +66.0** is common to the shaft collar face
  and the housing drive-end bore step face. Bearing span **150** is common to both parts.
- **-> cover (Make)**: no direct contact. The cover through-bore is dia 42 and the shaft is
  dia 40 there, giving 1.0 mm radial clearance.
- **-> drive pulley hub (out of scope)**: dia **35.000** h7 x 45 long at z = +120 … +165.

## Fit callouts (text only — the model is NOMINAL)

- Both bearing seats: **⌀40 k6** (ES/EI +0.018 / +0.002). Light interference into the
  6208 bore for a rotating-inner-ring load. **The CAD carries ⌀40.000.**
- Circlip groove: **⌀37.5 h11**, width **1.85 +0.14/0**, per DIN 471.
- Seal journal: **⌀40 h8**, ground, Ra <= 0.4 um, no spiral lead from grinding.
- Pulley extension: **⌀35 h7**.
- Concentricity of both bearing seats to the common axis: **0.015 TIR**.
- Perpendicularity of the dia 48 collar face (z = +66) to the axis: **0.010**.

## Manufacturing

- Primary process: **CNC_turning**
- Material class: **Steel C45 / EN8 (1.0503)**, normalised
- Secondary processes: induction-harden and grind both bearing seats and the seal journal
  (55-60 HRC case); groove turning for the circlip; deburr all edges.
- Stock: dia 50 bar, turn between centres (two-setup, flip at the mid-body).
- L/D 6.7:1 — within the 8:1 unsupported limit.
- Dynamic balance grade G6.3 at 1,500 rpm (note only, not a geometry feature).

## Must NOT

1. **No `.fillet()` anywhere.** Fillets are deferred project-wide. Chamfers only.
2. **No keyway, spline, flat, cross-hole or set-screw dimple** on the dia 35 extension.
3. **Do not change ⌀40.000** on either bearing seat — it is a catalogue-locked dimension
   (6208 bore). Never resize a seat to suit a DFM note.
4. **Do not change the circlip groove** (37.5 / 1.85) — DIN 471 locked.
5. **Do not move the collar face off z = +66.0 or the circlip groove off z = +84.0.**
   The 18.000 mm between them is the 6208 width; any change destroys the zero-float
   requirement and breaks the housing step plane.
6. **Do not change the 150 mm bearing span** — the housing is built around it.
7. No chamfer larger than 1 x 45 deg at any bearing shoulder (a bigger chamfer eats the
   bearing seating face).
8. No reduction of the dia 48 collar below 48 (it must clear the 6208 da-min of 47).
9. No through-bore, no hollow shaft, no lightening features.
