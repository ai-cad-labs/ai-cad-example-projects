import cadquery as cq
import math

# === PARAMETERS ===
# This script creates a reference model of an A60 (or A19) light bulb
# with a standard E26 screw base.
# It is intended for visualization and clearance checks, not for manufacturing.

# Overall dimensions
overall_length = 110.0  # mm, from base to top
envelope_max_dia = 60.0  # mm, max diameter of the glass envelope

# E26 Base dimensions
base_dia = 26.2  # mm, average major diameter for an E26 screw base
base_height = 26.0  # mm, typical height of the screw base

# Derived parameters for geometry construction
envelope_radius = envelope_max_dia / 2.0
# The center of the main sphere that forms the top of the bulb
sphere_center_z = overall_length - envelope_radius

# === FEATURE FUNCTIONS ===

def make_e26_base(dia, height):
    """Creates a simple cylinder to represent the E26 screw base."""
    return cq.Workplane("XY").circle(dia / 2).extrude(height)

def make_bulb_envelope(base_dia, base_height, max_dia, total_length):
    """
    Creates the glass envelope of the bulb using a combination of a sphere
    for the top and a lofted solid to create a smooth transition from the base.
    This method is more robust than revolving a complex profile.
    """
    # Derived values for the envelope
    env_radius = max_dia / 2.0
    sphere_center_z = total_length - env_radius

    # 1. Create the main spherical part of the envelope
    sphere = cq.Workplane("XY").workplane(offset=sphere_center_z).sphere(env_radius)

    # 2. Define the end-point for the lofted transition section on the sphere
    # This height is chosen to give a characteristic "A-shape" profile
    loft_end_z = 55.0
    
    # 3. Calculate the radius of the sphere at this height to ensure a smooth join
    # From sphere equation: r^2 + (z - z_center)^2 = R^2
    # This prevents a sharp edge between the loft and the sphere.
    try:
        r_at_loft_end = math.sqrt(env_radius**2 - (loft_end_z - sphere_center_z)**2)
    except ValueError:
        # Fallback in case parameters create an impossible geometry
        r_at_loft_end = env_radius * 0.9

    # 4. Define the two circular profiles (wires) for the loft
    wire_bottom = cq.Workplane("XY").workplane(offset=base_height).circle(base_dia / 2).val()
    wire_top = cq.Workplane("XY").workplane(offset=loft_end_z).circle(r_at_loft_end).val()

    # 5. Create the lofted solid connecting the base to the sphere
    loft = cq.Solid.makeLoft([wire_bottom, wire_top])

    # 6. Trim the bottom of the sphere so it sits flush on top of the loft
    # A large box is used to cut away everything below the join point
    cutter_box = cq.Workplane("XY").box(max_dia * 2, max_dia * 2, loft_end_z).translate((0, 0, 0))
    trimmed_sphere = sphere.cut(cutter_box)
    
    # 7. Union the loft and the trimmed sphere to form the complete envelope
    envelope = cq.Workplane(loft).union(trimmed_sphere)
    
    return envelope

# === COMPOSE ===
# Build the final part by creating and unioning the components.

# Create the base
bulb_base = make_e26_base(base_dia, base_height)

# Create the glass envelope
bulb_envelope = make_bulb_envelope(base_dia, base_height, envelope_max_dia, overall_length)

# Union the base and envelope to create the final bulb model
result = bulb_base.union(bulb_envelope)
