# Bill of Materials

| Qty | Part | Specification | Source | Notes |
|-----|------|--------------|--------|-------|
| 1 | Bronze small-end bushing (wrapped) | ⌀16 ID x ~⌀18 OD x ≤20 L wrapped bronze or DU (steel-backed PTFE) bushing; exact designation UNVERIFIED — needs catalog lookup (candidate family: ISO 3547 / DIN 1494 wrapped bushing, nominal 16x18x20) | — | Small-end bearing for connecting_rod on the ⌀16 gudgeon pin. **NOT modeled in v1 geometry** — the rod currently has a plain ⌀16.02 clearance bore (locked). See v1/v2 note below. |

## v1 / v2 geometry note (load-bearing)

- **v1 (current, locked)**: connecting_rod small end is a plain ⌀16.02 bore running
  directly on the ⌀15.99 gudgeon pin (full-floating clearance). The bushing land is
  intentionally OMITTED from v1 geometry. Do not design the rod around the bushing OD.
- **v2 (future change, if/when bushing is adopted)**: open the small-end bore from
  ⌀16.02 to the bushing OD at a press-fit allowance (nominal ~⌀18 for an 18 mm OD
  wrapped bushing; exact bore size and press-fit tolerance class per the verified
  catalog spec). Bushing ID after installation must finish at ⌀16.0 clearance
  (~16.02) on the pin. Rod small-end width is 20.0 mm — bushing length must be
  ≤ 20 mm (flush or sub-flush both faces). Details in `sourcing_notes.md`.

No other purchased parts: no fasteners (one-piece big end, no bolted cap) and no
bearings (main journals left free per project goals). All five parts in the plan
(piston, piston_ring, gudgeon_pin, connecting_rod, crankshaft) are Make.
