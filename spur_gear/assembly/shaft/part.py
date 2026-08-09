import cadquery as cq

# === PARAMETERS ===
shaft_diameter = 8.0   # mm — OD, slip-fit into gear ⌀8mm bores
shaft_radius = shaft_diameter / 2.0
shaft_length = 30.0    # mm — L/D = 3.75:1, trivially fine for 3D printing

# === COMPOSE ===
# Plain solid cylinder. Coordinate convention (COOKBOOK Principle 0):
# axis of revolution = Z-axis, centred on origin, extending Z=-15..+15.
# No bore, no chamfers, NO fillets (deferred project-wide).
result = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
    .translate((0, 0, -shaft_length / 2.0))
)
