# Bill of Materials — conveyor_shaft_unit

Duty: 40 mm conveyor drive shaft, 1500 rpm, 4 kN radial + 1 kN axial, 20,000 h L10h target.
All seven line items below are Buy.
Engineering checks and per-item rationale: see `sourcing_notes.md` in this directory.

> **Read `sourcing_notes.md` before designing to this BOM.**
> Two items carry open findings:
> the 6208 does **not** reach the 20,000 h target at the stated load (CONFLICT 1),
> and the M8x30 screw bottoms in a 16 mm deep tapped hole (CONFLICT 2).

| Item | Qty | Designation / standard | Key dimensions | Material/spec | Interfaces (mating Make part + dim) | Notes |
|---|---|---|---|---|---|---|
| Deep groove ball bearing | 2 | 6208-C3 (ISO 15:2017 dimension series 02, bore no. 08); open, or 6208-2RS1/C3 if sealed-for-life is preferred | d 40 × D 80 × B 18; r min 1.1 mm chamfer; da min 47, Da max 73 (abutment envelope); mass ≈ 0.37 kg | Through-hardened bearing steel 100Cr6 / AISI 52100; steel cage; C3 radial internal clearance 15–33 µm (ISO 5753, 30–40 mm bore band) | Shaft bearing seats **40 k6** (+0.002/+0.018); housing bores **80 H7** (0/+0.030) | C = 30.7 kN, C0 = 19 kN (SKF catalogue 6208). **Capacity shortfall — see CONFLICT 1.** C3 is the right call: the k6 press fit consumes ~80 % of the interference as lost clearance |
| External retaining ring (circlip) | 1 | **DIN 471 – 40 × 1.75** | Ring thickness s = 1.75 (−0.06); free outer dia d3 ≈ 43.5; radial width b ≈ 3.9; lug hole dia 2.5. Mating groove: dia d2 = **37.5** (−0.25), width m = **1.85** (+0.14/0), min land n = 3.0 | Spring steel C67S (1.1231), phosphated and oiled; alt. 1.4122 stainless | Shaft circlip groove: dia 37.5 × 1.85 wide, on the 40 mm shaft; abuts the locating bearing inner-ring face | Installed overhang ≈ 1.75 mm radial → contact band r 20 → 21.75 mm, inside the 6208 da max 47 abutment envelope → valid abutment. Axial play ring-in-groove 0.04–0.24 mm. Permissible thrust load: **UNVERIFIED: needs catalogue lookup** (qualitatively ≫ the 1 kN duty) |
| Radial lip seal, rotary shaft | 1 | **40 × 62 × 10**, type **AS** (DIN 3760 form AS / ISO 6194-1 type 2 — single lip + dust lip, garter spring, rubber-covered OD) | Shaft dia 40, bore dia 62, width 10; OD interference for rubber-covered case typ. +0.15/+0.30 on 62 | NBR (nitrile), −30 to +100 °C continuous; AISI 302 garter spring; steel reinforcing case | Cover seal pocket **62 H8** (0/+0.046) × 10 deep; shaft journal **40 ground, Ra ≤ 0.4 µm** | Shaft surface speed v = π·0.040·1500/60 = **3.14 m/s**, well under the ~10–14 m/s NBR limit. Type A (no dust lip) also exists in this size; AS chosen for a conveyor's dust environment. Pocket needs a 15–30° lead-in chamfer |
| Hex socket head cap screw | 4 | **M8 × 25, ISO 4762, property class 8.8**, zinc-plated | Thread M8 × 1.25 coarse, full thread over 25 mm length; head dia 13.0, head height 8.0, hex socket 6 mm AF | Steel, class 8.8 (Rm 800 MPa, Rp0.2 640 MPa) | Cover flange **dia 9 clearance holes** (ISO 273 medium fit for M8) on **104 mm bolt circle**, flange 12 thick → housing **M8 tapped, 16 deep** | Tightening torque ≈ 24 N·m dry, class 8.8, µ ≈ 0.14. ORCHESTRATOR RULING 2026-10-08: CONFLICT 2 RESOLVED by shortening the screw 30 → 25. Engagement = 25 − 12 flange = **13 mm into the 16 mm tapped hole** (1.6 × d, above the 1.5 × d minimum for a steel screw in cast iron, with 3 mm of thread run-out spare). Zero change to any Make part. Head OD 13 at BC 104 spans r 45.5–58.5, clear of the 80 bore wall by 7.5 mm |
| Hex bolt, foot mounting | 4 | **M12 × 40, ISO 4014, property class 8.8** (partially threaded: thread length b = 30, plain shank 10) | Thread M12 × 1.75 coarse; head AF 18, head height 7.5 | Steel, class 8.8, zinc-plated | Housing foot **dia 14 clearance holes**, foot plate 15 thick | Torque ≈ 87 N·m dry, class 8.8, µ ≈ 0.14. Dia 14 sits between ISO 273 medium (13.5) and coarse (14.5) — acceptable and deliberate: ±1 mm of foundation alignment. **Grip check:** 40 − 15 (foot) − 2×2.5 (washers) − 10.8 (nut) = 9.7 mm left for the foundation plate; thicker foundations need a longer bolt |
| Plain washer (for the above) | 4 | **ISO 7089 – 12 – 200 HV** (form A, unchamfered) | ID 13.0 × OD 24.0 × 2.5 thick | Steel, 200 HV, zinc-plated | Under bolt head and under nut on the housing foot | Pair one under head, one under nut — the 14 mm clearance hole is oversize for M12 and needs the washer's 24 OD to bridge it |
| Hex nut (for the above) | 4 | **ISO 4032 – M12 – class 8** | AF 18, height 10.8 | Steel, class 8, zinc-plated | Underside of the foundation / mounting plate | Omit if the foundation is tapped rather than through-bolted |
| Straight grease nipple | 2 | **DIN 71412 form A – AM8 × 1** (straight / 0°) | Thread M8 × 1 fine, parallel; hex AF 9 (*typical — confirm with supplier*); overall length ≈ 16; hardened ball dia 5 with spring, ball seat per DIN 3402 | Free-cutting steel, zinc-plated; hardened steel ball | Two tapped **M8 × 1** bosses on top of the housing, one per bearing bore, drilled through into the bearing seat | DIN 71412 form A is a **parallel** thread — it does not self-seal; use thread sealant or a sealing washer at the boss face. **See OPEN QUESTION 3: relubrication needs a grease escape path or the purge will lift the seal lip** |
| Grease (consumable) | 1 lot | **NLGI 2 lithium complex**, EP, base oil ISO VG 100–150 at 40 °C (e.g. the LGMT 2 / LGEP 2 product class) | Relubrication quantity Gp = 0.005 · D · B = 0.005 · 80 · 18 = **7.2 g per bearing per relube** | Lithium complex soap, dropping point ≈ 260 °C, service −20 to +140 °C | Packed into both 6208 bearings and injected through the DIN 71412 nipples | n·dm = **90,000 mm/min — PASS** (≈ 18 % of the ~500,000 lithium-grease limit). Relubrication interval tf ≈ **1,300 h** → ~15 relubes over 20,000 h. Specific product selection: **UNVERIFIED: needs catalogue lookup** (no vendor part number invented) |

