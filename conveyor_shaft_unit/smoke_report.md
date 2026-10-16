# Smoke report — conveyor_shaft_unit

**Date**: 2026-10-09 ·
**Run**: single session, 15 spawns ·
**Orchestrator status**: `complete` ·
**Reviewer verdict**: `ship`

**Smoke verdict**: **SHIP WITH TWO CONFIRMED CRITICALS — the models are sound, the
installation is not.**
All seven of `goals.md`'s success criteria are met or substantially met,
and every hard dimension the brief names is correct by measurement.
But a `dfma_inspector` that finished *after* the orchestrator had already closed the run
reported two CRITICAL defects,
and **both reproduce in independent measurement performed for this report**.
Neither is a geometry error in a part;
both are installation/serviceability defects that no per-part gate could see.

## How this report was produced

Every number below was **re-measured from the built solids** in a thread independent of
the orchestrator, the validators and the inspector.
Nothing is transcribed from their claims.
The measurement scripts and their raw JSON output were session-local
and are not shipped with this run.
Where my figure differs from an agent's, both are given and the difference explained.

Measurement conventions:
shaft axis = global Z, up = +Y, drive end = +Z,
origin midway between the bearing centres (z = ±75).
All three Make parts are modelled in this shared frame and placed with identity transforms.

---

## 1. Success criteria from `goals.md`

### 1.1 Every Make part parametric, 8 renders, `VALIDATION: PASSED`, a DFM report — **PASS**

| Part | `part.py` | Solids | Volume (mm³) | Bbox X×Y×Z (mm) | Renders | Final marker line | DFM report |
|---|---|---|---|---|---|---|---|
| shaft | `assembly/shaft/part.py` | 1 | 408,899.7 | 48 × 48 × 300 | 8 | `VALIDATION: PASSED` | `dfma_report.json` |
| housing | `assembly/housing/part.py` | 1 | 1,281,894.1 | 130 × 145 × 190 | 8 | `VALIDATION: PASSED` | `dfma_report.json` |
| cover | `assembly/cover/part.py` | 1 | 153,290.9 | 130 × 130 × 23 | 8 | `VALIDATION: PASSED` | `dfma_report.json` |

Each is a single closed solid, each re-executed cleanly in this verification thread,
and in each case `VALIDATION: PASSED` is the **last line** of `notes.md`, as the contract requires.
All three are genuinely parametric: named constants drive a revolved or cut profile,
not hard-coded vertices.

### 1.2 Complete `assembly/assembly.py` placing every part — **PARTIAL**

`assembly/assembly.py` executes and places **17 components**:

```
bearing_drive_end  bearing_far_end  circlip_din471_40  cover  housing  shaft
lip_seal_40x62x10  grease_nipple_z+70  grease_nipple_z-70
cap_screw_m8x25_{045,135,225,315}      bolt_m12x40_{x±45_z±55}
```

**Gap**: `external/bom.md` specifies **22 purchased pieces**;
14 are modelled.
Missing are the **4 × ISO 7089-12 washers** and **4 × ISO 4032 M12 nuts**,
both of which the BOM lists as required line items.
This is not cosmetic — see §4.1:
the unmodelled washer is exactly the part that collides,
and its absence from the assembly is *why* the interference sweep reported the foot bolts clear.

**Portability note**: `assembly.py` is not standalone-runnable.
It depends on a harness-injected global `__project_path__`
(supplied by `cadquery_executor.py` and `exporter.py`);
a bare `python assembly.py` raises `NameError`.
This is the repo's convention rather than a defect, but it is undocumented in the file.

### 1.3 Interfaces consistent — **PASS**

**Two in-line Ø80 H7 bores on a common axis.**
Bracketed by probe rather than read from source:

| Bore | Ø80 probe on axis | Ø81 probe on axis | Ø80 probe offset 0.5 mm in X |
|---|---|---|---|
| drive end (z +66…+84) | 124.62 mm³ * | 2,394.41 mm³ | 812.44 mm³ |
| far end (z −84…−66) | **0.000 mm³** | 2,269.79 mm³ | 719.99 mm³ |

A Ø80 cylinder passes through the far bore with **zero** material contact;
Ø81 bites; offsetting Ø80 by 0.5 mm bites.
The bore is therefore exactly Ø80, centred on the Z axis, at both stations.
\* The drive-end 124.62 mm³ is the 1 × 45° relief chamfer at z = +66…+67, not a bore error
(the chamfer is required — see §2.3).

