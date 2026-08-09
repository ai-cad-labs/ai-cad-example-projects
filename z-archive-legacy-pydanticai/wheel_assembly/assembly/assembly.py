import cadquery as cq
from pathlib import Path

# __project_path__ is automatically injected by the executor.
# It is an absolute Path to the project directory.

def load_part(part_name: str) -> object:
    """Execute a part.py and return the result solid."""
    part_file = __project_path__ / "assembly" / part_name / "part.py"
    if not part_file.exists():
        raise FileNotFoundError(f"Part not found: {part_file}")
    code = part_file.read_text()
    ns = {}
    exec(code, ns)
    return ns["result"]

# Load all parts from their respective directories
try:
    wheel_hub = load_part("wheel_hub")
    alloy_wheel = load_part("alloy_wheel")
    tire = load_part("tire")
except FileNotFoundError as e:
    # This block is for robustness, in case a part is missing.
    # In a real scenario, you might want to log this error more formally.
    print(f"Error loading parts: {e}")
    # Assign None to result to indicate failure
    result = None
    # Stop execution if parts can't be loaded
    raise

# Define locations for each part in the assembly.
# The assembly is built around the wheel_hub at the origin.

# 1. wheel_hub is placed at the origin.
# Its mounting face for the wheel is the front face of its flange, at Z=10mm.
hub_loc = cq.Location(cq.Vector(0, 0, 0))

# 2. alloy_wheel is mated to the wheel_hub.
# The wheel's mounting face (front of its hub section) is at Z=200mm in its local coordinates.
# To mate with the hub's face at Z=10mm, we need to rotate the wheel 180 degrees
# around the Y-axis and then translate it into position.
# After rotation, its mounting face is at Z=-200. We move it to Z=10.
wheel_loc = cq.Location(cq.Vector(0, 0, 10), cq.Vector(0, 1, 0), 180)

# 3. tire is mounted onto the alloy_wheel.
# The wheel rim is 200mm wide and centered at Z=100mm in its local coordinates.
# After the wheel's transformation (rotation and translation):
# - The center's Z-coordinate becomes -100mm due to rotation.
# - It is then translated by +10mm.
# So, the final Z-position for the tire's center is -90mm.
tire_loc = cq.Location(cq.Vector(0, 0, -90))


# Create the assembly
assy = (
    cq.Assembly()
    .add(wheel_hub, name="wheel_hub", loc=hub_loc, color=cq.Color("lightgray"))
    .add(alloy_wheel, name="alloy_wheel", loc=wheel_loc, color=cq.Color("gray"))
    .add(tire, name="tire", loc=tire_loc, color=cq.Color("black"))
)

# Convert the assembly to a compound solid for rendering and export.
# This is a critical step.
result = assy.toCompound()
