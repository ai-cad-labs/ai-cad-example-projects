import cadquery as cq

# __project_path__ is injected by the executor (absolute Path to the project dir).


def load_part(part_name: str) -> object:
    """Execute a part.py and return its `result` solid."""
    part_file = __project_path__ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError(f"Part not found: {part_file}")
    ns = {}
    exec(part_file.read_text(), ns)
    return ns["result"]


# --- Load parts (hinge_block loaded ONCE, placed twice) ---
base = load_part("base")
lid = load_part("lid")
hinge_block = load_part("hinge_block")
hasp_plate = load_part("hasp_plate")

# --- Placements (direct cq.Location; arithmetic from plan interface coords) ---
# base: reference frame == assembly frame → identity.
base_loc = cq.Location(cq.Vector(0, 0, 0))

# lid: flat bottom (local Z=0) seats on base top rim (Z=80). No rotation.
lid_loc = cq.Location(cq.Vector(0, 0, 80))

# hinge_block: local Z→assembled via +65 (pin local z=15 → 80; lower 7→72; upper 23→88).
# No rotation: block X-axis = pin axis (assembled X); mount holes along Y = pilot axis.
# Y: inner face against base rear (Y=60); block depth 25 → center Y=72.5 (external hinge).
# X: block centers at X=±50 (mount holes ±8 → ±{42,58} matching pilots).
hinge_l_loc = cq.Location(cq.Vector(-50.0, 72.5, 65.0))
hinge_r_loc = cq.Location(cq.Vector(+50.0, 72.5, 65.0))

# hasp_plate: mount holes (local z=10) aligned to base front pilots (Z=62) → +52 in Z.
# Y: outer face just outside front (Y=-60); thickness 4 → center Y=-62.
# NOTE: hasp latch hole lands at assembled Z=94 (local 42 + 52); the lid latch hole is
# at Z=86 → 8 mm mismatch. See CONFLICT-001 + hasp_plate/part.proposal.py. Composed
# as-is (mount interface prioritized) so the misalignment is visible in renders.
hasp_loc = cq.Location(cq.Vector(0.0, -62.0, 52.0))

# --- Assemble ---
assy = (
    cq.Assembly()
    .add(base, name="base", loc=base_loc, color=cq.Color("brown"))
    .add(lid, name="lid", loc=lid_loc, color=cq.Color("orange"))
    .add(hinge_block, name="hinge_block_left", loc=hinge_l_loc, color=cq.Color("gray"))
    .add(hinge_block, name="hinge_block_right", loc=hinge_r_loc, color=cq.Color("gray"))
    .add(hasp_plate, name="hasp_plate", loc=hasp_loc, color=cq.Color("yellow"))
)

result = assy.toCompound()
