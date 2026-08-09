import cadquery as cq

# === PARAMETERS ===
# All dimensions are in mm.
# --- Overall Dimensions ---
outer_diameter = 45.0
height = 60.0

# --- Socket Bore Features ---
socket_bore_diameter = 38.0
socket_bore_depth = 42.0

# --- Stem Mount Features ---
# Tapped hole for M12x1.5 thread.
# Per standards, the pilot drill diameter for M12x1.5 is 10.5mm.
stem_pilot_hole_diameter = 10.5
stem_hole_depth = 18.0 # This depth is specified to meet DFM rule (1.5 * 12mm)

# --- Cosmetic Features ---
top_edge_chamfer = 0.5

# === FEATURE FUNCTIONS ===

def create_blank(od, h):
    """Creates the main cylindrical blank."""
    return cq.Workplane("XY").circle(od / 2).extrude(h)

def add_socket_bore(body, bore_dia, bore_depth):
    """Cuts the large internal bore for the E26 socket from the top."""
    return (
        body.faces(">Z").workplane()
        .hole(bore_dia, bore_depth)
    )

def add_stem_hole(body, pilot_dia, hole_depth):
    """Cuts the pilot hole for the M12 tapped thread from the bottom."""
    return (
        body.faces("<Z").workplane()
        .hole(pilot_dia, hole_depth)
    )

def add_chamfers(body, chamfer_size):
    """Adds cosmetic and functional chamfers to the top edges."""
    # Chamfer for the outer top edge
    body = body.faces(">Z").edges().chamfer(chamfer_size)
    # Chamfer for the inner bore edge
    # The selector below is complex to avoid selecting the bottom edge of the chamfer just created
    body = body.faces(">Z").wires(cq.selectors.RadiusNthSelector(-1)).edges().chamfer(chamfer_size)
    return body

# === COMPOSE ===
# Build the part by applying features in sequence.
body = create_blank(outer_diameter, height)
body = add_socket_bore(body, socket_bore_diameter, socket_bore_depth)
body = add_stem_hole(body, stem_pilot_hole_diameter, stem_hole_depth)
result = add_chamfers(body, top_edge_chamfer)
