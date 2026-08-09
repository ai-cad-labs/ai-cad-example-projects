# bearing_housing — notes

## Provenance
Designed by cad_designer (S1). The agent completed part.py AND rendered all 8 views,
then died of context overflow before writing its own notes. The orchestrator salvaged the
work and re-verified it by direct execution rather than re-dispatching a finisher.

## Verified by direct execution (orchestrator S1)
- Solids: 1 · valid: True · volume 121138.3 mm3
- Bounding box 80.0 x 95.0 x 40.0 mm
- Y range -60.0 .. +35.0 (bore axis at Y=0, so the bore centre is 60 mm above the foot bottom
  and the plate top is 35 above the axis — 95 total, matching the plan)
- Z range -28.0 .. +12.0

## Datum
Local Z = 0 is the HOUSING'S IMPELLER-SIDE FACE, per constraints.md. That face is the reference
plane for the assembly's 0.8 mm running clearance (plan: local 0 -> global 0).

## Read this before calling the +Z overhang a collision
The bounding box extends to Z = +12, i.e. 12 mm PAST the impeller-side datum face. That is the
integral base FOOT (80 x 40 x 10), which is deeper in Z than the 16 mm plate for stability.
It is NOT a clash with the impeller: the foot occupies Y = -60..-50, while the impeller's Ø72
backplate only reaches down to Y = -36. Clearance to the rotating envelope is ~14 mm.
The plate itself spans Z = -16..0, so nothing protrudes from the datum face into the running gap.
(Repair attempt 2 widened the foot to 108 x 40 x 10 — see below; the Y/Z reasoning is unchanged.)

## Features
Upright plate + integral foot (one milled piece), Ø40 x 12 deep bearing pocket bored from the
impeller-side face, Ø34 back-bore forming the 3 mm outer-race retention shoulder and clearing
the Ø14 shaft, 4 x Ø5.5 bolt holes drilled in the foot.
No fillets or chamfers — deferred project-wide.

## Repair attempt 2 (DFA-005) — proposal written to part.proposal.py
**What was wrong**: the z = +5 bolt row at X = ±32 sat under the impeller's Ø72 backplate
overhang. A Ø12 socket needs ~6 mm radial room around the bolt axis; the socket envelope at
32 + 6 = 38 mm intersected the impeller's R36 disc (probe: 1697.7 mm3 per side), so two of the
four foundation bolts were untorquable in the assembled state.

**Root cause**: the bolt pattern was sized to the foot (80 wide, matching the plate), not to
the socket-access envelope of the rotating part above it — an assembly-sequence constraint,
not a geometry error in the original part.

**Fix (per orchestrator directive, widening chosen over lengthening)**:
- `foot_width_x` 80 → 108 (foot now spans X = −54 … +54; overhangs the plate 14 mm per side)
- `bolt_hole_x` 32 → 46 (BOTH rows moved, keeping the pattern rectangular and symmetric;
  the 8 mm hole-center-to-edge margin of the original design is preserved)
- Socket arithmetic: 46 − 6 = 40 > R36 → 4 mm clear per side; all four bolts torquable.
- Lengthening the foot in +Z was considered and REJECTED upstream (would need z ≥ +38,
  making a 68 mm deep foot on an 80 mm plate). Do not re-litigate.
- Deliberately NOT fixed: DFA-008 (missing lead-in chamfers) — WONTFIX this phase under the
  project-wide fillet/chamfer deferral; adding chamfers would itself be a regression.

**Verified numerically (repair agent, direct execution + probe intersections)**:
- Solids: 1 · valid: True · volume 132338.34 mm3
  (= 121138.3 + 28 × 10 × 40 foot widening, exact — no other volume change)
- Bounding box 108.0 × 95.0 × 40.0 (X × Y × Z). ONLY X changed (80 → 108), from the foot.
- Datum unchanged: Z = 0 impeller-side face; plate spans Z = −16 … 0; zero material
  protrudes past Z = 0 above the foot (probe intersect = 0.000000).
- Bore axis still exactly 60.0 mm above the foot bottom (Y range −60 … +35).
- Pocket still Ø40 × 12 from the datum face (void inside R19.9 = 0; wall outside R20 present).
- Back-bore still Ø34 (void inside R16.9 = 0; the 3 mm shoulder ring R17–R20 present).
- All 4 holes pass fully through the foot at (±46, −21) and (±46, +5), each with solid
  surrounding material; both rows outside the plate Z-span, both columns outboard of the
  plate X-span (holes go through foot material only).