**Bearing bore ↔ shaft seats.**
Measured clear of the chamfers (z 70…80 and −80…−70):
volume **12,566.371 mm³** against analytic π·20²·10 = **12,566.371 mm³** — exact to three decimals;
bbox 40.0000 × 40.0000; axis offset x = y = 0.0000.
Both seats are Ø40.000 on axis.

**Drive-end location: shoulder + circlip.**
From exact planar-face enumeration (not sampling):

| Feature | z (mm) | Annulus | Area (mm²) |
|---|---|---|---|
| shaft collar face | **+66.000** | r21 → r24 | 424.115 |
| circlip groove rear wall | **+84.000** | r18.75 → r20 | 152.171 |
| circlip groove front wall | +85.850 | r18.75 → r20 | 152.171 |

Clamped width = 84.000 − 66.000 = **18.000 mm exactly** = the 6208 width.
**Zero drive-end float; the bearing is fully located — as nominal geometry.** ✓

> **⚠️ Defeated in practice by ISSUE-010.** The 18.000 figure is measured face-to-face and is
> correct. But a real r1.1-cornered inner ring cannot close onto the collar: it seats
> **0.3556 mm proud**, at z = 66.356. That leaves 84.000 − 66.356 = **17.644 mm of space for
> an 18.000 mm wide ring**, so the circlip cannot be fitted to its groove.
> **The run's single most-celebrated number does not survive contact with the real catalogue
> part.** The nominal stack-up is right; the shoulder detailing is not.

**Far-end float 1–2 mm.**
Housing far shoulder flat face measured at **z = −64.500** (annulus r36 → r39, area 706.858 mm²);
bearing inboard face at z = −66.000.
Float = **1.500 mm**, inside the 1.0–2.0 mm spec. ✓

> A naive Ø80 sharp-cornered probe reports first contact at z = −65.51 (0.49 mm),
> because it clips the 1 × 45° relief chamfer spanning z = −65.5…−64.5.
> The real 6208 has an r1.1 corner radius that clears that relief,
> so **1.500 mm face-to-face is the correct figure** and 0.49 mm is a probe artifact.

**Catalogue abutment envelopes — both correct.**
Shaft shoulder (da) = Ø48 ≥ da min **47** ✓.
Housing shoulder (Da) = Ø72 passage ≤ Da max **73** ✓.
The planner sized the central passage to Ø72 deliberately against the catalogue limit.

**Cover bolt pattern ↔ housing face.**
Cover: 4 × Ø9 on BC 104.0, at 45/135/225/315°.
Housing: 4 × M8 tapped on BC 104 at the same clocking, in the Ø130 × 20 drive-end boss.
Measured thread engagement 13.0 mm into a 16 mm tapped hole (see §3, pairs 4–7). ✓

**Seal bore ↔ shaft.**
Cover seal pocket Ø62 H8 × 10 deep;
shaft seal journal Ø40 at z = +90…+100.
Matches the 40 × 62 × 10 AS seal in the BOM. ✓

### 1.4 No interference; wrench clearance at the four M8 cover bolts — **PARTIAL / PASS**

Full 136-pair exact-boolean sweep over all 17 components: **7 overlapping pairs, 0 boolean failures.**
Four are designed thread engagement.
**Three are a real interference class** at the bearing shoulders — see §3 and ISSUE-010.
Wrench clearance at the four M8 cover bolts passes outright.

M8 cover-bolt wrench access, measured as a driver column rising 30 mm in +Z
off the cover front face (z = +107) at each of the four bolt stations:

| Driver envelope | Obstruction other than the bolt being driven |
|---|---|
| Ø6 hex key (ISO 4762 calls for 6 mm AF) | **none** |
| Ø13 socket = head OD | **none** |
| Ø16 thin-wall socket | **none** |
| Ø18 socket | **none** |

Identical at 45°, 135°, 225° and 315°.
Nothing — not the housing, not the cover rim, not a neighbouring screw — enters the column.
**Wrench clearance at the four M8 cover bolts: PASS by measurement.** ✓

### 1.5 `external/bom.md` listing every catalogue part — **PASS**

