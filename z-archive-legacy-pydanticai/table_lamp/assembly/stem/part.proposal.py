import cadquery as cq

# === PARAMETERS ===
# All dimensions are in millimeters.

# Overall dimensions from constraints.md
length = 250.0
outer_diameter = 15.0
inner_diameter = 9.0

# Thread specifications from constraints.md
thread_spec = "M12x1.5"
thread_diameter = 12.0
thread_length = 15.0

# Derived values
main_body_length = length - 2 * thread_length

# === GEOMETRY ===

# This part is constructed as three separate cylinders which are then unioned
# to create the final shouldered shape. This is a robust way to model parts
# with varying diameters along their length.

# Create the main 15mm OD central body
# A workplane offset is used to position it correctly between the two shoulders.
main_body = (
    cq.Workplane("XY")
    .workplane(offset=thread_length)
    .circle(outer_diameter / 2)
    .extrude(main_body_length)
)

# Create the bottom 12mm OD shoulder for threading
bottom_shoulder = (
    cq.Workplane("XY")
    .circle(thread_diameter / 2)
    .extrude(thread_length)
)

# Create the top 12mm OD shoulder for threading
# A workplane offset is used to position it at the far end of the part.
top_shoulder = (
    cq.Workplane("XY")
    .workplane(offset=length - thread_length)
    .circle(thread_diameter / 2)
    .extrude(thread_length)
)

# Union the three cylindrical parts together to form the complete stem body
stem_solid = main_body.union(bottom_shoulder).union(top_shoulder)

# Create the central 9mm bore through the entire part for the power cord
stem_hollow = stem_solid.faces(">Z").workplane().hole(inner_diameter)

# Assign the final shape to the result variable
result = stem_hollow
