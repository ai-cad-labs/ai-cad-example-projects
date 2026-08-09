# Design Notes: piston

**Status**: part.py executes clean (volume 67,114 mm³ ≈ 181 g in Al 6061), bbox exactly ⌀60 x 55 centered on origin, dimension check PASS, all 8 renders visually verified.

## Approach

Adapted cookbook Pattern 10 (feature-decomposed piston), built as a subtractive sequence that reads like the CNC process plan: turn blank → bore stepped interior (protecting boss volumes) → turn 3 ring grooves → line-bore the pin bore. Bosses are kept by subtracting their solids from the cavity CUTTER (cutter = cavity − bosses) rather than unioning afterward — this guarantees the bosses stay fused to the crown and can never leave slivers inside the grooves.

## Coordinate frame (per constraints.md)

Piston axis = Z, centered at origin. Crown top Z=+27.5, skirt bottom Z=-27.5. Gudgeon-pin bore along **X** through (0, 0, **-4.5**) — compression height 32.0 from crown top.

## Key dimensions (as built)

- OD 60.0, height 55.0, crown 8.0 solid flat
- Grooves: 2.6 axial x 3.0 radial (root ⌀54.0) at 5.0–7.6, 10.6–13.2, 16.2–18.8 below crown top (Z bands 22.5–19.9, 16.9–14.3, 11.3–8.7)
- Bosses: inner faces at x=±11.0 (gap 22.0), outer faces at x=±24.0 (span 48.0), boss ⌀26 around bore, each hung from the crown underside by a 24 mm-wide web
- Pin bore: ⌀16.02 through, along X, cutter spans only ±25.0 — physically cannot touch the skirt wall (which starts at radius 27) → bore does NOT break skirt OD
- Skirt inner ⌀54.0 (3.0 mm wall) below Z=+5.7

## DISCOVERED CONSTRAINT — ring-belt wall (deviation, deliberate)

The literal constraints are geometrically infeasible in combination: interior hollowed to ⌀54 immediately below the 8 mm crown + groove root ⌀54 ⇒ **zero wall behind grooves 2 and 3** (10.6–18.8 below crown, i.e. below the crown underside at 8.0). Cutting those grooves would remove the full 54→60 annulus and sever the piston into two disconnected bodies.

**Resolution (how real pistons are built)**: stepped interior. Behind the ring belt the cavity is **⌀47.0** (3.5 mm wall behind the 3.0 mm-deep grooves ≥ 3.0 min-wall rule); the full ⌀54 skirt hollow starts at Z=+5.7 (= 3.0 mm below the bottom of groove 3). Everything the interfaces depend on is untouched: skirt inner is ⌀54 at the pin level (50 mm pin fits inside), grooves are exactly per spec, boss spacing/span exact. Parameter: `ring_belt_inner_dia = 47.0` in part.py.

## Design details adjacent parts should know

- **piston_ring**: grooves exactly per plan — 2.6 axial x 3.0 radial deep, root ⌀54.0, working OD 60.0. Groove positions as listed above. Rectangular profile, sharp corners (no fillets).
- **gudgeon_pin**: bore is ⌀16.02 through both bosses; boss outer span 48.0, so a 50 mm pin protrudes 1.0 mm past each boss outer face into open cavity (cavity radius there is 27 → clears). Bore ends at the boss outer faces; nothing retains the pin axially (no circlip grooves in v1 — full-floating, retention unmodeled).
- **connecting_rod**: 22.0 mm clear between boss inner faces (flat faces at x=±11.0, normal to pin axis). Small end (20.0 wide) has 1.0 mm per side. Clear swing space below the bosses down the open skirt.
- Bosses do NOT touch the skirt inner wall (outer face x=24 < inner wall radius 27); they hang from the crown underside via rectangular webs (24 wide in Y, from pin axis up to Z=+19.5). This matches "bore ends inside skirt inner wall".

## Trade-offs / potential issues

- Sharp internal corners everywhere (fillets deferred project-wide) — stress risers at boss-web-to-crown junctions; flag for the fillet phase.
- Web-to-boss union has near-tangent geometry avoided deliberately: web width 24 < boss ⌀26 so the union is transversal, and ring-belt cavity ⌀47 (not ⌀48) avoids a tangent plane/cylinder boolean at the boss outer face — keep these margins if editing.
- CNC note: the stepped internal bore + internal bosses require machining from the open skirt end; grooves finish-turned per constraints.

## Validation Report — 2026-07-13
- **Score**: 7/10
- **Volume**: 67114.33 mm^3
- **Bounding box**: -30.0-30.0 x -30.0-30.0 x -27.5-27.5 mm

