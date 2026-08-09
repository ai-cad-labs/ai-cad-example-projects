import cadquery as cq

# ============================================================
# Single-throw crankshaft — one-piece, Steel 304
# CNC_turning (journals, web ODs) + CNC_milling (offset crank pin)
#
# Coordinate convention (project Principle 0):
#   MAIN (rotation) axis = Z, part centered at origin -> Z spans +/-46.0
#   Crank pin axis parallel to Z through (throw, 0, 0) = (30, 0, 0)
#   Throw direction = +X, matching the TDC assembly pose in design_plan.md
#
# Axial stack (bottom -> top along Z):
#   25 journal | 10 web | 22 crank pin span | 10 web | 25 journal = 92 mm
# NO fillets (deferred project-wide). NO threads, NO oil holes (v1).
# ============================================================

# === PARAMETERS (all mm) ===
# PRIMARY dimensions (from constraints.md)
main_journal_dia = 30.0      # both main journals, coaxial on Z
main_journal_len = 25.0      # each journal
web_dia = 100.0              # web / counterweight discs (v1: full discs)
web_thickness = 10.0         # each web
crank_pin_dia = 38.0         # rod big-end interface (bore 38.05, rotating clearance)
crank_pin_span = 22.0        # FREE length between web INNER faces (rod big end 20 + 1/side)
crank_throw = 30.0           # pin axis offset from main axis (stroke = 60)

# DERIVED values
overall_length = 2 * main_journal_len + 2 * web_thickness + crank_pin_span  # 92.0
half_length = overall_length / 2.0                                          # 46.0
web_inner_z = crank_pin_span / 2.0                                          # 11.0 (web inner faces at Z = +/-11)
web_outer_z = web_inner_z + web_thickness                                   # 21.0

# GEOMETRY-STABILITY overlap (Cookbook Principle 1): embed each cylinder 1 mm
# into its neighboring web so the union never relies on exactly-coincident faces.
# The embeds are invisible externally: journals (r15) and pin (extremity at
# 30 + 19 = 49) are both fully inside the web silhouette (r50).
embed = 1.0

# Sanity: pin outer extremity must stay inside the web disc
assert crank_throw + crank_pin_dia / 2.0 <= web_dia / 2.0, "crank pin escapes web OD"


# === FEATURE FUNCTIONS ===
def main_journal(z_inner_face, direction):
    """One 30x25 main journal on the Z-axis; grows outward from a web outer face.

    z_inner_face: Z of the web outer face this journal sits on (+/-21.0)
    direction: +1 for the top journal, -1 for the bottom journal
    """
    length = main_journal_len + embed  # embed 1 mm into the web
    journal = (
        cq.Workplane("XY")
        .circle(main_journal_dia / 2.0)
        .extrude(direction * length)
        .translate((0, 0, z_inner_face - direction * embed))
    )
    return journal


def web_disc(z_inner_face, direction):
    """One 100x10 full web disc centered on the main axis (counterweight cutouts deferred).

    z_inner_face: Z of the web INNER face (+/-11.0); disc grows outward from it.
    """
    web = (
        cq.Workplane("XY")
        .circle(web_dia / 2.0)
        .extrude(direction * web_thickness)
        .translate((0, 0, z_inner_face))
    )
    return web


def crank_pin():
    """38 dia crank pin at 30 mm throw, axis parallel to Z through (30, 0).

    Free span Z = -11..+11 (22 mm for the 20 mm rod big end); the solid is
    extended 1 mm into each web so the one-piece union is robust.
    """
    length = crank_pin_span + 2 * embed
    pin = (
        cq.Workplane("XY")
        .circle(crank_pin_dia / 2.0)
        .extrude(length)
        .translate((crank_throw, 0, -length / 2.0))
    )
    return pin


# === COMPOSE (reads like the physical stack, bottom -> top) ===
body = main_journal(-web_outer_z, -1)            # bottom journal, Z -46..-21
body = body.union(web_disc(-web_inner_z, -1))    # bottom web,     Z -21..-11
body = body.union(crank_pin())                   # crank pin,      Z -11..+11 free span, at (30, 0)
body = body.union(web_disc(+web_inner_z, +1))    # top web,        Z +11..+21
body = body.union(main_journal(+web_outer_z, +1))  # top journal,  Z +21..+46

result = body
