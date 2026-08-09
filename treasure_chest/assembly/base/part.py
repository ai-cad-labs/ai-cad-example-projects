import cadquery as cq

# === PARAMETERS (engineering units: mm) ===
# Outer envelope — prismatic part, centered on XY, bottom at Z=0 (COOKBOOK Principle 0)
outer_L = 180.0   # X (length)
outer_W = 120.0   # Y (depth); Front = -Y, Rear = +Y
outer_H = 80.0    # Z (height); rim at Z=80

wall_t = 3.0      # side-wall thickness (all four walls)
floor_t = 3.0     # solid floor thickness

# === DERIVED ===
cavity_L = outer_L - 2 * wall_t   # 174
cavity_W = outer_W - 2 * wall_t   # 114
cavity_H = outer_H - floor_t      # 77 (cavity from Z=3 to Z=80, open top)

rear_y = outer_W / 2.0            # +60
front_y = -outer_W / 2.0          # -60

# Pilot holes — BLIND, drilled from outer face inward
pilot_dia = 2.5
pilot_r = pilot_dia / 2.0
pilot_depth = 2.0

# Hinge pilot holes: rear face (Y=+60), 2 clusters (X=-50, X=+50), 16mm X-spacing, Z=72
hinge_z = 72.0
hinge_x = [-58.0, -42.0, 42.0, 58.0]

# Hasp pilot holes: front face (Y=-60), X=±14, Z=62
hasp_z = 62.0
hasp_x = [-14.0, 14.0]


# === FEATURE FUNCTIONS ===
def blank(L, W, H):
    """Solid outer block, bottom at Z=0."""
    return cq.Workplane("XY").box(L, W, H, centered=(True, True, False))


def interior_cavity(body):
    """Hollow the interior, leaving 3mm walls + 3mm floor and an open top."""
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=floor_t)
        .box(cavity_L, cavity_W, cavity_H, centered=(True, True, False))
    )
    return body.cut(cutter)


def pilot_hole(body, x, y_face, z, direction):
    """Single blind pilot hole drilled from an outer face inward."""
    cutter = cq.Solid.makeCylinder(
        pilot_r, pilot_depth, cq.Vector(x, y_face, z), cq.Vector(*direction)
    )
    return body.cut(cutter)


def hinge_pilot_holes(body):
    """4 rear-face pilot holes (2 clusters) drilled inward (-Y)."""
    for x in hinge_x:
        body = pilot_hole(body, x, rear_y, hinge_z, (0, -1, 0))
    return body


def hasp_pilot_holes(body):
    """2 front-face pilot holes drilled inward (+Y)."""
    for x in hasp_x:
        body = pilot_hole(body, x, front_y, hasp_z, (0, 1, 0))
    return body


# === COMPOSE (reads as a manufacturing process plan) ===
body = blank(outer_L, outer_W, outer_H)
body = interior_cavity(body)
body = hinge_pilot_holes(body)
body = hasp_pilot_holes(body)
result = body