### DFMA Findings
- DFM-GEN-002 [critical]: FAIL — region inside the cavity directly above the pin bosses is inaccessible to milling tools entering from the open skirt bottom (undercut above bosses; boss ⌀26 overhangs the 24 mm-wide hanger web by 1 mm per side in Y, leaving pockets under the crown that have no straight-line tool path from below)
- DFM-CNC-004 [major]: FAIL — same undercut region, flagged against the 3-axis end-mill accessibility rule; recommendation from tool: extend the boss/web material fully up to the cavity ceiling with no overhang
- 10/16 rules passed; 4 warnings are PROPOSED-* rules about sharp edges/corners — these overlap the project-wide "no fillets" policy and are informational only, not held against the part
- Full report: dfma_report.json (written by evaluator)

### Placeholder Check
- [ok] placeholder_detector: "looks like a real design" — genuine implementation

### Execution
- [ok] part.py executes clean: Workplane result, 194.7 ms, volume 67,114.33 mm³, bbox exactly 60 x 60 x 55 centered at origin (Z -27.5 to +27.5)

### Visual Observations
- FRONT_CLEAN: I see a horizontal-axis cylinder silhouette (render orientation puts the piston axis horizontal, crown at left). From the left: one wider band, then two narrower bands, separated by three recessed gaps where the silhouette height steps down, then the long skirt rectangle. That is three distinct grooves cut to a reduced diameter, with the first land visibly wider than the two inter-groove lands (consistent with 5.0 top land vs 3.0 lands). The OD silhouette is unbroken — no hole appears anywhere on the outline.
- FRONT_WIREFRAME: hidden (dashed) lines show a stepped internal cavity — a narrower dashed bore under the ring-belt region and a wider dashed bore through the skirt, stepping at a point below the last groove. Two dashed rectangular clusters sit symmetrically about the axis at the pin level with solid gray boss outlines — the two pin bosses with bore lines running through them. The crown end shows a solid (un-hollowed) band.
- TOP_WIREFRAME: outer black circle (OD), a solid gray inner circle (skirt inner bore, ≈90% of OD ⇒ ⌀54-class), a dotted smaller circle (the ⌀47 ring-belt cavity), and two rectangular boss outlines on the left/right (X axis) with dashed bore edges. Both boss rectangles terminate clearly inside the gray inner circle — bosses do not reach the skirt wall.
- TOP_CLEAN: a single clean circle. Nothing else — confirms no feature penetrates the OD.
- RIGHT_WIREFRAME: viewed along the pin axis, I see a solid gray horseshoe/circular outline (boss ⌀26) with a dotted concentric circle inside it (the ⌀16-class bore), centered on the piston centerline, positioned in the crown half of the body at roughly the expected compression height. Bore circle is entirely internal (dotted = hidden), well clear of the OD silhouette.
- RIGHT_CLEAN: unbroken rectangle-with-groove-bands silhouette; no bore visible from the side ⇒ no OD breakout.
- ISO_CLEAN: cylinder with a distinct 3-ring groove belt near one end; the far face is a clean circle. Grooves read as three separate dark rings.
- ISO_WIREFRAME: dense hidden-line detail of the internal bosses, webs, bore, and stepped cavity visible through the open skirt end.
- NOT directly measurable in views: exact groove axial 2.6 / depth 3.0 values and the 22.0/48.0 boss spacings — verified from part.py derived values + execution bbox instead (see Findings).

### Findings
- [ok] Geometry: correct piston topology — solid flat crown, 3-groove ring belt, hollow skirt, two internal pin bosses hung from the crown
- [ok] Features/grooves: three rectangular grooves, 2.6 axial x 3.0 radial (root ⌀54.0), Z-bands 5.0–7.6, 10.6–13.2, 16.2–18.8 below crown (code: groove bands 22.5–19.9, 16.9–14.3, 11.3–8.7 in Z) — matches constraints exactly; 3 grooves confirmed visually in FRONT_CLEAN and ISO_CLEAN
- [ok] Features/bosses: inner faces at x=±11.0 (gap 22.0), outer faces at x=±24.0 (span 48.0), through ⌀16.02 bore along X at Z=-4.5 = compression height 32.0 from crown top — matches constraints; bosses and bore confirmed in TOP_WIREFRAME and RIGHT_WIREFRAME
- [ok] No breakout: bore cutter spans ±25.0 < skirt inner radius 27.0; TOP_CLEAN and RIGHT_CLEAN silhouettes show zero OD penetration
- [ok] Dimensions: dimension_checker PASS — expected [55.0, 60.0], actual [55.0, 60.0, 60.0], no deviations
- [ok] No fillets anywhere (project policy honored); no threads
- [ok] Coordinate convention (Principle 0): revolved-dominant part on Z axis, centered at origin, crown +27.5 / skirt -27.5, pin bore through (0,0,-4.5) — per constraints.md
- [ok] ACCEPTED DEVIATION (per task + prior notes above): stepped interior ⌀47 behind the ring belt instead of full ⌀54 hollow — required to keep ≥3 mm wall behind grooves 2–3; all interface dimensions (grooves, bosses, bore, skirt inner ⌀54 at pin level) untouched. Not held against the part.
- [critical] DFMA DFM-GEN-002: tool-access undercut above the pin bosses (see DFMA Findings). Per validation policy, a critical DFMA failure fails the part regardless of visual/dimensional correctness. This is the SOLE failure — every geometric, dimensional, and feature check passes.

