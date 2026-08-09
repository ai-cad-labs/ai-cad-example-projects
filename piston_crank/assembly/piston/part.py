import cadquery as cq

# ============================================================================
# PISTON — flat-crown aluminum piston, CNC_milling (Al 6061)
# Coordinate convention (per constraints.md): piston axis = Z, centered at
# origin. Crown top at Z=+27.5, skirt bottom at Z=-27.5, gudgeon-pin bore
# along X through (0, 0, -4.5).
# ============================================================================

# === PARAMETERS ===

# -- Primary envelope --
piston_od = 60.0                       # mm, skirt OD (constant, no barrel)
piston_height = 55.0                   # mm, crown top to skirt bottom
crown_top_z = piston_height / 2.0      # +27.5 (centered on origin)
skirt_bottom_z = -piston_height / 2.0  # -27.5

# -- Crown / skirt walls --
crown_thickness = 8.0                  # mm, solid flat crown
skirt_inner_dia = 54.0                 # mm -> 3.0 mm skirt wall
min_wall = 3.0                         # mm, project minimum wall everywhere

# -- Ring grooves (3x identical rectangular, turned into OD near crown) --
groove_axial = 2.6                     # mm axial height (2.5 ring + 0.1)
groove_root_dia = 54.0                 # mm -> radial depth 3.0 from OD 60
top_land = 5.0                         # mm, crown top to top of groove 1
inter_groove_land = 3.0                # mm between grooves
n_grooves = 3

# -- Ring-belt internal wall (DISCOVERED CONSTRAINT, see notes.md) --
# Literal constraints (skirt inner d54 immediately below the 8 mm crown AND
# groove root d54) give ZERO wall behind grooves 2 and 3 -> the ring belt
# would be fully severed and the piston would split into two bodies.
# Resolution: stepped interior. Behind the ring belt the cavity is d47
# (3.5 mm wall behind the 3.0 mm-deep grooves, > 3.0 min wall); the full
# d54 hollow starts min_wall below the bottom of groove 3.
ring_belt_inner_dia = 47.0

# -- Pin bosses / gudgeon-pin bore --
compression_height = 32.0              # mm, crown top to pin axis
pin_axis_z = crown_top_z - compression_height  # -4.5
pin_bore_dia = 16.02                   # clearance bore for d16.0 pin (15.99)
boss_inner_gap = 22.0                  # mm between boss inner faces
boss_outer_span = 48.0                 # mm across boss outer faces
boss_od = 26.0                         # mm, boss cylinder around the bore
web_width = 28.0                       # mm, hanger web (Y width); > boss_od so web fully covers boss (no undercut above boss; DFM-GEN-002 fix)
                                       # to avoid tangent boolean surfaces

# === DERIVED VALUES ===
crown_underside_z = crown_top_z - crown_thickness              # +19.5
groove_belt_bottom = top_land + n_grooves * groove_axial + (n_grooves - 1) * inter_groove_land
                                                               # 18.8 below crown
ring_belt_step_z = crown_top_z - groove_belt_bottom - min_wall  # +5.7
boss_inner_x = boss_inner_gap / 2.0    # 11.0
boss_outer_x = boss_outer_span / 2.0   # 24.0
boss_length = boss_outer_x - boss_inner_x  # 13.0 each

# Groove Z-bands (bottom edge, below crown top): 5.0-7.6, 10.6-13.2, 16.2-18.8
groove_bottoms_z = [
    crown_top_z - (top_land + (i + 1) * groove_axial + i * inter_groove_land)
    for i in range(n_grooves)
]  # [19.9, 14.3, 8.7]


# === FEATURE FUNCTIONS ===

def piston_blank():
    """Solid cylindrical stock: d60 x 55, centered on Z, crown top at +27.5."""
    return (
        cq.Workplane("XY")
        .workplane(offset=skirt_bottom_z)
        .circle(piston_od / 2.0)
        .extrude(piston_height)
    )


