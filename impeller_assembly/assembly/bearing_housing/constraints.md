# Constraints: bearing_housing

## Functional Requirements

- Simple, straight upright plate the assembly seats on (user spec), with an
  integral base foot for mounting.
- Grip the main bearing (BUY 6203, 17 × 40 × 12 mm) by its OUTER diameter in a
  stepped pocket; retain the outer race axially toward the pulley side.
- Its impeller-side face is the reference plane for the 0.8 mm running clearance
  to the impeller backface (user requirement window 0.5–1.0 mm) —
  the clearance itself is realized by the impeller's standoff boss;
  this part only needs the bearing FLUSH with that face.
- Clear the Ø14 shaft through the back-bore with no contact.

## Dimensions

- Overall: 108 x 40 x 95 mm   [REVISED S1 after DFM gate promoted the DFA-005 repair]   (bounding box: X width × Z depth incl. foot × Y height;
  upright plate 80 wide × 95 tall × 16 thick UNCHANGED, base foot widened to 108 × 40 × 10)
- Local coordinates (repo convention for parts with a primary bore):
  **bore axis = Z through origin**; **Z = 0 at the impeller-side face** (clearance datum),
  plate spans Z = −16 … 0.
  Plate height along Y: foot bottom (ground) at Y = −60, plate top at Y = +35
  → bore center 60 above ground.
  Width along X: ±40.
  Modeled this way, the assembly places it with pure Z-translation (no rotation).
- Foot: 108 (X) × 10 (Y = −60 … −50) × 40 (Z = −28 … +12), centered on the plate
  (widened from 80 so the impeller-side bolts clear the Ø72 wheel — see DFA-005 below)
  mid-plane (plate mid at Z = −8).

## Features

- Bearing pocket: Ø40.0 (`D_MB_OD`, H7 transition-fit intent, model nominal)
  × 12.0 deep (`W_MB`), opening on the impeller-side face (Z = −12 … 0).
- Back-bore: Ø34.0 (`D_HOUSING_BACKBORE`) through the remaining plate (Z = −16 … −12)
  → 3.0 mm annular shoulder retains the 6203 outer race (outer-race land ≈ Ø35.8 ✓)
  and clears the Ø14 shaft by 10 mm per side.
- 4 × Ø5.5 clearance holes (for M5 bolts, hardware not modeled) through the foot,
  at X = ±46, Z = −21 and Z = +5 (8 mm to every foot edge; depth/dia 10/5.5 ≈ 1.8 ✓).
  DFA-005 CONSTRAINT: the impeller-side pair (Z = +5) sits under the Ø72 impeller (R36).
  A Ø12 socket needs ~6 mm radial room, so |X| must be ≥ ~42. At |X| = 46 the socket
  envelope reaches R40 versus the impeller's R36 — 4 mm of genuine clearance. Do NOT move
  these holes inboard again; two foundation bolts become untorquable if you do.
- Sharp edges throughout — NO fillets, NO chamfers (deferred project-wide).
- No gussets, no lightening pockets: "fairly simple and straight" per user.

## Interfaces

- Connects to main_bearing (BUY 6203) via the Ø40 pocket; bearing right face
  flush with the impeller-side face (Z = 0) — this flushness is what makes the
  impeller's 0.8 boss thickness equal the running clearance exactly.
- Faces the impeller backplate (Ø72) across the 0.8 mm running clearance
  (`CLR_RUN`) for radii 20 … 36; face must be flat, no protruding features.
- Clears pulley_shaft: Ø14 shaft through the Ø34 back-bore, no contact;
  the shaft's Ø14→Ø10 shoulder plane sits at Z = −14, inside the back-bore span.
- Clears rotating parts vertically: foot top at Y = −50 vs impeller lowest sweep
  at Y = −36 → 14 mm clear ✓.

## Manufacturing

- Primary process: CNC_milling
- Material class: Aluminum 6061
- Secondary processes: none (pocket bored to H7 intent in the same setup)
- Pre-verified ratios: pocket depth/width 12/40 ✓ (≤4:1); min wall above bore
  = 15 mm (plate top Y=+35 vs pocket top Y=+20) ✓; side walls 20 mm each ✓;
  plate thickness 16 = pocket 12 + shoulder 4 ✓ (≥1.5 mm everywhere).
- Billet 113 × 100 × 45; mill foot and plate as one piece (single part, two setups).
