# Constraints: pulley_shaft

## Functional Requirements

- Pulley wheel and shaft as ONE part, turned from a single bar stock (user spec;
  no belt modeled).
- Carry the impeller on a Ø10 seat, clamped between a shaft shoulder and the
  nose lock nut (torque by clamp friction; no keyway by design).
- Provide the M10×1.5 nose thread for the BUY lock nut (ISO 4032 M10)
  and the Ø8 seat for the BUY inlet bearing (688, 8 × 16 × 5 mm).
- Pass through the bearing_housing back-bore (Ø34) without contact —
  the shaft does NOT touch the main bearing; the impeller spigot is interposed
  (per user spec).

## Dimensions

- Overall: ⌀48 x 118 mm   (revolved: Ø48 pulley max diameter × 118 total length)
- Local coordinates (repo convention): axis of revolution = Z;
  **Z = 0 at the clamp SHOULDER face (Ø14→Ø10 step)** — the assembly datum;
  +Z toward the inlet/nose end.
- Segment table, left (−Z) to right (+Z) — all LOCKED:

| Segment | Diameter | Local Z span | Length |
|---|---|---|---|
| Left stub | Ø14.0 | −44 … −36 | 8.0 |
| Pulley | Ø48.0 | −36 … −24 | 12.0 |
| Mid-section | Ø14.0 (`D_SHAFT_SHOULDER`) | −24 … 0 | 24.0 |
| Clamp shoulder face | Ø14.0 → Ø10.0 annular face | at Z = 0 | — |
| Impeller seat | Ø10.0 (`D_SHAFT_IMPELLER_SEAT`) | 0 … 45 | 45.0 |
| Nose thread | M10×1.5 (major 10.0) | 45 … 59 | 14.0 |
| Inlet-bearing tail | Ø8.0 (`D_SHAFT_INLET_SEAT`) | 59 … 74 | 15.0 |

- Pulley groove: round-belt U-groove, groove radius 3.5, groove root Ø40.0,
  centered on the pulley width (groove center at Z = −30).
- Clamp-stack closure (verify, do not change): impeller grip `L_IMP_GRIP` = 48.8
  from the shoulder face → nut seats at Z = +48.8, nut spans to +57.2 (8.4 high),
  inside the thread span 45 … 59 ✓; plain seat 45.0 < 48.8 so only thread
  (major 10.0 = bore 10.0) occupies the last 3.8 of the impeller bore ✓.

## Features

- 6 cylindrical segments + 1 thread, single setup turning; sharp steps
  (NO fillets — deferred project-wide; no undercut relief grooves either — keep geometry simple).
- Thread modeled as a plain Ø10.0 cylinder in CAD (annotation-level thread;
  do not model helix geometry).
- No keyway, no cross-holes, no flats.

## Interfaces

- Connects to impeller via Ø10.0 seat (slide fit H7/g6 intent, model nominal 10.0)
  and the Ø14→Ø10 shoulder face at Z = 0 clamping the spigot end face.
- Connects to lock_nut (BUY ISO 4032 M10) via M10×1.5 × 14 nose thread
  (external major = 10.0 = seat diameter — no step-up; standard, checked).
- Connects to inlet_bearing (BUY 688) via Ø8.0 tail; bearing occupies
  local Z = 61 … 66 (global +47 … +52); slide fit, model nominal 8.0.
- Clearance through bearing_housing back-bore: Ø14 inside Ø34, no contact
  (housing spans local Z = −2 … +14 in global terms — shaft local −2…0 region is Ø14 ✓).
- Pulley-to-housing standoff: pulley right face at local Z = −24,
  housing left face at local Z = −2 → 22 mm clear ✓.

## Manufacturing

- Primary process: CNC_turning
- Material class: Steel 1045
- Secondary processes: single-point threading M10×1.5
- NOTE: L/D ≈ 118/10 ≈ 11.8:1 — exceeds the 8:1 unsupported limit;
  within the 15:1 supported limit. Turn between centers / tailstock support REQUIRED
  (state in process notes; no geometry change needed).
- Bar stock Ø50 × 125; largest-to-smallest step 48→8 is turned, no premachining needed.
