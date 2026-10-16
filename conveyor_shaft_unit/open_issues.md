# Open Issues — conveyor_shaft_unit

> **AMENDED 2026-10-08 by the verification session.**
> `dfma_inspector` finished after the orchestrator closed the run and reported two CRITICALs.
> Both were re-measured independently and **confirmed**: see **ISSUE-008** and **ISSUE-009**.
> **ISSUE-005 is REOPENED** as a consequence.
> A third CRITICAL — **ISSUE-010**, neither bearing can seat on its shoulder — was found by
> the critical-thinking pass over this session's *own* report, by challenging its claim that
> the bearing overlaps were modelling artifacts. No agent in the run reported it.
> **ISSUE-008 and ISSUE-010 share one root cause**: `assembly.py` models catalogue parts as
> idealised primitives (washer absent, bearings sharp-cornered), so every catalogue-detail
> interaction is invisible to the interference sweep.
> The reviewer's `ship` verdict predates all four and does not account for them.
> Full measured evidence: `smoke_report.md` §4.

## ISSUE-001 — 6208 bearing life is 14,094 h against a 20,000 h brief requirement
**Status: OPEN — NEEDS_HUMAN_INPUT (engineering trade-off, not a modelling defect)**
**Raised:** 2026-10-08 by sourcing. **Ruling:** orchestrator S1.

The brief names BOTH a hard part selection (`size 6208`) and a hard duty
(`20,000 hours between services`). Catalogue arithmetic says the two cannot both hold.

Sourcing's computation (6208: C = 30.7 kN, C0 = 19 kN; Fr = 4 kN, Fa = 1 kN, n = 1500 rpm):

| Case | P | L10h | vs 20,000 h |
|---|---|---|---|
| Located (drive-end) bearing, radial shared 50/50, all thrust | 2.836 kN | **14,094 h** | **70 % — FAILS** |
| Floating (far-end) bearing | — | 40,187 h | passes |
| Worst case, one bearing carries everything | 4.0 kN | 5,023 h | fails badly |

Required C for 20,000 h at the located bearing = 34.5 kN. No variant inside the
40 x 80 x 18 envelope reaches it. The only part that closes it is a **6308
(40 x 90 x 23, C = 41 kN) -> 31,105 h**.

**ORCHESTRATOR RULING: keep the 6208. Do not upsize.**
The brief's part selection is an explicit hard requirement handed to this run, and a
6308 would move the housing bore 80 -> 90, the cover spigot, the bore lengths and the
whole axial stack — i.e. silently redesigning the unit around a number the customer
fixed. The shortfall is reported, not engineered away. Three legitimate resolutions are
the customer's to pick:
1. Accept a ~14,000 h relubrication/replacement interval for the drive-end bearing
   (the floating bearing already exceeds 20,000 h).
2. Approve the 6308 upsize and re-run the housing and cover.
3. Reduce the 1 kN thrust or share it, which is what actually drives P up
   (Y = 1.716 on the axial term contributes 1.716 of the 2.836 kN).

Nothing in the CAD model changes either way. The geometry is correct for a 6208.

---

## ISSUE-002 — M8 x 30 cover screw bottoms out in a 16 mm tapped hole
**Status: RESOLVED 2026-10-08 (orchestrator S1), no Make-part change.**

30 mm screw - 12 mm cover flange = 18 mm of screw into a 16 mm deep thread.
Changed the BOM line to **M8 x 25**: engagement 25 - 12 = **13 mm into 16 mm**
(1.6 x d, above the 1.5 x d minimum for steel-into-cast-iron, 3 mm run-out spare).
`external/bom.md` patched directly; no constraints.md, part.py or geometry touched.

---

## ISSUE-003 — grease purge has no dedicated escape path
**Status: RESOLVED 2026-10-08 (orchestrator S1) by existing geometry, no change.**

Sourcing flagged that ~7.2 g relubrication charges per bearing, with no relief, would
lift the lip seal. They do have a path: the **far-end bore is open to atmosphere**
(dia 80 bore runs to the z = -95 end face with no cover — the far end is the floating
end and the brief specifies a cover at the drive end only), and the **dia 72 central
passage connects both bores**, so purged grease vents at the far end, away from the
single lip seal at +Z. This is the conventional purge direction for a one-seal pillow
block. Recorded as a service note, not a geometry change.
A future revision adding a far-end closure must add a relief plug in the same change.