## Catalogue anchors

These envelopes are fixed by the purchased parts and must not be altered by the Make parts:

- **6208 bearing**: bore **40** / OD **80** / width **18**, corner radius r min **1.1**.
  Shaft abutment shoulder dia must fall between da min **47** and the inner-ring OD;
  housing abutment shoulder dia must not exceed Da max **73**.
- **DIN 471 – 40 × 1.75 groove**: dia **37.5** (−0.25) × **1.85** (+0.14/0) wide,
  with ≥ **3.0 mm** of land between the groove and the nearest shaft feature.
- **Radial lip seal**: OD **62** × width **10**, shaft journal **40**.
- **M8 × 25 ISO 4762**: clearance hole **Ø9**, head Ø **13** (no counterbore assumed),
  bolt circle **104**.
- **M12 × 40 ISO 4014**: clearance hole **Ø14**, washer OD **24**, nut AF **18** (hex clearance across corners ≈ 20.8).
- **DIN 71412 A M8 × 1 nipple**: tapped **M8 × 1** boss, hex AF **9** → allow ≥ 14 mm of spanner swing around each boss.

## Not purchased

The **shaft**, the **housing** and the **bearing cover** are Make parts —
custom-machined, designed around the envelopes above, and not sourced.
No vendor part numbers are claimed for them.

## Verification posture

Every designation above is grounded in a published standard
(ISO 15, ISO 5753, DIN 471, DIN 3760 / ISO 6194, ISO 4762, ISO 4014, ISO 4032, ISO 7089, ISO 273, DIN 71412).
Three figures are explicitly **UNVERIFIED** and marked as such in their rows:
the DIN 471 ring's permissible thrust load,
the grease nipple's hex AF,
and the specific grease product selection.
No vendor part number has been invented anywhere in this BOM.
