# Design Plan

## Overview
Reciprocating core of a single-cylinder engine — piston, 3 identical piston rings, full-floating gudgeon pin, one-piece connecting rod, and a single-throw crankshaft. NO cylinder block/bore, valves, or head. Assembly is posed at TDC with the crank main axis on Z. Project-wide policy: NO fillets (deferred), export STEP + STL per part after validation.

Every interface dimension is locked numerically in this plan and in the per-part constraints files, so downstream agents never have to negotiate a fit:

**Dimension chain (single source of truth):**
- Gudgeon pin ⌀16.0 (pin 15.99) ↔ piston boss bores ⌀16.0 (16.02) ↔ rod small end bore ⌀16.0 (16.02) — full-floating clearance
- Crank pin ⌀38.0 ↔ rod big end bore ⌀38.0 (38.05) — rotating clearance
- Ring section 2.5 axial x 2.5 radial ↔ piston groove 2.6 axial x 3.0 radial deep (groove root ⌀54.0; back clearance 0.5 at working OD 60.0)
- Piston boss inner spacing 22.0 ↔ rod small end width 20.0 (1.0 clearance/side)
- Piston boss outer span 48.0 ↔ pin length 50.0 (pin fully inside ⌀54 skirt inner wall)
- Crank pin length 22.0 (between web inner faces) ↔ rod big end width 20.0 (1.0 clearance/side)
- Rod center distance 95.0 + crank throw 30.0 (stroke 60.0) → TDC gudgeon-pin axis at 125.0 mm from crank main axis

## Parts
### 1. piston
- **Type**: Custom (make)
- **Description**: Flat-crown aluminum piston; 3 rectangular ring grooves near crown; 2 internal pin bosses with through ⌀16 pin bore
- **Key dimensions**: ⌀60 x 55 mm; compression height 32; grooves 2.6 x 3.0 deep; boss inner spacing 22, outer span 48
- **Interfaces**: Connects to piston_ring (grooves), gudgeon_pin (boss bores ⌀16), connecting_rod (small end fits between bosses)
- **parallel_safe**: true — all dimensions and both interface geometries are fully locked by constraints.md; it is an interface PROVIDER, consuming nothing from other parts

### 2. piston_ring
- **Type**: Custom (make) — one part, quantity 3 in assembly
- **Description**: Rectangular-section split ring (shared geometry for compression + oil rings in v1)
- **Key dimensions**: free OD 60.5, radial 2.5, axial 2.5, 1.0 mm end gap
- **Interfaces**: Connects to piston via ring grooves (2.6 axial x 3.0 deep)
- **parallel_safe**: false — ring section must match the piston's AS-DESIGNED groove geometry; if the piston design shifts groove height/depth, the ring must follow. Design after piston is locked.

### 3. gudgeon_pin
- **Type**: Custom (make)
- **Description**: Hollow full-floating wrist pin
- **Key dimensions**: ⌀16 x 50, ID ⌀9 through
- **Interfaces**: Clearance fit through piston boss bores and rod small end bore (all ⌀16 nominal)
- **parallel_safe**: false — pin length/retention depends on the piston's AS-DESIGNED boss outer span (48) and skirt inner wall (⌀54). Design after piston is locked.

### 4. connecting_rod
- **Type**: Custom (make)
- **Description**: One-piece steel rod, I-beam shank, ⌀16 small end (bronze-bushing land; bushing = Buy, not modeled in v1), ⌀38 one-piece big end (no bolted cap)
- **Key dimensions**: center distance 95; small end ⌀26 OD x 20 wide; big end ⌀52 OD x 20 wide; envelope 134 x 52 x 20
- **Interfaces**: gudgeon_pin (small end bore ⌀16), piston (width 20 between 22 boss faces), crankshaft (big end bore ⌀38 on crank pin, width 20 in 22 pin span)
- **parallel_safe**: false — small end width consumes the piston's boss spacing and big end width consumes the crankshaft's crank-pin span; both providers must be locked first.

### 5. crankshaft
- **Type**: Custom (make)
- **Description**: One-piece single-throw crank: 2x ⌀30 main journals, 2x ⌀100 x 10 web discs (counterweight cutouts deferred), 1x ⌀38 crank pin at 30 mm offset
- **Key dimensions**: overall ⌀100 x 92 along main axis; throw 30 (stroke 60); crank pin span 22
- **Interfaces**: Connects to connecting_rod via crank pin ⌀38 x 22
- **parallel_safe**: true — all dimensions fully locked by constraints.md; interface PROVIDER for the rod, consumes nothing

**Dispatch note for orchestrator**: the two providers (piston, crankshaft) have no inbound dependencies and can be designed in parallel with each other immediately. The three `parallel_safe: false` consumers (piston_ring, gudgeon_pin, connecting_rod) each depend only on provider outcomes — once piston + crankshaft geometry is validated, all three consumers are mutually independent and can be dispatched together.

## Interfaces
- piston ↔ piston_ring: 3 rectangular grooves 2.6 axial x 3.0 radial deep (root ⌀54.0) ↔ ring 2.5 x 2.5 section, free OD 60.5
- piston ↔ gudgeon_pin: boss through-bores ⌀16.0 (16.02) ↔ pin ⌀16.0 (15.99), full-floating clearance; boss outer span 48 vs pin length 50
- piston ↔ connecting_rod: boss inner faces 22.0 apart ↔ small end width 20.0
- gudgeon_pin ↔ connecting_rod: small end bore ⌀16.0 (16.02) ↔ pin ⌀16.0 (15.99), full-floating clearance
- crankshaft ↔ connecting_rod: crank pin ⌀38.0 x 22.0 ↔ big end bore ⌀38.0 (38.05) x 20.0 wide, rotating clearance

## Assembly Order
1. crankshaft (interface provider — crank pin geometry)
2. piston (interface provider — grooves, boss bores, boss spacing)
3. gudgeon_pin (consumer of piston bosses)
4. connecting_rod (consumer of piston boss spacing + crank pin)
5. piston_ring (consumer of piston grooves; instanced 3x in assembly)

## Make vs Buy
- **Buy**: bronze small-end bushing (⌀16 ID land in rod; deferred — not modeled in v1 geometry, sourcing agent to spec in external/bom.md). No other standard parts: no fasteners (one-piece big end), no bearings (journals left free per goals).
- **Make**: piston, piston_ring, gudgeon_pin, connecting_rod, crankshaft — all custom geometry.

## Assembly Pose (TDC, per convention)
- Crank main axis = global Z, crankshaft centered at origin
- Throw direction at TDC = +X: crank pin axis at (30, 0), gudgeon pin axis at (125, 0) — both parallel to Z
- Piston reciprocation axis = X; piston crown faces +X (crown top at X = 125 + 32 = 157)
- Rod long axis along X, big end at X=30, small end at X=125; rod/big-end/crank-pin/piston-pin all centered at Z=0
- No interference: piston skirt bottom at X = 102 clears web disc radius 50 ✓; big end (width 20) sits in the 22 mm crank-pin span ✓
