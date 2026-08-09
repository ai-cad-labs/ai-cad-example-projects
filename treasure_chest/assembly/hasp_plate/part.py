import cadquery as cq

# === PARAMETERS (local frame: X=width, Y=thickness, Z=height) ===
plate_width = 40.0          # X
plate_thickness = 4.0       # Y
plate_height = 50.0         # Z

latch_hole_dia = 6.0        # ⌀6 latch hole (pin/padlock shackle)
# PROPOSED (CONFLICT-001): 42.0 -> 34.0 so the latch hole aligns with the lid's
# front latch hole. With the assembly offset +52 (mount holes -> base pilots Z=62),
# local 34 maps to assembled Z=86, matching the lid latch hole (Z=86). The old
# value 42 mapped to Z=94, an 8 mm miss.
latch_hole_z = 34.0

mount_hole_dia = 3.2        # ⌀3.2 M3 clearance
mount_hole_x = 14.0         # X=±14
mount_hole_z = 10.0         # lower half (assembled Z=62)

# === DERIVED ===
cut_len = plate_thickness + 4.0   # cylinder length ensures full through-cut in Y


# === FEATURE FUNCTIONS ===
def flat_plate(w, t, h):
    """Flat latch plate blank — centered on XY, bottom at Z=0."""
    return cq.Workplane("XY").box(w, t, h).translate((0, 0, h / 2))


def y_through_hole(body, x, z, dia):
    """Through-hole drilled along the Y (thickness) axis at (x, z)."""
    cutter = cq.Solid.makeCylinder(
        dia / 2.0, cut_len,
        cq.Vector(x, -cut_len / 2.0, z),   # start below front face
        cq.Vector(0, 1, 0),                # bore along +Y
    )
    return body.cut(cutter)


def latch_hole(body):
    """Single ⌀6 latch hole near the top, centered X=0."""
    return y_through_hole(body, 0.0, latch_hole_z, latch_hole_dia)


def mount_holes(body):
    """Two ⌀3.2 mount holes in the lower half at X=±14."""
    body = y_through_hole(body, -mount_hole_x, mount_hole_z, mount_hole_dia)
    body = y_through_hole(body, +mount_hole_x, mount_hole_z, mount_hole_dia)
    return body


# === COMPOSE ===
body = flat_plate(plate_width, plate_thickness, plate_height)
body = latch_hole(body)
body = mount_holes(body)
result = body
