import cadquery as cq
import math

# === PARAMETERS (local frame: X = cylinder axis/length, Y = width, Z = height) ===
# Half-cylinder shell, flat face DOWN (open along Z=0), closed semicircular end walls.
R_out = 60.0            # outer radius (⌀120 = base outer width)
wall = 3.0              # shell wall thickness
R_in = R_out - wall     # inner radius = 57 mm
length = 180.0          # length along X (matches base)

# --- Hinge pilot holes (rear +Y flank) ---
pilot_dia = 2.5
pilot_depth = 2.0
pilot_z = 8.0                              # local Z (assembled Z=88 → local 8)
pilot_x = [-58.0, -42.0, 42.0, 58.0]      # 2 clusters (X=±50), 16 mm spacing

# --- Latch through-hole (front -Y lower edge) ---
latch_dia = 6.0
latch_x = 0.0
latch_z = 6.0                             # local Z (assembled Z=86 → local 6)


# === FEATURE FUNCTIONS ===
def half_cylinder_shell(r_out, r_in, ln, t):
    """Upper half of a hollow cylinder, capped at both ends, open on flat bottom.

    Build a full capped tube along X (outer cylinder minus a shorter inner
    cylinder → 3 mm shell + 3 mm end caps), then cut away everything below
    Z=0 to leave the upper half seated flat-face-down.
    """
    # Outer solid cylinder along +X (0 .. ln), on the YZ plane.
    outer = cq.Workplane("YZ").circle(r_out).extrude(ln)
    # Inner cylinder inset by `t` at each end → leaves solid end caps.
    inner = (cq.Workplane("YZ").workplane(offset=t)
             .circle(r_in).extrude(ln - 2 * t))
    tube = outer.cut(inner)
    # Centre on X.
    tube = tube.translate((-ln / 2.0, 0, 0))
    # Remove the lower half (everything below Z=0).
    cutter = cq.Workplane("XY").box(ln + 20, 4 * r_out, 4 * r_out)
    cutter = cutter.translate((0, 0, -2 * r_out))   # top face at Z=0
    return tube.cut(cutter)


def hinge_pilot_holes(body, xs, z0, dia, depth, r_out):
    """Blind pilot holes drilled radially-ish (along -Y) into the +Y flank."""
    surf_y = math.sqrt(r_out ** 2 - z0 ** 2)   # outer-surface Y at this Z
    y_start = surf_y - depth                    # inner end of the blind hole
    for x0 in xs:
        cutter = cq.Solid.makeCylinder(
            dia / 2.0, r_out,                   # length runs well past the surface
            cq.Vector(x0, y_start, z0), cq.Vector(0, 1, 0))
        body = body.cut(cutter)
    return body


def latch_through_hole(body, x0, z0, dia, r_out):
    """⌀6 through-hole through the front (-Y) shell wall only."""
    # Cut a Y-axis cylinder that spans the front wall but stops inside the
    # cavity so it does NOT pierce the rear wall.
    cutter = cq.Solid.makeCylinder(
        dia / 2.0, r_out - 5.0,                 # from y=-(r_out+2) to inside cavity
        cq.Vector(x0, -(r_out + 2.0), z0), cq.Vector(0, 1, 0))
    return body.cut(cutter)


# === COMPOSE (reads as a manufacturing plan) ===
body = half_cylinder_shell(R_out, R_in, length, wall)
body = hinge_pilot_holes(body, pilot_x, pilot_z, pilot_dia, pilot_depth, R_out)
body = latch_through_hole(body, latch_x, latch_z, latch_dia, R_out)
result = body
