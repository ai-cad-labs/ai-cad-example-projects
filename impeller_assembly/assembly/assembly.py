"""Assembly for impeller_assembly.

Global convention (locked interface spec):
  shaft axis = global Z; global Z=0 = bearing housing impeller-side face;
  +Z points toward the inlet. All placements are pure Z translations.

Make parts (loaded from their part.py, `result` variable):
  bearing_housing @ Z +0.0   (local Z0 = impeller-side face;   spans -28 .. +12)
  impeller        @ Z +0.8   (local Z0 = backplate backface;   spans -14.8 .. +34.0)
  pulley_shaft    @ Z -14.0  (local Z0 = clamp shoulder face;  spans -44 .. +74)

Buy parts (representational geometry authored inline from BOM dimensions):
  main_bearing   6203      bore 17.0 / OD 40.0 / width 12.0 -> global Z -12.0 .. 0.0
  lock_nut       ISO 4032 M10, 16.0 across flats, 8.4 high  -> global Z +34.8 .. +43.2
  inlet_bearing  688-2Z    bore 8.0 / OD 16.0 / width 5.0   -> global Z +47.0 .. +52.0

Key mates encoded by the translations:
  - shaft clamp shoulder face at global -14.0 meets the impeller spigot end face;
  - impeller Ø22 standoff boss back face bears on the 6203 inner race at Z=0,
    putting the backplate backface at +0.8 -> the 0.8 mm running clearance to
    the housing face at Z=0 (required window 0.5..1.0 mm);
  - lock nut (34.8..43.2) sits inside the shaft M10 thread span (31..45);
  - inlet bearing (47..52) sits on the shaft Ø8 tail span (45..60).
"""

import math
import runpy

import cadquery as cq

try:
    _PROJ = __project_path__  # injected by tools.cadquery_executor
except NameError:  # standalone execution (probe scripts, direct python)
    from pathlib import Path

    _PROJ = Path(__file__).resolve().parents[1]


def _as_shape(res):
    """Normalize a part.py `result` (Workplane / Shape / Assembly) to a Shape."""
    if isinstance(res, cq.Assembly):
        return res.toCompound()
    if isinstance(res, cq.Workplane):
        vals = res.vals()
        return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
    return res


def load_part(part_name):
    """Execute a part.py and return its `result` solid as a Shape."""
    part_file = _PROJ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError(f"Part not found: {part_file}")
    ns = runpy.run_path(str(part_file), init_globals={"__project_path__": _PROJ})
    return _as_shape(ns["result"])


def _ring_bearing(bore_d, od, width, band_frac=0.5):
    """Representational rolling bearing: outer race + inner race + ball band.

    Built with its back face at local Z=0, extending to Z=+width.
    """
    r_bore = bore_d / 2.0
    r_od = od / 2.0
    r1 = r_bore + (r_od - r_bore) * 0.35  # inner race outer radius
    r2 = r_bore + (r_od - r_bore) * 0.65  # outer race inner radius
    outer = cq.Workplane("XY").circle(r_od).circle(r2).extrude(width)
    inner = cq.Workplane("XY").circle(r1).circle(r_bore).extrude(width)
    bw = width * band_frac
    band = (
        cq.Workplane("XY")
        .workplane(offset=(width - bw) / 2.0)
        .circle(r2)
        .circle(r1)
        .extrude(bw)
    )
    return _as_shape(outer.union(inner).union(band))


def _hex_nut(across_flats, height, bore_d):
    """ISO 4032-style hex nut. across_flats = inscribed circle diameter.

    CadQuery's polygon() takes the CIRCUMSCRIBED diameter = AF / cos(30deg).
    16.0 AF -> circumradius 16.0/sqrt(3) ~= 9.2376.
    """
    circum_d = across_flats / math.cos(math.pi / 6.0)
    nut = (
        cq.Workplane("XY")
        .polygon(6, circum_d)
        .circle(bore_d / 2.0)
        .extrude(height)
    )
    return _as_shape(nut)


def _at_z(shape, dz):
    """Pure Z translation via direct placement (no constraint solver)."""
    return shape.moved(cq.Location(cq.Vector(0.0, 0.0, dz)))


# --- Make parts (pre-placed into global frame) ---
bearing_housing = _at_z(load_part("bearing_housing"), 0.0)
impeller = _at_z(load_part("impeller"), 0.8)
pulley_shaft = _at_z(load_part("pulley_shaft"), -14.0)

# --- Buy parts (representational, from BOM dims) ---
main_bearing = _at_z(_ring_bearing(17.0, 40.0, 12.0), -12.0)  # 6203: -12.0..0.0
lock_nut = _at_z(_hex_nut(16.0, 8.4, 10.0), 34.8)  # M10 nut: +34.8..+43.2
inlet_bearing = _at_z(_ring_bearing(8.0, 16.0, 5.0), 47.0)  # 688-2Z: +47.0..+52.0

placed = {
    "bearing_housing": bearing_housing,
    "main_bearing": main_bearing,
    "impeller": impeller,
    "pulley_shaft": pulley_shaft,
    "lock_nut": lock_nut,
    "inlet_bearing": inlet_bearing,
}

_COLORS = {
    "bearing_housing": "gray",
    "main_bearing": "red",
    "impeller": "orange",
    "pulley_shaft": "blue",
    "lock_nut": "green",
    "inlet_bearing": "magenta",
}

assy = cq.Assembly()
for _name, _shape in placed.items():
    assy.add(_shape, name=_name, color=cq.Color(_COLORS[_name]))

result = assy.toCompound()

_bb = result.BoundingBox()
print(f"CHECK components={len(placed)}")
print(
    "CHECK bbox "
    f"x=[{_bb.xmin:.2f},{_bb.xmax:.2f}] "
    f"y=[{_bb.ymin:.2f},{_bb.ymax:.2f}] "
    f"z=[{_bb.zmin:.2f},{_bb.zmax:.2f}]"
)
