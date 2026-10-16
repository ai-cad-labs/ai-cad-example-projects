# Assembly notes — conveyor_shaft_unit

## Assembly validation

**Date**: 2026-10-08 · **Role**: validator (assembly vision gate)
**Renders read**: `iso_clean.png`, `front_clean.png`, `top_clean.png`, `right_clean.png`
(clean set preferred; wireframes deliberately not used — three prior vision false positives in this project).

### Handedness established before judging anything

Fixed from the colour legend, not from intuition:

- `front_clean.png` is a **plan view looking down the +Y (up) axis**. Horizontal axis = Z.
  The red grease nipple (`grease_nipple_z+70`) sits at the LEFT, the magenta one (`z-70`) at the RIGHT
  → **left = +Z = drive end** in that image, and the green cover is indeed on the left.
- `right_clean.png` is the **side elevation with +Y pointing DOWN the page**.
  Teal bolt (`x+45_z-75`) at the left, brown bolt (`x+45_z+75`) at the right
  → **right = +Z = drive end**, and the green cover is on the right. Two independent confirmations agree.
- `top_clean.png` is the **end view looking along Z**, drive end toward the viewer.

Drive end = the end carrying the big green bolted cover, the brown lip seal and the thin protruding
shaft extension. Far end = the open bore with the long plain stub. Confirmed in two views.

### The nine judgements

**1. Does it read as a credible pillow-block bearing unit? — PASS** *(vision-only)*
`iso_clean.png` shows one cast red body sitting on a flat rectangular foot, a blue shaft running
straight through it and out both ends, a large green bolted circular cover closing the right-hand
(drive) end, and two stepped nipple bosses standing on top. Four bolt shanks hang below the foot.
It reads immediately as a two-bearing plummer/pillow block — an engineer would recognise it on sight.

**2. Shaft concentric through both bores, sensible protrusion at each end? — PASS** *(measured)*
In `top_clean.png` the shaft, both bearings, the seal, the circlip, the cover bore and the housing
bore all draw as one nest of **concentric** circles about a single centre — no eccentric ring anywhere.
Measured: shaft bbox `X -24..+24, Y -24..+24, Z -135..+165`, i.e. perfectly centred on the Z axis.
Housing ends at z = ±95, cover outer face at z = +107.
→ far-end plain stub protrudes **40 mm** past the housing (z -95 → -135);
drive-end extension protrudes **58 mm** past the cover face (z +107 → +165) at the reduced diameter.
Both visible as the long blue bars at the two ends of `right_clean.png`.

**3. Both bearings square in their bores, same axis, at the two ends? — PASS** *(measured)*
`right_clean.png` shows the purple annulus at the far end and the orange annulus at the drive end as
two equal-height rectangles with identical vertical extent — same axis, no tilt, no offset.
Measured: `bearing_far_end  X±40 Y±40 Z -84..-66`, `bearing_drive_end X±40 Y±40 Z +66..+84`.
Identical radial extent, 18.000 mm wide each, 150.000 mm centre span, both coaxial with the shaft.

**4. Cover seated flat with rim flush (cover OD 130 = housing boss OD 130)? — PASS** *(measured)*
In `top_clean.png` the green cover circle is the outermost circular silhouette and **no red housing
arc steps out past it or sits inside it** — one single clean rim. In `right_clean.png` the green bar
butts against the housing end face with no wedge or gap.
Measured: cover bbox `X ±65.00, Y ±65.00, Z +84..+107`; housing `X ±65.00`.
Housing drive-end boss radius independently confirmed as exactly 65.0 by the arithmetic in finding 8.
**Flush to 0.00 mm.** Housing ∩ cover intersection volume = **0.000 mm³** — the spigot enters the bore
cleanly and the flange does not bite into the casting.

**5. Four M8 cover screws standing proud with wrench clearance? — PASS** *(measured)*
`top_clean.png` shows exactly **four** small rings at 45°/135°/225°/315°, evenly spaced on a bolt
circle, each one drawn concentric with a red housing hole beneath it (correct clocking, visually
obvious). `right_clean.png` shows two of the heads as small blocks standing clear of the cover face
in open air.
Measured: screws at `Z +82..+115`; cover outer face at `z = +107` → **heads stand 8.0 mm proud**,
no counterbore. Bolt circle dia 104, adjacent head centres 73.5 mm apart, head across-corners 13 mm
→ **60.5 mm of open air between adjacent heads**, and the heads sit at r ≈ 52 with the cover rim at
r = 65 and the shaft extension at r ≤ 24 — nothing within reach of a socket. Generous clearance.

