# Single-Cylinder Piston-Crank Assembly
Design the reciprocating core of a single-cylinder engine — NO cylinder block/bore, NO valves, NO head:
- **Piston**: ~⌀60 mm x 55 mm tall, aluminum, CNC_milling. Flat crown. THREE ring grooves near the crown (two compression + one oil groove, rectangular profile). TWO pin bosses inside the skirt with a through ⌀16 mm gudgeon-pin bore, boss faces spaced to fit the rod small end between them.
- **Piston rings x3**: flat rectangular-section rings sized to the grooves (outer ⌀ ~60.5 mm free, radial thickness ~2.5 mm, axial height matching groove) — model as one ring part, quantity 3 (note the oil ring may share geometry for v1). Steel, CNC_turning.
- **Gudgeon pin**: ⌀16 mm x ~50 mm hollow tube (inner ⌀ ~9 mm), steel, CNC_turning. Full-floating fit through both bosses and the rod small end.
- **Connecting rod**: center distance ~95 mm. Small end: ⌀16 mm bore with bronze-bushing land. Big end: ⌀38 mm bore for the crank pin; I-beam shank; one-piece big end is acceptable for v1 (no bolted cap). Steel, CNC_milling.
- **Crankshaft**: single-throw. Two ⌀30 mm main journals on the main axis, one ⌀38 mm crank pin offset 30 mm (stroke 60 mm), two web/counterweight plates joining them. Steel, CNC_turning + CNC_milling.
- Assembly: crank main axis = Z per convention; rings seated in grooves; pin through bosses + small end; big end on crank pin; rod at TDC orientation. All parts fit without interference; export STEP + STL for every part once validated.
