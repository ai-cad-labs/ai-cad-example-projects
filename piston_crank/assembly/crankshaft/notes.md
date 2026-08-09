# Notes: crankshaft (fresh design, 2026-07-13)

## Approach
One-piece single-throw crank built as a union of 5 simple cylinders (Cookbook Pattern 10,
feature-decomposed): bottom journal -> bottom web -> crank pin -> top web -> top journal.
All geometry is `circle().extrude().translate()` + `union()` — no exotic API, zero fix cycles.

Coordinate convention (Principle 0): main rotation axis = Z, part centered at origin
(Z = ±46.0). Crank pin axis parallel to Z through (30, 0, 0) — throw along +X, matching
the TDC assembly pose in design_plan.md.

## Key dimensions (all verbatim from constraints.md — nothing negotiated)
- Overall: ⌀100 x 92 along Z (bbox verified exact: 100 x 100 x 92; volume 217,373 mm³)
- Main journals: ⌀30 x 25, coaxial on Z, spanning Z -46..-21 and +21..+46
- Webs: 2x ⌀100 x 10 full discs (counterweight cutouts DEFERRED per v1), Z -21..-11 and +11..+21
- Crank pin: ⌀38, free span exactly 22.0 between web inner faces (Z = ±11), axis at (30, 0)
- Throw 30.0 -> stroke 60.0
- NO fillets (project-wide deferral), no threads, no oil holes

## Design decision worth knowing: 1 mm embed overlaps (internal only)
Each journal and the crank pin are modeled 1 mm LONGER than nominal, embedded into the
adjacent web, per Cookbook Principle 1 (defensive offsets — avoid exactly-coincident faces
in booleans). This is INVISIBLE externally: journals (r15) and the pin (extremity at
30 + 19 = 49) are fully inside the web silhouette (r50), so no external face, the bbox,
and the 22.0 mm free pin span are all unaffected. An assert in part.py guards the
pin-inside-web condition if parameters change.

## Verification done
- Executor: success, bbox exactly (±50, ±50, ±46), volume matches hand calc (~218k mm³)
- Renderer dimension_check: PASS (expected 92/100, actual 92/100/100, zero deviation)
- All 8 renders visually inspected: pin bridges both webs (one connected solid), pin offset
  visible in front/top views and correctly edge-on in the right view, no fillets

## For adjacent parts (connecting_rod is the consumer)
- Crank pin interface AS-DESIGNED: ⌀38.0 exactly, free length 22.0 exactly between web
  inner faces at Z = ±11.0. Rod big end (⌀38.05 bore x 20 wide) gets 1.0 mm clearance/side.
- At TDC pose the pin axis is at (30, 0), parallel to Z — rod big end centers at
  (30, 0, 0) with no Z offset.
- Web discs are FULL ⌀100 discs in v1 — anything sweeping near the crank must clear r=50
  (design_plan.md already checks piston skirt at X=102 > 50 ✓).

## Trade-offs / potential issues
- Full-disc webs mean the part is NOT balanced (no counterweight relief) — acknowledged
  deferral in constraints.md v1; a later revision would mill cutouts on the +X side of the webs.
- Steel 304 is unusual for a crankshaft (typically 4140/EN19) but is the constraint-specified
  material class; no geometry impact.

## Validation Report — 2026-07-13
- **Score**: 9/10
- **Volume**: 217373.08 mm^3
- **Bounding box**: -50.0-50.0 x -50.0-50.0 x -46.0-46.0 mm

### DFMA Findings
- Overall: conditional_pass — 16 rules evaluated, 14 passed, 2 failed at warning level, 0 critical failures
- PROPOSED-3DP-003 [minor]: warn — sharp 90° internal corners at shaft/web intersections (expected: fillets are deferred project-wide; not a defect for v1)
- PROPOSED-GEN-001 [minor]: warn — sharp 90° external edges on shaft ends and web OD (same project-wide fillet deferral)
- Note: evaluator ran with process=CNC_milling; constraints.md names CNC_turning primary + CNC_milling secondary. No finding hinged on the difference.

