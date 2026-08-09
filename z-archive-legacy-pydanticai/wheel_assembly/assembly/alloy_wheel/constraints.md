# Constraints: alloy_wheel

## Functional Requirements
- Provides the primary structural support for the tire.
- Transfers loads from the tire contact patch to the wheel hub.
- Must be aesthetically pleasing with a 5-spoke pentagonal design.

## Dimensions
- Overall OD: 17 inches (432mm).
- Central Bore ID: 80mm (to fit over the wheel_hub).
- Width: Sized to accept a 225mm tread width tire (typically around 7.5-8 inches or ~190-203mm rim width).

## Features
- Spoke Design: 5-spoke pentagonal pattern.
- Bolt Pattern: 5 holes for M12 bolts.
- Pitch Circle Diameter (PCD): 100mm.
- Rim Flange: Designed to seat a standard 17-inch automotive tire.

## Interfaces
- Connects to `wheel_hub` via the 80mm central bore and the 5x M12 bolt pattern.
- Connects to `tire` via the rim flange. The geometry must conform to industry standards for tire seating (bead seat).

## Manufacturing
- Primary process: CNC milling
- Material class: Aluminum 6061
- Secondary processes: Potentially anodizing or painting for finish.
