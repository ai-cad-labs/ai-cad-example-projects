
import cadquery as cq

# === PARAMETERS ===
# All dimensions in mm

# Hub Body Dimensions
hub_od = 80.0
hub_thickness = 20.0 # Protrusion from flange

# Flange Dimensions
flange_od = 120.0
flange_thickness = 10.0

# Bore Dimensions
bore_id = 40.0

# Bolt Pattern
pcd = 100.0
bolt_hole_count = 5
bolt_hole_dia = 13.0 # For M12 bolts, providing 1mm clearance

# Chamfer
chamfer_size = 1.0

# === DERIVED VALUES ===
total_thickness = hub_thickness + flange_thickness

# === GEOMETRY ===

# 1. Create the main flange
# This provides the mounting face for the wheel.
flange = cq.Workplane("XY").circle(flange_od / 2).extrude(flange_thickness)

# 2. Create the hub body on top of the flange
# This part would interface with the axle/bearing assembly.
hub_body = (
    flange.faces(">Z").workplane()
    .circle(hub_od / 2)
    .extrude(hub_thickness)
)

# 3. Create the central bore for the axle
hub_with_bore = hub_body.faces(">Z").workplane().hole(bore_id)

# 4. Add the bolt hole pattern using a polar array
# These holes are for the wheel studs/bolts.
hub_with_holes = (
    hub_with_bore.faces("<Z").workplane()
    .polarArray(pcd / 2, 0, 360, bolt_hole_count)
    .hole(bolt_hole_dia)
)

# 5. Add chamfers for manufacturability and to break sharp edges
# Chamfer outer edge of flange
result = hub_with_holes.faces("<Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size)
# Chamfer outer edge of hub body
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size)
# Chamfer inner edge of bore on both sides
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(1)).chamfer(chamfer_size)
result = result.faces("<Z").edges(cq.selectors.RadiusNthSelector(1)).chamfer(chamfer_size)