### Visual Observations
- FRONT_WIREFRAME: Two tall thin vertical rectangles (webs, edge-on, full ⌀100 height, ~10 wide) with a horizontal rectangle protruding left and right at mid-height (journals, ~30 tall, ~25 long — journal length ≈ 2.5x web width by pixel ratio, matching 25:10). Between the webs the crank-pin region is clearly OFFSET upward (+X): its outer edge sits just inside the web top edge and its inner edge is a horizontal line above the centerline. Pixel-measuring against the ⌀100 web height, the pin spans ≈ X=+11 to X=+49 — i.e., center +30, ⌀38, outer extremity 49 < web radius 50. Silhouette is continuous — pin meets both web faces with no gap.
- FRONT_CLEAN: Same silhouette as wireframe (no internal features on this part), confirming external shape only.
- TOP_WIREFRAME: Large outer circle (⌀100 web), small solid concentric circle at exact center (⌀30 journal), and one dashed hidden-line circle offset to the RIGHT (+X). Hidden circle center measures ≈ 29-30 mm off the main axis with radius ≈ 19, right extremity just inside the web outline — this is the crank pin at throw 30, ⌀38.
- TOP_CLEAN: Only the ⌀100 web circle and centered ⌀30 journal circle; the hidden pin correctly disappears without hidden lines.
- RIGHT_WIREFRAME: As pre-warned by the designer, the throw is edge-on along X in this projection, so the pin region between the webs appears vertically CENTERED — and is visibly TALLER (⌀38) than the journals (⌀30), which is the correct signature for this view. Not evidence of a centering error.
- RIGHT_CLEAN: Same centered-pin silhouette; consistent.
- ISO_WIREFRAME: Stacked circular discs (two webs + journals) on a common axis; a distinct small cylinder end visible OFFSET from the journal circle — the crank pin end face offset from the main axis. Hidden dashed circles show the pin and journal passing through the webs.
- ISO_CLEAN: Web discs and journal cylinder plus the offset pin end face clearly visible as a separate circle displaced from the journal — offset construction confirmed in 3D.
- NOT visible: the 1 mm internal embed overlaps (by design — internal only); no fillets visible anywhere (correct per policy).

### Findings
- [ok] Geometry: single-throw crankshaft topology correct — journal | web | offset pin | web | journal along Z
- [ok] Dimensions: bbox exactly 100 x 100 x 92 (⌀100 x 92 spec); dimension_checker PASS with zero deviations
- [ok] Feature — main journals: two ⌀30 x 25 journals coaxial on Z (code Z -46..-21 and +21..+46; top view shows exact-center ⌀30 circle; front view shows both stickouts)
- [ok] Feature — webs: two ⌀100 x 10 full discs (front view pixel ratio 10:25 vs journal length; full discs are per-plan v1, not flagged)
- [ok] Feature — crank pin: ⌀38 at 30.0 offset (pixel-verified ≈ 30 in top view, span 11..49 in front view); free span between web inner faces exactly 22.0 (code: webs at Z ±11..±21, pin free span Z ±11)
- [ok] Connectivity: one connected solid — executor volume 217,373 mm³ matches analytic sum (2 webs 157,080 + 2 journals 35,343 + pin free span 24,953 = 217,376 mm³, Δ < 0.002%), which is only possible if the unions fused; pin has 1 mm embeds into each web guaranteeing overlap; front view silhouette continuous
- [ok] No fillets: none in code, DFM confirms sharp edges (per project deferral)
- [ok] Coordinate convention (Principle 0): revolved-dominant part with rotation axis on Z, centered at origin (Z ±46), pin axis parallel to Z through (30, 0, 0) — matches constraints.md convention section exactly
- [minor] DFMA warnings on sharp corners are the expected consequence of the fillet deferral — carry forward to the later fillet-optimization phase, no action now

### Recommendations
- None required for v1. For the later revision phase: add junction fillets (addresses both DFMA warnings) and counterweight cutouts on the +X web sides (balance), per the deferrals already recorded in constraints.md.

VALIDATION: PASSED