8 line items, 22 pieces plus one consumable, every designation grounded in a published standard
(ISO 15, ISO 5753, DIN 471, DIN 3760/ISO 6194, ISO 4762, ISO 4014, ISO 4032, ISO 7089, ISO 273, DIN 71412).
Covers the 2 × 6208, circlip, lip seal, 4 × M8, 4 × M12 + washers + nuts, 2 × grease nipples, grease.
Three figures are explicitly marked **UNVERIFIED** rather than invented
(DIN 471 permissible thrust, nipple hex AF, grease product).
No vendor part number is fabricated anywhere.
This is the strongest single document in the run.

### 1.6 STEP and STL exports for every validated Make part — **PASS**

| File | Bytes |
|---|---|
| `assembly/shaft/exports/shaft.step` | 40,728 |
| `assembly/shaft/exports/shaft.stl` | 239,284 |
| `assembly/housing/exports/housing.step` | 200,851 |
| `assembly/housing/exports/housing.stl` | 541,984 |
| `assembly/cover/exports/cover.step` | 42,029 |
| `assembly/cover/exports/cover.stl` | 227,684 |

6 / 6 present and non-trivially sized. ✓

### 1.7 DFM and DFA review recorded; reviewer verdict recorded — **PASS, but the DFM/DFA record is stale**

Recorded: `dfma_review.md`, four machine reports
(`assembly/{shaft,housing,cover}/dfma_report.json` + `assembly/dfa_report.json`),
reviewer verdict `ship` (completeness 0.97) in `design_log.md`.

**However** `dfma_review.md` was written by the orchestrator from the inspector's *machine artifacts*
when the inspector appeared to have finished mute.
The inspector was in fact still running.
Its consolidated review — carrying both CRITICALs and three MAJORs — landed afterwards and
**is not reflected in `dfma_review.md`, in `open_issues.md`, or in the reviewer's `ship` verdict.**
Its own overall DFA score is **2.4 / 5 — FAIL**.
See §4.

---

## 2. The brief's hard requirements, measured

| # | Requirement | Measured | Verdict |
|---|---|---|---|
| 1 | Two 6208 bearings (40 × 80 × 18) | both bores Ø80.000 on axis, seats Ø40.000, 18.000 clamp | ✓ |
| 2 | Drive end located between shoulder and circlip | collar +66.000, groove wall +84.000, span **18.000** = zero float | ✓ |
| 3 | Far end floats 1–2 mm | shoulder −64.500 vs bearing face −66.000 = **1.500 mm** | ✓ |
| 4 | Single cast body, two in-line bores | 1 solid, 1,281,894.1 mm³, both bores on the Z axis | ✓ |
| 5 | Mounting foot, four bolt holes | 4 × Ø14 at (X ±45, Z ±55) in the foot plate | ✓ geometry / ✗ access (§4.1) |
| 6 | Bolted steel cover with radial lip seal | cover Ø130 × 23, Ø62 H8 × 10 pocket, 40×62×10 AS seal in BOM | ✓ |
| 7 | Four M8 bolts with wrench clearance | 4 × Ø9 on BC 104; Ø18 driver column unobstructed at all four | ✓ |
| 8 | k6 on shaft seats | `shaft/constraints.md:88` — ⌀40 k6 (+0.018/+0.002) | ✓ recorded |
| 9 | H7 in housing bores | `housing/constraints.md:135` — ⌀80 H7 (+0.030/0) | ✓ recorded |
| 10 | 1 mm chamfers at every bearing shoulder | 4 / 4 bearing shoulders, each **axial length exactly 1.000** | ✓ |
| 11 | Minimum housing wall 8 mm | Ø80→Ø96 band 99.675 % filled; deficit = the grease drilling | ✓ |
| 12 | Grease nipple reachable from above | 2 bosses, top faces at Y = +70.0 = the housing global ymax | ✓ |

### 2.3 Chamfers in detail

11 conical faces across the three parts, **every one of axial length exactly 1.000 mm**
(fillets are deferred project-wide, so every cone is a chamfer):

| Part | n | At the bearing shoulders |
|---|---|---|
| shaft | 5 | z +66→+67 (r20→21) · z −67→−66 (r20→21) |
| housing | 4 | z +66→+67 (r39→40) · z −65.5→−64.5 (r39→40) |
| cover | 2 | both at the spigot nose z +84→+85 |