**6. Exactly four foot bolts, foot flat? — PASS** *(measured)*
`front_clean.png` (plan) shows four distinct bolt circles — orange, purple, teal, brown — one at each
corner of a rectangle, which is four separate components, not a doubled pair.
`top_clean.png` shows two shanks hanging below the foot with the other two exactly behind them.
Measured: four bolts at `x = ±45, z = ±75`, shank dia 12, head r 9 seated on the foot top face at
Y = -60 and standing 7.5 mm proud, 40 mm shank passing through the 15 mm foot and protruding 25 mm
below for the baseplate. Foot underside is a **single plane at Y = -75.00** across the full
Z -95..+95 span — in `right_clean.png` it is one unbroken straight red line. The foot sits flat.
(Wrench access at two of these four stations is compromised — see finding 8.)

**7. Grease nipples on top and reachable from directly above? — PASS** *(measured)*
In `right_clean.png` (+Y down) the two nipples are the furthest-projecting features on the +Y side,
standing in completely open air with nothing beyond them. In `top_clean.png` the nipple stands proud
at top dead centre, clearly breaking above the cover's circular silhouette.
Measured: both nipples `X ±5.5, Y +70..+82, Z ±70`, i.e. on the top centreline.
**Housing Ymax = +70, cover Ymax = +65, every other component Ymax ≤ +70.**
Nothing in the assembly occupies any point above Y = +70, so the 12 mm of nipple is fully exposed to
a straight vertical approach. Housing ∩ nipple = 0.000 mm³ at both stations (seated, not sunk).

**8. Interpenetration / floating / wrong-end / missing parts? — FAIL** *(measured)*
All 17 components are present and accounted for by colour across the four views; nothing floats
(every silhouette is contiguous with its neighbours) and nothing is at the wrong end — the single lip
seal, the circlip and the cover are all at +Z, the open bore is at -Z, exactly as briefed.

A full **pairwise interference sweep over all 17 solids** (136 pairs) returned only five non-zero
intersections. Three are the documented accepted artefacts. **Two are not:**

> `housing × bolt_m12x40_x-45_z+75` = **6.437 mm³**
> `housing × bolt_m12x40_x+45_z+75` = **6.437 mm³**
> `housing × bolt_m12x40_x-45_z-75` = 0.000 mm³
> `housing × bolt_m12x40_x+45_z-75` = 0.000 mm³

See the defect section below. The **asymmetry** is what makes this a real collision rather than a
modelling convention: a convention would show at all four bolts, not at exactly the two that sit
under the drive-end boss.

*(Also measured and explicitly NOT a defect: `housing × cap_screw_m8x25_*` = 181.333 mm³ at each of
the four screws. This is the dia-8 screw shank overlapping a dia-6.8 tapping-drill hole over 13.0 mm
of thread engagement — π/4 × (8² − 6.8²) × 13 = 181.33 exactly. That is the standard representation
of a tapped joint, and 13 mm = 1.6 × d is sound engagement in cast iron. Do not "fix" this.)*

**9. Overall bounding box ≈ X 130 / Y -100..+82 / Z -135..+165? — PASS** *(measured, not by eye)*
Executed `assembly.py`: `success: true`, volume 2,034,752.88 mm³, result type Compound.

> `X -65.00 .. +65.00` (130.00) · `Y -100.00 .. +82.00` · `Z -135.00 .. +165.00`

Exact match to the target on all six faces. Y-min is set by the four foundation bolt tips, Y-max by
the nipple tips, Z-min by the far-end shaft stub, Z-max by the drive-end shaft extension.

### Does the assembled unit satisfy the brief?

Substantially yes, and it is a coherent machine. The views and the measurements together show a
single cast body carrying **two in-line 6208 bearings** 150.000 mm apart on one axis, mounted on a
**flat four-bolt foot**. The bearing arrangement is correct and properly differentiated: the drive-end
bearing is **located** — its inner ring clamped over exactly 18.000 mm between the shaft collar and
the circlip with zero float, its outer ring trapped between the housing shoulder at z = +66 and the
cover spigot face bearing on it at z = +84 — while the far-end bearing is **floating**, with the
1.5 mm axial window measured clear of material. That is textbook located/floating practice and it
reads correctly in `right_clean.png`, where the drive end is dense with retaining features and the
far end is deliberately open. The **bolted cover** carries the single **lip seal** at the drive end
and is held by **four M8 cap screws whose heads stand 8 mm proud with 60 mm of open air between
them** — the wrench-clearance requirement is met with a wide margin. The **two grease nipples are on
top dead centre and nothing in the entire assembly rises above Y = +70**, so the reach-from-above
requirement is met absolutely, not marginally. The overall envelope hits the target exactly.