- All 8 views re-rendered from the proposal (renders/ now shows the proposal geometry).

**Constraints verified**: bearing grip (pocket), race retention (shoulder), shaft clearance
(back-bore), datum face flatness/no-protrusion, bore height 60, plate 80 × 95 × 16, foot edge
margins (8 mm sides / 7 mm front-rear), no fillets/chamfers, hole depth/dia 10/5.5 ≈ 1.8.

**⚠️ On promotion, constraints.md needs a sync** (repair agent did not edit the requirements
doc): "Overall: 80 x 40 x 95" → 108 × 40 × 95 (foot 108 × 40 × 10); hole positions X = ±32 →
±46; billet 85 × 100 × 45 → ≥113 × 100 × 45. The renderer's dimension_check currently flags
expected ~80 vs actual 108 for exactly this reason — it is the intentional repair delta.

---

## Validation Report: 2026-08-05

- **Score**: 9/10
- **Volume**: 132,338.34 mm^3
- **Bounding box**: -54..+54 (X, 108) x -60..+35 (Y, 95) x -28..+12 (Z, 40) mm
- **Topology**: 1 solid, `isValid() == True`, executor `success: true` (90.5 ms)

### DFMA Findings (from the promoted post-repair `dfma_report.json`)
- Overall verdict: **pass** - 22 rules evaluated, 18 passed, 3 failed, 1 uncertain.
- Every non-pass entry is a `PROPOSED-*` candidate rule
  (PROPOSED-001/002 major, PROPOSED-003 critical, PROPOSED-004 uncertain),
  i.e. rules not yet in the established rulebook.
  **No established DFM rule fails on this part.**
- `placeholder_detector`: not a placeholder ("looks like a real design").
- `dimension_checker`: **PASS** - expected [40.0, 95.0, 108.0], actual [40.0, 95.0, 108.0],
  zero deviations. The earlier renderer `dimension_check` flag ("expected ~80 vs actual 108")
  is **stale**: it predates the constraints.md sync and describes the *intentional*
  DFA-005 repair delta (foot widened 80 -> 108, bolt columns moved |X| 32 -> 46).
  It is not a defect and must not be "corrected".

### Numeric verification (boolean-intersection probes against the built solid)
All probes were run by intersecting the actual built solid with analytic probe volumes;
"void" means the intersection volume was 0.0 mm^3.

- **Bearing pocket O40 x 12**: r < 19.9 mm over Z = -11.9..-0.1 is fully void (0.0 mm^3);
  the annulus r 20.1..22 over the same Z-band carries 2965.3 mm^3 of material.
  The pocket is a true O40 bore, 12 deep, opening on the impeller-side face.
- **Back-bore O34**: r < 16.9 mm over Z = -15.9..-12.1 is fully void.
- **Retaining shoulder (3.0 mm annular land)**: the annulus r 17.1..19.9 over Z = -15.9..-12.1
  is **100.0 % solid** (solid fraction 1.000).
  The O34 -> O40 step is intact, so the 6203 outer race (land ~O35.8) is properly retained
  while the O14 shaft clears by 10 mm per side.
- **Impeller-side datum face at Z = 0**: the annulus r 20..36 over Z = +0.05..+1.0 is
  **completely void** (no protruding feature anywhere on the running-clearance datum),
  and the annulus r 20..34 over Z = -1.0..-0.05 is **100.0 % solid**.
  The datum face is flat and continuous across the clearance-critical radii.
- **4 x O5.5 foundation holes - the DFA-005 repair, verified NOT regressed**:
  all four positions (X = +46 and -46) x (Z = -21 and +5) are fully void
  through the whole foot height (Y = -59.9..-50.1) at r = 2.6 mm.
  The shell r 2.85..3.4 at (X=46, Z=-21) is 100 % solid (105.83 mm^3 of a 105.83 mm^3 probe),
  bounding the hole radius to 2.6..2.85 mm - consistent with the nominal O5.5.
