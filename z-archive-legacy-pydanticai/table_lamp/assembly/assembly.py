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

# Load all the parts
base = load_part("base")
stem = load_part("stem")
socket_housing = load_part("socket_housing")
shade = load_part("shade")
bulb = load_part("bulb")

# Define the vertical positions (Z-axis) for each part based on their dimensions.
# All parts are designed with their origin at the center of their bottom face.
base_height = 20.0
stem_height = 250.0
socket_housing_height = 60.0

# The stem sits on top of the base.
z_stem = base_height

# The socket housing sits on top of the stem.
z_socket_housing = z_stem + stem_height

# The shade rests on the top flange of the socket housing.
z_shade = z_socket_housing + socket_housing_height

# The bulb's base is positioned inside the socket housing.
# We place it 20mm below the top of the housing for a realistic look.
z_bulb = z_shade - 20.0

# Define the locations for each part in the assembly.
# No rotation is needed as all parts are cylindrical and aligned.
loc_base = cq.Location(cq.Vector(0, 0, 0))
loc_stem = cq.Location(cq.Vector(0, 0, z_stem))
loc_socket_housing = cq.Location(cq.Vector(0, 0, z_socket_housing))
loc_shade = cq.Location(cq.Vector(0, 0, z_shade))
loc_bulb = cq.Location(cq.Vector(0, 0, z_bulb))

# Create the assembly.
assy = (
    cq.Assembly()
    .add(base, name="base", loc=loc_base, color=cq.Color("darkgoldenrod"))
    .add(stem, name="stem", loc=loc_stem, color=cq.Color("lightgray"))
    .add(socket_housing, name="socket_housing", loc=loc_socket_housing, color=cq.Color("lightgray"))
    .add(shade, name="shade", loc=loc_shade, color=cq.Color("white"))
    .add(bulb, name="bulb", loc=loc_bulb, color=cq.Color("yellow"))
)

# Convert the assembly to a compound solid for rendering.
result = assy.toCompound()