---

## ISSUE-004 — housing casting carries no draft and no radii
**Status: ACCEPTED BY PROJECT RULE — do not "fix" during repair.**

Fillets are deferred project-wide (harness rule), so the cast iron housing models sharp
re-entrant corners at the pedestal-to-body and boss-to-body junctions, and no 2 deg
draft on as-cast faces. A production drawing would carry R5-R8 and 2 deg draft. The DFM
evaluator is expected to flag this; it is intentional. Repair agents must NOT add
fillets to silence a DFM finding.

---

## ISSUE-005 — drive-end flange boss overhung the M12 foot bolt heads
**Status: ⚠️ REOPENED 2026-10-08 by the verification session — superseded by ISSUE-008.**
~~RESOLVED 2026-10-08 (repair attempt 2 + orchestrator gate override).~~
The fix below is real and correct as far as it goes: the boss no longer overhangs the bolt
heads. But it was verified only against the Ø18 plain cylinder `assembly.py` models, and the
bolts' new home at Z = ±55 is blocked by the pedestal rib for the ISO 7089 washer the BOM
mandates and for any socket. **Read ISSUE-008 before acting on anything in this entry.**

Found by the assembly interference sweep, invisible to all four per-part validations:
`housing ∩ M12 bolt` = **6.437 mm³** at each of (X = ±45, Z = +75), and **exactly 0** at the
Z = -75 pair. The asymmetry is what proved it real rather than a modelling convention.
Cause: orchestrator ruling R2 thickened the dia-130 drive-end boss to 20 mm (so a 16 mm M8
thread would fit), which started it at z = +75 — directly over the drive-end foot bolts
placed there by ruling R4. At the bolt-head top plane Y = -52.5 the r 65 boss reaches
X = ±38.32 against head edges at ±36.00: a **2.32 mm overlap**. Two of the four mounting
bolts the brief requires could not be physically fitted.

**Fix**: foot bolt holes moved Z = ±75 -> **Z = ±55** (one constant). The boss was NOT
touched. An M12 socket (r 12) at Z = 55 now sweeps z = +43…+67 against a boss starting at
z = +75 — 8 mm clear. Independently re-measured in the orchestrator's own thread with a
self-checked probe: **0.000 mm³ at all four new stations**, reproducing 6.437/0.000 at the
old stations as a positive control.

---

## ISSUE-006 — DFM regression gate: three infrastructure failures on one part
**Status: OPEN — harness defect, no project impact. For the maintainers, not this design.**

All three hit the housing in a single session:
1. **Gate run 1**: completed its promotion correctly (wrote `part.py.stable`,
   `dfma_report.json.stable`, `renders.stable/`, replaced `part.py`) and was then killed by
   the harness background time limit **before printing its stdout JSON verdict**. Verdict
   lost, not failed. Reconstructed deterministically by re-scoring the two reports.
2. **Gate run 2**: the inner evaluator CLI **timed out at the 560 s default** and produced no
   verdict at all. Re-run needed `CAD_EVALUATOR_TIMEOUT_S=1800`.
3. **Gate run 3 (the serious one)**: the gate wrote the **PROPOSAL's content into
   `part.py.stable`**, destroying the rollback baseline. Both sides of the comparison were
   therefore the same geometry — and the two passes scored it **0 and 1**, producing a
   spurious REJECTED with a "new failure" (DFM-GEN-003) that the surviving
   `dfma_report.json` for that exact geometry records as **pass**.
   This silently defeats the gate's entire purpose and would corrupt the rollback on any part
   whose proposal was genuinely worse.

**Orchestrator ruling**: rejection 3 overridden, fix retained, NOT counted toward the
2-rejection escalation ladder. Full reasoning in `design_log.md` at 23:47Z.

---

## ISSUE-007 — DFMA evaluator selects the wrong manufacturing process
**Status: OPEN — harness defect, no project impact. For the maintainers.**

The evaluator ran the **cover** as `CNC_milling` although its `constraints.md` states
`Primary process: CNC_turning`, so **no turning rules were applied to a turned part**. This
is a silent coverage hole — worse than a wrong verdict, because the report looks clean.
Related: on the cover its summary counter claimed `rules_failed: 1` while the results array
held none and the failures list was empty.

