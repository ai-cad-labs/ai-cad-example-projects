"""Conveyor support unit - 40 mm steel drive shaft (CNC turning).

One solid of revolution, modelled DIRECTLY in the assembly's global frame:
shaft axis = global Z, drive end = +Z, origin midway between the two
6208 bearing centres (centres at z = -75 and z = +75).
The assembly places this part with an identity transform.

Built as a SINGLE revolve of one closed (radius, z) profile. No booleans,
no edge selection, no fillets: every chamfer and the circlip groove are
explicit profile geometry, so nothing depends on fragile edge selectors.
"""

import cadquery as cq

# === PARAMETERS (primary, all mm) ===
D_SEAT = 40.0  # bearing seat / seal journal diameter (40 k6)
D_MID = 45.0  # mid-body diameter between the bearings
D_COLLAR = 48.0  # thrust collar OD (max diameter on the part)
D_EXT = 35.0  # plain pulley extension diameter (taper-lock hub)
D_CIRCLIP = 37.5  # circlip groove floor dia (DIN 471 - 40 x 1.75)

BEARING_W = 18.0  # 6208 width: THE clamp dimension, drive end has zero float
W_CIRCLIP = 1.85  # circlip groove width
W_COLLAR = 6.0  # thrust collar axial length
CH = 1.0  # all chamfers are 1 x 45 deg

Z_FAR_END = -135.0  # far (non-drive) end face
Z_DRIVE_END = 165.0  # drive end face
Z_FE_SHOULDER = -66.0  # far-end bearing shoulder face (bearing sits -84..-66)
Z_DE_SHOULDER = 66.0  # drive-end bearing shoulder = collar front face
Z_STEP_EXT = 120.0  # dia 40 -> dia 35 step
Z_SEAL_START = 90.0  # seal journal runs +90..+100 on the dia 40 face
Z_SEAL_END = 100.0  # (callout only: ground Ra <= 0.4, no geometry change)

# === DERIVED VALUES ===
R_SEAT = D_SEAT / 2.0
R_MID = D_MID / 2.0
R_COLLAR = D_COLLAR / 2.0
R_EXT = D_EXT / 2.0
R_CIRCLIP = D_CIRCLIP / 2.0

Z_DE_SEAT_END = Z_DE_SHOULDER + BEARING_W  # = +84: circlip groove front wall
Z_CIRCLIP_END = Z_DE_SEAT_END + W_CIRCLIP  # = +85.85
Z_COLLAR_BACK = Z_DE_SHOULDER - W_COLLAR  # = +60: collar back face
Z_FE_SEAT_START = Z_FE_SHOULDER - BEARING_W  # = -84 (seat runs past it to the end)

LENGTH = Z_DRIVE_END - Z_FAR_END  # 300.0


# === PROFILE SEGMENTS (each returns (radius, z) points, far end -> drive end) ===
def far_end_and_bearing_seat():
    """Chamfered far end face, then the dia 40 far-end bearing seat (40 k6).

    The seat runs from the end face to the shoulder, so the bearing at
    z = -84..-66 is fully supported with run-out to spare.
    """
    return [
        (0.0, Z_FAR_END),  # end face, on axis
        (R_SEAT - CH, Z_FAR_END),  # out to the chamfer root
        (R_SEAT, Z_FAR_END + CH),  # 1 x 45 lead-in chamfer
        (R_SEAT, Z_FE_SHOULDER - CH),  # dia 40 seat
    ]


def far_bearing_shoulder_and_mid_body():
    """Chamfered locating shoulder at z = -66, then the dia 45 mid body.

    The shoulder chamfer clears the bearing's own corner radius so the
    inner ring seats flat on the shoulder face.
    """
    return [
        (R_SEAT + CH, Z_FE_SHOULDER),  # shoulder chamfer root
        (R_MID, Z_FE_SHOULDER),  # shoulder face out to dia 45
        (R_MID, Z_COLLAR_BACK),  # dia 45 mid body
    ]


