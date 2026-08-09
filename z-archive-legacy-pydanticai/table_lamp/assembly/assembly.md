# Assembly Specification

This document defines the interfaces between the components of the Table Lamp.

## Interfaces

### 1. Base ↔ Stem
- **Type**: Threaded Connection
- **Specification**: The `stem` has an M12x1.5 external thread which screws into a matching tapped hole in the center of the `base`.
- **Engagement**: 15mm of thread engagement.

### 2. Stem ↔ Socket Housing
- **Type**: Threaded Connection
- **Specification**: The top end of the `stem` has an M12x1.5 external thread which screws into a matching tapped hole in the bottom of the `socket_housing`.
- **Engagement**: 15mm of thread engagement.

### 3. Socket Housing ↔ Shade
- **Type**: Seated Fit
- **Specification**: The `shade` has an internal circular feature with a diameter of 45.5mm which rests on a 45mm diameter flange on the `socket_housing`.
- **Constraint**: This is a non-positive fit, relying on gravity.

### 4. Socket Housing ↔ E26 Socket (Standard Part)
- **Type**: Press Fit / Set Screw
- **Specification**: A standard E26 socket will be installed into the 38mm bore of the `socket_housing`. The exact mounting method depends on the sourced socket.

### 5. E26 Socket ↔ Bulb
- **Type**: Threaded Connection
- **Specification**: The `bulb`'s E26 base screws into the socket.

## Resolved Mates (in assembly.py)

The final assembly was constructed using direct placement based on part dimensions. All parts are centered on the Z-axis. The origin (0,0,0) is the center of the bottom face of the base.

- **base**: Placed at `(0, 0, 0)`.
- **stem**: Placed at `(0, 0, 20)`, sitting on top of the base.
- **socket_housing**: Placed at `(0, 0, 270)`, sitting on top of the stem.
- **shade**: Placed at `(0, 0, 330)`, resting on the top flange of the socket housing.
- **bulb**: Placed at `(0, 0, 310)`, with its base positioned inside the socket housing's bore.