The one thing standing between this and a shippable assembly is a **local collision between the
drive-end boss and the two foot bolts beneath it**. It is small, precisely located, and does not
touch the bearing system, the shaft, the cover or the sealing — but it does mean two of the four
foundation bolts cannot be seated or wrenched as drawn, so the gate cannot pass.

### Accepted artefacts — present, verified, and NOT defects

Confirmed by measurement; recorded here so nobody re-reports them:

- `shaft × bearing_drive_end` = **63.879 mm³** and `shaft × bearing_far_end` = **63.879 mm³** —
  sharp-cornered Buy annuli overlapping the 1 mm shaft-shoulder relief chamfers. Matches the
  documented 63.9 mm³/end. A real 6208 r_s min 1.1 corner radius covers it entirely.
- `housing × bearing_drive_end` = **124.617 mm³** — same artefact at the drive-end bore root.
  Matches the documented 124.6 mm³. Together these are 0.1–0.2 % of the 67,858 mm³ ring.
- `housing × cap_screw_m8x25_*` = 181.333 mm³ ×4 — major-diameter screw in a tapping-diameter tapped
  hole, the standard thread representation (see finding 8).
- Coincident mating faces everywhere (shaft seat 40 k6 in bearing bore, bearing OD 80 in bore 80 H7,
  cover spigot 80 h8, seal OD 62 in pocket 62 H8, seal ID 40 on the journal). Nominal geometry with
  tolerances carried as text callouts — touching solids are intended, not interference.
- **The cover spigot face at z = +84 bearing on the drive-end bearing outer ring** — required contact,
  this is what axially locates that bearing.
- No fillets and no casting draft anywhere — deferred project-wide, accepted as ISSUE-004.
- The far end is deliberately **open** (floating end + grease purge path). No far-end cover is correct.
- **One** lip seal only, at the drive end. Correct per the brief.

### Defect

**[major] Drive-end OD-130 boss overhangs and intersects the two z = +75 foot-bolt heads** *(measured)*

- **What**: `housing ∩ bolt_m12x40_x±45_z+75` = **6.437 mm³ each**. The matching z = −75 bolts are
  clean at 0.000 mm³.
- **Where**: intersection bbox `X [36.00, 38.32] · Y [−54.12, −52.50] · Z [75.00, 81.04]`
  (mirrored for the −45 bolt). This is the **inboard top corner of the hex head**, over the head's
  top 1.62 mm, encroaching **2.32 mm radially**.
- **Mechanism** (arithmetic, not inference): the housing's drive-end boss is radius 65.0 and begins at
  **z = +75.00**. At the bolt-head top plane Y = −52.5 that boss reaches X = ±√(65² − 52.5²) = **±38.32**.
  The bolt head is centred at x = ±45 with r = 9, so its inboard edge is at X = ±36.00 — a 2.32 mm
  overlap. The head's Z half-extent at that X is ±6.03, giving z 68.97..81.03; the boss front at
  z = 75 truncates it to the observed 75.00..81.04. Every digit reproduces, so this is a hard
  geometric collision, not a rendering or tolerance effect.
- **Why it is not an accepted artefact**: it appears at exactly two of four identical bolt stations.
  A sharp-corner modelling convention would appear at all four. The 2.32 mm encroachment also exceeds
  what a standard M12 hex-head top chamfer removes, and a real cast boss would carry draft and a root
  fillet there — adding material, making it worse.
- **Consequence**: the two drive-end foundation bolts cannot sit flat with the boss as drawn, and a
  socket cannot be dropped onto them from above on the inboard side. A supplementary probe confirms a
  dia-13 vertical column at (x = 45, z = +75) is obstructed from Y = −52.37 upward — i.e. material
  arrives 7.63 mm above the foot face, against a 7.5 mm head. At the z = −75 stations the same column
  is clear until Y ≈ −26.8 (the main body, radius ≈ 52.4), which is ample.

### Recommendations

Pick one; all are local to the housing and touch nothing else:

