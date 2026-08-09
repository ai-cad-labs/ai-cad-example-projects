import cadquery as cq
from pathlib import Path

# =============================================================================
# piston_crank — TDC assembly (design_plan.md § Assembly Pose)
#
# Global frame: crank MAIN axis = Z, crankshaft centered at origin.
# Throw at TDC = +X: crank pin axis through (30, 0) ∥ Z; gudgeon pin axis
# through (125, 0) ∥ Z; piston reciprocation axis = X (piston local +Z → +X);
# crown top at X = 125 + 32 = 157. Everything centered at Z = 0.
#
# Direct cq.Location placement only (constraint solver banned).
# =============================================================================

# __project_path__ is injected by the executor (absolute Path to project root).


def load_part(part_name: str) -> object:
    """Execute a part.py and return its result solid."""
    part_file = __project_path__ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError(f"Part not found: {part_file}")
    ns = {}
    exec(part_file.read_text(), ns)
    return ns["result"]


# === LOAD PARTS (never copy-paste part code) ===
crankshaft = load_part("crankshaft")        # main axis Z, centered origin, pin at (30,0)
connecting_rod = load_part("connecting_rod")  # big end bore = Z @ origin, long axis +X
gudgeon_pin = load_part("gudgeon_pin")      # axis Z, centered origin, Z ±25
piston = load_part("piston")                # axis Z, crown +27.5, pin bore along local X @ z=-4.5
piston_ring = load_part("piston_ring")      # axis Z, section centered origin, gap at local +X

# === PLACEMENT PARAMETERS (from the locked dimension chain) ===
crank_throw = 30.0            # crank pin axis X at TDC
rod_center_distance = 95.0    # big end → small end
gudgeon_axis_x = crank_throw + rod_center_distance          # 125.0
piston_pin_axis_local_z = -4.5   # pin bore local Z in piston frame (32 below crown +27.5)
# Rotation +90° about Y maps piston local +Z → global +X and local (0,0,-4.5) → (-4.5,0,0),
# so translate by 125 - (-4.5) = 129.5 to land the pin bore axis on (125, 0).
piston_tx = gudgeon_axis_x - piston_pin_axis_local_z        # 129.5
crown_top_x = piston_tx + 27.5                              # 157.0 (sanity: 125 + 32)

# Ring seats: groove mid-heights 6.3 / 11.9 / 17.5 below crown top (piston as-coded:
# top land 5.0, groove axial 2.6, inter-land 3.0) → global X = 150.7 / 145.1 / 139.5
ring_seat_xs = [crown_top_x - 6.3, crown_top_x - 11.9, crown_top_x - 17.5]
ring_clock_degs = [0.0, 120.0, 240.0]   # clock the +X end gaps ~120° apart about ring axis

# === LOCATIONS (rotate first, then translate) ===
Y_AXIS = cq.Vector(0, 1, 0)

crankshaft_loc = cq.Location(cq.Vector(0, 0, 0))
rod_loc = cq.Location(cq.Vector(crank_throw, 0, 0))          # pure translation: bore axes already ∥ Z
pin_loc = cq.Location(cq.Vector(gudgeon_axis_x, 0, 0))       # pure translation: axis already ∥ Z
piston_loc = cq.Location(cq.Vector(piston_tx, 0, 0), Y_AXIS, 90)

# Rings: pre-rotate each instance about its own (local Z) axis to clock the gap,
# then apply the same +90° about Y and translate to the seat center.
ring_instances = []
for i, (seat_x, clock) in enumerate(zip(ring_seat_xs, ring_clock_degs), start=1):
    clocked = piston_ring.rotate((0, 0, 0), (0, 0, 1), clock)
    loc = cq.Location(cq.Vector(seat_x, 0, 0), Y_AXIS, 90)
    ring_instances.append((f"piston_ring_{i}", clocked, loc))

# === ASSEMBLY ===
assy = (
    cq.Assembly()
    .add(crankshaft, name="crankshaft", loc=crankshaft_loc, color=cq.Color("gray"))
    .add(connecting_rod, name="connecting_rod", loc=rod_loc, color=cq.Color("blue"))
    .add(gudgeon_pin, name="gudgeon_pin", loc=pin_loc, color=cq.Color("red"))
    .add(piston, name="piston", loc=piston_loc, color=cq.Color("lightgray"))
)
for name, solid, loc in ring_instances:
    assy = assy.add(solid, name=name, loc=loc, color=cq.Color("orange"))

result = assy.toCompound()
