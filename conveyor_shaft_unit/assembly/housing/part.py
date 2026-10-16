"""Conveyor shaft support unit - cast iron HOUSING.

One cast body carrying TWO IN-LINE dia 80 H7 bores on the global Z axis for two
6208 bearings (OD 80, width 18), a mounting foot with four dia 14 bolt holes,
a bolted-cover flange boss at the drive end, and two top grease bosses.

Coordinate convention (shared by all three parts of the unit):
    shaft axis = global Z, up = +Y, drive end = +Z,
    origin on the axis midway between the two bearing centres.
Placed in the assembly with an IDENTITY transform.

NO FILLETS and NO DRAFT: deferred project-wide. A production casting would
carry R5-R8 junction radii and 2 deg draft; both are deliberately omitted.
"""

import cadquery as cq
import math

# === PARAMETERS (primary, all mm / deg) ===

# -- body --
BODY_OD = 100.0                 # cast body outside diameter
Z_END_DE = 95.0                 # drive-end face
Z_END_FE = -95.0                # far-end face

# -- bores --
BORE_D = 80.0                   # 6208 bearing OD, dia 80 H7 (nominal in CAD)
PASSAGE_D = 72.0                # central passage joining the two bores
CHAMFER = 1.0                   # 1 x 45 deg, bore mouths AND shoulder roots
Z_DE_SHOULDER = 66.0            # DE shoulder face: BACKS the DE bearing outer ring
Z_FE_BEARING_FACE = -66.0       # FE bearing outer ring inboard face (nominal)
FLOAT_GAP = 1.5                 # FE outer ring floats axially (brief: 1-2 mm)
Z_FE_SHOULDER = Z_FE_BEARING_FACE + FLOAT_GAP   # = -64.5, inboard of the ring face

# -- drive-end cover flange boss --
FLANGE_OD = 130.0
FLANGE_T = 20.0                 # z = +75 .. +95
BOLT_CIRCLE_D = 104.0
TAP_DRILL_D = 6.8               # M8 x 1.25 tapping drill
TAP_DEPTH = 18.0                # blind, from the z = +95 face
BOLT_ANGLES = (45.0, 135.0, 225.0, 315.0)   # clocked clear of the pedestal

# -- pedestal + foot --
PEDESTAL_X = 70.0               # X = -35 .. +35
PEDESTAL_Y_TOP = -40.0
PEDESTAL_Y_BOT = -60.0
FOOT_X = 120.0                  # X = -60 .. +60
FOOT_Y_TOP = -60.0
FOOT_Y_BOT = -75.0              # centre height 75.0
FOOT_HOLE_D = 14.0              # M12 clearance, NOT threaded
FOOT_HOLE_X = 45.0
FOOT_HOLE_Z = 55.0               # NOT 75: at z=75 the dia-130 boss overhangs the M12 head

# -- grease bosses (reachable from directly above) --
BOSS_D = 24.0
BOSS_Z = 70.0                   # one at +70 (over DE bore), one at -70 (over FE)
BOSS_Y_BOT = 20.0               # buried in the body; the bore cut clears it
BOSS_Y_TOP = 70.0               # nipple face, the highest point on the housing
NIPPLE_TAP_D = 7.0              # M8 x 1 tapping drill
NIPPLE_TAP_DEPTH = 12.0         # Y = +70 .. +58
FEED_D = 4.0                    # feed drilling to the bore
FEED_Y_END = 38.0               # bore top surface is Y = +40 -> clean break-through

MIN_WALL = 8.0                  # casting minimum wall, everywhere

# === DERIVED ===
BODY_R = BODY_OD / 2.0
BORE_R = BORE_D / 2.0
PASSAGE_R = PASSAGE_D / 2.0
FLANGE_R = FLANGE_OD / 2.0
BC_R = BOLT_CIRCLE_D / 2.0
BOSS_R = BOSS_D / 2.0
OVERSHOOT = 1.0                 # cutters run past open faces (no coplanar cuts)

Y_AXIS = cq.Vector(0, 1, 0)
Z_AXIS = cq.Vector(0, 0, 1)


def _cyl(radius, y_start, y_end, x=0.0, z=0.0):
    """Cylinder with its axis parallel to +Y (the vertical of this unit)."""
    return cq.Solid.makeCylinder(
        radius, y_end - y_start, cq.Vector(x, y_start, z), Y_AXIS
    )


# === FEATURE FUNCTIONS ===

def body_cylinder():
    """The cast barrel: dia 100 about Z, spanning both bearing stations."""
    return (
        cq.Workplane("XY")
        .workplane(offset=Z_END_FE)
        .circle(BODY_R)
        .extrude(Z_END_DE - Z_END_FE)
    )


