"""Drive-end bolted cover for the conveyor shaft support unit.

Turned steel disc (CNC_turning + secondary drilling) that does three jobs:
  1. carries a 40 x 62 x 10 radial lip seal running on the dia 40 shaft journal,
  2. clamps the drive-end 6208 bearing OUTER ring against the housing shoulder
     via its spigot front face at z = +84,
  3. bolts to the housing drive-end boss with 4 x M8 cap screws on BC dia 104.

Coordinate convention: shaft axis = global Z, drive end = +Z.
The cover is modelled DIRECTLY in the global frame, spanning z = +84 .. +107,
so the assembly places it with an identity transform.

Built as ONE closed profile revolved about Z plus 4 drilled holes.
Both required 1 x 45 chamfers are explicit profile geometry, so no edge is ever
selected for .chamfer() (edge selection on a revolve is brittle).
NO FILLETS anywhere - deferred project-wide.
"""

import math

import cadquery as cq

# === PRIMARY PARAMETERS (all nominal; fits are drawing callouts, never modelled) ===

# Axial stations in the GLOBAL frame (mm)
Z_SPIGOT_FACE = 84.0   # spigot front face: bears on the DE 6208 outer ring
Z_BOSS_FACE = 95.0     # flange back face: seats on the housing drive-end boss face
Z_SEAL_SHOULDER = 100.0  # lip seal butts this outboard shoulder
Z_OUTER_FACE = 107.0   # cover outer face; nothing in the unit rises above this

# Diameters (mm)
SPIGOT_D = 80.0         # dia 80 h8 pilot into the housing dia 80 H7 drive-end bore
FLANGE_OD = 130.0       # matches the housing drive-end boss OD (post-amendment)
SEAL_POCKET_D = 62.0    # dia 62 H8 for the 40 x 62 x 10 lip seal OD
SHAFT_CLEARANCE_D = 42.0  # 1.0 mm radial clearance over the dia 40 shaft

# Chamfers (1 x 45 deg, both required by the brief)
CHAMFER = 1.0

# Bolt pattern (shared verbatim with the housing's 4 x M8 tapped holes)
BOLT_HOLE_D = 9.0            # dia 9 H13 clearance for M8 (ISO 273 medium)
BOLT_CIRCLE_D = 104.0
BOLT_ANGLES_DEG = (45.0, 135.0, 225.0, 315.0)

# Seal / bearing interface data (used for reporting, not geometry)
SEAL_WIDTH = 10.0
BEARING_OUTER_RING_INNER_R = 36.5  # 6208 outer ring face spans r 36.5 .. r 40

# === DERIVED VALUES ===
SPIGOT_R = SPIGOT_D / 2.0                      # 40.0
FLANGE_R = FLANGE_OD / 2.0                     # 65.0
SEAL_POCKET_R = SEAL_POCKET_D / 2.0            # 31.0
SHAFT_CLEARANCE_R = SHAFT_CLEARANCE_D / 2.0    # 21.0
BOLT_CIRCLE_R = BOLT_CIRCLE_D / 2.0            # 52.0
FLANGE_THICKNESS = Z_OUTER_FACE - Z_BOSS_FACE  # 12.0
TOTAL_LENGTH = Z_OUTER_FACE - Z_SPIGOT_FACE    # 23.0

# Reported engineering numbers
SEAL_WALL = SPIGOT_R - SEAL_POCKET_R                        # 9.0 mm pocket-to-spigot wall
FLANGE_RIM = FLANGE_R - (BOLT_CIRCLE_R + BOLT_HOLE_D / 2.0)  # 8.5 mm rim
BEARING_BAND = (SPIGOT_R - CHAMFER) - BEARING_OUTER_RING_INNER_R  # 2.5 mm contact band


# === FEATURE FUNCTIONS ===

