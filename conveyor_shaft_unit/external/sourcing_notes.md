# Sourcing notes — conveyor_shaft_unit

Scope: confirm the seven Buy line items in `bom.md` against real catalogue data,
and verify the two engineering checks named in the sourcing brief.
No Make-part `constraints.md`, no `part.py`, and no `design_log.md` was touched —
every finding below is reported here instead of being edited into a live file.

---

# CATALOGUE CONFLICTS

Three findings. Two are hard conflicts, one is an open question for the orchestrator.
All three need an orchestrator decision; none of them can be resolved by sourcing alone.

## CONFLICT 1 — the 6208 does NOT reach 20,000 h at the stated load

**This is the big one.**
A 6208 exists in catalogue and fits the stated envelope perfectly (40/80/18),
so per the brief I have not re-selected it —
but at the stated duty its basic rating life is **14,094 h**,
a **30 % shortfall** against the 20,000 h requirement,
and that is with the favourable two-bearing load-sharing assumption.
Worst case (one bearing carries everything) it is **5,023 h**.
Full arithmetic in **Check 1** below.

The required dynamic capacity is **C ≥ 34.5 kN** at the locating bearing.
The 6208 offers 30.7 kN.
No variant inside the 40 × 80 × 18 envelope closes that gap:
C3 clearance does not change load rating,
and the premium / "explorer" class 6208 is still rated at 30.7 kN.
**The envelope itself is the constraint, not the part number.**

Decision paths for the orchestrator, in order of disruption:

1. **Modified rating life (cheapest, least certain).**
   ISO 281 a_ISO can exceed 1.0 with clean grease and κ ≥ 2,
   which could lift 14,094 h toward the target.
   I will not put a number on it:
   **UNVERIFIED: needs catalogue lookup** of the SKF a_ISO chart
   at the real contamination class and operating temperature.
   If the orchestrator wants the 6208 kept, this is the justification to go and fetch —
   but it is a paper rescue, not a design margin.
2. **Confirm the duty is not continuous.**
   20,000 h at *full* 4 kN + 1 kN is a harsh reading.
   If the 4 kN is a peak rather than a continuous equivalent load,
   the cubic-mean load over a real duty cycle may be well under 4 kN and the 6208 clears easily.
   This is a question for the requirement, not the catalogue.
3. **Step up to a 6308** (40 × 90 × 23, C = 41.0 kN, C0 = 24.0 kN).
   Same 40 mm bore, so the shaft seats and the circlip are untouched,
   but OD 80 → 90 and width 18 → 23 **changes the housing bore, the cover spigot and the axial stack-up**.
   Recomputed at the same shared load:
   Fa/C0 = 1/24 = 0.0417 → e ≈ 0.242, Y ≈ 1.789;
   Fa/Fr = 0.5 > e → P = 0.56·2 + 1.789·1 = **2.909 kN**;
   L10 = (41.0/2.909)³ = 14.094³ = 2799 million rev;
   L10h = 2799 × 10⁶/(60 × 1500) = **31,105 h — clears 20,000 h with 56 % margin.**

My recommendation: **path 3 if the 20,000 h figure is firm, path 2 first if it might not be.**
Sourcing cannot make this call — it changes three Make parts that are being designed right now.

## CONFLICT 2 — the M8 × 30 screw bottoms out in the 16 mm tapped hole

Stated geometry: cover flange **12 thick**, housing thread **16 deep**, screw **M8 × 30**.

```
screw length into the housing = 30 − 12 (flange) = 18 mm
available tapped depth                           = 16 mm
                                             → 2 mm interference
```

The screw runs out of thread **2 mm before the head seats on the flange**.
Result: no clamp load, a false "tight" feel at the wrench, and a galled thread at the hole bottom.
A deeper drill below the tapped depth does not save it —
the last 2 mm of screw would engage unthreaded bore.

Two fixes, either works:

- **Shorten the screw to M8 × 25.**
  Engagement = 25 − 12 = 13 mm = **1.63 × d**, comfortably above the 1.0–1.25 × d
  minimum for a class 8.8 screw into steel, and 3 mm clear of the hole bottom.
  This is the lazy fix: one BOM line changes, no Make part moves.
  M8 × 25 ISO 4762 class 8.8 is a stock size.
