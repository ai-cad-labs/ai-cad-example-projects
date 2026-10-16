"""Conveyor shaft support unit - top-level assembly.

COORDINATE CONVENTION (shared global frame):
    shaft axis = global Z,  up = +Y,  drive end = +Z
    origin sits on the axis midway between the two bearing centres
    bearing centres at z = +75 (drive end, located) and z = -75 (far end, floating)

The three Make parts (shaft, housing, cover) are each already modelled directly
in this frame, so every one of them is placed with an IDENTITY transform:
no rotations, no offsets. The seven Buy items are catalogue parts, modelled
inline here as representative primitives and placed by direct cq.Location.

Several mating faces are EXACTLY COINCIDENT at nominal because the real fits
are tolerance callouts carried in text, not in geometry (shaft seats 40 k6,
housing bores 80 H7, cover spigot 80 h8, seal pocket 62 H8). Those contacts
are designed, not clashes -- see assembly.md.
"""

import math

import cadquery as cq

# =====================================================================
# AXIAL STATIONS (global Z, mm) -- the single source of the stack-up
# =====================================================================
BEARING_CENTRE_DRIVE = 75.0       # located bearing centre
BEARING_CENTRE_FAR = -75.0        # floating bearing centre
BEARING_WIDTH = 18.0
BEARING_OD = 80.0
BEARING_BORE = 40.0

Z_BEARING_DRIVE_BACK = 66.0       # shaft collar face / housing bore shoulder
Z_BEARING_DRIVE_FRONT = 84.0      # circlip face / cover spigot front face
Z_BEARING_FAR_BACK = -84.0
Z_BEARING_FAR_FRONT = -66.0       # housing far shoulder sits at -64.5 -> 1.5 float

Z_CIRCLIP_BACK = 84.0             # groove runs z = +84.0 .. +85.85 (1.85 wide)
CIRCLIP_THK = 1.75
CIRCLIP_ID = 37.5
CIRCLIP_OD = 43.5

Z_SEAL_BACK = 90.0                # cover seal pocket, seal spans +90 .. +100
SEAL_WIDTH = 10.0
SEAL_OD = 62.0
SEAL_ID = 40.0

Z_COVER_OUTER_FACE = 107.0        # M8 cap-screw head underside bears here

# --- M8 x 25 cover cap screws -----------------------------------------
M8_BOLT_CIRCLE_R = 52.0           # bolt circle dia 104
M8_ANGLES_DEG = (45.0, 135.0, 225.0, 315.0)
M8_HEAD_D, M8_HEAD_H = 13.0, 8.0
M8_SHANK_D, M8_SHANK_L = 8.0, 25.0   # 12 through the flange + 13 into the thread

# --- M12 x 40 foundation bolts ----------------------------------------
Y_FOOT_TOP = -60.0                # foot plate top face: head underside bears here
M12_X = (-45.0, 45.0)
M12_Z = (-55.0, 55.0)   # moved from +/-75: the dia-130 drive-end boss (z=+75..+95) overhung the +75 heads
M12_HEAD_D, M12_HEAD_H = 18.0, 7.5
M12_SHANK_D, M12_SHANK_L = 12.0, 40.0   # down to Y = -100 into the foundation

# --- Grease nipples M8x1 DIN 71412 form A ------------------------------
Y_BOSS_TOP = 70.0                 # housing boss top faces; nipple tops at Y = +82
NIPPLE_Z = (-70.0, 70.0)
NIPPLE_HEX_AF, NIPPLE_HEX_H = 11.0, 6.0
NIPPLE_BALL_D, NIPPLE_BALL_H = 6.5, 6.0

# Rotation that maps a part's local +Z onto global +Y (for the radial items
# that stand along the vertical axis: foundation bolts and grease nipples).
X_AXIS = cq.Vector(1, 0, 0)
LOCAL_Z_TO_GLOBAL_Y = -90.0


# =====================================================================
# MAKE PARTS -- loaded from part.py, never copy-pasted
# =====================================================================
def load_part(part_name):
    """Execute a part.py in this project and return its `result` solid."""
    part_file = __project_path__ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError("Part not found: {}".format(part_file))
    ns = {}
    exec(part_file.read_text(), ns)
    return ns["result"]


shaft = load_part("shaft")        # z = -135 .. +165, max dia 48
housing = load_part("housing")    # z =  -95 ..  +95, bbox X130 / Y145 / Z190
cover = load_part("cover")        # z =  +84 .. +107, dia 130

IDENTITY = cq.Location()


# =====================================================================
# BUY PARTS -- representative catalogue primitives
# =====================================================================
def annulus(outer_d, inner_d, width):
    """Ring on the Z axis spanning local z = 0 .. width."""
    return (cq.Workplane("XY")
            .circle(outer_d / 2.0)
            .circle(inner_d / 2.0)
            .extrude(width))


