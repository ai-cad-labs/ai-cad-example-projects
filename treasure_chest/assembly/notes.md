# Assembly Notes — treasure_chest

## Validation Report — 2026-07-21
- **Score**: 9/10
- **Volume**: 380768.35 mm^3
- **Bounding box**: -90..90 x -64..85 x 0..140 mm (X x Y x Z)

### Color Legend (for findings)
- base: red · lid: blue · hinge_block_left: green · hinge_block_right: orange · hasp_plate: purple

### Interface / Fit Assessment (ground-truthed against part bboxes + assembly offsets)
- **Base**: local bbox X-90..90, Y-60..60, Z0..80 → 180x120x80, hollow open-top box. OK.
- **Lid**: local bbox 180x120x60, flat-face-down half-cylinder (footprint 120 wide, dome to Z=60). Placed at Z=80 → occupies Z80..140, footprint matches base 180x120, seated flat on top rim Z=80. OK. (The half-disc appears rotated in the right/front projections — that is the renderer's in-plane orientation, NOT a geometry fault; local bbox confirms flat-down.)
- **Hinges**: both at rear (assembled Y 60..85, external to rear wall), X=-50 / X=+50 (symmetric, confirmed in TOP view), Z 65..95 bridging the base/lid seam at Z=80, pin bore at Z=80 along X. OK.
- **Hasp**: centered front (X-20..20 @ X=0), Y -64..-60 against front face, Z 52..102 straddling the seam. OK.
- **Latch alignment (the just-corrected feature)**: hasp latch hole local Z=34 + offset 52 = **assembled Z=86**; lid latch hole local Z=6 + offset 80 = **assembled Z=86**, both X=0 on the front face → **holes are coaxial/aligned**. Correction landed. (NOTE: assembly.py's inline comment still says "lands at Z=94 / 8mm miss" — that comment is STALE; the hasp part.py now uses latch_hole_z=34.0.)

### Visual Observations
- ISO_CLEAN/WIREFRAME: reads as a coherent treasure chest — red open-top box, blue domed half-cylinder lid on top spanning full length, green+orange hinge blocks on the rear top corners bridging the seam, purple hasp on the front bridging the seam. No colors occupying the same space.
- TOP_CLEAN: base & lid rectangles overlap (matching 180x120 footprint); hinge blocks symmetric at rear X=±50; hasp centered on front edge. XY layout correct.
- FRONT_WIREFRAME: hinge mount holes render as circles, pin bores as hidden dashes; hasp latch hole (large ⌀6) sits on the lid/base seam line at center — consistent with X=0, Z=86.
- RIGHT_CLEAN: lid half-disc profile + base rectangle + external hinge/hasp; no cavity intrusion.

### Findings
- [ok] Geometry: base hollow open-top box, lid domed half-cylinder — both correct topology.
- [ok] Fit: lid seats on base top rim Z=80; footprints match 180x120.
- [ok] Hinges: 2 blocks, rear top edge, X=±50, pin axis Z=80, bridge base+lid.
- [ok] Hasp: centered front, straddles seam; latch hole aligns with lid latch (both Z=86, X=0).
- [ok] No wild interpenetration — hinges & hasp mount external; lid/base meet flush at Z=80.
- [minor] assembly.py comment about the latch Z=94 mismatch is stale (not a geometry defect; safe to clean up).
- [deferred] DFM-3DP-002 horizontal-bore overhang (hinge pin bore, lid latch) — documented/accepted per dispatch; NOT counted against this assembly.

### Recommendations
- Optional: update the stale hasp-latch comment block in assembly.py to reflect the Z=86 correction (documentation only).

VALIDATION: PASSED
