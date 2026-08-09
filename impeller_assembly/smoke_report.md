# Smoke Report — impeller_assembly

**Outcome: COMPLETE.** Reviewer verdict `ship` (completeness 0.97, convergence: converging).
Run spanned 2 orchestrator sessions on 2026-08-05, ~14:48 to ~17:00 IST.

A small belt-driven centrifugal air-compressor assembly, designed from the user's hand sketch
and written brief. Six components: 3 Make parts designed from scratch, 3 Buy parts specified
from catalog.

---

## What was built

| Part | Type | Solids | Valid | Bounding box (mm) | Volume (mm³) | Validation |
|---|---|---|---|---|---|---|
| pulley_shaft | Make | 1 | yes | 48 × 48 × 118 | 28,846.4 | PASSED |
| bearing_housing | Make | 1 | yes | 108 × 95 × 40 | 132,338.3 | PASSED |
| impeller | Make | 1 | yes | 72.000 × 72.000 × 48.800 | 33,617.4 | PASSED |
| main_bearing (6203, 17×40×12) | Buy | — | — | — | — | BOM |
| inlet_bearing (688-2Z, 8×16×5) | Buy | — | — | — | — | BOM |
| lock_nut (ISO 4032 M10) | Buy | — | — | — | — | BOM |

`assembly/assembly.py` places all six components by pure Z translation, no rotations.
The three Buy parts are authored inline as representational geometry, so they need no part
directories. Assembly validated in S1: **VALIDATION: PASSED**, score 7.5/10.

## Verified final geometry

```
component        global Z span        assembly bbox: X[-54,+54] Y[-60,+36] Z[-58,+60]
bearing_housing  -28.000 ..  12.000   total volume 207,148.16 mm³
main_bearing     -12.000 ..   0.000
impeller         -14.000 ..  34.800   running clearance to housing = 0.8000 mm  [PASS]
lock_nut          34.800 ..  43.200   impeller ∩ housing  = 0.0000 mm³ (no interference)
inlet_bearing     47.000 ..  52.000   shaft    ∩ housing  = 0.0000 mm³ (no interference)
pulley_shaft     -58.000 ..  60.000
```

Every span matches the design plan's placement table exactly.

## Success criteria — all met

| Criterion (from goals.md) | Status | Evidence |
|---|---|---|
| All parts parametric CadQuery, validated with renders | ✅ | 3/3 parts, 8 renders each, all three notes.md end `VALIDATION: PASSED` |
| Complete assembly.py in sketch position, renders proving the stack fits | ✅ | assembly.py + 8 assembly renders; assembly VALIDATION: PASSED |
| Interfaces consistent (bearing OD ↔ housing bore, bearing ID ↔ impeller spigot, shaft ↔ bearing bores) | ✅ | Ø40 pocket ↔ 6203 OD; Ø17 spigot ↔ 6203 bore; Ø8 tail ↔ 688 bore; Ø10 seat ↔ impeller bore |
| Running clearance 0.5–1.0 mm present | ✅ | **0.8000 mm**, measured (see below) |
| STEP/STL exports for all validated parts | ✅ | 6 files: `.step` + `.stl` under each part's `exports/` |
| Integrated pulley-shaft as ONE part | ✅ | single turned solid, pulley + shaft + thread + tail |
| Impeller with BACKSWEPT blades | ✅ | 6 blades, 10.5° plan-view shift measured between r=20 and r=34 |
| Inlet bearing small enough not to block the inducer | ✅ | 688 OD 16.0 ≤ the Ø18 hub-nose ceiling |

### The headline requirement, measured rather than asserted

The impeller-backface-to-housing running clearance is **0.8000 mm**, inside the user's 0.5–1.0 mm
window. It was confirmed by five independent measurements across three agents and two
orchestrators. Most importantly it is realized **structurally, not as an assembly gap**: a
Ø22 × 0.8 standoff boss on the impeller bears directly on the 6203's inner-race face, so the
clearance is a machined dimension that cannot drift during assembly.

## Design decisions worth knowing

- **Sizing was anchored on catalog bearings, per the brief.** The 6203 (17×40×12) set the
  impeller spigot and housing bore; the 688 (8×16×5) set the shaft tail; the ISO 4032 M10 set
  the nose thread. Nothing was sized arbitrarily.
