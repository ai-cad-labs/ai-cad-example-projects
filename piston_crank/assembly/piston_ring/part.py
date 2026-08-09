import cadquery as cq

# =====================================================================
# piston_ring — rectangular-section split piston ring (Steel 304, CNC turning)
# One geometry shared by both compression rings and the oil ring (v1);
# instanced 3x in the assembly.
#
# Coordinate convention (Principle 0): ring axis = Z, section centered at
# origin — ring spans Z = -1.25 .. +1.25, OD/ID concentric with Z through (0,0).
# =====================================================================

# === PARAMETERS (mm) ===
# PRIMARY dimensions (from constraints.md — do not drift)
free_od = 60.5            # free (uncompressed) outer diameter
radial_thickness = 2.5    # radial wall of the rectangular section
axial_height = 2.5        # axial height (0.1 mm side clearance in 2.6 mm groove)
end_gap = 1.0             # split-ring end gap, straight radial cut width

# DERIVED values
free_id = free_od - 2.0 * radial_thickness   # 55.5 — ring inner diameter
outer_r = free_od / 2.0                      # 30.25
inner_r = free_id / 2.0                      # 27.75

# Gap cutter sizing: a rectangular slot along +X, 1.0 mm wide tangentially,
# spanning radially past both faces of the section and axially past both
# flat faces (defensive overshoot so the cut fully clears the solid).
cut_overshoot = 1.0
cutter_radial_len = radial_thickness + 2.0 * cut_overshoot          # 4.5
cutter_center_x = (inner_r + outer_r) / 2.0                          # 28.875 (mid-section)
cutter_axial = axial_height + 2.0 * cut_overshoot                    # 4.5

# === GEOMETRY ===
# Annular body: rectangular cross-section ring (no taper, no chamfer, no
# fillets — fillets deferred project-wide). extrude(both=True) centers the
# section on Z = 0 per convention.
ring = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)             # inner circle becomes the bore of the annulus
    .extrude(axial_height / 2.0, both=True)
)

# End gap: 1.0 mm straight radial slot through the section on the +X side
# (manufactured by wire EDM / slitting saw after turning).
gap_cutter = (
    cq.Workplane("XY")
    .box(cutter_radial_len, end_gap, cutter_axial)
    .translate((cutter_center_x, 0.0, 0.0))
)
ring = ring.cut(gap_cutter)

result = ring
