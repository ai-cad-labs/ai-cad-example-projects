# Smoke Report — spur_gear

**Status: ✅ COMPLETE / SHIPPED**
**Date:** 2026-07-21 · Run: resumed after mid-validation interruption (single continuous session to completion).

## Goal
Meshing involute spur-gear pair (pinion 18T + gear 30T, module 2, 20° pressure angle) on a plain shaft, 3D-printed. Pinion and gear must mesh at 48 mm centre distance with a half-tooth phase offset so teeth interlock without interpenetration; the shaft part is instanced twice (one per gear).

## Parts (all designed, executor-passed, validated)
| Part | Spec | Executor | DFM | Validation |
|------|------|----------|-----|------------|
| pinion | 18T, m=2, α=20°, OD⌀40 × 10 mm, bore ⌀8.2 slip-fit, centred on Z | ✅ | conditional_pass (0 failed; tip-land ground-truthed ~1.36 mm ≥ 0.5) | ✅ PASSED |
| gear | 30T, m=2, α=20°, OD⌀64 × 10 mm, bore ⌀8.2 slip-fit, centred on Z | ✅ | pass | ✅ PASSED |
| shaft | plain cylinder ⌀8 × 30 mm, centred on Z (instanced ×2) | ✅ | pass (6/6 rules; vol 1507.96 mm³ = π·4²·30) | ✅ PASSED |

**Design note:** golden `cylindrical_gear.py` arc-stitching failed for these params on both gears; designers switched to a robust point-sampled polyline involute (12–14 samples/flank). Bores ⌀8.2 = nominal ⌀8 + 0.2 mm print clearance (all slip-fit clearance taken on bore side; shaft OD is nominal).

## Assembly
`assembly/assembly.py` executes → single Compound, 39,739 mm³.
- pinion @ origin; gear @ (48, 0, 0) rotated **−6° about Z** (half-tooth phase); two shafts coaxial through each bore.
- **Mesh verified (two independent methods):** (a) orchestrator's Z=0 section-interference — 0° phase = 18.04 mm² overlap → −6° = 0.00 mm²; (b) parent-session **plane-independent 3D boolean** `pinion ∩ gear` over the full 10 mm face = **0.0000 mm³** at −6° vs a **180.36 mm³ control at 0°** (test discriminates). The two agree: 18.04 mm² × 10 mm face = 180.36 mm³. Clean, zero-interpenetration mesh at 48 mm centre distance.
- **Volume conservation check:** assembly 39,739.0 mm³ = pinion 9,363.6 + gear 27,359.5 + 2 × shaft 1,508.0 — exact, confirming the assembly holds exactly the 4 intended bodies (no fusion/loss).
- Colour legend: pinion=red, gear=blue, shaft_pinion=green, shaft_gear=orange.
- Assembly validation: ✅ **PASSED** (mesh + 48 mm centre distance + coplanar gears + coaxial shafts confirmed).

## DFMA sweep (`--mode=sweep`, no token-ceiling hit)
- **DFM:** gear=pass, pinion=conditional_pass, shaft=pass — **0 rules failed** across all parts.
- **DFA:** conditional_pass, 2 major flags, both accepted OUT OF SCOPE:
  - DFA-002 (no self-locating hub feature) — goals mandate a plain shaft + slip-fit bore, not a press-fit/locating hub.
  - DFA-008 (no lead-in chamfer) — chamfers/fillets deferred project-wide.
- No repair warranted.

## Reviewer verdict: **ship**
goals_met=yes · completeness=100% · converging · 0 repair iterations.

## Exports (all non-empty, independently verified)
| File | Bytes |
|------|-------|
| pinion.step / pinion.stl | 2,153,825 / 140,484 |
| gear.step / gear.stl | 4,445,618 / 247,284 |
| shaft.step / shaft.stl | 5,752 / 25,084 |
| assembly.step / assembly.stl | 6,704,065 / 437,684 |

(shaft.step is legitimately small — a plain cylinder is trivial STEP topology.)

## Deviations / follow-ups
1. `tools.exporter` only targets `part.py`; the assembly was exported by exec'ing `assembly.py` through the same `CadQueryExecutor` + `cq.exporters` path. **Recommend adding an `--entry-file` flag to the exporter.**
2. DFA-002 / DFA-008 major flags left unrepaired by deliberate scope call (documented in design_log).

No blockers. Pipeline ran to completion in one continuous session.