- **Or deepen the tapped hole to ≥ 22 mm** (18 engagement + ~4 mm runout/swarf relief)
  and keep the M8 × 30.
  This changes the housing.

**I have left M8 × 30 in `bom.md`** because the brief said not to re-select,
and because the choice between these two belongs to whoever owns the housing.
Flagging rather than silently swapping:
if the orchestrator picks the screw-length fix, it is a one-word edit to the BOM row.

## OPEN QUESTION 3 — relubrication has no escape path

Two grease nipples feed two bearings that are closed by a lip seal on one side
and a bolted cover on the other.
Each relube injects **7.2 g** (Check 2) into a cavity with nowhere to vent.
Grease pressure in a sealed cavity lifts the lip seal —
the standard failure mode is a seal that weeps for the rest of its life after the first service.

The usual answer is a grease exit: a relief plug, a drain boss low on the housing,
or a deliberately generous clearance at the cover's inboard face acting as a labyrinth purge.
This is a housing feature, so it is a note, not an edit.
If the orchestrator decides the unit is grease-for-life instead,
then the two DIN 71412 nipples come off the BOM entirely
and the bearings become **6208-2RS1/C3** — that is a coherent alternative, and simpler.

---

# Engineering checks

## Check 1 — 6208 bearing life (ISO 281 basic rating life)

### Inputs

| Symbol | Value | Source |
|---|---|---|
| C | **30.7 kN** | SKF catalogue, 6208, basic dynamic load rating. Matches the figure given in the brief. |
| C0 | **19.0 kN** | SKF catalogue, 6208, basic static load rating. |
| Fr (total) | 4 kN | Duty |
| Fa (total) | 1 kN | Duty |
| n | 1500 rpm | Duty |
| Required L10h | 20,000 h | Duty |

### Step 1 — pick e, X and Y from the deep-groove table

The single-row deep groove X/Y table is indexed on Fa/C0:

| Fa/C0 | e | Y (for Fa/Fr > e) |
|---|---|---|
| 0.025 | 0.22 | 2.0 |
| 0.04 | 0.24 | 1.8 |
| 0.07 | 0.27 | 1.6 |
| 0.13 | 0.31 | 1.4 |

With Fa = 1 kN against a single bearing:

```
Fa/C0 = 1.0 / 19.0 = 0.0526
```

Linear interpolation between the 0.04 and 0.07 rows,
interpolation fraction = (0.0526 − 0.04)/(0.07 − 0.04) = 0.0126/0.03 = 0.42:

```
e = 0.24 + 0.42 × (0.27 − 0.24) = 0.24 + 0.0126 = 0.2526
Y = 1.80 − 0.42 × (1.80 − 1.60) = 1.80 − 0.084  = 1.716
```

For Fa/Fr ≤ e:  X = 1,    Y = 0   → P = Fr
For Fa/Fr > e:  X = 0.56, Y = 1.716 → P = 0.56·Fr + 1.716·Fa

### Step 2 — worst case: ONE bearing takes the entire load

```
Fa/Fr = 1.0 / 4.0 = 0.250     versus  e = 0.2526
```

0.250 < 0.2526, so formally the axial load is ignored: **P = Fr = 4.000 kN**.
This sits within 1 % of the e boundary, so I checked the other branch too:
P = 0.56 × 4.0 + 1.716 × 1.0 = 2.24 + 1.716 = 3.956 kN.
The two branches converge at the boundary, as they must.
**Take the larger: P = 4.000 kN.**

```
L10  = (C/P)³ = (30.7 / 4.000)³ = 7.675³
     = 7.675² × 7.675 = 58.906 × 7.675 = 452.1 million revolutions

L10h = L10 × 10⁶ / (60 × n) = 452.1 × 10⁶ / (60 × 1500)
     = 452.1 × 10⁶ / 90,000
     = 5,023 hours
```

### Step 3 — shared case: load split across the two bearings

**Split assumption, stated plainly:**
the radial load divides **50 / 50** between the two bearings (2 kN each),
and the **entire 1 kN axial is carried by the locating bearing** —
the one retained by the DIN 471 circlip against a shaft shoulder.
The second bearing is the non-locating (floating) one:
its outer ring must be free to slide in the 80 H7 bore, so it takes **zero** axial load.
This is the standard locating/non-locating arrangement
and it is what the single circlip in the BOM implies.
A true 50/50 radial split assumes the load is applied symmetrically between the bearings;
a load applied off-centre, or an overhung drive pulley,
loads one bearing harder and pushes the governing number below what follows.

