# Assembly Spec — impeller_assembly

Single-axis stack, turbocharger-style, per `../design_plan.md`
(the Interfaces table there is the binding contract; this file is the resolver view).

## Global frame

- Shaft axis = global **Z axis**; +Z toward the inlet end (right in the user sketch).
- Global **Z = 0 = the bearing_housing impeller-side face** (the running-clearance reference).
- Ground plane (housing foot bottom) at global Y = −60; gravity −Y.
- Every part is modeled with its rotation/bore axis on local Z per the repo convention,
  so placement is pure Z-translation — **no rotations required**:
  - `bearing_housing` is modeled with its bore axis on Z (plate height along Y, foot in −Y),
    exactly so it drops in with translation only.

## Placement table (translations only)

| # | Component | Local datum (Z=0 in part file) | Global Z placement |
|---|---|---|---|
| 1 | bearing_housing | impeller-side face | 0 |
| 2 | main_bearing (BUY 6203, 17×40×12) | — (representational) | occupies Z = −12 … 0, flush in pocket |
| 3 | impeller | backplate backface | +0.8 (spigot end −14.0; boss contact at 0; nose face +34.8) |
| 4 | pulley_shaft | clamp shoulder face (Ø14→Ø10) | −14.0 |
| 5 | lock_nut (BUY ISO 4032 M10) | seating face | +34.8 (spans to +43.2) |
| 6 | inlet_bearing (BUY 688, 8×16×5) | — (representational) | Z = +47 … +52 on the Ø8 tail |

## Contact / clearance checks the assembly render must prove

1. **6203 OD ↔ housing pocket**: Ø40 in Ø40 pocket, 12 deep, right face flush at Z = 0.
2. **Impeller spigot ↔ 6203 bore**: Ø17 in Ø17, spigot spans Z = −14.0 … −0.8
   (2.0 mm protrusion past the inner race left face at Z = −12).
3. **Standoff boss ↔ inner-race face**: Ø22 boss face contacts at Z = 0; boss must NOT
   overlap housing material (housing face material starts at Ø40 — verify no contact).
4. **Running clearance (user requirement)**: backplate backface at Z = +0.8 vs housing
   face at Z = 0 → **0.8 mm open gap** for Ø40 < ⌀ < Ø72. Must be visible/measurable.
5. **Shaft shoulder ↔ spigot end face**: shaft Ø14→Ø10 shoulder contacts at Z = −14.0.
6. **Shaft ↔ impeller bore**: Ø10 through Ø10, spans Z = −14.0 … +34.8 (grip 48.8).
7. **Lock nut ↔ nose**: nut seats on the impeller nose face (Ø18) at Z = +34.8;
   thread engagement M10×1.5 within shaft thread span Z = +31 … +45.
8. **Shaft ↔ housing back-bore**: Ø14 shaft inside Ø34 back-bore (Z = −16 … −12), no contact.
9. **Inlet bearing ↔ tail**: 688 bore Ø8 on Ø8 tail; **OD 16.0 ≤ 18.0 ceiling**
   (= hub nose Ø) so it sits inside the hub's flow shadow — zero inducer blockage.
10. **Foot ↔ rotating parts**: foot top at Y = −50; impeller lowest sweep Y = −36;
    pulley lowest sweep Y = −24 → no interference, ≥14 mm clearance.

## Buy-part representation rule

`main_bearing`, `inlet_bearing`, `lock_nut` are BUY (see design_plan Make-vs-Buy;
sourcing writes `external/bom.md`).
Model them representationally in `assembly.py` from BOM catalog dims:
bearings = outer race ring + inner race ring + simple ball-band torus/ring;
lock nut = hex prism (16 A/F × 8.4 high) with Ø10 bore (thread not modeled).
No fillets anywhere — deferred project-wide.

## RESOLVED — measured verification results (2026-08-05, assembly_resolver)

`assembly.py` composed with direct `cq.Location` placement (pure Z translations,
zero rotations, constraint solver not used).
All 6 components load and place; executor reports success
(Compound, 749.9 ms, total volume 195,948.16 mm³).

Measured numbers (BRep face probes + boolean intersections, not assertions):

| Check | Measured | Verdict |
|---|---|---|
| Component count | 6/6 (housing, main_bearing, impeller, pulley_shaft, lock_nut, inlet_bearing) | ✅ |
| Assembly bbox | X [−40, +40] · Y [−60, +36] · Z [−58, +60] | ✅ matches expected 80×96, Z −58..+60 |
| Housing impeller-side face | planar +Z face at Z = 0.0000 (area 5543.4 mm²) | ✅ datum holds |
| Impeller backplate backface | largest −Z planar face at Z = +0.8000 (area 3691.4 mm²) | ✅ |
| **Running clearance** | **0.8000 mm** (face-to-face); corroborated by min-distance impeller↔housing = 0.8000 mm | ✅ inside required 0.5–1.0 mm |
| Impeller datum faces | boss backface at Z = 0.0000 (on inner race); spigot end at Z = −14.0000 (on shaft shoulder) | ✅ chain closes |
| impeller ∩ bearing_housing | intersection volume = 0.0 | ✅ no contact, gap only |
| pulley_shaft ∩ bearing_housing | intersection volume = 0.0 | ✅ Ø14 free in Ø34 back-bore |
| impeller ∩ main_bearing | intersection volume = 0.0 (Ø17/Ø17 exact surface contact — intended) | ✅ |
| pulley_shaft ∩ impeller | intersection volume = 0.0 (Ø10/Ø10 exact surface contact — intended) | ✅ |

Buy parts authored inline in `assembly.py` per the representation rule above:
6203 (rings + ball band) at Z −12..0 · M10 hex nut (circumradius 16/√3 ≈ 9.2376) at
Z +34.8..+43.2 (inside thread span +31..+45) · 688-2Z at Z +47..+52 (on Ø8 tail +45..+60).

Renders: 8/8 generated at `renders/` ({front,top,right,iso} × {clean,wireframe}),
renderer success=true with per-part color legend.
Visual verification is owned by the downstream validator (per run directive:
resolver did not read the PNGs).

**Conflicts opened: NONE** — no interface mismatch found; every measured value
matches the binding spec exactly.