def interior_cavity_cutter():
    """Stepped internal void: d47 behind the ring belt (keeps >=3 mm wall
    behind the d54-root grooves), d54 through the skirt below it, open at
    the skirt bottom. Solid crown (8 mm) is left untouched above."""
    # Lower (skirt) bore: d54 from below the skirt bottom up to the step
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=skirt_bottom_z - 1.0)
        .circle(skirt_inner_dia / 2.0)
        .extrude((ring_belt_step_z - skirt_bottom_z) + 1.0)
    )
    # Upper (ring-belt) bore: d47 from the step up to the crown underside
    cutter = cutter.union(
        cq.Workplane("XY")
        .workplane(offset=ring_belt_step_z)
        .circle(ring_belt_inner_dia / 2.0)
        .extrude(crown_underside_z - ring_belt_step_z)
    )
    return cutter


def pin_boss_solids():
    """Two internal pin bosses on the X axis at Z = pin_axis_z: d26 cylinder
    from |x|=11 to |x|=24 (inner gap 22, outer span 48), each hung from the
    crown underside by a rectangular web. Bosses do NOT reach the skirt
    inner wall (pin sits fully inside the d54 skirt bore)."""
    bosses = None
    for sign in (+1, -1):
        # Boss cylinder around the future pin bore
        cyl = (
            cq.Workplane("YZ")
            .workplane(offset=sign * boss_inner_x)
            .center(0, pin_axis_z)
            .circle(boss_od / 2.0)
            .extrude(sign * boss_length)
        )
        # Hanger web: from pin axis up into the crown underside
        web_top_z = crown_underside_z + 0.1  # overlap into crown for clean union
        web_height = web_top_z - pin_axis_z
        web = (
            cq.Workplane("YZ")
            .workplane(offset=sign * boss_inner_x)
            .center(0, pin_axis_z + web_height / 2.0)
            .rect(web_width, web_height)
            .extrude(sign * boss_length)
        )
        boss = cyl.union(web)
        bosses = boss if bosses is None else bosses.union(boss)
    return bosses


def hollow_interior_keeping_bosses(body):
    """Cut the stepped cavity, but protect the boss volumes so they remain
    as solid material attached to the crown (cutter = cavity - bosses)."""
    cutter = interior_cavity_cutter().cut(pin_boss_solids())
    return body.cut(cutter)


def ring_grooves(body):
    """Three rectangular grooves turned into the OD: 2.6 axial x 3.0 radial
    deep (root d54.0), at 5.0-7.6, 10.6-13.2, 16.2-18.8 below the crown."""
    for z_bottom in groove_bottoms_z:
        annulus = (
            cq.Workplane("XY")
            .workplane(offset=z_bottom)
            .circle(piston_od / 2.0 + 1.0)      # outer: clear of OD
            .circle(groove_root_dia / 2.0)       # inner: groove root
            .extrude(groove_axial)
        )
        body = body.cut(annulus)
    return body


def gudgeon_pin_bore(body):
    """Through d16.02 clearance bore along X through both bosses at
    Z = -4.5. Cutter spans only the boss region (+/-25) so it can NEVER
    break through the d60 skirt OD (skirt wall starts at radius 27)."""
    cutter_half_len = boss_outer_x + 1.0  # 25.0 < 27 -> skirt untouched
    bore = (
        cq.Workplane("YZ")
        .workplane(offset=-cutter_half_len)
        .center(0, pin_axis_z)
        .circle(pin_bore_dia / 2.0)
        .extrude(2.0 * cutter_half_len)
    )
    return body.cut(bore)


# === COMPOSE (reads like the manufacturing process plan) ===
body = piston_blank()                      # turn stock d60 x 55
body = hollow_interior_keeping_bosses(body)  # bore stepped interior, leave bosses
body = ring_grooves(body)                  # turn 3 ring grooves into OD
body = gudgeon_pin_bore(body)              # line-bore d16.02 through bosses
result = body
