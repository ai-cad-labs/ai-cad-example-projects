# Design Notes: connecting_rod

## Approach
One-piece steel con-rod built as a single-thickness (20.0 mm) plate from three
unioned blanks — big end eye cylinder (⌀52), small end eye cylinder (⌀26), and a
rectangular shank stock (16 x 20 section) spanning the full 95.0 center distance —
then milled: two I-beam pockets cut into the ±Y side faces, then the two through
bores. Feature-decomposed per cookbook Pattern 10; the COMPOSE section reads as the
CNC milling process plan. Verified executed + rendered (8 views inspected).

## Key dimensions (all per constraints.md, verified)
- Bounding box: exactly 134.0 x 52.0 x 20.0 (deterministic dimension_check: PASS, zero deviation)
- Center distance: 95.0 (big end axis at origin, small end axis at (95, 0))
- Big end: OD 52.0, bore ⌀38.05 (crank pin ⌀38.0 rotating clearance), width 20.0
- Small end: OD 26.0, bore ⌀16.02 (gudgeon pin ⌀15.99 full-floating), width 20.0 — PLAIN bore; bronze bushing is a Buy item, NOT modeled in v1
- I-beam: section 16(Y) x 20(Z); pockets 5.5 deep x 12 tall milled from both ±Y faces → web 5.0, flanges 4.0 top/bottom
- Pockets span X = 26.0 → 82.0 (start/end exactly at the eye ODs, so eye walls are never undercut)
- Walls: big end 6.975 (vs 7.0 nominal — see constraints discovered), small end 4.99 (vs 5.0 nominal), web 5.0
- Volume: 37,260.78 mm³ (≈ 0.293 kg in steel)

## Coordinate convention (constraints.md override of the prismatic default)
Big end bore axis = Z through origin; rod long axis = +X; small end bore axis =
Z-parallel through (95, 0, 0); width centered Z = ±10.0. Assembly can place the rod
at TDC with big end onto the crank pin at (30, 0) via a rotation + translation only.

## Constraints discovered
- None new. One nuance: the "minimum wall 7.0 big end / 5.0 small end" figures in
  constraints.md are computed from NOMINAL bores (38.0/16.0). With the clearance
  bores actually modeled (38.05/16.02) the true walls are 6.975 and 4.99 — i.e.
  25/10 µm under the stated minimums. This is inherent to the locked dimension
  chain (OD and clearance bore are both locked), not a design choice here.

## Trade-offs
- Pockets are simple rectangular prisms with sharp corners (NO fillets — project
  deferral). Sharp internal pocket corners will need corner radii ≥ cutter radius
  when fillets are un-deferred; pocket 5.5 deep x 12 wide (ratio 0.46) is easily
  millable with a ⌀6-8 end mill.
- Shank blank runs the full 0→95 span and lets the boolean union absorb overlap
  with the eyes; pocket X-limits at the eye ODs (26 / 82) keep a solid transition
  wedge where the shank blends into each eye — conservative and stiff.

## For adjacent parts / validator
- Big end width 20.0 fits the crankshaft's 22.0 crank-pin span (1.0 mm/side); bore
  38.05 spins on the ⌀38.0 pin.
- Small end width 20.0 fits the piston's 22.0 boss-face spacing (1.0 mm/side);
  bore 16.02 floats on the ⌀15.99 gudgeon pin.
- At TDC assembly pose: rotate so rod X is radial from crank axis, big end center
  → (30, 0), small end center → (125, 0) per design_plan.md.
- v2 rework hook: small end bore becomes a bushing land (bore opens up to the
  bushing OD; bronze bushing pressed in, reamed to ⌀16.02).

## Validation Report — 2026-07-13
- **Score**: 9/10
- **Volume**: 37260.78 mm^3
- **Bounding box**: -26.0-108.0 x -26.0-26.0 x -10.0-10.0 mm (134.0 x 52.0 x 20.0)

### DFMA Findings
- Overall verdict: conditional_pass (18 rules, 14 passed, 0 critical/major failures, 4 warnings)
- PROPOSED-3DP-003 [warning]: sharp internal corners where shank meets cylindrical ends and inside side pockets — consistent with project-wide fillet deferral, not counted against the part
- PROPOSED-GEN-001 [warning]: all external edges sharp (no edge breaks) — fillet deferral, not counted
- PROPOSED-CNC-001 [warning]: sharp internal corners at shank/eye intersections and pocket corners — fillet deferral; part's own notes already record the ⌀6-8 end-mill corner-radius plan for when fillets are un-deferred
- PROPOSED-ASSY-003 [warning]: bore entrances have sharp edges (no lead-in chamfer) — fillet/chamfer deferral, not counted

