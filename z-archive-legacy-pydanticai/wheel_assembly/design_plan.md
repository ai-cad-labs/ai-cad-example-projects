# Design Plan: Car Wheel Assembly

## Overview
This project is to design a standard car wheel assembly. The assembly consists of a central hub that mounts to an axle, a 5-spoke alloy wheel that bolts to the hub, and a rubber tire mounted on the wheel. The primary components will be designed for CNC machining from aluminum.

## Parts
### 1. wheel_hub
- **Type**: Custom (Make)
- **Description**: A cylindrical hub that acts as the interface between the axle and the alloy wheel. It features a central bore and a 5-bolt pattern.
- **Key dimensions**: 80mm OD, 40mm bore, 30mm thick.
- **Interfaces**: Connects to `axle` and `alloy_wheel`.

### 2. alloy_wheel
- **Type**: Custom (Make)
- **Description**: A 17-inch, 5-spoke wheel. It mounts to the hub and holds the tire.
- **Key dimensions**: 432mm (17") OD, 80mm central bore.
- **Interfaces**: Connects to `wheel_hub` and `tire`.

### 3. tire
- **Type**: Standard (Buy)
- **Description**: A standard 225mm rubber tire designed to fit on a 17-inch rim.
- **Key dimensions**: 225mm width, 17" inner diameter.
- **Interfaces**: Connects to `alloy_wheel`.

### 4. M12 Bolts (x5)
- **Type**: Standard (Buy)
- **Description**: Standard metric bolts used to fasten the alloy wheel to the wheel hub.
- **Key dimensions**: M12 thread. Length to be determined based on final part thicknesses.
- **Interfaces**: Connects `alloy_wheel` and `wheel_hub`.

## Interfaces
- `axle` ↔ `wheel_hub`: 40mm bore fit (specific fit type TBD, e.g., press-fit, keyed).
- `wheel_hub` ↔ `alloy_wheel`: Mated via flat faces. Fastened with 5x M12 bolts on a 100mm PCD. The 80mm OD of the hub pilots into the 80mm ID of the wheel's central bore for alignment.
- `alloy_wheel` ↔ `tire`: Standard 17-inch tire bead seat on the rim flange. This is an interference fit maintained by air pressure.

## Assembly Order
1.  The `wheel_hub` is mounted onto the `axle`.
2.  The `alloy_wheel` is placed over the `wheel_hub`.
3.  The 5x M12 bolts are inserted and torqued to fasten the wheel to the hub.
4.  The `tire` is professionally mounted onto the `alloy_wheel` rim and inflated.

## Make vs Buy
- **Make**: `wheel_hub`, `alloy_wheel`
- **Buy**: `tire`, `M12 bolts`
