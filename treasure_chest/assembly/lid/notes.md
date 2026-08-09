# Lid — design notes

## Approach
Half-cylinder shell (barrel lid), flat face DOWN, hollow ~3 mm, closed at both
ends, open only on the flat underside so it caps the open base.

**Build method (box-cut, most robust of the two hinted options):**
1. Outer solid cylinder along X: `Workplane("YZ").circle(60).extrude(180)`.
2. Inner cylinder inset 3 mm at each end (`workplane(offset=3).circle(57).extrude(174)`)
   cut from outer → 3 mm shell wall + 3 mm solid semicircular END CAPS at X=±90.
3. Translate −90 in X to centre on the axis.
4. Cut everything below Z=0 with a large box → keep the UPPER half only.

Result: flat bottom at Z=0 open, arch peak at Z=60, two long lower rims at Y=±60
seat on the base top rim. Verified in right_wireframe (inner cavity shows as dashed
hidden semicircle → hollow confirmed).

## Key dimensions
- Local bbox EXACTLY 180 (X) × 120 (Y) × 60 (Z), origin-centered on XY, flat bottom Z=0.
- Outer R 60, inner R 57 (3 mm wall). Volume 129 739 mm³. Executes clean (~160 ms).

## Interface features (LOCAL frame; assembled Z = local Z + 80)
- Hinge pilot holes: 4 blind holes ⌀2.5 × 2 mm deep on the +Y (rear) flank at
  local Z=8, X ∈ {−58,−42,42,58} (two clusters @ X=±50, 16 mm spacing). Drilled
  along −Y into the curved flank. Depth measured into the wall from the outer
  surface (surface Y at Z=8 = √(60²−8²)=59.46; hole bottom at Y=57.46 → 2 mm,
  stays inside the 3 mm wall, does not break through to the cavity).
- Latch through-hole: ⌀6 at X=0, local Z=6, through the FRONT (−Y) shell wall only.
  Cutter length capped so it exits into the cavity and does NOT pierce the rear wall.

## Deviations
- Pilot/latch holes sit on the CURVED flank (as spec'd) rather than a flat face, so
  their mouths are slightly elliptical on the surface — acceptable for self-tapping
  pilots and a padlock latch; both are geometrically within the wall as required.
- No fillets (deferred project-wide).

## For adjacent parts
- Seat: flat bottom (local Z=0) → assembled Z=80, footprint 180×120 matches base rim.
- hinge_block upper flange ⌀3.2 clearance holes mate to these ⌀2.5 pilots at
  assembled Z=88, X∈{−58,−42}/{42,58}.
- hasp_plate ⌀6 latch hole aligns to this ⌀6 through-hole at assembled Z≈86, X=0, Y=−60.

## Validation Report — 2026-07-21
- **Score**: 9/10
- **Volume**: 129739.17 mm^3
- **Bounding box**: -90 to 90 x -60 to 60 x 0 to 60 mm (180 x 120 x 60)

### DFMA Findings
- Verdict: conditional_pass — 5 rules, 0 failed, 2 uncertain, no critical/major failures.
- DFM-3DP-001 [uncertain]: wall reads as a uniform shell in wireframe; renders carry no absolute scale, but volume (129.7k ≈ 3mm half-annulus×180 + two 3mm caps) confirms the ~3mm wall.
- DFM-3DP-002 [uncertain]: curved crown is an overhang in the as-rendered pose, but self-supporting when printed flat-face-down as specced.

### Visual Observations
- RIGHT_CLEAN: solid filled semicircle ("D") — flat straight edge + curved arch = semicircular end cap seen face-on (caps closed).
- RIGHT_WIREFRAME: a dashed inner arc uniformly offset inside the outer arc — the hollow ~3mm shell wall, confirmed from this section.
- FRONT_CLEAN: rectangular flank with one solid circle (the ⌀6 latch through-hole) on the near (-Y) wall.
- FRONT_WIREFRAME: dashed inner rectangle (cavity/shell) + 4 small dashed circles = the 4 rear-flank pilot holes seen through the part.
- TOP_CLEAN/WIREFRAME: 180x120 footprint; 4 marks along the rear edge (pilot clusters at X=+-50), 1 mark at front-center (latch); inner dashed rectangle = cavity.
- ISO_CLEAN: barrel/half-cylinder shell lying flat-face-down, arch up, 4 pilot holes near the rear crown edge, semicircular end cap visible.
- ISO_WIREFRAME: inner shell dashed outline confirms hollow cavity open along the flat underside.

### Findings
- [ok] Geometry: half-cylinder shell, flat-face-down, arch up — matches description.
- [ok] Dimensions: bbox 180x120x60 exact (dimension_checker PASS); volume consistent with 3mm shell.
- [ok] Shell wall: ~3mm confirmed from right_wireframe inner arc + front_wireframe inner rectangle + volume.
- [ok] Flat underside OPEN; semicircular end caps closed (right_clean solid D, code insets inner cylinder by t each end).
- [ok] Features: 4 rear pilot holes ⌀2.5 (blind 2mm, stays in wall) + 1 front latch through-hole ⌀6 (pierces front wall into cavity only). Counts and placement verified across front/top/iso views.
- [ok] Coordinate convention (Principle 0): centered on XY, flat face at Z=0 — correct prismatic-style origin per constraints.

### Recommendations
- None blocking. Minor: hole mouths are slightly elliptical on the curved flank (as-designed, acceptable).

VALIDATION: PASSED
