# wheel_assembly

> Built with: PydanticAI (legacy/predecessor) · Parts: 3 · Exports: STEP + STL · DFA + DFMA

**What it is.**
A car wheel assembly:
a machined aluminum hub (80 mm OD, 5-bolt circle on 100 mm PCD),
a 17-inch 5-spoke pentagonal alloy wheel with a matching central bore and bolt pattern,
and a rubber tire, assembled with 5 M12 bolts.
The tire is rubber molding, so CNC rules are waived for it.

**What it demonstrates.**
A full 3-part assembly with design-for-assembly and design-for-manufacturing analysis
plus top-level assembly constraints:
a good example of the system reasoning about bolt patterns, PCD matching,
and mixed-material manufacturing (machined vs molded).

**How to read.**
`goals.md` → `design_plan.md` → `design_log.md`
→ per-part geometry, renders, and exports under `assembly/`
→ full agent trace in `wheel_assembly.log`.