### Recommendations
- Eliminate the undercut above the bosses: widen the hanger web so no boss material overhangs it — e.g., set `web_width = 28.0` (> boss_od 26.0). Note part.py's own caveat: web 24 < boss ⌀26 was chosen to avoid a TANGENT boolean; going WIDER than the boss (28 > 26) keeps the union transversal while removing the 1 mm overhang lip, so it respects the same margin rule from the other side. Verify the wider web still clears the ⌀47 ring-belt cavity wall (28/2 = 14 < 23.5 ⇒ clears).
- Alternatively, extend each boss/web as a full prismatic block from the boss bottom up to the crown underside across the boss's full Y extent, ensuring straight-line access from the open skirt end for everything else.
- After the fix, re-run `tools.dfma_evaluator --mode=dfm` to confirm DFM-GEN-002 and DFM-CNC-004 clear; geometry and dimension checks need no changes.
- Context for orchestrator/repair: the flagged undercut is small (1 mm lips) and real pistons carry such geometry via casting/forging before machining — if the CNC_milling-only process assumption is revisited, this finding may warrant a rule-severity review. For now it governs.

VALIDATION (superseded): FAILED

## Repair attempt 1 — 2026-07-13

**Targeted**: DFM-GEN-002 [critical] + DFM-CNC-004 [major] — tool-access undercut in the cavity directly above the pin bosses.

**Root cause**: single parameter, not a structural flaw. `web_width = 24.0 < boss_od = 26.0` in `pin_boss_solids()` meant the boss cylinder's upper half overhung its hanger web by 1.0 mm per side in Y, leaving pockets under the crown with no straight-line tool path from the open skirt bottom. (The 24 < 26 choice was deliberate in the fresh design — to avoid a tangent boolean — but it created the undercut.)

**Change** (in `part.proposal.py`, ONLY the failing feature function's parameter + comments; Pattern-10 structure preserved):
- `web_width: 24.0 → 28.0` (> boss ⌀26). The boss cylinder's entire upper half is now embedded in the web, so no material overhangs anything viewed from below — the undercut is gone. The union stays TRANSVERSAL from the wide side (web ±14 vs boss r 13, 1 mm margin — same anti-tangency margin as before, approached from the other side, per the validator's own recommendation).

**Geometry verified**:
- Executes clean: 165.7 ms, volume 68,917.28 mm³ (was 67,114.33; +1,803 mm³ = the added web material, all internal), bbox exactly 60 x 60 x 55 centered at origin. dimension_checker PASS.
- 28/2 = 14 < 23.5 (⌀47 ring-belt cavity radius) — web does not blank the ring-belt cavity.
- SECOND-ORDER effect (checked deliberately): web corners at (x=24, y=±14) sit at radius 27.78 > 27, so over Z −4.5…+5.7 (the ⌀54 skirt zone) the web corners now merge into the skirt inner wall. This is PERMITTED — constraints.md says "boss OD ~26 mm blending into skirt" — and the plane-vs-cylinder intersection is transversal (~31°, no tangency, no slivers). The earlier notes line "bosses do NOT touch the skirt inner wall" now holds for the boss cylinders/outer faces but NOT for the web corners; the LOCKED requirement ("pin bore does not break through skirt OD"; 50 mm pin inside the skirt) is untouched — bore cutter still spans only ±25 < 27.
- Renders (all 8 PNGs read): RIGHT_WIREFRAME shows the boss arc protruding only BELOW the web, web sides just outside the arc rising straight to the crown — no overhang. TOP_WIREFRAME shows web rectangles as the outermost boss contour with dashed boss/bore edges inside. TOP_CLEAN/RIGHT_CLEAN: zero OD penetration. FRONT: 3 grooves at unchanged positions.

