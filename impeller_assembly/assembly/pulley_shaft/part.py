import cadquery as cq

# ============================================================================
# pulley_shaft — integrated grooved pulley + stepped shaft, ONE turned part
#
# Coordinate convention (constraints.md, LOCKED):
#   axis of revolution = Z; Z = 0 at the CLAMP SHOULDER FACE (the Ø14→Ø10
#   annular step) — the assembly datum. +Z toward the inlet/nose end.
#   The assembly resolver places this part by that datum (local 0 → global −14).
#
# Design intent: single-setup CNC turning from Ø50 bar stock. All segments are
# one revolved profile; the round-belt U-groove is a torus cut in the pulley rim.
# The M10x1.5 nose thread is modeled as a PLAIN Ø10 cylinder (annotation-level
# thread — major 10.0 equals the impeller-seat diameter, so seat + thread form
# one continuous Ø10 land in CAD). NO fillets/chamfers: deferred project-wide.
# ============================================================================

# === PARAMETERS (all mm; segment table from constraints.md, LOCKED) ===

# Diameters
D_LEFT_STUB = 14.0            # left stub, outboard of the pulley
D_PULLEY = 48.0               # pulley max diameter
D_SHAFT_SHOULDER = 14.0       # mid-section through the housing back-bore (Ø34)
D_SHAFT_IMPELLER_SEAT = 10.0  # impeller seat; ALSO the thread major (no step-up)
D_THREAD_MAJOR = 10.0         # M10x1.5 external major — modeled plain
D_SHAFT_INLET_SEAT = 8.0      # tail for the 688 inlet bearing (8 x 16 x 5)

# Segment lengths, left (−Z) to right (+Z)
L_LEFT_STUB = 8.0
L_PULLEY = 12.0
L_MID_SECTION = 24.0
L_IMPELLER_SEAT = 45.0
L_NOSE_THREAD = 14.0
L_INLET_TAIL = 15.0

# Belt groove (round-belt U-groove, centered on the pulley width)
GROOVE_TUBE_R = 3.5           # groove (belt) radius
D_GROOVE_ROOT = 40.0          # diameter at groove root

# Clamp-stack closure (verify only — the plan's LOCKED grip length)
L_IMP_GRIP = 48.8             # shoulder face -> nut seating face
NUT_HEIGHT = 8.4              # ISO 4032 M10 max height (BOM)

# === DERIVED Z STATIONS (datum: Z = 0 at the clamp shoulder face) ===
Z_SHOULDER = 0.0
Z_MID_LEFT = Z_SHOULDER - L_MID_SECTION            # -24  (pulley right face)
Z_PULLEY_LEFT = Z_MID_LEFT - L_PULLEY              # -36
Z_LEFT_END = Z_PULLEY_LEFT - L_LEFT_STUB           # -44  (leftmost face)
Z_THREAD_START = Z_SHOULDER + L_IMPELLER_SEAT      # +45
Z_THREAD_END = Z_THREAD_START + L_NOSE_THREAD      # +59
Z_TAIL_END = Z_THREAD_END + L_INLET_TAIL           # +74  (rightmost face)
Z_GROOVE_CENTER = (Z_PULLEY_LEFT + Z_MID_LEFT) / 2 # -30  (pulley mid-width)

TOTAL_LENGTH = Z_TAIL_END - Z_LEFT_END             # 118

# Self-check the LOCKED axial chain before any geometry is built
assert Z_LEFT_END == -44.0, f"left end {Z_LEFT_END} != -44"
assert Z_TAIL_END == 74.0, f"tail end {Z_TAIL_END} != 74"
assert TOTAL_LENGTH == 118.0, f"total length {TOTAL_LENGTH} != 118"
# Nut seating face must land ON the thread, with the nut fully on-thread
NUT_SEAT_Z = Z_SHOULDER + L_IMP_GRIP               # +48.8
assert Z_THREAD_START < NUT_SEAT_Z < Z_THREAD_END, "nut seat off-thread"
assert NUT_SEAT_Z + NUT_HEIGHT <= Z_THREAD_END, "nut overhangs thread end"
assert D_GROOVE_ROOT / 2 + 2 * GROOVE_TUBE_R > D_PULLEY / 2, \
    "groove torus must break through the pulley rim"


# === FEATURE FUNCTIONS ===

def stepped_shaft_body():
    """The full turned profile: 6 cylindrical segments as ONE revolve.

    Half cross-section drawn in the XZ plane (local x = radius,
    local y = global Z), revolved 360 deg about the Z axis — mirrors the
    single-setup turning operation that makes the real part.
    """
    r_stub = D_LEFT_STUB / 2
    r_pulley = D_PULLEY / 2
    r_mid = D_SHAFT_SHOULDER / 2
    r_seat = D_SHAFT_IMPELLER_SEAT / 2   # == thread major radius
    r_tail = D_SHAFT_INLET_SEAT / 2

    profile = (
        cq.Workplane("XZ")
        .polyline([
            (0.0, Z_LEFT_END),           # start ON the axis (left end)
            (r_stub, Z_LEFT_END),        # left stub end face
            (r_stub, Z_PULLEY_LEFT),     # left stub OD
            (r_pulley, Z_PULLEY_LEFT),   # pulley left face
            (r_pulley, Z_MID_LEFT),      # pulley rim (groove cut separately)
            (r_mid, Z_MID_LEFT),         # pulley right face
            (r_mid, Z_SHOULDER),         # mid-section OD (through housing bore)
            (r_seat, Z_SHOULDER),        # CLAMP SHOULDER FACE — assembly datum
            (r_seat, Z_THREAD_END),      # impeller seat + plain-modeled thread
            (r_tail, Z_THREAD_END),      # Ø10 -> Ø8 step
            (r_tail, Z_TAIL_END),        # inlet-bearing tail OD
            (0.0, Z_TAIL_END),           # tail end face
        ])
        .close()  # closes (0, +74) -> (0, -44) ALONG THE AXIS
    )
    return profile.revolve(360, (0, 0, 0), (0, 1, 0))


def belt_groove(body):
    """Round-belt U-groove in the pulley rim: a torus cut.

    Tube radius 3.5, deepest point at the groove root Ø40 -> torus
    center-circle radius = 40/2 + 3.5 = 23.5. Centered on the pulley
    width (Z = -30). The torus breaks through the Ø48 rim leaving a
    ~6.9 mm wide U-opening — no sharp undercut, single-point turnable.
    """
    torus_major_r = D_GROOVE_ROOT / 2 + GROOVE_TUBE_R
    cutter = cq.Solid.makeTorus(
        torus_major_r,
        GROOVE_TUBE_R,
        pnt=cq.Vector(0, 0, Z_GROOVE_CENTER),
        dir=cq.Vector(0, 0, 1),
    )
    return body.cut(cutter)


# === COMPOSE (reads as the turning process plan) ===
body = stepped_shaft_body()   # turn all diameters between centers
body = belt_groove(body)      # form the belt groove with a radius tool

result = body
