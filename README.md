# AI-CAD: Example Projects

A browsable showcase of **real, unedited design runs** from the [AI-CAD](https://github.com/ai-cad-labs/ai-cad) system:
an open-source AI-CAD engineering department
where LLM agents generate, evaluate, and iteratively refine
parametric CAD ([CadQuery](https://github.com/CadQuery/cadquery)) designs
through visual and deterministic feedback loops.

Every run here is the **verbatim output of one autonomous run**:
the design spec the system generated from the goal,
the plan it wrote, its step-by-step reasoning log,
the per-part geometry it authored, the multi-view renders it evaluated,
the STEP/STL it exported,
and a structured self-debrief of what failed and what the run improvised to protect the result.
No geometry here was human-authored:
one run even starts from a hand-drawn sketch,
and everything after that sketch is the machine's.
The point of the gallery is to let you watch the machine think.

![The lead exhibit in shaded isometric: a centrifugal compressor assembly with backswept impeller in green, bearing housing in red, grooved pulley-shaft behind](impeller_assembly/iso_filled.png)

*The lead exhibit:
a six-component centrifugal compressor assembly
the system designed from a hand-drawn sketch;
[`impeller_assembly`](impeller_assembly/) holds the sketch, the brief,
and every artifact in between.*

---

## The showcase

| Project | What it shows | Render | Design spec | The debrief |
|---|---|---|---|---|
| [`impeller_assembly`](impeller_assembly/) | **The hero run, and the gallery's first image-input project**: a hand-drawn sketch became a 6-component centrifugal compressor with its 0.8000 mm running clearance measured five independent ways, and the system twice refused DFM advice that would have straightened the user's backswept blades, defending design intent against its own tooling. | [Shaded ISO](impeller_assembly/iso_filled.png) | [`goals.md`](impeller_assembly/goals.md) | [`run_reflection.md`](impeller_assembly/run_reflection.md) |
| [`piston_crank`](piston_crank/) | The 5-part IC-engine core assembled at top-dead-center: a fit/clearance dimension chain locked in the plan that held end-to-end, plus a deliberate mid-run self-checkpoint and cold resume. | [ISO wireframe](piston_crank/assembly/renders/iso_wireframe.png) | [`goals.md`](piston_crank/goals.md) | [`run_reflection.md`](piston_crank/run_reflection.md) |
| [`spur_gear`](spur_gear/) | A meshing involute gear pair: when the reference gear method proved numerically fragile, the run adapted to a point-sampled involute and proved the mesh with a deterministic interference test (0.00 mm³ at the correct half-tooth phase). | [ISO wireframe](spur_gear/assembly/renders/iso_wireframe.png) | [`goals.md`](spur_gear/goals.md) | [`run_reflection.md`](spur_gear/run_reflection.md) |
| [`treasure_chest`](treasure_chest/) | The clean control baseline: a 4-part chest shipped by 13 agents with zero failures and zero repair cycles, and three manufacturability findings deferred with written reasoning rather than repaired on reflex. | [ISO wireframe](treasure_chest/assembly/renders/iso_wireframe.png) | [`goals.md`](treasure_chest/goals.md) | [`run_reflection.md`](treasure_chest/run_reflection.md) |

---

## How to read a run

Each run lives in its own folder at the repo root and tells its story in this order:

1. **`README.md`**: the run's own summary, what it is and what it demonstrates.
2. **`goals.md`**: the design spec the system wrote for itself from the goal.
   Start here.
3. **`design_plan.md`** and **`design_log.md`**: the plan written before any geometry,
   then the agents' step-by-step reasoning as the design was built and validated.
4. **`run_reflection.md`**: the structured self-debrief,
   covering what happened, what failed, how the run self-healed,
   and what would make the next run smarter.
   The single best window into how the system reasons under friction.
5. **`assembly/renders/`**: the multi-view PNGs (clean + wireframe) the vision evaluator looked at;
   per-part geometry and renders sit under `assembly/<part>/`.
6. **Exports**: the `.step` / `.stl` CAD files, under `assembly/<part>/exports/`
   (and an assembly-level `exports/` where present).

These runs ship no raw session logs: the narrative documents above are the run's trace.

---

Archived examples from the predecessor PydanticAI implementation live in
[`z-archive-legacy-pydanticai/`](z-archive-legacy-pydanticai/): see its README.

---

## Related repositories

- **[`ai-cad-labs/ai-cad`](https://github.com/ai-cad-labs/ai-cad)**: the AI-CAD system itself.
  Start here to run your own designs.
- **[`ai-cad-labs/ai-cad-pydanticai`](https://github.com/ai-cad-labs/ai-cad-pydanticai)**:
  the predecessor PydanticAI implementation that produced the archived runs.

---

## License

Apache-2.0: see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

The example runs are provided as-is for illustration and research.