def cover_flange_boss(body):
    """Dia 130 pad at the drive end: the bolted cover's mating face."""
    boss = (
        cq.Workplane("XY")
        .workplane(offset=Z_END_DE - FLANGE_T)
        .circle(FLANGE_R)
        .extrude(FLANGE_T)
    )
    return body.union(boss)


def pedestal(body):
    """Solid rib carrying the barrel down onto the foot plate."""
    rib = (
        cq.Workplane("XY")
        .box(
            PEDESTAL_X,
            PEDESTAL_Y_TOP - PEDESTAL_Y_BOT,
            Z_END_DE - Z_END_FE,
        )
        .translate((0.0, (PEDESTAL_Y_TOP + PEDESTAL_Y_BOT) / 2.0, 0.0))
    )
    return body.union(rib)


def foot_plate(body):
    """Machined-underside mounting foot, 15 thick, centre height 75."""
    plate = (
        cq.Workplane("XY")
        .box(FOOT_X, FOOT_Y_TOP - FOOT_Y_BOT, Z_END_DE - Z_END_FE)
        .translate((0.0, (FOOT_Y_TOP + FOOT_Y_BOT) / 2.0, 0.0))
    )
    return body.union(plate)


def grease_bosses(body):
    """Two dia 24 tapped bosses on TOP, one directly over each bearing bore.

    Unioned BEFORE the bore is cut, so the buried stock is removed by the bore.
    """
    for z in (BOSS_Z, -BOSS_Z):
        body = body.union(_cyl(BOSS_R, BOSS_Y_BOT, BOSS_Y_TOP, z=z))
    return body


def bearing_bores(body):
    """ONE revolved cutter carrying both dia 80 bores, the dia 72 passage, both
    bearing shoulders and all four 1 x 45 chamfers as explicit profile geometry.

    No edge selection, hence no .chamfer() and no selector fragility.
    On an XZ workplane a local point (u, v) maps to global (u, 0, v), so the
    profile is written directly as (radius, z).
    """
    profile = [
        (0.0, Z_END_FE - OVERSHOOT),                        # axis, outside FE face
        (BORE_R + CHAMFER, Z_END_FE - OVERSHOOT),           # overshoot, outer radius
        (BORE_R + CHAMFER, Z_END_FE),                       # FLAT RUN-OUT to the face
        (BORE_R, Z_END_FE + CHAMFER),                       # FE mouth chamfer, true 1x45
        (BORE_R, Z_FE_SHOULDER - CHAMFER),                  # dia 80 FE bore
        (BORE_R - CHAMFER, Z_FE_SHOULDER),                  # FE shoulder relief 1x45
        (PASSAGE_R, Z_FE_SHOULDER),                         # FE shoulder face @ -64.5
        (PASSAGE_R, Z_DE_SHOULDER),                         # dia 72 central passage
        (BORE_R - CHAMFER, Z_DE_SHOULDER),                  # DE shoulder face @ +66
        (BORE_R, Z_DE_SHOULDER + CHAMFER),                  # DE shoulder relief 1x45
        (BORE_R, Z_END_DE - CHAMFER),                       # dia 80 DE bore
        (BORE_R + CHAMFER, Z_END_DE),                       # DE mouth chamfer, true 1x45
        (BORE_R + CHAMFER, Z_END_DE + OVERSHOOT),           # FLAT RUN-OUT past the face
        (0.0, Z_END_DE + OVERSHOOT),                        # back to the axis
    ]
    cutter = (
        cq.Workplane("XZ")
        .polyline(profile)
        .close()
        .revolve(360.0, (0, 0), (0, 1))   # LOCAL 2D axis: (0,0)->(0,1) = global Z
    )
    return body.cut(cutter)


def cover_tapped_holes(body):
    """4 x M8 x 1.25 BLIND tapped holes, BC 104, in the drive-end flange boss."""
    for ang in BOLT_ANGLES:
        x = BC_R * math.cos(math.radians(ang))
        y = BC_R * math.sin(math.radians(ang))
        drill = cq.Solid.makeCylinder(
            TAP_DRILL_D / 2.0,
            TAP_DEPTH + OVERSHOOT,
            cq.Vector(x, y, Z_END_DE - TAP_DEPTH),
            Z_AXIS,
        )
        body = body.cut(drill)
    return body


