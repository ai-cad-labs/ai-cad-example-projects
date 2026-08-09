# Sourcing Notes — piston_crank

## Make-vs-Buy summary

| Part | Plan designation | Sourcing verdict | Rationale |
|------|-----------------|------------------|-----------|
| piston | Make | Make — agreed | Custom geometry (grooves, bosses); no standard equivalent |
| piston_ring | Make | Make — agreed | v1 uses a shared rectangular-section ring geometry custom to the ⌀54 groove root; real engine rings are catalog items, but the plan explicitly keeps this as modeled custom geometry for v1 |
| gudgeon_pin | Make | Make — agreed | ⌀16 x 50, ID ⌀9 hollow pin; simple turned part, dimensions locked to piston boss span |
| connecting_rod | Make | Make — agreed | Fully custom |
| crankshaft | Make | Make — agreed | Fully custom one-piece single-throw crank |
| bronze small-end bushing | **Buy** | **Buy — agreed** | Plain bearings are always purchased; sintered/wrapped bronze and DU bushings in the 16 mm shaft class are ubiquitous catalog items |

Task string and design_plan.md agree: the bushing is the ONLY Buy item. No
fasteners (one-piece big end) and no main bearings (journals free per goals.md).

## Bushing selection reasoning

**Duty**: small-end bearing between the ⌀15.99 full-floating gudgeon pin and the
connecting rod small end (bore land ⌀16 nominal, boss OD 26, width 20). Oscillating
(not fully rotating) motion, boundary lubrication — the classic use case for a
wrapped bronze (e.g., CuSn8 with lubrication indents) or DU-type (steel-backed
PTFE-lined) bushing.

**Geometry targets** (from design_plan.md dimension chain + rod constraints.md):
- ID (installed, finished): ⌀16.0 nominal, running clearance ~16.02 on the ⌀15.99 pin
- OD: ~⌀18 (1 mm wall) — thin-wall wrapped bushing class; keeps small-end boss wall
  at (26 − 18)/2 = 4.0 mm, still ≥ 1.5 mm minimum ✓
- Length: ≤ 20 mm (rod small end width is 20.0; flush or sub-flush)

**Candidate standard family**: wrapped bushings per ISO 3547 / DIN 1494 in the
nominal 16 (ID) x 18 (OD) x 20 (L) size. This size family is a plausible standard
fit for the targets above, **but bushings are not in my verifiable knowledge
baseline** (which covers screws, 6000-series bearings, retaining rings, O-rings,
dowel pins), so per the honesty rule the BOM row is marked
**UNVERIFIED — needs catalog lookup**. What the lookup must confirm:
1. That a 16x18x20 (or 16x18x16) wrapped bronze/DU size exists in the chosen
   vendor's catalog (SKF PCM series, GGB DU, INA/permaglide, or generic CuSn8 wrapped)
2. The housing-bore press-fit tolerance class (typically H7 housing bore for
   ISO 3547 wrapped bushings) and the resulting installed ID
3. Whether the installed ID lands at the required ~16.02 running clearance
   as-pressed, or needs a post-install finish ream

## v1 vs v2 — connecting rod small end (IMPORTANT: v1 is locked)

- **v1 (current)**: rod small end = plain ⌀16.02 bore, steel directly on pin.
  `assembly/connecting_rod/constraints.md` is LOCKED to this and was deliberately
  NOT modified by sourcing (per orchestrator directive). Its Manufacturing section
  already notes "bronze bushing (Buy) pressed into small end in a later revision" —
  no purchased-part interface block was added, so the cad_designer will not
  accidentally design around the bushing OD.
- **v2 (deferred change, guidance lives here only)**: once the catalog lookup
  verifies the bushing, open the small-end bore from ⌀16.02 to the bushing's
  specified housing bore (nominal ~⌀18, press fit — expect an H7-class housing
  bore per the verified spec), press the bushing, and verify/ream installed ID to
  ⌀16.0 (+0.02) clearance on the pin. Bushing length ≤ 20 mm flush with rod faces.
  Boss OD 26 stays unchanged (4.0 mm wall over an 18 OD bushing ✓).

## Open questions for the orchestrator

1. Catalog lookup needed to close the UNVERIFIED BOM row (blocked until the
   sourcing-tables capability lands, or a human/web lookup is done). Not blocking
   for v1 — the bushing is not modeled.
2. Material choice within the family (wrapped CuSn8 bronze vs DU/PTFE-lined) can be
   deferred to the same lookup; both fit the oscillating small-end duty.