Also recorded, two refuted vision false positives worth a rule fix:
**DFM-TURN-002** computed the shaft's L/D as 8.6:1 by dividing total length (300) by the
**smallest** diameter (35, a short overhung stub) instead of the governing turned body
(45) — true ratio **6.67:1**. And a "no circlip groove" finding fired on a 1.85 mm feature
that occupies roughly **7 pixels** of render; the groove is present and measured.

---

## ISSUE-008 — CRITICAL: the M12 foot bolts cannot be washered or socketed
**Status: OPEN — BLOCKING. Supersedes the RESOLVED status of ISSUE-005.**
**Raised:** 2026-10-08 by `dfma_inspector`. **Independently confirmed** by the
verification session with a separate probe. No CAD change applied.

The pedestal rib (a solid wall at X = ±35 running the full 190 mm at Y = −60…−40) stands
10 mm from the M12 bolt axes at X = ±45. Cast iron measured inside each tool envelope,
**identical at all four stations**:

| Envelope about the bolt axis | Cast iron inside | Verdict |
|---|---|---|
| Ø18 plain cylinder — *what `assembly.py` models* | **0.000 mm³** | clear |
| ISO 4014 head across corners, Ø20.04 | 0.338 mm³ | marginal |
| **ISO 7089-12 washer, OD 24, seated** | **45.016 mm³** | **blocked** |
| Thin-wall socket, Ø24 | 360.124 mm³ | **blocked** |
| Standard socket, Ø26 | 681.556 mm³ | **blocked** |

The washer is **mandated by this project's own BOM**, whose row reads *"the 14 mm clearance
hole is oversize for M12 and needs the washer's 24 OD to bridge it."* Two of the four
mounting bolts the brief requires cannot be properly fitted or tightened.

**Why ISSUE-005's fix did not close this.** `assembly.py` models fastener heads as plain
cylinders (`M12_HEAD_D = 18.0`) with no washer. All three "independent" verifications of
ISSUE-005 probed that Ø18 envelope and correctly measured 0.000 mm³. Moving the bolts
Z ±75 → ±55 escaped the flange boss and landed beside the pedestal rib — one blocked
position traded for another. **Three agreeing threads measured the same too-small
abstraction.**