def thrust_collar():
    """Square dia 48 collar, +60..+66. Its front face is the drive-end
    bearing shoulder and takes the belt-pull thrust (no chamfer by design).
    """
    return [
        (R_COLLAR, Z_COLLAR_BACK),  # step up to dia 48
        (R_COLLAR, Z_DE_SHOULDER),  # collar OD, 6 long
        (R_SEAT + CH, Z_DE_SHOULDER),  # collar front face in to the chamfer root
    ]


def drive_bearing_seat_and_circlip_groove():
    """Dia 40 drive-end seat (+66..+84) plus the DIN 471 circlip groove.

    Collar face to groove wall is exactly BEARING_W: the drive-end bearing
    is axially clamped with zero float. This is the critical dimension.
    """
    return [
        (R_SEAT, Z_DE_SHOULDER + CH),  # 1 x 45 shoulder chamfer
        (R_SEAT, Z_DE_SEAT_END),  # dia 40 seat, bearing +66..+84
        (R_CIRCLIP, Z_DE_SEAT_END),  # groove rear wall
        (R_CIRCLIP, Z_CIRCLIP_END),  # groove floor, dia 37.5 x 1.85
        (R_SEAT, Z_CIRCLIP_END),  # groove front wall
    ]


def seal_journal_and_step():
    """Dia 40 continues to z = +120 (the seal journal is +90..+100 on this
    face, ground only - no geometry), then steps down to the extension.
    """
    return [
        (R_SEAT, Z_STEP_EXT),  # dia 40 through the seal journal
        (R_EXT + CH, Z_STEP_EXT),  # step face down to the chamfer root
        (R_EXT, Z_STEP_EXT + CH),  # 1 x 45 chamfer at the dia 40 -> 35 step
    ]


def pulley_extension():
    """Plain dia 35 extension for a taper-lock hub: no keyway, no flats."""
    return [
        (R_EXT, Z_DRIVE_END - CH),  # dia 35 plain extension
        (R_EXT - CH, Z_DRIVE_END),  # 1 x 45 chamfer at the drive end face
        (0.0, Z_DRIVE_END),  # end face, on axis
    ]


# === COMPOSE (reads as a turning sequence, far end -> drive end) ===
PROFILE = (
    far_end_and_bearing_seat()
    + far_bearing_shoulder_and_mid_body()
    + thrust_collar()
    + drive_bearing_seat_and_circlip_groove()
    + seal_journal_and_step()
    + pulley_extension()
)

# cq.Workplane("XZ") maps local (u, v) -> global (u, 0, v), so profile points
# are (radius, z). The revolve axis args are LOCAL coords: local (0,0)->(0,1)
# is the global Z axis. (Local (0,0,1) would be the plane normal = global -Y.)
result = cq.Workplane("XZ").polyline(PROFILE).close().revolve(360.0, (0, 0), (0, 1))

try:  # harness convention: some viewers execute this file directly
    show_object(result)  # noqa: F821
except NameError:
    pass


if __name__ == "__main__":
    bb = result.val().BoundingBox()
    vol = result.val().Volume()
    print(f"bbox  x={bb.xlen:.3f} y={bb.ylen:.3f} z={bb.zlen:.3f}")
    print(f"zmin={bb.zmin:.3f} zmax={bb.zmax:.3f}")
    print(f"volume={vol:.1f} mm^3   solids={result.solids().size()}")
    print(f"collar face -> circlip wall = {Z_DE_SEAT_END - Z_DE_SHOULDER:.3f} mm")

    assert result.solids().size() == 1, "must be one solid"
    assert abs(bb.xlen - D_COLLAR) < 1e-3, bb.xlen
    assert abs(bb.ylen - D_COLLAR) < 1e-3, bb.ylen
    assert abs(bb.zlen - LENGTH) < 1e-3, bb.zlen
    assert abs(bb.zmin - Z_FAR_END) < 1e-3, bb.zmin
    assert abs(bb.zmax - Z_DRIVE_END) < 1e-3, bb.zmax
    assert abs((Z_DE_SEAT_END - Z_DE_SHOULDER) - BEARING_W) < 1e-9, "zero float"
    assert vol > 0.0
    print("ALL CHECKS PASS")
