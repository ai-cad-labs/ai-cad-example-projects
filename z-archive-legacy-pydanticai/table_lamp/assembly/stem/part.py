import cadquery as cq

# === PARAMETERS ===
# All dimensions are in millimeters.

# Stem dimensions
length = 250.0
outer_diameter = 12.0  # M12 thread major diameter
inner_diameter = 9.0

# Thread specifications (for notation, not modeled)
thread_spec = "M12x1.5"
thread_length = 15.0

# === GEOMETRY ===

# Create the main cylindrical body of the stem.
# This represents the blank before threading. The threads themselves are
# not modeled geometrically, as is common practice for CNC parts.
# The manufacturing drawing would specify "M12x1.5" on both ends.
stem = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(length)
)

# Create the central bore for the power cord.
stem = stem.faces(">Z").workplane().hole(inner_diameter)

# Assign the final shape to the result variable
result = stem
