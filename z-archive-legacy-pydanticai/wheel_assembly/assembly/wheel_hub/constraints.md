# Constraints: wheel_hub

## Functional Requirements
- Mounts the wheel assembly to the vehicle's axle.
- Provides a secure, flat mounting surface for the alloy wheel.
- Transfers torque from the axle to the wheel.

## Dimensions
- Overall OD: 120mm
- Bore ID: 40mm
- Thickness: 30mm

## Features
- Bolt Pattern: 5 holes for M12 bolts.
- Pitch Circle Diameter (PCD): 100mm.
- The bolt holes should be through-holes, sized appropriately for M12 bolts (e.g., 13mm diameter).

## Interfaces
- Connects to `axle` via the 40mm bore. This will likely be a press-fit or a keyed fit.
- Connects to `alloy_wheel` via the 5x M12 bolt pattern. The mating surface must be flat and perpendicular to the bore axis.

## Manufacturing
- Primary process: CNC milling
- Material class: Aluminum 6061
- Secondary processes: None specified.
