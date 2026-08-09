# Sourcing Notes

## Make vs Buy Rationale

- **wheel_hub**: Custom designed for specific axle interface and wheel bolt pattern.
- **alloy_wheel**: Custom designed for aesthetic and performance requirements, and to interface with the custom hub.
- **tire**: Standard component. Purchasing a standard tire significantly reduces cost and development time, and leverages existing automotive industry standards.
- **M12 Bolts**: Standard fasteners. Readily available off-the-shelf, cost-effective, and meet required strength specifications.

## Standard Part Specifications

- **Tire**: A standard 225/45R17 tire is recommended. The exact model can be selected based on performance and budget requirements. The "45" aspect ratio is a common placeholder; final selection may vary.
- **M12 Bolts**: DIN 933 Hex head cap screws are recommended for their common availability and strength. The length of the M12 bolts needs to be determined once the thicknesses of the `wheel_hub` and `alloy_wheel` at the bolt interface are finalized. This will ensure proper thread engagement without bottoming out.

## Constraints Discovered

- The `wheel_hub` and `alloy_wheel` designs must accommodate M12 bolts for fastening. This includes appropriate hole diameters and counterbores/spotfaces if necessary.
- The total thickness of the `wheel_hub` and `alloy_wheel` at the bolt interface will dictate the required length of the M12 bolts.