def foot_bolt_holes(body):
    """4 x dia 14 M12 clearance holes through the foot plate (no thread)."""
    for x in (FOOT_HOLE_X, -FOOT_HOLE_X):
        for z in (FOOT_HOLE_Z, -FOOT_HOLE_Z):
            body = body.cut(
                _cyl(
                    FOOT_HOLE_D / 2.0,
                    FOOT_Y_BOT - OVERSHOOT,
                    FOOT_Y_TOP + OVERSHOOT,
                    x=x,
                    z=z,
                )
            )
    return body


def grease_feeds(body):
    """Per boss: an M8 x 1 nipple port, then a dia 4 feed into its own bore."""
    tap_bot = BOSS_Y_TOP - NIPPLE_TAP_DEPTH          # Y = +58
    for z in (BOSS_Z, -BOSS_Z):
        body = body.cut(
            _cyl(NIPPLE_TAP_D / 2.0, tap_bot, BOSS_Y_TOP + OVERSHOOT, z=z)
        )
        body = body.cut(
            _cyl(FEED_D / 2.0, FEED_Y_END, tap_bot + 0.5, z=z)
        )
    return body


# === COMPOSE (reads as the manufacturing sequence; unions BEFORE the bore) ===
housing = body_cylinder()
housing = cover_flange_boss(housing)
housing = pedestal(housing)
housing = foot_plate(housing)
housing = grease_bosses(housing)
housing = bearing_bores(housing)
housing = cover_tapped_holes(housing)
housing = foot_bolt_holes(housing)
housing = grease_feeds(housing)
result = housing


# === SELF-CHECK MEASUREMENTS (printed unconditionally; asserts guarded) ===
def _probe_is_open(radius, z, half_t=0.1):
    """True if a disc of this radius at this z sits in open space (the bore)."""
    disc = cq.Solid.makeCylinder(
        radius, 2 * half_t, cq.Vector(0, 0, z - half_t), Z_AXIS
    )
    try:
        vol = result.intersect(disc).val().Volume()
    except Exception:
        return True, 0.0
    return vol < 1e-6, vol


_bb = result.val().BoundingBox()
_vol = result.val().Volume()
_solids = result.solids().size()
print(f"housing bbox X={_bb.xlen:.3f} Y={_bb.ylen:.3f} Z={_bb.zlen:.3f}")
print(f"housing bbox ranges X[{_bb.xmin:.1f},{_bb.xmax:.1f}] "
      f"Y[{_bb.ymin:.1f},{_bb.ymax:.1f}] Z[{_bb.zmin:.1f},{_bb.zmax:.1f}]")
print(f"housing volume {_vol:.1f} mm^3   solids {_solids}")
print(f"DE shoulder z={Z_DE_SHOULDER}  FE shoulder z={Z_FE_SHOULDER}  "
      f"float gap {FLOAT_GAP} mm")

for _r, _z, _label in (
    (BORE_R - 0.1, -80.0, "FE bore dia80 open"),
    (BORE_R - 0.1, 80.0, "DE bore dia80 open"),
    (PASSAGE_R - 0.1, 0.0, "passage dia72 open"),
    (PASSAGE_R + 0.1, 0.0, "material outside dia72 @z=0"),
    (BORE_R + 0.1, 80.0, "material outside dia80 @z=+80"),
):
    _open, _v = _probe_is_open(_r, _z)
    print(f"probe r={_r:.1f} z={_z:+.1f} {_label}: open={_open} vol={_v:.3f}")

if __name__ == "__main__":
    assert _solids == 1, f"expected ONE solid, got {_solids}"
    assert abs(_bb.xlen - FLANGE_OD) < 0.01
    assert abs(_bb.ylen - (BOSS_Y_TOP - FOOT_Y_BOT)) < 0.01
    assert abs(_bb.zlen - (Z_END_DE - Z_END_FE)) < 0.01
    assert _vol > 0
    # min-wall ledger (constraint 3)
    assert BODY_R - BORE_R >= MIN_WALL                      # 10.0 body over bore
    assert BODY_R - PASSAGE_R >= MIN_WALL                   # 14.0 body over passage
    assert (BC_R - TAP_DRILL_D / 2.0 - 0.6) - BORE_R >= MIN_WALL   # 8.0 thread->bore
    assert FLANGE_R - (BC_R + TAP_DRILL_D / 2.0 + 0.6) >= MIN_WALL  # 9.0 thread->OD
    assert BOSS_R - (NIPPLE_TAP_D / 2.0 + 0.5) >= MIN_WALL  # 8.0 boss wall at M8
    assert FOOT_X / 2.0 - (FOOT_HOLE_X + FOOT_HOLE_D / 2.0) >= MIN_WALL  # 8.0 edge
    assert BOSS_Y_TOP > FLANGE_R, "grease nipples must be the highest feature"
    print("ALL ASSERTS PASS")
