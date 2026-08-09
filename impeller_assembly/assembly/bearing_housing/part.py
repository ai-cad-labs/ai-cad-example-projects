import cadquery as cq

# ============================================================================
# BEARING HOUSING — upright plate with integral base foot (impeller_assembly)
#
# Coordinate convention (constraints.md, LOCKED):
#   * bore axis = Z axis, through the origin
#   * Z = 0 is the IMPELLER-SIDE FACE — the clearance datum for the whole
#     assembly (impeller backface runs 0.8 mm off this face)
#   * plate spans Z = -16 ... 0; foot bottom (ground plane) at Y = -60;
#     plate top at Y = +35  ->  bore center sits exactly 60 mm above ground
#   * assembly resolver places this part with pure Z-translation (no rotation)
#
# REPAIR (attempt 2, DFA-005): the z = +5 bolt row at X = +/-32 sat under the
# impeller's Ø72 backplate overhang (R36 vs socket envelope 32 + 6 = 38), so a
# Ø12 socket could not reach two of the four foundation bolts with the wheel
# fitted. Fix: foot widened in X (80 -> 108) and BOTH bolt columns moved
# outboard to X = +/-46 (socket envelope 46 - 6 = 40 > R36, 4 mm clear; the
# rectangular symmetric pattern is kept). Datum, plate, pocket, back-bore,
# and bore height are UNCHANGED.
# ============================================================================

# === PARAMETERS (all mm) ===

# --- LOCKED interface parameters (design_plan.md § Interfaces) ---
D_MB_OD = 40.0             # 6203 bearing OD -> pocket diameter (H7 transition intent)
W_MB = 12.0                # 6203 bearing width -> pocket depth (bearing flush at Z=0)
D_HOUSING_BACKBORE = 34.0  # back-bore: leaves 3.0 mm outer-race retention shoulder
                           # and clears the Ø14 shaft by 10 mm per side

# --- Plate envelope ---
plate_width_x = 80.0       # plate width along X (spans X = -40 ... +40)
plate_height_y = 95.0      # ground (Y = -60) up to plate top (Y = +35)
plate_thickness = 16.0     # plate spans Z = -16 ... 0 (= pocket 12 + shoulder 4)
ground_y = -60.0           # foot bottom = the assembly's mounting/ground plane

# --- Integral base foot ---
foot_width_x = 108.0       # WIDER than the plate (DFA-005 repair): spans X = -54 ... +54
                           # so the bolt columns at X = +/-46 keep the original 8 mm
                           # hole-center-to-edge margin. A foot wider than the plate it
                           # supports is normal and improves tipping stability.
foot_height_y = 10.0       # foot spans Y = -60 ... -50
foot_depth_z = 40.0        # foot spans Z = -28 ... +12
foot_center_z = -8.0       # centered on the plate mid-plane (plate mid at Z = -8)

# --- Foot mounting holes (M5 clearance; hardware not modeled) ---
bolt_hole_dia = 5.5        # Ø5.5 clearance for M5 bolts
bolt_hole_x = 46.0         # DFA-005 repair: columns at X = +/-46 (were +/-32).
                           # A Ø12 socket needs ~6 mm radial room around the bolt
                           # axis; 46 - 6 = 40 clears the impeller's R36 backplate
                           # by 4 mm, so ALL four bolts torque with the wheel fitted.
                           # 8 mm to the side edges (foot edge at +/-54) as before.
bolt_hole_z_rear = -21.0   # rear row  (7 mm to the foot rear edge at Z = -28)
bolt_hole_z_front = 5.0    # front row (7 mm to the foot front edge at Z = +12)

# --- Derived values ---
plate_center_y = ground_y + plate_height_y / 2.0   # -12.5
plate_center_z = -plate_thickness / 2.0            # -8.0
foot_center_y = ground_y + foot_height_y / 2.0     # -55.0
foot_top_y = ground_y + foot_height_y              # -50.0
cut_overshoot = 2.0        # defensive cutter overshoot: cutters never end
                           # exactly on a body face (except intentional floors)


# === FEATURE FUNCTIONS ===

def upright_plate():
    """The main upright plate: 80 wide x 95 tall x 16 thick.

    Impeller-side face lands exactly on Z = 0 (the clearance datum);
    the plate reaches the ground plane at Y = -60 so the bore axis (Y = 0)
    sits exactly 60 mm above the mounting surface.
    """
    return (
        cq.Workplane("XY")
        .box(plate_width_x, plate_height_y, plate_thickness)
        .translate((0.0, plate_center_y, plate_center_z))
    )


