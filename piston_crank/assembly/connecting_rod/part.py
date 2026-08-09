import cadquery as cq

# =============================================================================
# connecting_rod — one-piece steel con-rod, I-beam shank, CNC milled
#
# Coordinate convention (per constraints.md):
#   BIG END bore axis = Z through origin (0,0,0)
#   Rod long axis = +X; small end bore axis = Z-parallel line through (95, 0, 0)
#   Width (plate thickness) centered on Z = +/-10.0
# =============================================================================

# === PARAMETERS ===
# -- primary (from constraints.md) --
center_distance = 95.0        # mm, small end bore axis to big end bore axis

big_end_od = 52.0             # mm, big end boss outer diameter
big_end_bore_dia = 38.05      # mm, rotating clearance on crank pin (pin 38.0)
big_end_width = 20.0          # mm, fits in 22.0 crank pin span (1.0 mm/side)

small_end_od = 26.0           # mm, small end boss outer diameter
small_end_bore_dia = 16.02    # mm, full-floating clearance (gudgeon pin 15.99)
small_end_width = 20.0        # mm, fits between piston boss faces 22.0 apart

shank_section_width = 16.0    # mm, I-beam overall section width (Y)
shank_section_depth = 20.0    # mm, I-beam overall section depth (Z = plate thickness)
flange_thickness = 4.0        # mm, top/bottom flange thickness (Z)
web_thickness = 5.0           # mm, central web thickness (Y)

# -- derived --
rod_width = big_end_width                 # 20.0 — single-thickness plate blank
pocket_depth = (shank_section_width - web_thickness) / 2.0   # 5.5 mm into each +/-Y face
pocket_height = shank_section_depth - 2.0 * flange_thickness  # 12.0 mm in Z
pocket_x_start = big_end_od / 2.0                             # 26.0 — clear of big end OD
pocket_x_end = center_distance - small_end_od / 2.0           # 82.0 — clear of small end OD
pocket_length = pocket_x_end - pocket_x_start                 # 56.0
overcut = 1.0                 # mm, cutter margin past faces for clean booleans

# === FEATURE FUNCTIONS ===

def big_end_boss():
    """Cylindrical big end eye blank, OD 52, on the Z-axis at the origin."""
    return (
        cq.Workplane("XY")
        .workplane(offset=-rod_width / 2.0)
        .circle(big_end_od / 2.0)
        .extrude(rod_width)
    )


def small_end_boss():
    """Cylindrical small end eye blank, OD 26, axis at (center_distance, 0)."""
    return (
        cq.Workplane("XY")
        .workplane(offset=-rod_width / 2.0)
        .center(center_distance, 0)
        .circle(small_end_od / 2.0)
        .extrude(rod_width)
    )


def shank_blank():
    """Rectangular shank stock joining the eyes: 16 wide (Y) x 20 deep (Z),
    running the full center distance along X (booleans absorb the overlap)."""
    return (
        cq.Workplane("XY")
        .box(center_distance, shank_section_width, shank_section_depth)
        .translate((center_distance / 2.0, 0, 0))
    )


def i_beam_pockets(body):
    """Mill a pocket into each +/-Y side face of the shank, leaving 4 mm
    flanges (top/bottom) and a 5 mm central web -> I-beam section.
    Pockets span X 26..82, staying clear of both eye ODs."""
    pocket_x_center = (pocket_x_start + pocket_x_end) / 2.0
    cutter_width = pocket_depth + overcut  # 5.5 deep + margin past the face
    # +Y side pocket: from pocket floor (Y = web/2) outward past the face
    cutter_y_center = web_thickness / 2.0 + cutter_width / 2.0
    pocket_plus_y = (
        cq.Workplane("XY")
        .box(pocket_length, cutter_width, pocket_height)
        .translate((pocket_x_center, cutter_y_center, 0))
    )
    pocket_minus_y = (
        cq.Workplane("XY")
        .box(pocket_length, cutter_width, pocket_height)
        .translate((pocket_x_center, -cutter_y_center, 0))
    )
    return body.cut(pocket_plus_y).cut(pocket_minus_y)


def big_end_bore(body):
    """Through bore 38.05 for the crank pin (rotating clearance), on Z at origin."""
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=-(rod_width / 2.0 + overcut))
        .circle(big_end_bore_dia / 2.0)
        .extrude(rod_width + 2.0 * overcut)
    )
    return body.cut(cutter)


def small_end_bore(body):
    """Through bore 16.02 for the gudgeon pin (full-floating clearance).
    Plain bore in v1 — the bronze bushing is a Buy item, not modeled."""
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=-(rod_width / 2.0 + overcut))
        .center(center_distance, 0)
        .circle(small_end_bore_dia / 2.0)
        .extrude(rod_width + 2.0 * overcut)
    )
    return body.cut(cutter)


# === COMPOSE (reads as the milling process plan) ===
body = big_end_boss()                    # 1. big end eye blank
body = body.union(small_end_boss())     # 2. small end eye blank
body = body.union(shank_blank())        # 3. rectangular shank stock between eyes
body = i_beam_pockets(body)             # 4. mill I-beam pockets from both side faces
body = big_end_bore(body)               # 5. finish-bore big end (38.05)
body = small_end_bore(body)             # 6. finish-bore small end (16.02)

result = body
