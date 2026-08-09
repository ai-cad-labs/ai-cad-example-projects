# notes — pinion (involute spur gear)

## Approach
Involute spur gear built from **point math**, not from CadQuery arc-stitching.
`.gear()` / `.involute()` do not exist; the golden `cylindrical_gear.py` arc-stitch
technique (parametricCurve + radiusArc + `.combine().wire()`) was tried first and
**failed to close the tooth wire** for these parameters ("outer wire is not closed"
at extrude). Switched to the robust primary method the constraints recommend: sample
each involute flank in Python, assemble one closed tooth as a `polyline().close()`,
rotate it z times, union, then union onto a hub disc and cut the bore.

## Key dimensions (all derived from m, z, alpha in the file)
- module m = 2, teeth z = 18, pressure angle = 20°, face width = 10mm
- pitch dia 36 · base dia 33.83 (r_base 16.914) · root dia 31 (r_root 15.5) · tip/OD 40 (r_addendum 20)
- No undercut: r_base (16.914) > r_root (15.5), so the flank is well-formed.
- Tooth centred on +X: right flank pitch point placed at −π/(2z) using inv(α)=t−atan(t);
  left flank is the mirror. Radial stubs bridge r_base→r_root (flank can't reach root).

## Bore — READ THIS (interface with `shaft`)
Bore modelled at **⌀8.2** (nominal ⌀8 + 0.2mm diametral slip-fit clearance), per
constraints.md line 25-26 which invites ~0.2mm print clearance for a functional slip
fit over the ⌀8 shaft OD. If the assembly/shaft convention expects a nominal ⌀8 bore
instead, set `bore_clearance_mm = 0.0`. Bore runs full 10mm along Z on the axis.

## Coordinate convention (Principle 0)
Revolved part, axis of revolution = Z, centred at origin. Built Z=0..10 then
`translate((0,0,-5))` → face width spans Z ∈ [−5, +5]. Bore axis = Z through origin.

## Verification
Executor: success, volume 9363.6mm³, bbox X/Y ≈ ±20 (OD 40), Z ±5 (face 10).
Renderer: 8 views, **zero dimensional deviations** (bbox 40/39.6/10 vs spec 40×40×10).
Top + iso renders visually confirm 18 clean involute teeth, rounded roots, tip lands,
and the central through-bore.

## For adjacent parts / assembly_resolver
- Tooth phase: tooth #0 is centred on +X (first tooth's centreline lies on the X axis).
  The mating `gear` must be phase-rotated by a half-tooth at assembly time to mesh.
- Mesh centre distance to `gear` = 48mm is an ASSEMBLY-TIME constraint — not modelled here.
- No fillets (root fillets deferred per project policy).

## Trade-offs / notes
- Union-in-a-loop of 18 extruded teeth (~0.9s exec) — clear and robust; fine at this scale.
- `flank_samples = 14` per flank gives smooth involute; raise for finer flanks if needed.

## Validation Report — 2026-07-21
- **Score**: 9/10
- **Volume**: 9363.64 mm^3
- **Bounding box**: -19.99..19.99 x -19.8..19.8 x -5.0..5.0 mm (OD ~40, face 10, centred on Z)

### DFMA Findings
- DFM-3DP-003 [minor/uncertain]: feature-size check returned `uncertain` — evaluator could not confirm tooth-tip land >= 0.5mm because renders carry no dimensional scale. RESOLVED by dimensional grounding: for a module-2, 20 deg PA, 18-tooth gear the tooth-tip land = 20*[3.1416/18 + 2*(inv20 - inv(alpha_a))] ~ 1.36mm >> 0.5mm; root spacing is larger still. Feature size is safe.
- All other DFM rules PASSED (5/5, including both critical rules). Overall evaluator verdict: conditional_pass — no critical or major failures; only the scale-limited uncertain above. Report at dfma_report.json.

### Visual Observations
- TOP_CLEAN: face-on view down Z shows a spur gear with 18 evenly-spaced, well-formed involute teeth (rounded valleys, defined tip lands) and a single concentric central circular bore. No missing/merged teeth, no interpenetration.
- TOP_WIREFRAME: same 18-tooth silhouette plus the inner bore circle; outline closed and clean.
- ISO_CLEAN: 3D view — teeth extrude cleanly through the full face width; central bore visible as a through-hole. Solid, coherent gear blank.
- ISO_WIREFRAME: hidden geometry (far-side teeth, far bore edge) rendered as grey/dashed lines — correct hidden-line behaviour, NOT broken geometry or interpenetration.
- FRONT/RIGHT CLEAN + WIREFRAME: edge-on side profile is a ~4:1 tall-narrow rectangle (OD ~40 tall x face 10 wide); horizontal white lines = tooth tip/root and bore edges; dashed grey lines in wireframe = hidden bore/back edges. Consistent across both orthographic pairs.

### Findings
- [ok] Geometry: involute spur gear, topology correct; 18 teeth present and well-formed.
- [ok] Dimensions: dimension_checker PASS — expected [10, 40], actual [10, 39.6, 40]. Y 39.6 vs 40 is expected from even-tooth angular placement (tooth #0 on +X lands tip lands on the X axis, so X spans full OD; Y falls between tips). Within tolerance.
- [ok] Features: 18 involute teeth + central through-bore all present. No fillets (correctly deferred per policy).
- [ok] Bore: modelled at ⌀8.2 (nominal ⌀8 + 0.2mm slip-fit clearance) — deliberate print clearance per constraints, NOT a defect.
- [ok] Coordinate convention (Principle 0): revolved part, axis of revolution on Z, cross-section centred at origin, face width Z in [-5, +5], bore axis on Z through origin. Correct.
- [ok] Manufacturability: min wall (bore-to-root) = 11.5mm; tooth-tip land ~1.36mm; both well above 0.8mm / 0.5mm 3D-print thresholds.

### Recommendations
- None blocking. The DFM `uncertain` is resolved above; no repair needed. Part is ready for assembly (half-tooth phase rotation of the mating `gear` is an assembly-time concern, not a part defect).

VALIDATION: PASSED
