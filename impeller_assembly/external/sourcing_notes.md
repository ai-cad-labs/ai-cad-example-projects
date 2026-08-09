# Sourcing Notes — impeller_assembly

Posture for this pass: **confirm-or-flag, not re-choose.**
The plan is dimensioned around the three catalog parts;
this pass verified them and pinned procurement details,
changing zero boundary dimensions.

## Verdict per selection

1. **6203 (17 × 40 × 12) — CONFIRMED.**
   Standard 62-series progression (6200 = 10×30×9 … 6202 = 15×35×11, 6203 = 17×40×12);
   dimensions ISO-standardized across all major brands.
2. **688 (8 × 16 × 5) — CONFIRMED, variant pinned to 688-2Z/688ZZ.**
   Bore 8 and OD 16 hold for every variant;
   the 5 mm width is the SHIELDED variant's width
   (the plain open 688 is commonly cataloged at 8 × 16 × 4).
   The BOM therefore specifies 688-2Z, which is also the practically better choice
   at an air inlet (dust exclusion). No plan dimension changes.
3. **ISO 4032 M10 (8.4 high, 16 A/F) — CONFIRMED, including the overhang claim.**
   ISO 4032 M10: height 8.04–8.40, across flats 15.73–16.00,
   across corners 17.77 min to ≈18.48 theoretical max.
   Worst-case overhang on the Ø18.0 hub nose = (18.48 − 18.0)/2 = 0.24 mm/side,
   under the plan's 0.3 mm/side claim ✓.
   **Substitution trap: DIN 934 M10 is 17 A/F (≈19.6 across corners →
   0.8 mm/side overhang), which would violate the claim — the BOM row forbids it.**

## Make-vs-buy rationale

- Both bearings: textbook Buy — precision rolling elements are never custom-made
  at this scale; the entire plan correctly sizes the Make parts AROUND them.
- lock_nut: the planner's BUY call is confirmed —
  a plain catalog hex nut on a standard M10×1.5 spindle thread;
  custom-making it would add cost with zero functional gain.
- No plan-marked Buy part should be Made; no plan-marked Make part should be Bought.

## Duty suitability (rotating compressor wheel on a pulley drive)

- Load path: belt pull enters at the pulley → shaft → impeller clamp →
  spigot → 6203 inner race → housing.
  The 6203 inner ring rotates relative to the radial load direction,
  so the INNER ring is the interference seat and the outer ring the transition seat —
  exactly the fit directions the plan already locks (textbook correct).
- 6203 C ≈ 9.95 kN dwarfs any plausible belt tension + compressor thrust
  at this scale; deep-groove bearings carry the modest axial thrust
  (toward the inlet/suction side) without a separate thrust element.
- 688 is a lightly loaded pilot bearing well inside its rating;
  its OD 16 sits within the Ø18 hub-nose flow shadow (`OD_INLET_MAX`) with margin.
- Speed: verify the duty-point rpm against the chosen brand's grease limiting speed
  (order 17–22 krpm for the 6203) if the drive ratio pushes past ~15 krpm.

## Fit intent to machine to (Make parts model at NOMINAL — this records the real intent)

| Interface | Plan parameter | Modeled | Real fit intent |
|---|---|---|---|
| Impeller spigot → 6203 bore | `D_MB_BORE` 17.0 | 17.0 / 17.0 | PRESS/interference (rotating inner-ring load). Spigot is aluminum in a steel ring: consider the upper interference band (m5-class) or a bearing-retaining compound (Loctite 641 class) to cover differential thermal expansion |
| 6203 OD → housing pocket | `D_MB_OD` 40.0 | 40.0 / 40.0 | Transition, housing bored to **H7** (stationary outer-ring load) |
| Shaft → impeller through-bore | `D_SHAFT_IMPELLER_SEAT` 10.0 | 10.0 / 10.0 | Slide/clearance, **H7/g6** — torque passes by clamp friction, not this fit |
| Shaft tail → 688 bore | `D_SHAFT_INLET_SEAT` 8.0 | 8.0 / 8.0 | Slide per plan. Advisory only: a rotating inner ring normally prefers a light interference (j5-class); for this pilot duty a slide fit + optional retaining compound is acceptable — no change requested |

## Lubrication / sealing

- Specify **2Z (shielded)** on both bearings: grease-for-life at this size,
  no relubrication provision needed anywhere in the design,
  and shields matter at a compressor inlet (airborne dust).
  The plan already allows "open or 2Z" for the 6203; 2Z is the recommendation.
- No seals (2RS) required: shields have lower drag and the housing is not wet.

## Lock-nut retention recommendation (advisory — modeled geometry unchanged)

- A plain hex nut alone is NOT adequate practice on a rotating spindle nose:
  specify **medium-strength threadlocker (Loctite 243 class) at assembly**,
  torqued to a normal M10 class-8 preload against the aluminum hub nose
  (the clamp preload is also what transmits drive torque — do not undertorque).
- A prevailing-torque nut was considered and NOT specified, for two reasons:
  ISO 7040 (nyloc) / ISO 7042 (all-metal) M10 nuts are ~10 mm high,
  taller than the modeled 8.4 envelope;
  and a nyloc needs 1–2 pitches of thread proud of the nut,
  but the thread ends 0.2 mm past the modeled nut top — insufficient engagement.
  Threadlocker achieves the locking function with zero geometry change.
- Detail-design note (no action now): check nut hand vs shaft rotation direction
  at drive-spec time — standard spindle practice is that deceleration
  should tend to tighten, addressed here by threadlocker regardless.

## Open questions for the orchestrator

None blocking. Two advisories already folded into the BOM:
the 688 variant pin (2Z for the 5 mm width) and the DIN 934 substitution ban.
No CONFLICT entries were warranted — designations exist,
dimensions verified, duty appropriate.
