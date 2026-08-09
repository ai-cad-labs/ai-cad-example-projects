
import cadquery as cq

# === PARAMETERS ===
# Dimensions based on a standard 225mm tire for a 17-inch rim.
rim_diameter = 432.0  # 17 inches
section_width = 225.0  # The nominal width of the tire in mm.
aspect_ratio = 0.60  # The ratio of section height to section width.
corner_radius_factor = 0.2 # Factor for rounding the tread corners.

# === DERIVED VALUES ===
# Calculate section height from aspect ratio.
section_height = section_width * aspect_ratio
rim_radius = rim_diameter / 2.0
# The radius to the center of the tire's cross-section.
profile_center_radius = rim_radius + section_height / 2.0
# Radius for the fillets on the tread.
corner_radius = section_height * corner_radius_factor

# === GEOMETRY ===
# This script creates a representative solid model of a standard automotive tire.
# The method involves creating a 2D cross-sectional profile and then revolving it.

# To create a 2D profile with fillets (a rounded rectangle), a common CadQuery
# technique is used: first create a thin 3D plate, fillet its 3D edges, and
# then extract the resulting face as the desired 2D profile.
temp_plate = (
    cq.Workplane("XZ")
    .rect(section_height, section_width, centered=True)
    .extrude(1.0) # Extrude a minimal amount along Y to create a solid
)

# Fillet the edges that correspond to the outer tread of the tire.
# The selector '|Y and >X' picks the vertical edges on the side with the largest X value.
filleted_plate = temp_plate.edges("|Y and >X").fillet(corner_radius)

# Extract the front face of the filleted plate to use as the 2D profile.
profile_face = filleted_plate.faces(">Y").val()

# Translate the profile to the correct radial position for the tire.
profile_in_position = profile_face.translate(cq.Vector(profile_center_radius, 0, 0))

# Revolve the face 360 degrees around the Z-axis to create the final 3D tire solid.
# The static cq.Solid.revolve method is used here as it proved more robust for
# this geometry than the Workplane.revolve method.
result = cq.Solid.revolve(profile_in_position, 360, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