- **Old pre-repair positions are solid**: probes at X = +/-32, Z = -21 return
  208.12 mm^3 of material each (a completely full 9.8 mm x r2.6 cylinder).
  The bolt columns really did move outboard and have **not** drifted back inboard.
- Source parameters corroborate the geometry: `foot_width_x = 108.0`, `bolt_hole_x = 46.0`,
  `bolt_hole_dia = 5.5`, `plate_width_x = 80.0`.

### Visual Observations (3 renders read)
- **FRONT_WIREFRAME** (projection along Y - the foot in plan): the solid outline is a 2.7:1
  rectangle = the 108 x 40 foot. Four holes sit near the corners; scaled off the outline they
  are ~7.8 mm in from each 108-end (**X = +/-46**, 8 mm edge margin) and ~7 mm in from each
  40-edge (Z = -21 and +5), each ~5.5 mm across. A dashed 80 x 16 rectangle - the upright
  plate footprint - is centred on the foot, and inside it two nested dashed rectangles show
  the O40 x 12 pocket stepping down to the O34 back-bore, with the shoulder step visible.
- **RIGHT_WIREFRAME** (elevation along X; the renderer draws +Y downward, so the foot appears
  at the top): an inverted-T silhouette - a 4:1 bar (foot, 40 deep x 10 tall) with a 16-thick,
  95-tall web (the plate) hanging from it, the plate sitting symmetrically within the foot
  depth (~11.7 mm proud each side). Dashed lines show the stepped bore opening on the
  right-hand face; the bore centre measures **60.0 mm** from the foot bottom line, confirming
  the 60 mm shaft height. The Z = 0 face is one unbroken straight line - nothing protrudes
  from the datum. Dashed pairs inside the foot bar are the bolt holes at Z ~ -21 and ~ +5.
- **ISO_CLEAN**: a simple straight upright plate on a wider, thinner base foot, clearly one
  integral piece with no seam. The foot overhangs the plate at both X ends and all four holes
  sit in those overhangs, outboard of the plate footprint. The bore is horizontally centred
  and set high on the plate (~0.37 of the plate height down from the top - matching bore
  Y = 0 with the plate spanning Y = -60..+35), and the smaller concentric circle visible
  inside it is the O34 back-bore forming the retaining shoulder. All edges sharp.

### Findings
- [ok] **Topology**: single valid solid; volume 132,338.34 mm^3 matches the verified figure.
- [ok] **Overall dimensions**: 108 x 95 x 40 mm; dimension_checker passes with zero deviation.
- [ok] **Bearing grip**: O40.0 x 12.0 pocket opening on the impeller-side face - correct
  interface for the 6203 outer diameter.
- [ok] **Race retention**: 3.0 mm annular shoulder proven 100 % solid; O34 back-bore clears
  the shaft.
- [ok] **Datum face**: Z = 0 flat and unobstructed for r = 20..36 - running clearance safe.
- [ok] **DFA-005 repair intact**: four O5.5 holes at X = +/-46, Z = -21 / +5, with the former
  |X| = 32 positions now solid material. Socket access to the impeller-side bolts is preserved
  (envelope reaches R40 vs the impeller R36).
- [ok] **Coordinate convention**: bore axis on Z through the origin, Z = 0 on the mating
  (impeller-side) face - the documented local datum for this part.
- [ok] **Manufacturability**: prismatic 3-axis milled part; O5.5 holes at 10 mm depth
  (L/D ~ 1.8); minimum wall at the pocket ~20 mm; no thin sections, no impossible geometry.
- [ok] Sharp edges / no fillets / no chamfers, no gussets, no lightening pockets - all
  deliberate (project-wide fillet deferral; user asked for "fairly simple and straight").
  Not defects.
- [minor] The three failed and one uncertain DFMA entries are all `PROPOSED-*` candidate
  rules; they are informational until those rules are promoted into the rulebook.

### Recommendations
- No changes required. Do **not** move the foundation holes inboard: |X| = 46 is the
  DFA-005 fix and two bolts become untorquable at |X| = 32.
- If the renderer's cached `dimension_check` note is ever re-surfaced, treat "expected ~80"
  as pre-repair provenance; `dimension_checker` against the current constraints.md passes.
- Optional future work (not blocking): revisit chamfering the pocket mouth and the shoulder
  corner once the project-wide fillet/chamfer deferral is lifted.

VALIDATION: PASSED