def base_foot(body):
    """Integral mounting foot, 108(X) x 10(Y) x 40(Z), straddling the plate.

    Centered on the plate mid-plane (Z = -8) so it extends -28 ... +12 in Z.
    Wider than the 80 mm plate by 14 mm per side (DFA-005 repair) so the
    bolt columns sit outboard of the impeller's swept disc. Its forward
    reach past Z = 0 is 14 mm BELOW the impeller's lowest sweep
    (foot top Y = -50 vs impeller lowest point Y = -36), so it never enters
    the running-clearance zone.
    """
    foot = (
        cq.Workplane("XY")
        .box(foot_width_x, foot_height_y, foot_depth_z)
        .translate((0.0, foot_center_y, foot_center_z))
    )
    return body.union(foot)


def bearing_pocket(body):
    """Ø40 x 12 deep bearing pocket, opening on the impeller-side face.

    Grips the 6203's outer diameter; the pocket floor at Z = -12 puts the
    12 mm wide bearing exactly FLUSH with the Z = 0 datum face — that
    flushness is what makes the impeller's 0.8 boss equal the running
    clearance. Cutter floor is EXACT at -W_MB; the open end overshoots
    past Z = 0 so no coincident-face booleans occur at the datum.
    """
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=-W_MB)              # exact pocket floor at Z = -12
        .circle(D_MB_OD / 2.0)
        .extrude(W_MB + cut_overshoot)        # spans Z = -12 ... +2
    )
    return body.cut(cutter)


def back_bore(body):
    """Ø34 back-bore through the remaining 4 mm of plate (Z = -16 ... -12).

    Dual role: (1) the Ø40 -> Ø34 step forms the 3.0 mm annular shoulder
    that axially retains the 6203's outer race toward the pulley side
    (outer-race land ~Ø35.8 per BOM, so the shoulder engages race only);
    (2) clears the Ø14 shaft passing through with 10 mm per side.
    Cutter runs full-through for robustness — inside the pocket span it
    removes nothing (Ø34 < Ø40 is already void there).
    """
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=-(plate_thickness + cut_overshoot))  # Z = -18
        .circle(D_HOUSING_BACKBORE / 2.0)
        .extrude(plate_thickness + 2.0 * cut_overshoot)        # to Z = +2
    )
    return body.cut(cutter)


def foot_bolt_holes(body):
    """4 x Ø5.5 vertical clearance holes through the foot (M5 bolts).

    At (X, Z) = (+/-46, -21) and (+/-46, +5): 8 mm to the side edges,
    7 mm to the front/rear edges, depth/dia = 10/5.5 ~ 1.8. Both rows lie
    OUTSIDE the plate's Z span (-16 ... 0) AND both columns lie outboard
    of the plate's X span (+/-40), so each hole passes through foot
    material only and every bolt head is socket-accessible from above
    with the impeller fitted (DFA-005).
    Axis along Y (drilled from above the foot top, through to the ground).
    """
    points = [
        (bolt_hole_x, bolt_hole_z_rear),
        (-bolt_hole_x, bolt_hole_z_rear),
        (bolt_hole_x, bolt_hole_z_front),
        (-bolt_hole_x, bolt_hole_z_front),
    ]
    # Workplane("XZ"): local (u, v) -> global (X, Z); plane normal = -Y.
    # offset moves the plane along -Y, so offset = +48 puts it at Y = -48
    # (2 mm above the foot top at Y = -50); extrude 14 reaches Y = -62.
    cutter = (
        cq.Workplane("XZ")
        .workplane(offset=-foot_top_y - cut_overshoot)         # plane at Y = -48
        .pushPoints(points)
        .circle(bolt_hole_dia / 2.0)
        .extrude(foot_height_y + 2.0 * cut_overshoot)          # through to Y = -62
    )
    return body.cut(cutter)


# === COMPOSE (reads like the process plan: mill blank -> bore -> drill) ===
body = upright_plate()
body = base_foot(body)          # union: one integral milled piece
body = bearing_pocket(body)     # bore Ø40 x 12 from the impeller-side face
body = back_bore(body)          # Ø34 through the back -> retention shoulder
body = foot_bolt_holes(body)    # drill 4 x Ø5.5 in the foot

result = body
