import cadquery as cq

# === PARAMETERS (primary — independent) ===
block_x = 30.0   # width along hinge axis (X)
block_y = 25.0   # stand-off depth (Y)
block_z = 30.0   # height (Z)

pin_bore_dia = 4.0     # ⌀4 hinge rotation axle, through full X
pin_bore_z = 15.0      # mid-height → assembled Z=80

mount_hole_dia = 3.2   # M3 clearance, through full Y
mount_hole_x = 8.0     # X-spacing 16 mm → X = ±8 (matches ±50±8 pilot pattern)
lower_hole_z = 7.0     # base-side flange → assembled Z=72
upper_hole_z = 23.0    # lid-side flange  → assembled Z=88

# === DERIVED ===
pin_r = pin_bore_dia / 2.0
mount_r = mount_hole_dia / 2.0

# === FEATURE FUNCTIONS ===
def block_blank(lx, ly, lz):
    """Solid bracket body — prismatic, centered on XY, bottom at Z=0."""
    return cq.Workplane("XY").box(lx, ly, lz).translate((0, 0, lz / 2.0))

def pin_bore(body, r, z, lx):
    """Horizontal ⌀4 axle bore through the full X extent at mid-height."""
    cutter = (cq.Workplane("YZ").center(0, z).circle(r)
              .extrude(lx, both=True))  # spans ±lx along X, well past ±15
    return body.cut(cutter)

def mount_holes(body, r, xs, zs, ly):
    """4× ⌀3.2 through-holes along Y: 2 lower (base) + 2 upper (lid)."""
    for z in zs:
        for x in xs:
            cutter = (cq.Workplane("XZ").center(x, z).circle(r)
                      .extrude(ly, both=True))  # spans ±ly along Y, past ±12.5
            body = body.cut(cutter)
    return body

# === COMPOSE (reads as a build sequence) ===
body = block_blank(block_x, block_y, block_z)
body = pin_bore(body, pin_r, pin_bore_z, block_x)
body = mount_holes(body, mount_r, [-mount_hole_x, mount_hole_x],
                   [lower_hole_z, upper_hole_z], block_y)
result = body