### Visual Observations
- TOP_CLEAN: classic one-piece con-rod silhouette — a large annular eye on the left (two concentric circles: OD and bore), a straight parallel-sided shank, and a small annular eye on the right. Measured off the image at ~8.96 px/mm (134 mm total length): eye-center to eye-center ≈ 95 mm; big-eye bore/OD diameter ratio ≈ 0.75 (38.05/52 = 0.73 expected). No split line, no bolt holes, no cap seam anywhere on the big end.
- TOP_WIREFRAME: same silhouette plus hidden detail — a pair of dashed lines running close to the shank centerline (the pocket floors / 5 mm web at Y ±2.5, well inside the visible ±8 flange edges), terminated by short dashed verticals at the pocket X-limits. Converting pixel positions, those verticals sit at X ≈ 26 and X ≈ 82 — exactly the eye OD tangency points, so neither pocket undercuts either eye.
- FRONT_WIREFRAME: a uniform-thickness strip (20 mm) in three zones — bottom zone ≈ 51 mm with dashed bore-silhouette lines (big end), middle zone ≈ 60 mm carrying a visible inset rectangle (the milled I-beam pocket, height ≈ 0.6 of the strip thickness — 12/20 expected), top zone ≈ 23 mm with dashed bore lines (small end). Pocket recess is visible as a face feature, i.e., milled INTO the ±Y face, not through.
- FRONT_CLEAN: same three-zone strip, constant 20 mm thickness end to end — confirms the single-thickness plate blank; no steps between eyes and shank.
- RIGHT_WIREFRAME: 52 x 20 end-on section with TWO dashed pocket rectangles, one on each side of the centerline — direct evidence the pockets are cut from BOTH ±Y faces (true I-beam, not a channel). Pocket rectangles measure ≈ 12 mm in the thickness direction. Dashed horizontal bore-silhouette lines also present.
- RIGHT_CLEAN: clean 52 x 20 outer rectangle with silhouette division lines from the small-end OD (≈ 26 mm centered band); no protrusions outside the envelope.
- ISO_CLEAN + ISO_WIREFRAME: both bores read as clear through-holes; the shank pocket recess is visible along the shank top face; every edge is sharp (no fillet arcs anywhere); big end is visibly monolithic with the shank — no cap, no fasteners.

### Findings
- [ok] Focus 1 — Center distance: exactly 95.0 (code: bosses/bores at X=0 and X=95; bbox xmax = 108.0 = 95 + 13, xmin = -26.0; TOP view pixel measurement ≈ 95 mm)
- [ok] Focus 2 — Big end: OD 52.0, bore ⌀38.05, width 20.0, one-piece — no bolted cap, no split line, no bolt holes in code or in any view
- [ok] Focus 3 — Small end: OD 26.0, bore ⌀16.02, width 20.0, plain bore (bushing correctly left as Buy item, not modeled in v1)
- [ok] Focus 4 — I-beam shank: pockets milled from both ±Y faces (RIGHT_WIREFRAME shows both), web = 16 - 2x5.5 = 5.0, flanges = (20 - 12)/2 = 4.0, pockets span X 26.0→82.0 = exactly the eye OD tangencies, no undercut of either eye
- [ok] Focus 5 — Envelope: dimension_checker PASS, expected [20, 52, 134] vs actual [20, 52, 134], zero deviation
- [ok] Focus 6 — No fillets: no .fillet()/.chamfer() calls; all render edges sharp (per project deferral)
- [ok] Coordinate convention (Principle 0): big end bore axis = Z through origin, rod long axis +X, width centered Z ±10.0 — matches constraints.md override; assembly placement is rotation + translation only
- [ok] Placeholder check: real design (is_placeholder: false)
- [ok] Volume plausibility: 37,260.78 mm³ consistent with hand estimate (annuli + I-beam section ≈ 37k mm³)
- [minor] Min walls 6.975 (big end) / 4.99 (small end) vs 7.0/5.0 nominal — KNOWN ACCEPTED DEVIATION per dispatch: 25/10 µm shortfall is inherent to the locked clearance bores (38.05/16.02) against locked ODs; documented in this file's "Constraints discovered". NOT a failure.
- [minor] DFMA sharp-corner warnings (4) — all downstream of the project-wide fillet deferral; revisit when fillets are un-deferred

### Recommendations
- None required for v1 acceptance. When fillets are un-deferred: add pocket corner radii ≥ cutter radius (⌀6-8 end mill per design notes), bore-entrance chamfers, and shank-to-eye blend fillets — these clear all 4 DFMA warnings.
- v2 hook already documented: small end bore opens to bushing land when the bronze bushing (Buy) is introduced.

VALIDATION: PASSED
