import cadquery as cq
import math

# === PARAMETERS ===
# All dimensions are in mm
base_diameter = 150.0
base_height = 20.0
central_hole_tap = "M12x1.5"
thread_major_diameter = 12.0
thread_pitch = 1.5
thread_depth = 15.0
cord_channel_width = 6.0
cord_channel_depth = 6.0
pad_recess_diameter = 140.0
pad_recess_depth = 2.0
top_edge_fillet_radius = 2.0

# === DERIVED PARAMETERS ===
# For modeling, we use the tap drill diameter for the hole
tap_drill_diameter = thread_major_diameter - thread_pitch

# === FEATURE FUNCTIONS ===

def create_base_blank(diameter, height):
    """Creates the main cylindrical body of the base."""
    return cq.Workplane("XY").circle(diameter / 2).extrude(height)

def add_pad_recess(body, recess_diameter, recess_depth):
    """Cuts a circular recess on the bottom face for a rubber pad."""
    return (
        body.faces("<Z")
        .workplane()
        .circle(recess_diameter / 2)
        .cutBlind(-recess_depth)
    )

def add_central_hole(body, drill_diameter, depth):
    """Drills the central hole for the threaded stem."""
    return body.faces(">Z").workplane().hole(drill_diameter, depth)

def add_cord_channel(body, width, depth, base_diameter):
    """Cuts a channel for the power cord from the center to the edge."""
    return (
        body.faces(">Z")
        .workplane()
        .center(0, 0)
        .rect(base_diameter, width, centered=(True, True))
        .cutBlind(-depth)
    )

def add_top_edge_fillet(body, radius):
    """Applies a fillet to the top outer edge."""
    return body.faces(">Z").edges().fillet(radius)

# === COMPOSE ===
# Build the part by applying features in a logical sequence
base_blank = create_base_blank(base_diameter, base_height)
base_with_recess = add_pad_recess(base_blank, pad_recess_diameter, pad_recess_depth)
base_with_hole = add_central_hole(base_with_recess, tap_drill_diameter, thread_depth)
base_with_channel = add_cord_channel(base_with_hole, cord_channel_width, cord_channel_depth, base_diameter)
result = add_top_edge_fillet(base_with_channel, top_edge_fillet_radius)