1. **Move the boss back**: start the drive-end OD-130 boss at z ≥ +85 instead of +75. The cover only
   needs the flush rim at the end face (z = +95), and the spigot bore already carries the bearing
   shoulder at z = +66, so the boss has no reason to extend to z = +75. Cheapest fix, removes the
   collision outright and restores vertical socket access.
2. **Spot-face the boss** over each z = +75 bolt head: a dia-26 flat normal to Y at Y = −52.5,
   centred on x = ±45, z = +75. Mirrors standard foundry practice.
3. **Shift the drive-end bolt pair outboard** from x = ±45 to x = ±48.5 (clears 38.32 + 9 = 47.32 with
   margin). Least preferred — it breaks the symmetric 90 × 150 bolt pattern and the foot is only 130
   wide, leaving just 16.5 mm of edge distance.

After the fix, re-run the pairwise sweep and confirm all four `housing × bolt_m12x40_*` pairs read
0.000 mm³. Everything else in this assembly is clean and should not be touched.

VALIDATION (superseded): FAILED

## Assembly re-validation (post foot-bolt fix)

Date: 2026-10-08.
Scope: narrow re-validation of the one failed judgement (housing overhanging the drive-end M12 bolt
heads) plus a full no-regression pass.
Renders used: `iso_clean.png`, `right_clean.png` (both current, post-fix).
Every number below is **measured** from the built solids unless explicitly labelled vision-only.

### Check 1 — the fix (MEASURED, PASS)

Probe: an M12 head envelope built explicitly as a cylinder of radius 9.0 about the Y axis,
`cq.Solid.makeCylinder(9.0, 7.5, Vector(x, -60.0, z), Vector(0, 1, 0))`, intersected with the
housing solid.

Envelope self-check before trusting it (guards the earlier wrong-direction-extrude failure):

| property | measured | required |
|---|---|---|
| bbox Y | −60.00 .. −52.50 | −60.00 .. −52.50 |
| volume | 1908.518 mm³ | 1908.518 mm³ (= pi x 81 x 7.5) |

The envelope is correct and sits above the foot plate top face, not inside it.

**New bolt stations (z = ±55) — housing ∩ head envelope:**

| station | intersection |
|---|---|
| X = +45, Z = +55 | **0.000 mm³** |
| X = +45, Z = −55 | **0.000 mm³** |
| X = −45, Z = +55 | **0.000 mm³** |
| X = −45, Z = −55 | **0.000 mm³** |

All four read zero solids from the boolean, not merely a small volume.

**Positive control at the OLD stations (z = ±75), same probe, same run:**

| station | intersection | expected |
|---|---|---|
| X = +45, Z = +75 | **6.437 mm³** | 6.437 mm³ |
| X = +45, Z = −75 | **0.000 mm³** | 0.000 mm³ |
| X = −45, Z = +75 | 6.437 mm³ | (mirror) |
| X = −45, Z = −75 | 0.000 mm³ | (mirror) |

The probe reproduces both control numbers exactly, so it is measuring the right thing. The defect is
real at the old stations and fully absent at the new ones: **the fix landed.** All four M12 foot
bolts can now be socketed vertically.

### Check 2 — four foot holes, still four, in the right places (MEASURED, PASS)

Two independent methods agree:

1. Bore-openness probe through the foot plate band (Y −75 .. −60): a radius-6.9 cylinder reads
   **0.000 mm³** at each of (±45, ±55) — clear through-hole — while a radius-7.1 cylinder reads
   **66.445 mm³**, matching the analytic thin-ring reference pi x (7.1² − 7.0²) x 15 = 66.445 mm³ to
   three decimals. That pins the hole diameter at exactly **dia 14.00**, through the full 15 mm plate.
2. Face enumeration: exactly **4** cylindrical faces of dia 14.00 exist in the foot plate band, at
   (x +45, z −55), (x +45, z +55), (x −45, z −55), (x −45, z +55).

No hole remains at z = ±75: the radius-6.9 probe there returns the **full** 2243.568 mm³ solid
cylinder at all four old stations, i.e. solid cast iron, correctly healed.

The four-bolt foot of the brief is intact and the pattern stays symmetric at 90 x 110 mm.

### Check 3 — no regression (all PASS)