- **Sourcing caught two real traps.** The OPEN 688 is 4 mm wide, not 5, so the BOM pins the 2Z
  shielded variant to hold the planned width. DIN 934 M10 would overhang the Ø18 hub nose by
  0.8 mm/side; ISO 4032 stays within 0.24 mm/side, so ISO 4032 was specified.
- **Torque is carried by clamp friction, not a keyway** — shaft shoulder against the spigot end
  face, lock nut against the hub nose, grip length 48.8 mm. This was a deliberate scope choice.
- **The shaft deliberately does not touch the main bearing.** The impeller's spigot is interposed,
  per the user's spec.

## Deviations and open items

**One real manufacturability defect was found and fixed.** DFA-005: two of the four foundation
bolts were socket-blocked by the impeller's Ø72 overhang (a Ø12 socket intersected the wheel by
1697.7 mm³ per side). Repaired surgically as two parameters — foot width 80→108, bolt circle
|X| 32→46 — which passed the DFM regression gate, was promoted, and was re-verified this session
as still holding. **Assembly note for the builder: torque the foundation bolts before fitting the
impeller** is no longer required by this geometry, but remains good practice.

**Three MAJOR DFM findings on the impeller remain open, and are tooling defects rather than
design defects.** The evaluator judged a backswept centrifugal wheel under the 3-axis
`CNC_milling` ruleset even though its constraints declare `5_axis_milling`, because of a
confirmed harness bug. Under 3-axis rules a backswept wheel is correctly and inevitably
unmachinable — real impellers are 5-axis milled. The evaluator's own top recommendation was to
re-declare the process as 5-axis. **Its geometry recommendation — cut to 4 blades and straighten
them to radial walls — was deliberately REFUSED**, because the user explicitly asked for
backswept blades and the sketch draws them curved. See ISSUE-005 and ISSUE-006.

**Fillets and chamfers are absent everywhere.** Deferred project-wide by explicit repo doctrine
(fillets are this repo's most common CadQuery failure mode; correct geometry comes first). This
is a known, recorded scope boundary, not an oversight. See ISSUE-002.

**Manufacturing notes that travel with the parts:**
- pulley_shaft: turn between centres with tailstock support; steady rest when finishing the Ø8
  tail; take the Ø8 tail as a final light pass to avoid deflection chatter. (ISSUE-007)
- impeller: 5-axis mill the blade passages; billet stock Ø75 × 55.
- Blade thickness is 2.0 mm, which sits at the **floor** of the suggested 2.0–2.5 mm band. There
  is no margin above the recommendation. If a future revision raises the exducer blade height
  above 6.0 mm, revisit the thickness at the same time. (ISSUE-009)

## Tool reliability observed during this run

Recorded because it affects how much weight to give the DFM reports shipped alongside these parts:
- The DFM report **asserts the impeller has five blades. It has six** — refuted numerically by
  section cuts at three radii, each returning six disjoint solids at 60.00° spacing. (ISSUE-010)
- The same impeller geometry, byte-identical, evaluated twice returned `fail` and then
  `conditional_pass`, with the rule count applied dropping from 20 to 10. (ISSUE-006)
- The DFA evaluator earlier misidentified a bearing as a "washer". (ISSUE-003)

Every part verdict in this report is backed by numeric geometry probes, not by vision alone.

## What a human should look at first

1. Confirm that refusing the blade-straightening advice matches your intent — the wheel keeps
   6 curved backswept blades.
2. The 2.0 mm blade thickness has no margin above the DFM recommendation band's floor.
3. The impeller's DFM verdict cannot be cleanly resolved in this harness today: the 5-axis
   rulebook contains zero active rules (ISSUE-005). This is queued as a product fix.

## Artifacts

```
projects/impeller_assembly/
├── goals.md · design_plan.md · design_log.md · open_issues.md (10 issues)
├── smoke_report.md · run_reflection.md · reflection_notes.md · checkpoint.md
├── external/bom.md · external/sourcing_notes.md
└── assembly/
    ├── assembly.py + renders/ (8 views + color_legend.txt)
    ├── pulley_shaft/    part.py · constraints.md · notes.md · dfma_report.json
    │                    attempt_log.json · renders/ (8) · exports/ (.step .stl)
    ├── bearing_housing/ (same layout)
    └── impeller/        (same layout)
```
