# Goals — conveyor_shaft_unit

Design a two-bearing shaft support unit for a small industrial conveyor drive.
No input sketch: text brief only.
Size everything from the stated 40 mm shaft diameter and the 6208 catalogue envelope
(40 × 80 × 18 mm); anchor every other dimension on standard catalogue parts.

## Design brief (user's spec, verbatim)

Design a bearing support unit for a 40 mm steel shaft that drives a small industrial conveyor. The shaft turns at 1,500 rpm, carries a radial load of about 4 kN at the drive pulley and a light axial thrust of about 1 kN, and must run 20,000 hours between services. Support the shaft on two deep groove ball bearings, size 6208: one at the drive end located between a shaft shoulder and a circlip, one at the far end free to float axially by 1 to 2 mm. House both bearings in a single cast iron body with two in-line bores and a mounting foot with four bolt holes. Close the drive end with a bolted steel cover that carries a radial lip seal, held by four M8 bolts with wrench clearance. Use k6 fits on the shaft seats and H7 in the housing bores, 1 mm chamfers at every bearing shoulder, a minimum housing wall of 8 mm, and a grease nipple reachable from above. Deliver the parametric 3D model of every made part, the assembled unit, the bill of materials with catalogue parts, and the manufacturability and assembly review.

## Sizing guidance

- The shaft diameter (40 mm) and the 6208 envelope (bore 40, OD 80, width 18 mm) are fixed inputs.
- Bearings, circlip, lip seal, bolts and grease nipple are catalogue Buy parts:
  size the shaft seats, housing bores, cover and spacing around them, never the other way around.
- The drive-end bearing is axially located (shoulder + circlip); the far-end bearing floats 1 to 2 mm axially.
- Fits: k6 on shaft seats, H7 in housing bores (record them in constraints; the model carries nominal geometry).
- 1 mm chamfers at every bearing shoulder; minimum housing wall 8 mm; grease nipple reachable from above.
- Fillets are deferred project-wide; chamfers are required where the brief names them.

## Success criteria

- Every Make part modeled as parametric CadQuery code, validated with renders (8 views each),
  `notes.md` ending `VALIDATION: PASSED`, and a DFM report.
- A complete `assembly/assembly.py` placing every part (Make and Buy) in position,
  with assembly renders proving the stack fits.
- Interfaces consistent: bearing OD ↔ housing bores (two in-line bores, same axis),
  bearing bore ↔ shaft seats, shoulder + circlip location at the drive end,
  1 to 2 mm axial float at the far end, cover bolt pattern ↔ housing face, seal bore ↔ shaft.
- No interference between parts; wrench clearance at the four M8 cover bolts.
- `external/bom.md` listing every catalogue part (2 × 6208, circlip, lip seal, 4 × M8 bolts, grease nipple, and any others the plan adds).
- STEP (and STL) exports for every validated Make part.
- Manufacturability (DFM) and assembly (DFA) review recorded; reviewer verdict recorded.