All **four** bearing shoulders carry their 1 mm chamfer, exactly as the brief demands.

**But 1 mm is the one value that cannot work against a 6208.**
A 45° chamfer of leg *c* clears a bearing corner radius *R* only when
*c* ≤ *R*(2 − √2) = **0.644 mm** or *c* ≥ *R*(2 + √2) = **3.76 mm**.
At *c* = 1.0 the chamfer ramps straight through the space the r1.1 corner needs.
Measured directly: the bore void runs r = 39.2 at z = 66.2, r = 39.5 at 66.5,
r = 39.8 at 66.8, reaching the full r = 40 only at z = 67 —
so the chamfer *adds* material into the bore mouth rather than relieving the corner.
A bearing seat wants a fillet of *ra* ≤ 1.0 **or** an undercut, never a mid-band 45° ramp.
**This is a brief-versus-catalogue conflict of exactly the same kind as ISSUE-001**
and is escalated, not silently corrected — see **ISSUE-010**.

### 2.4 Minimum wall in detail

An 8 mm radial band (Ø80 → Ø96) around each bore has volume 30,963.54 mm³.
Housing fills 30,862.95 mm³ (drive end) and 30,862.86 mm³ (far end) — **99.675 %**.
The deficit is 100.59 and 100.68 mm³.
A Ø4 grease feed drilling through an 8 mm wall is π·2²·8 = **100.53 mm³**.
The shortfall is accounted for, to within 0.15 mm³, by exactly one deliberate grease drilling per bore.
**The 8 mm minimum wall holds everywhere except where the design intentionally drills through it.** ✓

---

## 3. Interference sweep — all 7 overlaps adjudicated

136 pairs tested across 17 components, exact booleans, no bbox shortcuts on the reported pairs.

| Pair | Overlap (mm³) | Adjudication |
|---|---|---|
| `bearing_drive_end` ∩ `housing` | 124.617 | **REAL — not an artifact.** See the correction below and ISSUE-010. |
| `bearing_drive_end` ∩ `shaft` | 63.879 | **REAL.** See below. |
| `bearing_far_end` ∩ `shaft` | 63.879 | **REAL.** Mirror of the above, identical to the digit. |
| `cap_screw_m8x25_*` ∩ `housing` (×4) | 181.333 each | **Designed thread engagement.** Ø8 screw in a Ø6.8 tapping-drill hole: annulus π(4² − 3.4²) = 13.94 mm²/mm × **13.0 mm** = 181.3 mm³. Exactly the 13 mm engagement the BOM specifies (25 mm screw − 12 mm flange). ✓ |

> **CORRECTION (this section first called the three bearing overlaps modelling artifacts —
> that was wrong, and the error is instructive).**
> The reasoning was: `assembly.py` models bearings as sharp-cornered Ø80 primitives, a real
> 6208 has an r1.1 corner radius, the catalogue gives `ra max` = 1.0 mm for such a corner,
> therefore a 1 mm chamfer is standard-correct and the real ring clears.
> **`ra max` governs a shoulder FILLET, not a 45° chamfer.** They are different geometries
> and the substitution is invalid.
> Re-measured with a realistic r1.1-cornered ring built by revolved profile:
> **housing overlap 59.255 mm³, shaft overlap 30.590 mm³ — it does not clear.**

**One genuine interference class, affecting all four bearing shoulders.**
Both rings must back off **0.3556 mm** axially to clear their shoulder.
Closed-form check: for a 45° chamfer of leg *c* against a corner radius *R*, the back-off is
√2·(*R* − |*c* − 2*R*|/√2) = 1.4142 × (1.1 − 0.8485) = **0.3557 mm** — matching the measured
0.3556 to four decimals, from a different method.
Consequences in §4.6 / **ISSUE-010**.

The four screw overlaps remain the most useful *clean* number in the sweep:
they independently confirm the BOM's engagement arithmetic from the geometry.

**Method note.** The three bearing overlaps are mirrored to the digit, and this report's own
§6 heuristic says symmetric findings on symmetric designs are *suspect*. Suspicion is not
disproof — the symmetry proves the model is symmetric and says nothing about whether the
overlap is physical. Treating a heuristic as a verdict is what produced the error.

---

## 4. Confirmed defects the `ship` verdict does not account for

These arrived from the `dfma_inspector` after the orchestrator closed the run.
**I reproduced both from scratch rather than accept them.**