**Constraints verified after the change** (all of constraints.md, not just the flagged issue): OD 60 / height 55 / crown 8 solid flat — unchanged. Grooves 2.6 x 3.0, root ⌀54, bands 5.0–7.6 / 10.6–13.2 / 16.2–18.8 below crown — untouched code path. Boss inner gap 22.0 / outer span 48.0 / bore ⌀16.02 along X at Z=−4.5 (compression height 32.0) — untouched. Stepped interior ⌀47/⌀54 (accepted deviation) — untouched. Min wall 3.0 — walls only got thicker. NO fillets added. Coordinate convention unchanged (Z axis, origin-centered).

**DFM regression posture**: fixes critical (−10) + major (−5); no rule that currently passes is plausibly regressed (walls thicker → CNC-001/006 safer; cavity ratio, bore ratio, symmetry, deburring unchanged). Probationary teardrop/fillet/chamfer failures deliberately NOT touched (project policy).

**Next**: orchestrator runs the DFM gate (`promote_or_reject_proposal`), then re-validate.

## Validation Report — 2026-07-13 (RE-VALIDATION after promoted repair: web_width 24 → 28)
- **Score**: 9/10
- **Volume**: 68917.28 mm^3
- **Bounding box**: -30.0-30.0 x -30.0-30.0 x -27.5-27.5 mm