**Proposed fix** (inspector's, not applied, not measured): `FOOT_X` 120 → 130 and
`FOOT_HOLE_X` 45 → 50. Zero envelope growth — the flange is already Ø130, so bbox X stays
130. Gives 15 mm to the pedestal wall. Note the resulting outboard edge distance is exactly
8.0 mm, which reproduces the zero-margin pattern already flagged against the 8 mm wall rule.

**Do not re-close this without re-running the interference sweep with the washers and nuts
added to `assembly.py`.** The sweep is only as good as the envelopes it is given.

---

## ISSUE-009 — CRITICAL: the documented assembly sequence is physically impossible
**Status: OPEN — BLOCKING, but PROCEDURAL. No geometry change required.**
**Raised:** 2026-10-08 by `dfma_inspector`. **Independently confirmed** by the
verification session with a swept-volume probe.

The sequence in `assembly.md` presses both bearings onto the shaft and inserts the stack
from the drive end. That requires an OD-80 bearing to traverse the Ø72 central passage.

Swept annulus r36–40 along z = −63.5 … +67: volume 124,633.3 mm³, of which
**123,802.8 mm³ is cast iron — 99.3 % blocked.** Blocked from either end. The shaft alone
passes freely: its Ø48 envelope over its full length meets **0.000 mm³**.

**The unit is assemblable; only the documented order is wrong.** Corrected sequence:

1. DE bearing + circlip onto the shaft.
2. Insert the shaft from +Z — the DE bearing then travels only +95 → +66, entirely inside
   the Ø80 drive-end bore, and never meets the Ø72 passage.
3. FE bearing from the far face, sliding along the exposed journal.
4. Cover → grease nipples → foot bolts.

The housing never needs turning over; ops 2–5 happen with it sitting on its feet. Penalty
is two opposed axial insertion directions plus one vertical (3 vectors, 2 working stations).

**Fix**: rewrite the sequence prose in `assembly.md` and reorder the `cq.Assembly().add()`
calls to match. No part geometry changes.

**Why no gate caught it.** Static interference asks whether anything overlaps *in the final
pose* — always no, by construction. This run hit the same blind spot twice: once caught by
luck (a Ø62 seal behind a Ø46 bore, spotted only because the orchestrator mentally walked
the sequence before dispatching), once shipped. See `run_reflection.md` §5 for the proposed
swept-volume DFA gate.

---

## ISSUE-010 — CRITICAL: neither bearing can seat on its shoulder; the 1 mm chamfer is the wrong value for a 6208
**Status: OPEN — BLOCKING. NEEDS_HUMAN_INPUT (brief-versus-catalogue conflict).**
**Raised:** 2026-10-08 by the verification session's critical-thinking pass.
Found by challenging that session's own claim that the bearing overlaps were artifacts.
No agent in the run reported this.

The interference sweep's three bearing overlaps (124.617 / 63.879 / 63.879 mm³) were
initially dismissed as artifacts of `assembly.py` modelling bearings as sharp-cornered Ø80
primitives, on the reasoning that a real 6208 has an r1.1 corner and the catalogue gives
`ra max` = 1.0 mm. **That reasoning is invalid: `ra max` governs a shoulder FILLET, not a
45° chamfer.**

Re-measured with a realistic r1.1-cornered ring built by revolved profile:

| Interface | Sharp primitive | Realistic r1.1 ring | Axial back-off to clear |
|---|---|---|---|
| outer ring ∩ housing shoulder | 124.617 mm³ | **59.255 mm³** | **0.3556 mm** |
| inner ring ∩ shaft collar | 63.879 mm³ | **30.590 mm³** | **0.3556 mm** |

Closed-form cross-check √2·(R − |c − 2R|/√2) with R = 1.1, c = 1.0 → **0.3557 mm**.
Measured 0.3556. Two independent methods, four decimals.

**The geometric rule.** A 45° chamfer of leg *c* clears a bearing corner radius *R* only when
*c* ≤ *R*(2 − √2) = **0.644 mm** or *c* ≥ *R*(2 + √2) = **3.76 mm**.
**The brief mandates *c* = 1.0 — squarely inside the forbidden band.**
Directly measured on the housing: the bore void reaches r = 39.2 at z = 66.2, r = 39.5 at
66.5, r = 39.8 at 66.8 and the full r = 40.0 only at z = 67 — the chamfer ramps material
*into* the bore mouth rather than relieving the corner.

**Consequences.**
- Drive end: the inner ring seats at z = 66.356, not 66.000. Space to the circlip groove wall
  at z = 84.000 is **17.644 mm for an 18.000 mm wide ring — the circlip cannot be fitted.**
  **The located bearing is not located**, and the run's headline "18.000 mm exactly, zero
  float" holds only as nominal geometry.
- The outer ring seats at 66.356…84.356 against a cover spigot face at z = 84.000: 0.356 mm
  of clash, so the spigot cannot clamp the outer ring as designed.
- All four bearing shoulders are affected — both ends, both parts.

**DO NOT SILENTLY FIX.** This is a brief-versus-catalogue conflict of exactly the same class
as ISSUE-001. The brief names "1 mm chamfers at every bearing shoulder" explicitly, and the
specified catalogue part cannot accept one. The correct bearing-seat detail is a **fillet of
ra ≤ 1.0** or a **corner undercut**, both of which depart from the brief's literal wording.
Per this project's own doctrine — obey the stated requirement, compute and report the
conflict, never redesign around a customer-fixed number — this goes to the operator.

Options, none applied:
1. Reduce the shoulder chamfer to **0.6 × 45°** (inside the ≤ 0.644 clearance band). Smallest
   change; keeps a chamfer; departs from the stated 1 mm.
2. Replace the shoulder chamfers with **fillets of ra = 1.0** (textbook bearing-seat detail).
   Conflicts with the project-wide fillet deferral as well as the brief's chamfer wording.
3. Cut a **corner undercut / relief groove** at each shoulder. Most manufacturable for the
   cast-then-bored housing; most geometry change.
4. Keep 1 mm as specified and accept that the bearings seat on the ramp. **Not recommended:**
   it loses the circlip, the outer-ring clamp, and flat-face load transfer.

**Why nothing caught it.** Same root cause as ISSUE-008: `assembly.py` models catalogue parts
as idealised primitives — the washer absent entirely, the bearings sharp-cornered. **One
abstraction gap produced three defects** (ISSUE-008, ISSUE-010, and the cover-spigot clash).
Fix the envelope library before trusting any future interference sweep on this project.
