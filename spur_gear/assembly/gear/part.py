"""Involute spur gear (driven member) — 30-tooth, module 2, 20 deg pressure angle.

Involute tooth flanks are built from the involute-of-a-circle parametric equations
(point math, per reference/cadquery-contrib/examples/cylindrical_gear.py). Rather than
assembling one fragile per-tooth wire and unioning z copies, the ENTIRE gear outline is
generated as a single ordered list of points (both flanks + tip land + root gap sampled
around all 30 teeth), drawn as one closed polyline and extruded once — a far more robust
construction. The central through-bore is then cut. NO fillets (deferred project policy).
Centred on the Z-axis at the origin per COOKBOOK Principle 0.
"""

import cadquery as cq
from math import cos, sin, sqrt, radians, atan2, pi

# === PARAMETERS (primary) ===
module = 2.0            # mm, gear module (m)
num_teeth = 30          # z, number of teeth
pressure_angle = 20.0   # deg (alpha)
face_width = 10.0       # mm, gear thickness (b)
bore_dia = 8.0          # mm, nominal central through-bore
bore_clearance = 0.2    # mm, print slip-fit clearance added to bore diameter

# Sampling resolution (points, not fillets — pure geometric approximation of curves)
flank_samples = 12      # points along each involute flank
tip_samples = 5         # points across the tip land arc
root_samples = 6        # points across the root gap arc

# === DERIVED VALUES ===
r_pitch = module * num_teeth / 2.0                  # 30.0  -> pitch dia 60
r_addendum = r_pitch + module                       # 32.0  -> tip dia 64
r_root = r_pitch - 1.25 * module                    # 27.5  -> root dia 55
r_base = r_pitch * cos(radians(pressure_angle))     # 28.19 -> base dia 56.38
effective_bore_dia = bore_dia + bore_clearance      # 8.2 mm for functional slip fit

if r_base < r_root:
    raise ValueError("r_base < r_root: gear undercut; raise teeth/pressure angle.")


# === INVOLUTE GEOMETRY (point math) ===
def _involute_polar(t):
    """Polar (radius, angle) of the involute of the base circle at parameter t.

    Involute of a circle: x = rb(cos t + t sin t), y = rb(sin t - t cos t).
    Starts at (rb, 0) so angle(0)=0; both radius and angle grow with t.
    """
    x = r_base * (cos(t) + t * sin(t))
    y = r_base * (sin(t) - t * cos(t))
    return sqrt(x * x + y * y), atan2(y, x)


# Involute parameters at the pitch and tip circles.
t_pitch = sqrt((r_pitch / r_base) ** 2 - 1)
t_tip = sqrt((r_addendum / r_base) ** 2 - 1)

# Angular offset that centres the tooth: half the circular tooth thickness at the
# pitch circle (pi/(2z)) plus the involute roll angle consumed reaching the pitch point.
half_tooth_pitch_angle = pi / (2 * num_teeth)
_, phi_pitch = _involute_polar(t_pitch)
offset = half_tooth_pitch_angle + phi_pitch

pitch_angular = 2 * pi / num_teeth  # angular pitch (tooth + gap)


def _pt(radius, angle):
    return (radius * cos(angle), radius * sin(angle))


def _tooth_points(theta_center):
    """CCW-ordered outline points for ONE tooth (+ trailing root gap), absolute coords.

    Walk order (monotonically increasing angle): right flank root->tip, tip land arc,
    left flank tip->root, root gap arc to the next tooth's right flank.
    """
    pts = []
    # Right flank, root -> base -> tip (relative angle = phi(t) - offset).
    pts.append(_pt(r_root, theta_center - offset))  # root point (radial line to base)
    for i in range(flank_samples + 1):
        t = t_tip * i / flank_samples
        r, phi = _involute_polar(t)
        pts.append(_pt(r, theta_center + phi - offset))
    # Tip land arc, right tip -> left tip (constant radius r_addendum).
    a_right = theta_center + _involute_polar(t_tip)[1] - offset
    a_left = theta_center - _involute_polar(t_tip)[1] + offset
    for i in range(1, tip_samples):
        a = a_right + (a_left - a_right) * i / tip_samples
        pts.append(_pt(r_addendum, a))
    # Left flank, tip -> base -> root (mirror: relative angle = offset - phi(t)).
    for i in range(flank_samples, -1, -1):
        t = t_tip * i / flank_samples
        r, phi = _involute_polar(t)
        pts.append(_pt(r, theta_center - phi + offset))
    pts.append(_pt(r_root, theta_center + offset))  # root point
    # Root gap arc, this tooth's left root -> next tooth's right root.
    a0 = theta_center + offset
    a1 = theta_center + pitch_angular - offset
    for i in range(1, root_samples):
        a = a0 + (a1 - a0) * i / root_samples
        pts.append(_pt(r_root, a))
    return pts


# === FEATURE FUNCTIONS ===
def gear_blank():
    """Full toothed cross-section extruded to the face width, centred about Z=0."""
    outline = []
    for k in range(num_teeth):
        outline.extend(_tooth_points(k * pitch_angular))
    body = cq.Workplane("XY").polyline(outline).close().extrude(face_width)
    return body.translate((0, 0, -face_width / 2.0))  # centre on origin (Principle 0)


def central_bore(body):
    """Axial through-bore (with slip-fit clearance) along Z through the origin."""
    cutter = (
        cq.Workplane("XY")
        .circle(effective_bore_dia / 2.0)
        .extrude(face_width + 2.0)
        .translate((0, 0, -(face_width + 2.0) / 2.0))
    )
    return body.cut(cutter)


# === COMPOSE (reads like a manufacturing process plan) ===
gear = gear_blank()
gear = central_bore(gear)
result = gear