**Locating bearing** — Fr = 2.0 kN, Fa = 1.0 kN:

```
Fa/C0 = 1.0/19.0 = 0.0526        → e = 0.2526, Y = 1.716   (as Step 1)
Fa/Fr = 1.0/2.0  = 0.500 > e     → the axial branch applies

P    = 0.56 × 2.0 + 1.716 × 1.0 = 1.120 + 1.716 = 2.836 kN

L10  = (30.7 / 2.836)³ = 10.825³ = 117.18 × 10.825 = 1,268.5 million revolutions
L10h = 1,268.5 × 10⁶ / 90,000    = 14,094 hours
```

**Floating bearing** — Fr = 2.0 kN, Fa = 0:

```
P    = Fr = 2.000 kN
L10  = (30.7 / 2.000)³ = 15.35³ = 235.62 × 15.35 = 3,616.8 million revolutions
L10h = 3,616.8 × 10⁶ / 90,000   = 40,187 hours
```

The assembly's life is set by the shorter-lived bearing: **14,094 h**.

### Step 4 — capacity required to actually hit 20,000 h

```
L10 required = 20,000 × 60 × 1500 / 10⁶ = 1,800 million revolutions
C required   = P × L10^(1/3) = 2.836 × 1,800^(1/3) = 2.836 × 12.164 = 34.50 kN
```

6208 offers 30.7 kN. **Short by 3.8 kN, i.e. 12 % on capacity / 30 % on life.**

### VERDICT

> **FAIL. A 6208 does NOT clear the 20,000 h requirement.**
>
> | Case | P (kN) | L10h | vs 20,000 h |
> |---|---|---|---|
> | Worst case — one bearing carries all 4 kN + 1 kN | 4.000 | **5,023 h** | **FAIL — 25 % of target** |
> | Shared — locating bearing, 2 kN radial + 1 kN axial | 2.836 | **14,094 h** | **FAIL — 70 % of target** |
> | Shared — floating bearing, 2 kN radial, no axial | 2.000 | 40,187 h | PASS |
> | **Governing (shared-load assumption)** | **2.836** | **14,094 h** | **FAIL** |
>
> Required C = **34.5 kN**; 6208 delivers **30.7 kN**.
> Mitigations, in CONFLICT 1 above:
> load-sharing is already assumed and is not enough;
> the real options are an a_ISO modified-life lookup, a duty-cycle reality check,
> or stepping to a **6308** (40 × 90 × 23, C = 41.0 kN → **31,105 h**, clears with margin).
> **Stepping to the 6308 changes the housing bore, the cover spigot and the axial stack —
> it is an orchestrator decision, not a sourcing one.**

A note on honesty here: this is the ISO 281 *basic* rating life, which is the right
first-pass number and the one the requirement is almost certainly written against.
It carries no lubrication, contamination or temperature modifier.
I have not applied a_ISO because I cannot verify the chart value for this application,
and inventing one to make the number pass would be exactly the failure mode this role exists to avoid.

## Check 2 — grease speed factor

### Speed factor

```
dm   = (d + D)/2 = (40 + 80)/2 = 60 mm
n·dm = 1500 rpm × 60 mm        = 90,000 mm/min
```

Typical limits for grease in a deep groove ball bearing:

| Grease type | Typical n·dm limit (mm/min) |
|---|---|
| Standard lithium soap, NLGI 2 | ~500,000 |
| Lithium **complex**, NLGI 2 (the specified grease) | ~500,000–700,000 |

```
90,000 / 500,000 = 0.18  → the application runs at ~18 % of the conservative limit
```

> **VERDICT: PASS, comfortably.**
> At n·dm = 90,000 mm/min this is a slow-to-moderate speed application.
> NLGI 2 lithium complex is well inside its working range —
> there is no case here for a lower-consistency NLGI 1 or an oil-mist system,
> and the NLGI 2 consistency is the right choice for a horizontal shaft
> where a softer grease would slump out of the bearing.

### Relubrication interval

Using the standard relubrication-interval relation for a horizontal-shaft
deep groove ball bearing (Kf = 1), d in mm, n in rpm:

