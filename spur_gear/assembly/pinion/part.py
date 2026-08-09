import cadquery as cq
from math import cos, sin, atan, sqrt, radians, pi

# === PARAMETERS (primary, independent) ===
module_mm = 2.0             # gear module m (meshing gears must share module)
num_teeth = 18             # z — number of teeth
pressure_angle_deg = 20    # alpha — standard involute pressure angle
face_width_mm = 10.0       # b — gear thickness, extruded along Z
bore_dia_mm = 8.0          # nominal central bore diameter (slip-fit over ⌀8 shaft)
bore_clearance_mm = 0.2    # diametral print clearance for a functional slip fit
flank_samples = 14         # points sampled along each involute flank

# === DERIVED VALUES (dependency order) ===
r_pitch = module_mm * num_teeth / 2.0                    # 18.000  pitch radius
r_addendum = r_pitch + module_mm                         # 20.000  tip radius  -> OD 40
r_root = r_pitch - 1.25 * module_mm                      # 15.500  root radius -> root dia 31
r_base = r_pitch * cos(radians(pressure_angle_deg))      # 16.914  base circle radius
r_bore = (bore_dia_mm + bore_clearance_mm) / 2.0         # 4.100   bore radius (⌀8.2)

# involute parameter t where the flank reaches the tip radius:
#   ||involute(t)|| = r_base*sqrt(1+t^2) = r_addendum  ->  t = sqrt((r_a/r_b)^2 - 1)
t_tip = sqrt((r_addendum / r_base) ** 2 - 1)
# involute parameter at the pitch radius (used to centre the tooth thickness)
t_pitch = sqrt((r_pitch / r_base) ** 2 - 1)


# === INVOLUTE HELPERS (all tooth math done in Python -> guaranteed closed wire) ===
def _involute_point(r, t):
    """Point on the involute of a circle of radius r at parameter t."""
    return (r * (cos(t) + t * sin(t)), r * (sin(t) - t * cos(t)))


def _rotate(p, ang):
    """Rotate a 2D point about the origin by ang radians."""
    c, s = cos(ang), sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def _tooth_points():
    """Return the ordered (x,y) vertices of ONE tooth, symmetric about +X.

    Loop order (CCW): root_right -> right involute flank (base->tip) -> tip ->
    left involute flank (tip->base) -> root_left -> chord back to root_right.
    The radial stub from r_base down to r_root bridges the region below the
    base circle (r_base > r_root here, so the flank cannot reach the root)."""
    # Polar angle gained along the involute from the base circle to the pitch
    # circle equals inv(alpha) = t_pitch - atan(t_pitch). Placing the pitch
    # point at -pi/(2z) (half the pitch tooth thickness) centres the tooth on +X.
    inv_pitch = t_pitch - atan(t_pitch)
    half_tooth_angle = pi / (2 * num_teeth)
    theta0 = -(half_tooth_angle + inv_pitch)   # base-circle start angle, right flank

    # Right flank: base -> tip, rotated so the pitch point lands correctly.
    right_flank = [
        _rotate(_involute_point(r_base, t_tip * i / (flank_samples - 1)), theta0)
        for i in range(flank_samples)
    ]
    # Left flank is the mirror across the X axis.
    left_flank = [(x, -y) for (x, y) in right_flank]

    right_base = right_flank[0]
    left_base = left_flank[0]
    # Radial stubs down to the root radius (same polar angle as the base point).
    right_root = _rotate((r_root, 0), theta0)
    left_root = (right_root[0], -right_root[1])

    pts = [right_root, right_base]
    pts += right_flank[1:]              # up the right flank to the tip
    pts += list(reversed(left_flank))   # tip down the left flank to its base
    pts += [left_root]                  # radial stub in on the left
    # polyline().close() adds the final chord left_root -> right_root
    return pts


# === FEATURE FUNCTIONS ===
def gear_teeth():
    """z involute teeth arrayed 360 degrees about the Z-axis, extruded to the
    face width. Each tooth is an explicitly-closed polyline (robust: no arc
    stitching), rotated into position and unioned."""
    base_pts = _tooth_points()
    teeth = None
    for i in range(num_teeth):
        ang = 2 * pi * i / num_teeth
        pts = [_rotate(p, ang) for p in base_pts]
        tooth = cq.Workplane("XY").polyline(pts).close().extrude(face_width_mm)
        teeth = tooth if teeth is None else teeth.union(tooth)
    return teeth


def gear_body():
    """Central hub disc (up to the root radius) unioned with the teeth, giving
    the complete solid gear blank from Z=0 to Z=face_width."""
    hub = cq.Workplane("XY").circle(r_root).extrude(face_width_mm)
    return hub.union(gear_teeth())


def central_bore(body):
    """⌀8mm (+0.2 slip-fit clearance) through-bore on the Z-axis."""
    return body.faces(">Z").workplane().hole(2 * r_bore)


# === COMPOSE (reads as a manufacturing process plan) ===
gear = gear_body()                 # solid gear, Z = 0 .. face_width
gear = central_bore(gear)          # cut the central shaft bore
# Centre the face width about Z=0 per COOKBOOK Principle 0 (revolved part on Z axis).
result = gear.translate((0, 0, -face_width_mm / 2.0))
