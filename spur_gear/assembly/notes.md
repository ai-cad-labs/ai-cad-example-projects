# Assembly Validation Report — 2026-07-21

- **Subject**: ASSEMBLY at projects/spur_gear/assembly
- **Score**: 10/10
- **Volume**: 39739.02 mm^3
- **Bounding box**: -19.99..79.89 x -32.0..32.0 x -15.0..15.0 mm
- **Execution**: SUCCESS (Compound, 1.1s)
- **Renders**: 8 colored PNGs + color_legend.txt written to assembly/renders/

### Color legend
- pinion = red | gear = blue | shaft_pinion = green | shaft_gear = orange

### Visual Observations
- TOP_CLEAN: small red pinion (left) + large blue gear (right); the two share a
  common tooth size at the mesh line (same module 2). The red pinion's rightmost
  tooth enters a blue-gear GAP and the blue tooth enters a red gap — clean interlock.
  A green ring sits concentric at the pinion center; an orange ring concentric at
  the gear center (the two bores, each holding a shaft).
- TOP_WIREFRAME: same picture with hidden edges; tooth flanks interleave at the
  tangent line, no solid overlap. Tooth counts consistent with 18T (red) / 30T (blue).
- ISO_CLEAN: both gear discs occupy the SAME axial band (coplanar / same Z), teeth
  interlocking. Green shaft passes through the pinion bore (red bore ring around it);
  orange shaft passes through the gear bore (blue bore ring around it). Both shafts
  protrude symmetrically past both gear faces → shaft (30) longer than face (10),
  centered on the bore axis.
- ISO_WIREFRAME: confirms the shafts are cylinders coaxial with each gear's bore;
  no cross-part interpenetration between gear bodies and the wrong shaft.
- FRONT/RIGHT (edge-on ortho): unusual projection orientation — the gears project
  onto/behind one another and read as stacked colored bars crossed by the shaft
  rings. Ambiguous edge-on artifact; not used as a fail basis (gear anti-false-
  positive discipline). The decisive top + iso views are clean.

### Interface / Fit Assessment
- [ok] Mesh — pinion + gear teeth INTERLOCK without interpenetration. Ground-truthed
  against the resolver's Z=0 section-interference test: phase 0° = 18.04 mm^2 overlap,
  phase -6° = 0.00 mm^2 (clean). assembly.py applies PHASE_DEG = -6.0 on the gear.
- [ok] Centre distance = 48.0 mm — pinion at origin, gear at x=48 (cq.Location).
  Bbox corroborates: xmin -19.99 (pinion OD r~20 at origin) to xmax 79.89
  (gear at 48 + OD r~32 = 80). y extent ±32 = gear OD r32. z ±15 = shaft half-length.
- [ok] Pitch circles tangent — pinion pitch r18 (⌀36) reaches x=18; gear pitch r30
  (⌀60) reaches x = 48-30 = 18. Tangent on the centre line at x=18.
- [ok] Coplanar — both gears placed with identical Z; iso view confirms same axial band.
- [ok] Same module at mesh — red and blue teeth are visibly the same size at the
  tangent line (necessary meshing condition).
- [ok] Shaft_pinion (green) coaxial through pinion bore at origin (no XY translate).
- [ok] Shaft_gear (orange) coaxial through gear bore at gear centre (x=48).
- [ok] Parts loaded unmodified via load_part(); geometry not re-derived in the assembly.

### Findings
- [ok] Geometry: meshing spur-gear pair on two parallel shafts, exactly per goals.md.
- [ok] Assembly executes and renders 8 colored views + legend.
- [ok] No interference — analytic (0.00 mm^2) + multi-view visual agree.

### Recommendations
- None blocking. Optional: goals.md/design_plan cite bore ⌀8; part comments note the
  designer added ⌀8.2 print clearance on the bore — intentional slip fit, consistent
  with the stated "~0.2mm print clearance may be added." No action needed.

VALIDATION: PASSED