```
tf = Kf × [ 14 × 10⁶ / (n × √d) − 4d ]
   = 1  × [ 14 × 10⁶ / (1500 × √40) − 4 × 40 ]

√40        = 6.3246
1500 × √40 = 9,487
14 × 10⁶ / 9,487 = 1,475.7
4 × 40           = 160

tf = 1,475.7 − 160 = 1,316 hours  ≈ 1,300 h
```

### Implication for a 20,000 h service life

```
20,000 h / 1,316 h = 15.2  → about 15 relubrication events over the service life
```

Grease quantity per event:

```
Gp = 0.005 × D × B = 0.005 × 80 × 18 = 7.2 g per bearing per relube
```

Total grease consumed over the life ≈ 15 × 7.2 g × 2 bearings ≈ **216 g**.

Three consequences the design has to answer for:

1. **The two grease nipples are justified** — at ~1,300 h this unit cannot be grease-for-life
   as specified. Either the nipples stay, or the bearings become sealed 2RS1 units
   and the whole relubrication scheme is dropped (see OPEN QUESTION 3).
2. **15 purges of 7.2 g need somewhere to go.** That is OPEN QUESTION 3 — no escape path exists today.
3. **The interval halves** if the shaft runs vertically, above ~70 °C, or in a wet/dusty conveyor
   environment. 1,300 h is the favourable case, and a conveyor gearbox-adjacent bearing
   running warm should be planned closer to 650 h.

Caveats stated rather than buried:
the tf relation assumes a horizontal shaft, operating temperature ≤ 70 °C,
and clean conditions.
The required base oil viscosity for κ ≥ 1 at dm = 60 mm and n = 1500 rpm is
ν1 ≈ 20 mm²/s — **that figure is an approximate chart read and is UNVERIFIED**;
the ISO VG 100–150 base oil of a standard NLGI 2 lithium complex should satisfy it
at a 60–70 °C operating temperature, but confirm against the actual product data sheet
once a specific grease is chosen.

---

# Per-item selection rationale

## 1. Deep groove ball bearing — 6208-C3 (×2)

**Confirmed as a catalogue part, flagged on capacity.**
The 6208 is a bog-standard ISO 15 dimension-series-02 bearing:
40 × 80 × 18, universally stocked, cheap, and dimensionally exactly what the plan assumed.
There is nothing wrong with the *part*; the problem is that the duty needs more capacity
than the envelope can hold (CONFLICT 1).
The **C3** clearance call is correct and worth keeping whatever happens to the size:
the 40 k6 shaft fit is an interference fit in every tolerance combination,
and roughly 80 % of that interference is consumed as lost radial clearance.
Worst-case stack: 0.030 mm interference × 0.8 = 0.024 mm of clearance eaten,
against a Normal-class range of only 0.006–0.020 mm — i.e. a CN bearing could be
driven into **preload** at the bad end of the stack.
C3 (0.015–0.033 mm) survives that stack.
Open/2RS choice is left open in the BOM because it depends on OPEN QUESTION 3:
open bearings if the relubrication scheme stays, 2RS1 if the unit goes grease-for-life.

## 2. External retaining ring — DIN 471 – 40 × 1.75

**Confirmed exactly as planned.**
DIN 471 for a 40 mm shaft is a 1.75 mm thick ring in a 37.5 dia × 1.85 wide groove —
the plan's numbers match the standard table line for line, nothing to correct.
Worth noting for whoever machines the groove: the ring's installed outer diameter is
≈ 43.5 mm, so it overhangs the shaft by only ~1.75 mm radially and contacts the bearing
inner-ring face across r 20 → 21.75 mm.
That band sits inside the 6208's da min 47 abutment envelope, so it is a valid abutment —
the circlip is pushing on the inner ring, not fouling the seal or the cage.
Ring-in-groove axial play is 0.04–0.24 mm (groove 1.85 +0.14, ring 1.75 −0.06),
which is normal and acceptable for a bearing that is shoulder-located and circlip-retained.
The ring's permissible thrust load is **UNVERIFIED: needs catalogue lookup** —
I am not quoting a number I cannot source.
Qualitatively it is not close: DIN 471 rings in this size are rated in the tens of kN
and the duty here is 1 kN.

## 3. Radial lip seal — 40 × 62 × 10 AS, NBR