| # | Item | Verdict | Evidence (measured) |
|---|---|---|---|
| a | Executes, renders, 17 components | PASS | executor `success: true`, 375.8 ms, Compound; 17 named parts in `color_legend.txt` and in the assembly tree |
| b | Assembly bbox | PASS | X −65.0 .. +65.0 (130), Y −100.0 .. +82.0, Z −135.0 .. +165.0 — matches the expected envelope exactly |
| c | Shaft concentric through both bores; bearings square | PASS | shaft, both bearings, cover, seal and circlip all centre on xc = +0.000, yc = +0.000; bearings span z +66 .. +84 and z −84 .. −66, both exactly 18.0 wide and normal to Z |
| d | Cover seated flat, rims flush | PASS | cover z +84 .. +107, housing DE face z = +95; both ODs measure 130.000; housing ∩ cover absent from the interference sweep (0.000 mm³) |
| e | Four M8 cover screws, heads proud, wrench clearance | PASS | 4 screws at 45/135/225/315 deg on the dia-104 bolt circle, head pitch 73.5 mm centre-to-centre vs dia-13 heads (60.5 mm clear between heads); heads stand z +107 .. +115, i.e. 8 mm proud of the cover face with open air all round |
| f | Four foot bolts through the foot, foot flat | PASS | 4 M12 bolts, heads Y −60.0 .. −52.5 bearing on the foot top face, shanks to Y −100.0 (25 mm into the foundation below the flat foot underside at Y −75.0) |
| g | Two grease nipples on top, reachable from above | PASS | the ONLY two parts exceeding Y = +70 are the nipples themselves (Y +70.00 .. +82.00 at z = ±70); every other part tops out at or below Y = +70 (housing +70, cover +65, screws +43.27), so a grease gun has a clear straight-down approach |
| h | No new interpenetration, floating or misplaced parts | PASS | full 136-pair sweep over all 17 parts returns **7** overlapping pairs, all seven on the pre-accepted list: 4 x cap-screw-in-tapping-drill 181.333 mm³ (thread representation), bearing_drive_end ∩ housing 124.617 mm³ and bearing ∩ shaft 63.879 mm³ x2 (sharp-cornered Buy bearings vs the 1 mm relief chamfers). **Zero housing ∩ bolt pairs remain.** No part is detached and none sits at the wrong end |

### Visual observations (2 renders, clean)

- `right_clean` (side elevation, +Y down, right = +Z): the foot plate reads as the horizontal band
  across the top of the frame with two M12 bolts (teal z −55, brown z +55) standing off it, their
  heads in a clear band immediately outboard of the plate. The brown z = +55 head terminates well
  short of the drive-end boss's left edge — the former collision zone is visibly open air. The green
  cover sits at the right-hand (+Z) end against the housing face with coincident rims, the blue shaft
  passes through and protrudes both ends, and the two grease nipples stand clear at the bottom of the
  frame (= real-world top). Four M8 screw heads project as two overlapping pairs at y = ±36.77, as a
  side elevation of a 4-hole circle should.
- `iso_clean`: one cast body on a flat plate with four distinct bolt cylinders hanging beneath it
  (orange, purple, teal, brown) — four, not two, not six — all heads flush on the plate. Two nipple
  bosses on top carry the magenta and red nipples with nothing over them. The cover face shows four
  small screw-head circle pairs evenly spaced round the bolt circle with wide gaps between them.
  The teal bolt visually crosses the cover outline in this projection; that is **vision-only**
  parallax (bolt at z = +55, cover at z = +84 .. +107) and the sweep measures no contact.

### Brief compliance (whole unit)

The assembled unit satisfies the brief. It carries two 6208 bearings on a common axis — the drive-end
one located, clamped between the housing shoulder at z = +66 and the cover spigot face bearing on its
outer ring at z = +84, with the shaft collar and circlip taking the inner ring; the far-end one
floating, with a 1.5 mm axial gap at its shoulder and a deliberately open far face for thermal growth
and grease purge. The body is a single casting with two in-line dia-80 H7 bores and an integral
mounting foot now carrying four dia-14 through-holes on a clean 90 x 110 pattern, all four of which
can be bolted with a standard M12 socket. The bolted cover closes the drive end, holds the 40x62x10
lip seal in its dia-62 H8 pocket on the dia-40 journal, and is retained by four M8 cap screws on a
dia-104 circle with 60.5 mm of clear space between adjacent heads. Two grease nipples sit on top at
z = ±70, the highest features on the unit, reachable vertically from above. Remaining open items are
the previously accepted ones only: no fillets or casting draft modelled (ISSUE-004), and nominal
tolerance-callout fits that render as coincident faces.

VALIDATION: PASSED
