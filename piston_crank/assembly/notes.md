# Assembly Notes — piston_crank

## Validation Report — 2026-07-13
- **Score**: 9/10
- **Volume**: 333808.54 mm^3 (compound of 7 instances)
- **Bounding box**: -50.0–157.0 x -50.0–50.0 x -46.0–46.0 mm

### Execution
`tools.cadquery_executor` on `assembly/assembly.py`: success, 308.5 ms, result_type=Compound. Bounding box matches the plan-predicted envelope EXACTLY: xmax=157.0 (crown top X=157 ✓), y ±50.0 (web disc radius 50 ✓), z ±46.0 (crankshaft overall 92 along main axis ✓).

### Color Legend (renderer-assigned)
| Part | Color |
|---|---|
| crankshaft | red |
| connecting_rod | blue |
| gudgeon_pin | green |
| piston | orange |
| piston_ring_1 (seat X=150.7) | purple |
| piston_ring_2 (seat X=145.1) | teal |
| piston_ring_3 (seat X=139.5) | brown |

### Visual Observations
- TOP_CLEAN: Large red circle (⌀100 web disc) centered at the origin with a small red ⌀30 circle (main journal) concentric at the same center — crank main axis on Z through origin. Blue big-end circles (⌀52 OD / ⌀38 bore) centered at X≈30; the red ⌀38 crank pin circle is coincident with (masked by) the blue bore circle — concentric fit. Blue shank runs along +X to the small end, where green concentric circles (⌀16 pin OD / ⌀9 ID) sit dead-center in the blue small-end boss at X≈125. Orange piston rectangle spans X≈102→157, Y ±30; three ring strips (brown/teal/purple, left to right) sit near the crown end, inside the piston band.
- TOP_WIREFRAME: Hidden dashed blue lines through the shank (I-beam web edges); orange dashed skirt interior and boss outlines around the green pin; green/orange dashes coincide at the boss bores — pin passes through both bosses and the small end on one shared axis.
- FRONT_CLEAN: Assembly reads bottom-to-top as crank → rod → piston with no floating parts. Two red vertical web bars (100 tall × 10 wide) flank the blue big end, which is visibly centered in the web gap with clearance on both sides. Blue I-beam shank runs straight up along X to the small end inside the piston. Green gudgeon pin (50 long) spans horizontally inside the orange piston, ending inside the piston silhouette (Z ±25 < ±30). Three ring strips at the top: purple topmost, then teal, then brown — matching seat order 150.7/145.1/139.5, each a hair proud of the orange flanks (the known free-OD 60.5 non-issue). Clear white gap between piston skirt bottom (X=102) and web disc top (X=50) — no contact.
- FRONT_WIREFRAME: Red dashed segments of the crank pin appear top and bottom inside the blue big-end rectangle — pin concentric behind the bore, no offset. Green dashed pin continues through the orange boss regions on both sides of the blue small end.
- RIGHT_CLEAN: Perfect left-right symmetry about Z=0. Two red web bars with the blue big end (20 wide) centered in their 22 mm gap; ~1 mm of red crank pin visible above/below on each side of the rod — exactly the expected 1.0 mm/side clearance. Green pin rectangle (16 × 50) centered, ends tucked inside the ring/piston circles. Concentric ⌀60 piston / ⌀60.5 ring circles centered on the gudgeon/reciprocation axis. Small purple segment at ~9 o'clock and teal segments at ~1:30/~4:30 on the ring circle — the other rings peeking through the nearer ring's end gap, direct visual evidence the gaps are clocked apart (~120°).
- RIGHT_WIREFRAME: Dashed orange interior (stepped skirt bore) concentric with the ring circles; dashed green boss-bore lines collinear with the solid green pin — one shared ⌀16 axis through bosses + small end.
- ISO_CLEAN: All 7 instances form one connected chain: red crank at left, blue rod bridging to the orange piston at right, green pin visible through the open skirt end, purple/teal/brown rings stacked near the crown. No part floats; no two colors occupy the same space.
- ISO_WIREFRAME: Hidden red circles (journals/pin) and dashed blue shank lines consistent with the clean view; ring dashes sit in the groove band only.

### Findings
- [ok] Pose: crank main axis on global Z, crankshaft centered at origin (top view concentricity + bbox z ±46)
- [ok] Crank pin axis at (30,0) ∥ Z — blue big end concentric on it (front wireframe shows pin dashes centered in the bore)
- [ok] Gudgeon pin axis at (125,0) ∥ Z — green ⌀16/⌀9 circles concentric in the small end (top view); crown top at X=157.0 exactly (bbox)
- [ok] Rod along X: big end at X=30 centered in the 22 mm web gap with visible ~1 mm/side clearance (right view); small end at X=125 between the piston bosses (front + top wireframes)
- [ok] Rings: 3 instances seated in the 3 grooves at X = 150.7/145.1/139.5 (front view strip order purple/teal/brown matches), end gaps clocked ~120° apart (right view shows other-ring colors through each gap)
- [ok] No interpenetration, no floating parts; piston skirt bottom (X=102) clears the ⌀100 web discs (X ≤ 50) with a large visible gap
- [ok] Known non-issues confirmed as such and NOT penalized: rings 0.25 mm proud of piston OD (free ring by design); piston stepped interior ⌀47/⌀54; sharp edges everywhere (fillets deferred project-wide)
- [minor] Score held at 9/10 only because groove-seat X positions are verified by the code's exact arithmetic + evenly-spaced strips in the renders, not by an independent dimensional probe of each seat — no visual evidence of any misseating

### Interface / Fit Assessment
Every interface in design_plan.md § Interfaces is visually consistent: pin↔bosses↔small-end share one axis; big-end↔crank-pin concentric with symmetric axial clearance; rings in grooves with back clearance. Dimension chain lands exactly on the planned envelope (157 / ±50 / ±46).

### Recommendations
- None blocking. Ready for STEP/STL export per goals.md.

VALIDATION: PASSED
