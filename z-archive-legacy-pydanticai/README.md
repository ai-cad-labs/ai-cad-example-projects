# Legacy PydanticAI runs (archive)

These are archived example runs from the **predecessor PydanticAI implementation** of AI-CAD
([`ai-cad-labs/ai-cad-pydanticai`](https://github.com/ai-cad-labs/ai-cad-pydanticai)),
kept as historical reference:
a snapshot of what the first-generation system could do end-to-end.
The current showcase lives one level up in [../README.md](../README.md).

| Project | What it shows | Render | Design spec |
|---|---|---|---|
| [`table_lamp/`](table_lamp/) | Five-part desk lamp (weighted base, stem, socket housing, shade, Edison-base bulb) with a full DFA/DFMA pass and 54 render PNGs | [assembly collage](table_lamp/assembly/renders/collage.png) | [goals.md](table_lamp/goals.md) |
| [`wheel_assembly/`](wheel_assembly/) | Three-part car wheel (machined hub, 17-inch 5-spoke alloy wheel, rubber tire, bolted with 5 M12s) with DFA/DFMA plus top-level assembly constraints | [assembly collage](wheel_assembly/assembly/renders/collage.png) | [goals.md](wheel_assembly/goals.md) |

*Render links point to each run's assembly-level `renders/collage.png`:*

the eight-view collage (four wireframe + four clean views) of the full assembly.

Each run also carries per-part collages under `assembly/<part>/renders/`.
