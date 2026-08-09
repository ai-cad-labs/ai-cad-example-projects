import cadquery as cq
from pathlib import Path

# __project_path__ is injected by the executor (absolute Path to the project dir).


def load_part(part_name: str) -> object:
    """Execute a part.py and return its `result` solid. Never re-derive geometry."""
    part_file = __project_path__ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError(f"Part not found: {part_file}")
    ns = {}
    exec(part_file.read_text(), ns)
    return ns["result"]


# === LOAD THE THREE VALIDATED PARTS (unmodified) ===
pinion = load_part("pinion")   # 18T, OD⌀40, bore ⌀8.2, centred on Z, tooth #0 on +X
gear = load_part("gear")       # 30T, OD⌀64, bore ⌀8.2, centred on Z, tooth #0 on +X
shaft = load_part("shaft")     # plain ⌀8 × 30 cylinder, centred on Z (Z=-15..+15)

# === PLACEMENT SPEC (from design_plan.md interfaces) ===
# Centre distance = (pitch⌀36 + pitch⌀60)/2 = 48mm. Pinion at origin; gear along +X.
# Pitch circles (⌀36 pinion + ⌀60 gear) are tangent at x=18mm on the centre line.
CENTRE_DISTANCE = 48.0
# Half-tooth-pitch phase on the 30T gear = 360/(2*30) = 6°. Both gears carry tooth #0
# on +X, so an UNPHASED gear presents a tooth (not a gap) to the pinion's +X tooth
# -> tooth-on-tooth interpenetration. A half-tooth phase swaps teeth<->gaps at the
# mesh line so the pinion tooth enters a gear gap. VERIFIED by Z=0 section-interference
# test: phase 0° -> 18.04 mm^2 of tooth overlap; phase -6° -> 0.00 mm^2 (clean mesh,
# zero interpenetration). +6° is equivalently clean by tooth symmetry; -6° chosen.
PHASE_DEG = -6.0

# pinion: at origin, no transform.
pinion_loc = cq.Location(cq.Vector(0, 0, 0))
# gear: translate to centre distance along +X, phase-rotate about Z (coplanar, same Z).
gear_loc = cq.Location(cq.Vector(CENTRE_DISTANCE, 0, 0), cq.Vector(0, 0, 1), PHASE_DEG)
# shaft #1: coaxial through the pinion bore (pinion centre = origin) -> no XY translate.
shaft1_loc = cq.Location(cq.Vector(0, 0, 0))
# shaft #2: coaxial through the gear bore (gear centre) -> same XY as the gear.
shaft2_loc = cq.Location(cq.Vector(CENTRE_DISTANCE, 0, 0))

assy = (
    cq.Assembly()
    .add(pinion, name="pinion", loc=pinion_loc, color=cq.Color("red"))
    .add(gear, name="gear", loc=gear_loc, color=cq.Color("blue"))
    .add(shaft, name="shaft_pinion", loc=shaft1_loc, color=cq.Color("green"))
    .add(shaft, name="shaft_gear", loc=shaft2_loc, color=cq.Color("orange"))
)

# ALWAYS call .toCompound() — the renderer cannot handle raw Assembly objects.
result = assy.toCompound()
