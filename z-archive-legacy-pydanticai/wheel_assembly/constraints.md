# Design Constraints

## From Sourcing Agent

### M12 Bolt Interface

- **wheel_hub**: Must include features (e.g., through-holes, spotfaces) to accommodate 5x M12 bolts on a 100mm PCD for fastening to the `alloy_wheel`. The 80mm OD of the hub pilots into the 80mm ID of the wheel's central bore for alignment.
- **alloy_wheel**: Must include features (e.g., through-holes, counterbores) to accommodate 5x M12 bolts on a 100mm PCD for fastening to the `wheel_hub`. The 80mm ID of the wheel's central bore pilots onto the 80mm OD of the hub for alignment.
- **M12 Bolt Length Determination**: The combined thickness of the `wheel_hub` and `alloy_wheel` at the bolt interface must be considered to determine the appropriate length of the M12 bolts to ensure sufficient thread engagement without bottoming out.