**Confirmed as a standard catalogue size.**
40 × 62 × 10 is a published DIN 3760 / ISO 6194-1 size, stocked by every seal vendor —
no bespoke tooling, no minimum order.
I specified type **AS** (lip + dust lip) over plain type A: a conveyor runs in a dirty,
abrasive environment and the dust lip is nearly free insurance.
Both types exist in this size, so this is a cheap reversal if the orchestrator disagrees.
NBR is the right elastomer: the 3.14 m/s surface speed
(v = π × 0.040 × 1500/60) is far below NBR's ~10–14 m/s capability,
and nothing in the duty suggests the temperature or chemical exposure that would force FKM.
The spring-loaded lip is non-negotiable and is already in the plan's spec.
The one thing this seal *demands* from the Make parts is counterface quality:
a **plunge-ground** journal at Ra ≤ 0.4 µm with no machining lead.
A turned or spiral-ground 40 journal will pump oil along the lead angle and leak
regardless of how good the seal is.

## 4. Hex socket head cap screw — M8 × 30, ISO 4762, class 8.8 (×4)

**Designation confirmed, length conflicts — see CONFLICT 2.**
ISO 4762 is the correct current standard for a hex socket head cap screw
(DIN 912 is the superseded national equivalent and will still get you the same part
over the counter; I have cited the ISO number as the primary).
Class 8.8 is the right strength grade for a steel cover onto a steel housing,
giving ~24 N·m of tightening torque and more clamp load than this joint will ever need.
The Ø9 clearance hole is ISO 273 **medium** fit for M8 — correct, standard, no comment.
The bolt circle at 104 with Ø13 heads leaves 7.5 mm of housing wall between the hole edge
and the 80 mm bore, which is adequate.
The only defect is the length: 18 mm of screw into a 16 mm hole.
**M8 × 25 fixes it with no change to any Make part** — that is my recommendation.

## 5. Hex bolt set — M12 × 40 ISO 4014 + ISO 7089 washer + ISO 4032 nut (×4)

**Confirmed, with a grip-length caution.**
ISO 4014 is the partially-threaded hex bolt (thread length b = 30 mm at this size),
which is the correct choice for a foot mounting — the plain shank sits in the clearance hole
and resists shear better than a fully-threaded ISO 4017 would.
Class 8.8, ~87 N·m, well matched to a foundation bolt.
I have **added the washer and the nut as explicit BOM lines** rather than leaving them implied:
the plan said "bolt + washer + nut" but named no standards, and an unnamed washer is
exactly the kind of gap that turns into a missing part at assembly.
ISO 7089 (200 HV form A, 13/24/2.5) and ISO 4032 class 8 are the matching standards.
The washer earns its place here: the Ø14 clearance hole is oversize for M12
(ISO 273 medium is 13.5, coarse is 14.5), so the bolt head alone would bear on a thin
annulus. The 24 mm washer OD bridges it properly.
That oversize hole is a sensible deliberate choice, not an error —
it buys ±1 mm of alignment against a foundation whose hole positions are never perfect.
**The caution**: 40 mm of bolt against a 15 mm foot leaves
40 − 15 − 5 (two washers) − 10.8 (nut) ≈ **9.7 mm** for the foundation plate.
If the unit bolts to anything thicker than ~9 mm, the bolt is too short.
Since the foundation is outside this assembly, I have left M12 × 40 as specified and flagged it.

## 6. Straight grease nipple — DIN 71412 form A, AM8 × 1 (×2)

**Confirmed as a standard part.**
DIN 71412 form A is the straight (0°) grease nipple;
the M8 × 1 fine-thread variant is the common small size and is stocked everywhere.
A hardened spring-loaded ball seals it between services, per the DIN 3402 ball seat.
Two of them, one per bearing bore, is the correct arrangement —
one nipple feeding both bearings through a drilling would preferentially grease
whichever path has less resistance and starve the other.
The hex size is **AF 9 for this variant, which I have marked "confirm with supplier"**
in the BOM: I am confident about the thread and the standard, less so about the exact
across-flats, and it matters only for spanner access clearance around the boss.
Two things the housing has to provide: a flat, perpendicular seat face at the boss
(form A has a **parallel** thread, so it seals on the face with sealant or a washer,
not on the thread like a taper fitting would), and spanner swing clearance.
And the unresolved one: somewhere for the grease to go — OPEN QUESTION 3.

