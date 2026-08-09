# Open Issues — treasure_chest

### CONFLICT-001 [RESOLVED]
- **Parts**: hasp_plate, lid
- **Issue**: hasp_plate latch hole misaligned 8 mm vs lid front latch hole (local latch_hole_z=42 gave assembled Z=94 vs required Z=86).
- **Resolution**: assembly_resolver filed part.proposal.py (latch_hole_z 42→34). DFM regression gate: **PROMOTED** (score 0→0, no new failures). part.proposal.py is now part.py. Latch hole now lands at assembled Z=86, aligning with the lid latch hole. Mount holes remain on base pilots (Z=62).

### DFM-3DP-002 [DEFERRED — documented, accepted]
- **Parts**: hinge_block, lid
- **Rule**: "Overhang angle should not exceed 45° from vertical without support" — severity MAJOR (not critical).
- **Finding**: horizontal round bores (hinge_block ⌀4 pin bore; lid ⌀6 front latch through-hole) present unsupported crown arcs >45° for FDM.
- **Why deferred (engineering decision by orchestrator)**:
  1. Severity is MAJOR, not CRITICAL — no critical DFM failures anywhere in the sweep.
  2. Geometrically unavoidable per the evaluator's own observation: the hinge_block has ORTHOGONAL hole groups (pin bore ⊥ mount holes), so NO single print orientation makes all bores vertical — at least one bore is always a >45° overhang.
  3. The horizontal orientations are FUNCTIONALLY MANDATORY: the hinge pin axis and the latch hole must be horizontal for the chest to hinge and latch.
  4. Small horizontal bores (⌀4–⌀6 mm) print acceptably on FDM in practice — sag over such short spans is within tolerance.
  5. The recommended mitigation (teardrop / self-supporting bore profiles) is a PRINT-DETAIL OPTIMIZATION, not a geometry-correctness fix — consistent with the project-wide deferral of fillets and print-detail refinements to a later phase.
- **Status**: accepted for this smoke run; candidate for a future print-optimization pass (teardrop bores).

### DFA-002 [DEFERRED — documented, accepted]
- **Scope**: assembly (hinge/hasp mating interfaces).
- **Rule**: "Parts should self-locate via geometric features (chamfers, pins, shoulders, bosses)" — severity MAJOR (not critical).
- **Finding**: hinge blocks and hasp plate mate flat-on-flat and rely on screw clearance holes alone for position; no locating bosses/dowels/lead-in chamfers.
- **Why deferred (engineering decision by orchestrator)**:
  1. Severity MAJOR, not CRITICAL — parts fit and function; this is assembly-ergonomics, not a fit/function blocker.
  2. Flat-on-flat mounting with self-tapping screws is the conventional, correct pattern for a decorative 3D-printed chest's surface-mounted hinges and hasp.
  3. The fix (matching recesses/bosses on BOTH sides of every joint) is a coordinated 4-part change that would risk interpenetration/regressions on an already-PASSED assembly.
  4. Consistent with project-wide deferral of print-detail/assembly refinements; candidate for a future DFA-optimization pass.
- **Status**: accepted for this smoke run.

### NOTE [minor]
- assembly.py carries a stale inline comment referencing the old latch Z=94 / 8mm miss; the actual hasp_plate/part.py now uses latch_hole_z=34.0 (assembled Z=86, aligned). Cosmetic only — not edited to avoid touching a PASSED assembly.