### 4.1 CRITICAL — the M12 foot bolts cannot be washered or socketed · **CONFIRMED**

Bolt axis vertical (+Y) at (X ±45, Z ±55), head seating on the foot plate top face Y = −60.
Cast iron found inside each envelope, **identical at all four stations**:

| Envelope about the bolt axis | Cast iron inside | Verdict |
|---|---|---|
| Ø18 plain cylinder — *what `assembly.py` models* | **0.000 mm³** | clear |
| ISO 4014 head across corners, Ø20.04 | 0.338 mm³ | marginal |
| **ISO 7089-12 washer, OD 24, seated** | **45.016 mm³** | **blocked** |
| Thin-wall socket, Ø24 | 360.124 mm³ | **blocked** |
| Standard socket, Ø26 | 681.556 mm³ | **blocked** |

The obstruction is the pedestal rib (a solid wall at X = ±35 running the full 190 mm at Y = −60…−40),
10 mm from the bolt axes.

**The washer is mandated by this project's own BOM** — the row reads
*"the 14 mm clearance hole is oversize for M12 and needs the washer's 24 OD to bridge it."*
So the part that collides is a part the design requires and the assembly never modelled.

**Why every earlier check missed it.**
`assembly.py` models fastener heads as plain cylinders, `M12_HEAD_D = 18.0`, with no washer.
`ISSUE-005` records this exact position as RESOLVED,
"independently re-measured … 0.000 mm³ at all four new stations",
confirmed by three separate threads.
All three probed Ø18.
**Three independent confirmations of the same too-small abstraction.**
The earlier fix (moving the bolts Z ±75 → ±55 to escape the flange boss) traded one
blocked position for another.

*The inspector's figure for the washer is 135.047 mm³ against my 45.016 mm³ —
it swept a 7.5 mm column, I probed the washer's own 2.5 mm seated thickness.
Same defect, different probe depth; both non-zero.*

**Inspector's proposed fix** (not applied): `FOOT_X` 120 → 130 and `FOOT_HOLE_X` 45 → 50.
Zero envelope growth — the flange is already Ø130, so the bbox X stays 130.
One or two constants.

### 4.2 CRITICAL — the documented assembly sequence is physically impossible · **CONFIRMED**

The sequence in `assembly.md` presses both bearings onto the shaft and inserts the stack from the drive end.
That requires an OD-80 bearing to traverse the Ø72 central passage.

Swept annulus r36–40 along z = −63.5 … +67:
volume 124,633.3 mm³, of which **123,802.8 mm³ is cast iron — 99.3 % blocked.**
The shaft alone passes freely: its Ø48 envelope over its full length meets **0.000 mm³**.

**This is a documentation defect, not a geometry defect.**
The unit *can* be assembled, in a different order:
DE bearing + circlip onto the shaft → insert from +Z
(the DE bearing then travels only +95 → +66, entirely inside the Ø80 drive-end bore,
never meeting the Ø72 passage) → FE bearing from the far face along the exposed journal →
cover → nipples → foot bolts.
The housing never needs turning over.
Fix is prose plus the `add()` ordering; no geometry changes.

**Why every earlier check missed it**: static interference testing is blind to installability.
In the final pose nothing overlaps.
The orchestrator's own `reflection_notes.md` flags this class of blindness after
catching a related case (a Ø62 seal behind a Ø46 bore) by mentally walking the sequence —
and then the same class recurred, uncaught, in the shipped sequence.

### 4.3 MAJOR — square step in the lip seal's slide path · **CONFIRMED**

Cross-sectional diameter along the shaft at the Ø40 → Ø35 transition:

| z (mm) | 119.0 | 119.9 | **120.0** | 120.4 | 120.6 | 121.0 |
|---|---|---|---|---|---|---|
| Ø (mm) | 40.00 | 40.00 | **36.98** | 36.18 | 35.78 | 35.00 |

The 1 × 45° chamfer bridges Ø35 → Ø37 only.
At z = 120.0 the diameter jumps 36.98 → 40.00: a **1.51 mm square radial shoulder**.
The cover-and-seal sub-assembly slides on from +Z,
so the seal lip climbs the ramp to Ø37 and then must jump a square step to reach the Ø40 journal.
That destroys lips.
Fix: replace the 1 mm chamfer at `Z_STEP_EXT` with a lead taper spanning the full Ø35 → Ø40
(two profile points; this chamfer is **not** one of the four the brief protects).

