import cadquery as cq

# === PARAMETERS ===
# Description: These parameters define the geometry of the lamp shade.

# --- Overall Dimensions
height = 100.0  # mm, Overall height of the shade
bottom_od = 120.0 # mm, Outer diameter at the base
top_od = 60.0   # mm, Outer diameter at the top
wall_thickness = 3.0 # mm, Uniform wall thickness

# --- Seating Interface
# This feature allows the shade to rest on the socket_housing flange.
seating_interface_id = 45.5 # mm, Inner diameter of the seating rim
seating_interface_depth = 5.0 # mm, Depth of the seating counterbore from the bottom face

# === DERIVED PARAMETERS ===
bottom_outer_rad = bottom_od / 2.0
top_outer_rad = top_od / 2.0
bottom_inner_rad = bottom_outer_rad - wall_thickness
top_inner_rad = top_outer_rad - wall_thickness

# === GEOMETRY GENERATION ===
# The shade is created using a subtractive method for robustness.

# 1. Create the solid outer cone.
# The cone is defined by its base radius, top radius, and height.
outer_cone = cq.Solid.makeCone(bottom_outer_rad, top_outer_rad, height)

# 2. Create the inner cone that will be subtracted.
inner_cone = cq.Solid.makeCone(bottom_inner_rad, top_inner_rad, height)

# 3. Perform the boolean cut to hollow out the shade.
shade_body = cq.Workplane(outer_cone).cut(inner_cone)

# 4. Create the seating interface feature.
# This is a counterbore on the inside bottom of the shade.
# A cylindrical cutting tool is created and subtracted.
seating_cutter = (
    cq.Workplane("XY")
    .circle(seating_interface_id / 2.0)
    .extrude(seating_interface_depth)
)

# 5. Subtract the cutter to create the final seating rim.
result = shade_body.cut(seating_cutter)