def cover_profile():
    """The closed (radius, z) section of the turned cover.

    An annulus in section - it never touches the axis, so the revolve yields a
    hollow body directly, with no bore cut needed. Order is a single loop:
    spigot face -> spigot OD -> flange -> outer face -> shaft bore -> seal pocket.
    """
    return [
        (SEAL_POCKET_R + CHAMFER, Z_SPIGOT_FACE),          # (32, 84) pocket chamfer root
        (SPIGOT_R - CHAMFER, Z_SPIGOT_FACE),               # (39, 84) bearing-clamp face
        (SPIGOT_R, Z_SPIGOT_FACE + CHAMFER),               # (40, 85) spigot lead-in chamfer
        (SPIGOT_R, Z_BOSS_FACE),                           # (40, 95) spigot OD dia 80
        (FLANGE_R, Z_BOSS_FACE),                           # (65, 95) flange back face
        (FLANGE_R, Z_OUTER_FACE),                          # (65,107) flange OD dia 130
        (SHAFT_CLEARANCE_R, Z_OUTER_FACE),                 # (21,107) cover outer face
        (SHAFT_CLEARANCE_R, Z_SEAL_SHOULDER),              # (21,100) dia 42 shaft bore
        (SEAL_POCKET_R, Z_SEAL_SHOULDER),                  # (31,100) SEAL SHOULDER
        (SEAL_POCKET_R, Z_SPIGOT_FACE + CHAMFER),          # (31, 85) dia 62 seal pocket
    ]


def turned_body():
    """Revolve the section 360 deg about the Z axis.

    API TRAP: on a "XZ" workplane revolve()'s axis arguments are LOCAL 2D points,
    not global 3D vectors. Local (0,1) is the plane's y direction = global +Z.
    Passing (0,0,0),(0,0,1) would revolve about the plane normal (global -Y).
    """
    return (
        cq.Workplane("XZ")
        .polyline(cover_profile())
        .close()
        .revolve(360.0, (0, 0), (0, 1))
    )


def bolt_holes(body):
    """4 x dia 9 clearance holes through the flange on BC 104 at 45/135/225/315 deg.

    Drilled along Z straight through the flange (z = +95 .. +107); the cutter
    overshoots 1 mm each side so no coincident faces are left behind.
    """
    points = [
        (
            BOLT_CIRCLE_R * math.cos(math.radians(a)),
            BOLT_CIRCLE_R * math.sin(math.radians(a)),
        )
        for a in BOLT_ANGLES_DEG
    ]
    cutter = (
        cq.Workplane("XY", origin=(0, 0, Z_BOSS_FACE - 1.0))
        .pushPoints(points)
        .circle(BOLT_HOLE_D / 2.0)
        .extrude(FLANGE_THICKNESS + 2.0)
    )
    return body.cut(cutter)


# === COMPOSE (reads as the process plan: turn, then drill) ===
body = turned_body()
result = bolt_holes(body)


# === MEASUREMENTS (printed unconditionally; asserts stay guarded) ===
_bb = result.val().BoundingBox()
_vol = result.val().Volume()
_solids = result.solids().size()
print(f"solids            : {_solids}")
print(f"bbox X,Y,Z        : {_bb.xlen:.3f}, {_bb.ylen:.3f}, {_bb.zlen:.3f}")
print(f"z extent          : {_bb.zmin:.3f} .. {_bb.zmax:.3f}")
print(f"volume mm^3       : {_vol:.1f}")
print(f"bolt holes        : {len(BOLT_ANGLES_DEG)} x dia {BOLT_HOLE_D} on BC {BOLT_CIRCLE_D}")
print(f"seal pocket wall  : {SEAL_WALL:.1f} mm (r{SEAL_POCKET_R} -> r{SPIGOT_R})")
print(f"flange rim        : {FLANGE_RIM:.1f} mm (r{BOLT_CIRCLE_R + BOLT_HOLE_D / 2.0} -> r{FLANGE_R})")
print(f"bearing band      : {BEARING_BAND:.1f} mm (r{BEARING_OUTER_RING_INNER_R} -> r{SPIGOT_R - CHAMFER})")
print(f"bolt head pitch   : {2 * BOLT_CIRCLE_R * math.sin(math.radians(45.0)):.1f} mm centre-to-centre")

if __name__ == "__main__":
    assert _solids == 1, f"expected one solid, got {_solids}"
    assert abs(_bb.xlen - FLANGE_OD) < 1e-6, _bb.xlen
    assert abs(_bb.ylen - FLANGE_OD) < 1e-6, _bb.ylen
    assert abs(_bb.zlen - TOTAL_LENGTH) < 1e-6, _bb.zlen
    assert abs(_bb.zmin - Z_SPIGOT_FACE) < 1e-6, _bb.zmin
    assert abs(_bb.zmax - Z_OUTER_FACE) < 1e-6, _bb.zmax
    assert _vol > 0.0
    print("self-check OK")