### 4.4 MAJOR — tolerance zoning (reported, not independently re-measured)

`shaft/constraints.md:88` calls ⌀40 k6 over the whole seat length,
and `part.py` models one Ø40 cylinder from z = −135 to −66.
The FE bearing would be pressed **51 mm** along k6, and the DE bearing driven **36 mm**
across the ground Ra ≤ 0.4 seal journal.
Fix is a callout change with zero geometry impact:
confine k6 to the two 18 mm seats, call the journal ⌀40 f7, relieve the intervening runs to ⌀39.8.

### 4.5 MAJOR — no cover extraction provision (reported, not independently re-measured)

Cover OD 130 is exactly flush with the housing flange OD 130;
no pry lip, notch or jacking thread anywhere on the joint.
Fix: two tapped jacking holes at 0°/180° on BC 104, clear of the fixing screws at 45/135/225/315°.

### 4.6 CRITICAL — neither bearing can seat on its shoulder · **FOUND BY THIS REPORT**

Not reported by any agent in the run.
Surfaced only when the critical-thinking pass challenged this report's own claim that the
three bearing overlaps were modelling artifacts.

A realistic 6208 with r1.1 corner radii, built by revolved profile and intersected with the
as-built parts:

| Interface | Sharp-cornered primitive | Realistic r1.1 ring | Axial back-off to clear |
|---|---|---|---|
| outer ring ∩ housing shoulder | 124.617 mm³ | **59.255 mm³** | **0.3556 mm** |
| inner ring ∩ shaft collar | 63.879 mm³ | **30.590 mm³** | **0.3556 mm** |

Closed-form cross-check: √2·(*R* − |*c* − 2*R*|/√2) with *R* = 1.1, *c* = 1.0 gives
**0.3557 mm**. Measured 0.3556. Four decimals, two independent methods.

**Root cause.** A 45° chamfer of leg *c* clears a corner radius *R* only when
*c* ≤ *R*(2 − √2) = 0.644 or *c* ≥ *R*(2 + √2) = 3.76.
**The brief mandates *c* = 1.0 — inside the forbidden band.**
Directly measured: the bore void reaches only r = 39.2 at z = 66.2 and r = 40.0 at z = 67,
so the chamfer ramps material *into* the bore mouth instead of relieving the corner.

**Consequences.**
- Drive end: the inner ring seats at z = 66.356, leaving **17.644 mm for an 18.000 mm ring**.
  **The circlip cannot be fitted.** The located bearing is not located.
- The outer ring seats at 66.356…84.356 against a cover spigot face at z = 84.000 —
  0.356 mm of clash, so the spigot cannot clamp as designed.
- All four bearing shoulders are affected (both parts, both ends).

**Do not silently "fix" this.** It is a brief-versus-catalogue conflict of the same class as
ISSUE-001: the brief names 1 mm chamfers explicitly, and the catalogue part cannot accept
one. The correct detail is a fillet of *ra* ≤ 1.0 or a corner undercut — both of which depart
from the brief's literal instruction. Escalate; the operator decides.

**Why nothing caught it.** Same root cause as ISSUE-008: `assembly.py` models catalogue parts
as idealised primitives. The washer is absent entirely; the bearings are sharp-cornered.
**One abstraction gap, three defects** (ISSUE-008, ISSUE-010, and the cover-spigot clash).

---

## 5. Process findings for the operator

### 5.1 Fence breach — `rules/` was modified

Operator instruction 7 was *"never edit anything under `.shared/`, `frontend/`, `docs/`, `rules/` or `tests/`."*
All five files in `rules/` carry mtime **2026-10-09 00:42**:
`dfm_rules.json`, `dfa_rules.json`, both `.proposed.json` siblings, and `rule_lifecycle_log.json`
(now 43 entries).
The `dfma_inspector` retired 12 rules and proposed 2 via the evaluator's
`--retire-rule` / `--propose-rule` CLI, which writes there as a side effect.

The fence was in the operator instructions but **the orchestrator did not relay it into the
inspector's task string** — the death-guard block was relayed, the write-fence was not.
I have left the changes in place rather than revert them;
reverting is the operator's call and would need a git operation, which is also fenced.