def hex_head_fastener(head_d, head_h, shank_d, shank_l):
    """Fastener with the head UNDERSIDE at local z = 0:
    head runs z = 0 .. +head_h, shank runs z = 0 .. -shank_l."""
    head = cq.Workplane("XY").circle(head_d / 2.0).extrude(head_h)
    shank = cq.Workplane("XY").circle(shank_d / 2.0).extrude(-shank_l)
    return head.union(shank)


def grease_nipple():
    """DIN 71412 form A, representative: hex body + ball head,
    standing on local z = 0, total height 12."""
    body = (cq.Workplane("XY")
            .polygon(6, NIPPLE_HEX_AF, circumscribed=True)
            .extrude(NIPPLE_HEX_H))
    ball = (cq.Workplane("XY")
            .circle(NIPPLE_BALL_D / 2.0)
            .extrude(NIPPLE_BALL_H)
            .translate((0, 0, NIPPLE_HEX_H)))
    return body.union(ball)


bearing_6208 = annulus(BEARING_OD, BEARING_BORE, BEARING_WIDTH)
circlip_din471_40 = annulus(CIRCLIP_OD, CIRCLIP_ID, CIRCLIP_THK)
lip_seal_40x62x10 = annulus(SEAL_OD, SEAL_ID, SEAL_WIDTH)
cap_screw_m8x25 = hex_head_fastener(M8_HEAD_D, M8_HEAD_H, M8_SHANK_D, M8_SHANK_L)
bolt_m12x40 = hex_head_fastener(M12_HEAD_D, M12_HEAD_H, M12_SHANK_D, M12_SHANK_L)
nipple_m8 = grease_nipple()


# =====================================================================
# COMPOSE
# =====================================================================
assy = (
    cq.Assembly()
    # --- Make parts: identity, all three already in the global frame ---
    .add(housing, name="housing", loc=IDENTITY, color=cq.Color("gray"))
    .add(shaft, name="shaft", loc=IDENTITY, color=cq.Color("lightgray"))
    .add(cover, name="cover", loc=IDENTITY, color=cq.Color("blue"))
    # --- Rolling elements -------------------------------------------
    .add(bearing_6208, name="bearing_drive_end",
         loc=cq.Location(cq.Vector(0, 0, Z_BEARING_DRIVE_BACK)),
         color=cq.Color("orange"))
    .add(bearing_6208, name="bearing_far_end",
         loc=cq.Location(cq.Vector(0, 0, Z_BEARING_FAR_BACK)),
         color=cq.Color("orange"))
    # --- Retention + sealing -----------------------------------------
    .add(circlip_din471_40, name="circlip_din471_40",
         loc=cq.Location(cq.Vector(0, 0, Z_CIRCLIP_BACK)),
         color=cq.Color("red"))
    .add(lip_seal_40x62x10, name="lip_seal_40x62x10",
         loc=cq.Location(cq.Vector(0, 0, Z_SEAL_BACK)),
         color=cq.Color("magenta"))
)

# --- 4x M8 x 25 cover cap screws, bolt circle dia 104 at 45/135/225/315 ---
for angle_deg in M8_ANGLES_DEG:
    theta = math.radians(angle_deg)
    assy.add(
        cap_screw_m8x25,
        name="cap_screw_m8x25_{:03.0f}".format(angle_deg),
        loc=cq.Location(cq.Vector(M8_BOLT_CIRCLE_R * math.cos(theta),
                                  M8_BOLT_CIRCLE_R * math.sin(theta),
                                  Z_COVER_OUTER_FACE)),
        color=cq.Color("yellow"),
    )

# --- 4x M12 x 40 foundation bolts, heads on the foot plate top face ---
for bolt_x in M12_X:
    for bolt_z in M12_Z:
        assy.add(
            bolt_m12x40,
            name="bolt_m12x40_x{:+.0f}_z{:+.0f}".format(bolt_x, bolt_z),
            loc=cq.Location(cq.Vector(bolt_x, Y_FOOT_TOP, bolt_z),
                            X_AXIS, LOCAL_Z_TO_GLOBAL_Y),
            color=cq.Color("green"),
        )

# --- 2x grease nipples standing on the housing boss top faces ---------
for nipple_z in NIPPLE_Z:
    assy.add(
        nipple_m8,
        name="grease_nipple_z{:+.0f}".format(nipple_z),
        loc=cq.Location(cq.Vector(0, Y_BOSS_TOP, nipple_z),
                        X_AXIS, LOCAL_Z_TO_GLOBAL_Y),
        color=cq.Color("cyan"),
    )

result = assy.toCompound()