### DFMA Findings
- Fresh DFM run this validation: verdict **conditional_pass**, 18 rules evaluated, 13 passed, **0 active failures** (`failures: []`) — DFM-GEN-002 [critical] and DFM-CNC-004 [major] from the first validation are CLEARED. Consistent with the pre-recorded eval in dfma_report.json/attempt_log.json (no stochastic disagreement).
- 5 warnings, all PROPOSED-* (probationary, informational): PROPOSED-3DP-001 (no teardrop bore — part is CNC, not 3DP), PROPOSED-3DP-003 (sharp cavity corners), PROPOSED-GEN-001 (sharp skirt/bore edges), PROPOSED-CNC-001 (sharp vertical internal corners at boss-face/skirt-wall intersections — end-mill radius note; flag for the deferred fillet phase), PROPOSED-ASSY-003 (no pin-bore lead-in chamfer). None held against the part; edge-break/fillet work is deferred project-wide.
- Tool anomaly (non-blocking): the evaluator's second inner LLM pass (engineering_domain) errored with `pydantic_ai.exceptions.UnexpectedModelBehavior: Model token limit (8192) exceeded before any response was generated. Increase the max_tokens model setting, or simplify the prompt to result in a shorter response that will fit within the limit.` The tool still exited 0 with a valid verdict from the manufacturing_technique pass (success: true). Infrastructure note for the orchestrator, not a part defect.
- Full report: dfma_report.json (rewritten by this run's evaluator).

### Placeholder Check
- [ok] placeholder_detector: "looks like a real design"

### Execution
- [ok] part.py executes clean: Workplane result, 142.9 ms, volume 68,917.28 mm³ (matches the promoted proposal's recorded volume exactly — confirms I validated the repaired geometry), bbox exactly 60 x 60 x 55 centered at origin (Z −27.5 to +27.5)

### Visual Observations
- FRONT_WIREFRAME (axis horizontal, crown/ring belt at left): silhouette shows 3 narrow bands separated by recessed gaps at the left end, then the long skirt body. Hidden lines: a large dashed rectangle through the skirt (⌀54 hollow) stepping to a narrower dashed region under the ring belt (⌀47 cavity), and a solid crown band at the far left with no hidden lines through it. Two hidden boss/web clusters sit symmetrically top and bottom (bosses at ±X), each connected by lines running to the crown-underside line; both clusters terminate inside the dashed skirt-inner boundary — nothing reaches the outer silhouette.
- FRONT_CLEAN: unbroken outline; from the left one visibly wider band (5.0 top land) then two narrower equal bands (3.0 lands) — no hole or breakout anywhere on the OD silhouette.
- TOP_WIREFRAME: outer black ⌀60 circle; solid gray circle just inside (⌀54 skirt inner); dashed circle inside that (⌀47 ring-belt cavity); two rectangular boss/web blocks left and right on the X axis with dashed boss/bore edges inside them and a clear gap between their inner faces at center. The blocks' outer corners touch the gray ⌀54 circle — this is the web-corner merge into the skirt inner wall (ACCEPTED DEVIATION 2, constraint-sanctioned "blending into skirt"). Blocks stay well inside the black OD circle.
- TOP_CLEAN: a single clean circle — flat crown, zero OD penetration from above.
- RIGHT_WIREFRAME (viewed along the pin axis; crown/ring belt at right): dashed bore circle (⌀16-class) on the piston centerline, positioned skirt-side of mid-length consistent with compression height 32 of 55. **NEW CHECK — boss vs web**: the solid-gray boss arc (⌀26-class) is visible ONLY as the lower/skirt-side horseshoe around the bore; on the crown side the web's straight edges run just OUTSIDE the boss arc and rise unbroken to the cavity ceiling. There is no re-entrant notch or pocket line between the top of the boss arc and the crown underside — the boss no longer overhangs its web; boss material protrudes only BELOW the web. Confirmed.
- RIGHT_CLEAN: unbroken banded silhouette; no bore visible from the side ⇒ no OD breakout.
- ISO_WIREFRAME: dense hidden-line detail of both bosses, webs, through-bore and stepped cavity seen through the open skirt end; ring-groove stack reads as tight parallel rings.
- ISO_CLEAN: clean cylinder with the 3-ring groove belt near one end; far face is an unbroken circle.
- NOT directly measurable in views: exact 2.6/3.0 groove values and 22.0/48.0 boss spacings — verified from part.py parameters/derived values + execution bbox (see Findings).

### Findings
- [ok] Geometry: correct piston topology — solid flat 8 mm crown, 3-groove ring belt, hollow skirt, two internal pin bosses hung from the crown by webs
- [ok] Grooves: three rectangular grooves 2.6 axial x 3.0 radial, root ⌀54.0, at 5.0–7.6 / 10.6–13.2 / 16.2–18.8 below crown top (code Z-bands 22.5–19.9 / 16.9–14.3 / 11.3–8.7) — per constraints; 3 grooves confirmed in FRONT_CLEAN + ISO_CLEAN
- [ok] Bosses/bore: inner gap 22.0 (faces x=±11.0), outer span 48.0 (x=±24.0), through ⌀16.02 bore along X at Z=−4.5 = compression height 32.0 — per constraints; confirmed in TOP_WIREFRAME + RIGHT_WIREFRAME
- [ok] NEW CHECK — no undercut above bosses: web_width 28.0 > boss ⌀26; RIGHT_WIREFRAME shows the boss arc only below the web, web edges outside the arc rising straight to the cavity ceiling — no pocket between boss top and crown (DFM-GEN-002/DFM-CNC-004 fix visually confirmed AND confirmed by fresh DFM 0-active-failure run)
- [ok] No OD breakout: bore cutter spans ±25.0 < skirt inner radius 27.0; TOP_CLEAN and RIGHT_CLEAN show zero OD penetration
- [ok] Dimensions: dimension_checker PASS — expected [55.0, 60.0], actual [55.0, 60.0, 60.0], no deviations; overall ⌀60 x 55 exact
- [ok] No fillets, no threads (project policy honored)
- [ok] Coordinate convention (Principle 0): revolved-dominant part, axis on Z, centered at origin, crown +27.5 / skirt −27.5, pin bore through (0,0,−4.5)
- [ok] ACCEPTED DEVIATION 1: stepped interior — ⌀47 cavity behind ring belt, ⌀54 skirt hollow below Z=+5.7 (documented constraint-infeasibility resolution). Not held against the part.
- [ok] ACCEPTED DEVIATION 2: web corners (x=±24, y=±14, radius 27.78) merge into the ⌀54 skirt inner wall over Z −4.5..+5.7 — intentional, constraint-sanctioned ("boss OD blending into skirt"); visible as the block corners touching the gray ⌀54 circle in TOP_WIREFRAME. Not held against the part.
- [minor] PROPOSED-* warnings (sharp edges, no lead-in chamfers, internal corner radii for end mills) — deferred to the project-wide fillet/edge-break phase; informational only

### Recommendations
- None blocking. For the future fillet/edge-break phase: pin-bore lead-in chamfers (PROPOSED-ASSY-003), skirt bottom edge break (PROPOSED-GEN-001), and internal corner radii ≥ end-mill radius at boss-face/skirt-wall junctions (PROPOSED-CNC-001).
- Orchestrator note: dfma_evaluator's engineering_domain inner pass hit an 8192 max_tokens limit (see DFMA Findings) — worth raising the eval model's max_tokens; does not affect this verdict.

VALIDATION: PASSED