### 5.2 The reviewer's `ship` is built on an incomplete DFM/DFA record

Not the reviewer's fault — it reviewed what existed.
But the causal chain is worth recording:
the inspector was slow, not mute → the orchestrator applied the correct doctrine
("verify the filesystem, the deliverable on disk is what counts")
→ found four machine reports and no consolidated review
→ synthesised `dfma_review.md` from the machine artifacts at zero spawn cost
→ the machine reports contained the scores but not the *reasoning*, and both CRITICALs lived in the reasoning
→ reviewer saw a clean DFM/DFA record and returned `ship`.

**The doctrine that normally prevents a miss caused one here.**
"Silent finish is the default — verify the filesystem" is sound when an agent has died;
it is wrong when an agent is merely slow.
There was no signal available to distinguish the two.

### 5.3 Harness defects confirmed in passing

- **`spec_validator --query=state` under-reports.**
  It returns `parts_validated: 3` but `open_issues: []` / `open_issues_count: 0`
  while `open_issues.md` holds seven issues, one `NEEDS_HUMAN_INPUT`;
  and `assembly_executes: null` for an assembly that executes and renders.
  Already logged by the orchestrator; confirmed here.
- **Process misdetection** (`ISSUE-007`), root-caused by the inspector to
  `.shared/tools/dfma_evaluator.py:372-394`:
  `_parse_manufacturing` ignores the `Primary process:` line and returns the first
  `_PROCESS_KEYWORDS` hit *in dict order*, where bare `"milling"` precedes `"cnc turning"`.
  The cover says `Primary process: **CNC_turning**` and, two lines later,
  `drill 4 x dia 9 on a milling station` — the secondary op wins.
  **No turning rule has ever been applied to this turned part.**
  Reproducible; not fixed here (`.shared/` is fenced).
- **Zero active casting rules.** No rule in `rules/dfm_rules.json` lists `casting`,
  so the housing — the most manufacturing-sensitive part in the unit — was graded on
  2 generic rules out of 47. Its "pass" carries little information.

---

## 6. Bottom line

**What is genuinely good**: three clean single-solid parametric parts, first-try on all three,
zero valid gate rejections, every brief-named *nominal* dimension correct to three decimals,
an exceptionally well-grounded BOM that caught a capacity shortfall no geometry check could,
and four interference overlaps that independently reproduce the BOM's own thread-engagement
arithmetic.

**What is not ready**: the unit cannot be bolted down with its specified washers,
cannot be assembled in its documented order,
and **neither bearing can seat on its shoulder**.
The first two are small fixes — two constants and a paragraph.
The third is a genuine engineering conflict with the brief's own wording.

**Recommended status: `pause_for_human`, not `ship`.**
Four items for the operator, in order:

1. **Decide ISSUE-010 (new, found by this report).** The brief's 1 mm bearing-shoulder
   chamfer is the one value a 6208's r1.1 corner cannot accept; both rings seat 0.356 mm
   proud and the drive-end circlip cannot be fitted. Needs a fillet (*ra* ≤ 1.0) or an
   undercut — both departures from the brief's literal text. **This is the item that most
   changes the design.**
2. Apply the foot-bolt fix (`FOOT_X` 120 → 130, `FOOT_HOLE_X` 45 → 50) and re-run the
   interference sweep **with the washers, nuts and realistic bearing corner radii in
   `assembly.py`** — the sweep is only as good as the envelopes it is given, and that single
   abstraction gap produced three of this report's findings.
3. Rewrite the assembly sequence in `assembly.md:62-65` and reorder the `add()` calls.
4. Decide `ISSUE-001` — the brief fixes both the 6208 and 20,000 h and they are arithmetically
   incompatible (L10h = 14,094 h; required C = 34.5 kN against the 6208's 30.7 kN).
   The reviewer's addition stands: the ~1,300 h grease relubrication interval means a literal
   "20,000 hours between services" fails for *any* bearing choice.
   This needs the customer, not a redesign.

**A note on this report's own reliability.** §3 originally dismissed the three bearing
overlaps as modelling artifacts, on a catalogue rule that governs fillets being applied to a
chamfer. That claim was wrong and is corrected in place rather than quietly edited out. The
error is the same species as the one this report criticises in the run — reasoning about an
idealised abstraction instead of measuring the specified part — which is worth more to the
dev loop than a clean report would have been.
