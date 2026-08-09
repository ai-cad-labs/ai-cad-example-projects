import cadquery as cq

# === PARAMETERS ===
# Full-floating gudgeon (wrist) pin — Steel 304, CNC turned + through-drilled.
# Clearance-side OD: nominal 16.0 mm, pin made at 15.99 mm so BOTH the piston
# boss bores (16.02) and the rod small end bore (16.02) get a free-rotating fit.
pin_od = 15.99            # mm — outer diameter (clearance side of 16.0 nominal fit)
pin_length = 50.0         # mm — spans piston boss outer span 48.0 with 1.0 mm
                          #      protrusion per side; half-length 25.0 < skirt
                          #      inner radius 27.0, so the pin stays inside the piston
bore_id = 9.0             # mm — through bore, reduces reciprocating mass
                          #      (wall = (15.99 - 9.0)/2 = 3.495 mm >= 1.5 mm min)

# === GEOMETRY ===
# Coordinate convention (Principle 0): axis of revolution = Z, centered at the
# origin -> pin runs Z = -25.0 .. +25.0. Assembly mates by aligning Z axes only.
# Plain hollow cylinder: annulus profile (outer circle + coaxial inner circle)
# extruded symmetrically about Z=0. Flat square ends, no chamfers/fillets
# (deferred project-wide), no circlip grooves in v1.
result = (
    cq.Workplane("XY")
    .circle(pin_od / 2.0)
    .circle(bore_id / 2.0)
    .extrude(pin_length / 2.0, both=True)
)
