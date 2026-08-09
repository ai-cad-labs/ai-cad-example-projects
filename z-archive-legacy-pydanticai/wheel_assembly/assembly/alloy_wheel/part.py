
import cadquery as cq
import math

# === PARAMETERS ===
# --- Main Dimensions
wheel_diameter = 432.0  # 17 inches
wheel_width = 200.0

# --- Hub Dimensions
hub_od = 160.0
hub_id = 80.0
hub_thickness = 25.0

# --- Rim Dimensions
rim_id = 390.0

# --- Spoke Dimensions
spoke_count = 5
spoke_width = 50.0 # Width of the spoke in XY plane
spoke_thickness = 25.0 # Thickness of spoke in Z direction

# --- Bolt Pattern
pcd = 110.0
bolt_hole_count = 5
bolt_hole_dia = 13.0 # Clearance for M12 bolts

# --- Fillets
fillet_radius = 4.0

# === DERIVED VALUES ===
hub_radius = hub_od / 2.0
rim_outer_radius = wheel_diameter / 2.0
rim_inner_radius = rim_id / 2.0
spoke_length = rim_inner_radius - hub_radius

# === FEATURE FUNCTIONS ===

def make_hub(od, thickness, bore_id):
    """
    Creates the central hub, including the main bore.
    The main bore is created here as it's integral to the hub.
    """
    hub = (
        cq.Workplane("XY")
        .circle(od / 2)
        .extrude(thickness)
        .faces(">Z")
        .workplane()
        .hole(bore_id)
    )
    return hub

def make_rim(outer_dia, inner_dia, width):
    """Creates the outer rim barrel as a simple hollow cylinder."""
    rim = (
        cq.Workplane("XY")
        .circle(outer_dia / 2)
        .circle(inner_dia / 2)
        .extrude(width)
    )
    return rim

def make_spokes(count, hub_r, spoke_len, spoke_w, spoke_t, z_pos):
    """
    Creates and patterns the spokes using simple rectangular boxes.
    This additive method with overlapping solids is robust.
    """
    # Create a single spoke as a simple box.
    # It is created in place, overlapping where the hub and rim will be.
    single_spoke = (
        cq.Workplane("XY")
        .box(spoke_len, spoke_w, spoke_t, centered=(False, True, True))
        .translate(cq.Vector(hub_r, 0, z_pos))
    )

    # Pattern the spokes in a circular array.
    spokes = cq.Workplane("XY")
    angle = 360.0 / count
    for i in range(count):
        rotated_spoke = single_spoke.rotate((0, 0, 0), (0, 0, 1), i * angle)
        spokes = spokes.add(rotated_spoke)
    return spokes

def add_bolt_holes(body, pcd, hole_dia, count, thickness):
    """Adds the mounting bolt holes to the hub face."""
    # Select the front face of the wheel for the holes.
    body = (
        body.faces(">Z").workplane(centerOption="CenterOfBoundBox")
        .polarArray(pcd / 2.0, 0, 360, count)
        .hole(hole_dia, depth=thickness)
    )
    return body

# === COMPOSE ===
# The design is built using a robust, additive process.

# 1. Create the rim. This is the base component.
rim = make_rim(wheel_diameter, rim_id, wheel_width)

# 2. Create the spokes. They are positioned to be in the vertical center of the rim.
spokes = make_spokes(spoke_count, hub_radius, spoke_length, spoke_width, spoke_thickness, wheel_width / 2)

# 3. Create the hub, which already includes the central bore.
hub = make_hub(hub_od, hub_thickness, hub_id)
# Translate the hub to sit on the front face of the rim.
hub = hub.translate((0, 0, wheel_width))

# 4. Union all the simple, overlapping solids into one body.
# This is a robust way to create the main geometry.
body = rim.union(spokes).union(hub)

# 5. Add the bolt holes as a final subtractive feature on the hub.
body = add_bolt_holes(body, pcd, bolt_hole_dia, bolt_hole_count, hub_thickness)

# 6. Add fillets as the very last step.
# Applying fillets to all vertical edges is a simple and robust way to
# ensure all spoke junctions are filleted, satisfying manufacturability.
# This also fillets the inner and outer rim edges, which is acceptable.
result = body.edges("|Z").fillet(fillet_radius)
