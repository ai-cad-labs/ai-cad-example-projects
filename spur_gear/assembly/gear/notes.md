# notes — gear (involute spur gear, driven member)

## Approach
Involute spur gear built from **point math**, not any (nonexistent) `.gear()`/`.involute()`
helper. I started from the golden reference `cylindrical_gear.py` but its per-tooth
`.combine().wire().clean()` construction FAILED at these parameters ("outer wire is not
closed" on extrude). Rather than fight per-tooth wire closure + z unions, I switched to a
more robust construction: **generate the entire gear cross-section as one ordered list of
points** (both involute flanks + tip-land arc + root-gap arc, sampled around all 30 teeth),
draw it as a single `.polyline(pts).close()`, and `.extrude(face_width)` once. Then cut the
central bore. One closed wire, one extrude, one cut — no fragile wire assembly, no unions.

## Key dimensions (all derived from m=2, z=30, α=20°)
- Pitch dia 60 (r_pitch 30), tip dia 64 (r_addendum 32), root dia 55 (r_root 27.5),
  base dia 56.38 (r_base 28.19). r_base > r_root so the gear is NOT undercut — the flank
  has a valid short radial segment from root up to the base circle.
- Face width 10 mm, centred about Z=0 (Principle 0): `.translate((0,0,-5))`.
- Bore: nominal ⌀8 + 0.2 mm print slip-fit clearance = **⌀8.2 modelled**, full-length
  through-bore on the Z-axis. (Constraints explicitly permit ~0.2mm bore clearance.)

## Tooth-centering math
`offset = π/(2z) + inv(α_pitch)` positions each flank so the circular tooth thickness at
the pitch circle equals half the circular pitch. Tip-land is non-zero (teeth are not
pointed) and the root gap is wide (valid), both checked numerically before extrude.

## Verification
- Executor: success, volume 27359 mm³, bbox x/y ±32/±31.9, z ±5 → ⌀~64 × 10 mm centred on origin. ✓
- Dimension check: actual [10, 63.8, 64] vs spec [10, 64] — within tolerance, 0 deviations. ✓
- Renders (8 views) inspected: 30 clean involute teeth, flat tip lands, rounded root gaps,
  centered through-bore, correct 10mm slab in side view. ✓

## Trade-offs / things adjacent parts should know
- **Curves are polyline-approximated**, not true B-spline flanks — flanks use 12 sample
  points each, tip/root arcs 4–5 points. Visually and functionally fine for a 3D-printed
  PLA/PETG gear; if a downstream step needs analytically-exact flanks, raise `flank_samples`.
- **No fillets** (root fillets deferred project-wide) — the golden example's `.fillet(0.4m)`
  root-relief was intentionally dropped.
- **Phase/meshing is NOT modelled here** (correctly). Tooth #0 is centred on the +X axis.
  assembly_resolver must apply the half-tooth phase offset = 360/(2·30) = **6°** when meshing
  against the pinion at 48 mm centre distance, plus the ⌀8 bore slip-fit over the shaft.
- Wall between bore and root = (55−8)/2 = 23.5 mm — very robust, no thin-wall risk.

## Validation Report — 2026-07-21
- **Score**: 9/10
- **Volume**: 27359.45 mm^3
- **Bounding box**: -32.0–32.0 x -31.89–31.89 x -5.0–5.0 mm

### DFMA Findings
- Overall verdict: conditional_pass (6 rules, 5 passed, 0 failed, 1 uncertain).
- DFM-3DP-003 [minor/uncertain]: cannot measure absolute tooth-tip/root-gap size from unscaled renders; tooth tips look proportionate for a spur gear. No failure.

### Visual Observations
- TOP_CLEAN: circular gear disc with ~30 evenly-spaced teeth around the rim; curved (involute-ish) flanks, flat tip lands, rounded root gaps; single small circular through-bore centred at origin.
- TOP_WIREFRAME: same tooth pattern, confirms uniform spacing and centred bore — no extra/missing teeth.
- ISO_CLEAN: 3D gear body, teeth around full perimeter, small central bore (shown as ellipse under iso projection). Consistent thickness.
- ISO_WIREFRAME: dashed hidden circle confirms the through-bore runs the full face width on the Z-axis.
- FRONT/RIGHT (clean+wireframe): identical edge-on rectangular slab (64 tall × 10 wide) with fine tooth serrations on the edges — correct for a rotational gear seen side-on; face width 10mm.

### Findings
- [ok] Geometry: involute spur gear disc, correct topology (toothed rim + central bore).
- [ok] Tooth count: 30 teeth (construction loops z=30; render shows uniform full-circle teeth, no anomalies).
- [ok] Dimensions: OD ⌀64 (bbox 64.0), root ⌀55 (r_root 27.5), face width 10mm (z ±5); dimension_checker PASS, 0 deviations.
- [ok] Bore: ⌀8.2 (⌀8 nominal + 0.2 print slip-fit clearance) — explicitly acceptable per constraints/task.
- [ok] Coordinate convention (Principle 0): revolved part on Z-axis, cross-section centred at origin; bore axis on Z through origin.
- [ok] Involute flanks: polyline-approximated flanks present (acceptable for 3D printing per task).
- [ok] No fillets (deferred). Process 3D_printing satisfied; wall bore→root = 23.5mm, no thin-wall risk.

### Recommendations
- None blocking. assembly_resolver must apply the 6° half-tooth phase offset + ⌀8 bore slip-fit at 48mm centre distance when meshing with the pinion (assembly-time, not a part defect).

VALIDATION: PASSED