## 7. Grease — NLGI 2 lithium complex

**Specification confirmed, product deliberately not named.**
NLGI 2 lithium complex is the right class for this duty and the speed factor check
backs it up with margin (18 % of limit).
Lithium complex over plain lithium soap buys a higher dropping point (~260 °C vs ~190 °C)
and better water resistance, both of which a conveyor bearing appreciates.
Base oil ISO VG 100–150 at 40 °C is the normal spec for this class
and should satisfy the κ ≥ 1 viscosity requirement at a 60–70 °C running temperature.
I have **not named a vendor product**:
"NLGI 2 lithium complex, EP, ISO VG 100–150" is a procurable specification that any
lubricant supplier can quote against, whereas a specific invented product code would be
a fabrication. Marked **UNVERIFIED: needs catalogue lookup** in the BOM for that reason.
Quantities that *are* grounded: 7.2 g per bearing per relube (Gp = 0.005·D·B),
~15 relubes over the service life, ~216 g total.
Initial fill is the usual 30–50 % of bearing free space with the housing cavity at ~30 % —
the exact gram figure depends on the final housing cavity volume and is not knowable from here.

---

# Fit and tolerance callouts

These are restated for the record.
They are **already final in the Make parts' `constraints.md`** and were not edited by this agent —
this section exists so the numbers and their justification live in one place.

| Feature | Fit | Limits (mm) | Why |
|---|---|---|---|
| Shaft bearing seats | **40 k6** | +0.002 / +0.018 | Rotating inner ring under circumferential load **must** be an interference fit or it will creep and fret the seat. Against the bearing bore tolerance (0 / −0.012) the interference is 0.002 min to 0.030 max — never loose. |
| Housing bores | **80 H7** | 0 / +0.030 | Stationary outer ring under point load. Against the bearing OD (0 / −0.013) this gives 0 to 0.043 clearance — line-to-line at worst, which is correct: the floating bearing's outer ring **must** be able to slide axially to avoid cross-loading the pair. |
| Cover spigot | **80 h8** | 0 / −0.046 | Pilot only, carries no load. Into the 80 H7 bore the clearance is 0 to 0.076 (≤ 0.038 radial eccentricity). That is well inside the ~0.25 mm shaft-to-bore misalignment a DIN 3760 lip seal tolerates, so the seal stays happy. Needs a lead-in chamfer since the minimum condition is line-to-line. |
| Seal pocket | **62 H8** | 0 / +0.046 | The ISO 6194 recommended housing bore for a rubber-covered-OD lip seal. Preserves the seal's +0.15/+0.30 OD interference across the whole tolerance range — press-fit retained, no retaining ring needed. |
| Seal counterface journal | **40, ground, Ra ≤ 0.4 µm** | — | Plunge-ground, **no machining lead** — a spiral lead pumps lubricant past the lip and leaks regardless of seal quality. Ra 0.2–0.4 is the sweet spot: rougher abrades the lip, smoother starves the lip of its lubricant film. Deburr and chamfer the lead-in so the lip is not cut during assembly. |
| Circlip groove | **37.5 (−0.25) × 1.85 (+0.14/0)** | — | DIN 471 table values for a 40 mm shaft. Keep ≥ 3.0 mm of land to the nearest feature. |

## Summary of what sourcing changed vs the plan

- **Confirmed unchanged (5 of 7):** 6208-C3, DIN 471 40 × 1.75, 40 × 62 × 10 NBR lip seal,
  M12 × 40 ISO 4014, DIN 71412 A M8 × 1.
- **Confirmed with the standard pinned down:** the lip seal is specified as **type AS**
  (dust lip) rather than left as "A/AS"; the M12 line gained explicit
  **ISO 7089** washer and **ISO 4032** nut rows that the plan only implied.
- **Flagged, not changed:** the 6208's 30 % life shortfall (CONFLICT 1) and the
  M8 × 30 bottoming out (CONFLICT 2). Both need an orchestrator decision; both were
  left as the plan specified because changing them touches Make parts under active design.
- **UNVERIFIED rows (3):** DIN 471 permissible thrust, grease nipple hex AF,
  specific grease product. No vendor part number invented anywhere.
