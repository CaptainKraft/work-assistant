# EmberGen 2 — MVP Planning

- Date: 2026-06-02
- Duration: 01:40:07
- Attendees: Nick, Daniel, Jason, Morten, Said, Jeremiah (others present but not on-mic; Mike, Dale, Vitalii, and Jan were referenced for work assignments)

## Overview

The first full team meeting in a while, called to get EmberGen 2 back on track. EG2 has slipped repeatedly — originally targeted as a beta at the end of last year, then this summer — and after years of work the team has a strong smoke renderer and sparse simulations but no usable tooling and a combustion system that doesn't really work. Nick walked through an MVP spec (shared as a PDF) to define a deliberately stripped-down first target, how to reach it, and who works on what. The team aligned on the scope and agreed to spend the upcoming cooldown assigning work and setting up milestones.

## Key Decisions

- **MVP = explosions only.** One clear visual target (realistic fire + smoke explosion, plus a secondary black-powder-style explosion). Explicitly out of scope: clouds, dust puffs, zero-gravity fire, mesh import/painting/texture emission. Final outputs: VDBs, flipbooks, and image sequences.
- **Temperature channel must be correct first.** EG1's temperature is physically wrong (a white blob requiring reverse-gradient hacks). EG2 must look like fire out of the box. This is the top priority and a prerequisite — fire rendering is blocked until it's right. Temperature is treated as inherent to the sim, **not** a component.
- **Build the Combustion Lab ("ChemLab") for the MVP.** A simplified chemistry system: components (e.g. "fuel A") have triggers (e.g. temperature over a threshold) that produce products (flames, smoke, etc.), with value ranges instead of single values to break up homogeneity. Implement the existing mockups as-is and iterate by actually using it rather than debating further.
- **Component / material system replaces hardcoded channels.** Emitters emit chosen components rather than fixed fuel/smoke/flames. A component contains a material (a rendering preset, browsable with thumbnails), so any component can be rendered as flames, smoke, vapor, or nothing. The separate shading node is eliminated and folded into components.
- **Port IlluGen's UI into EG2** (pins, node previews, node presets, sub-graphs). LiquiGen will get the same treatment later.
- **MVP can be janky.** Gray boxes, placeholder panels, and black-square previews are acceptable; polish comes over the following ~2 years. The only bars are "does it feel good" and "does the output match the target image."
- **Strict scope discipline.** If work doesn't move toward the MVP target image, it stops. Work not finishable by end of this week (end of the current cycle) is paused.

## Action Items

- Sim team (Morten) — Implement the most basic Combustion Lab and get core combustion + temperature correct; decide which ChemLab parts to build first vs. defer; confirm the component limit (~16) — toward MVP, 2026
- Render team (Dale) — Fire and smoke rendering (emissive volumes for fire, particulate-vs-vapor materials, scattering) — starts once temperature is correct
- Mike — Port IlluGen's UI to EG2; rough/placeholder is fine for now
- Export — Assign a couple of people to export passes: EXR/image sequence, VDB, flipbook (channels: final, emissive, scattering, emissive+scattering, density, six-point lighting, alpha; straight + premultiplied)
- Nick + Vitalii — Continue iterating ChemLab mockups and stand up a placeholder Combustion Lab UI for feel-testing
- Jeremiah — Build GitHub milestones for the MVP and clean up the EG2 project (still cluttered with EG1 items); break work down by cycle
- Nick + Jeremiah + Morten — Over the 2-week cooldown, finalize scope, assign people to specific items, and set the cycle plan
- Daniel + Jason — Hold off on using EG2 until the MVP is ready, then run a recorded testing session to capture genuine first-use impressions before getting habituated to rough edges
- Jan — Pause path-tracer work (not MVP-relevant); to be reassigned
- Whole team — Finish current cycle work by end of this week; route EG2 decisions/discussions back to Nick to close the communication gap

## Discussion by Topic

### Combustion Lab / components
Components are emitted from emitters and react via triggers (temperature, overlap, proximity/radiant heat) to produce other components. Properties like buoyancy, density, dissipation, and diffusion move from the sim node down to individual components, greatly simplifying the sim node. Multiple smoke colors are wanted for the MVP; multiple fuel and flame types are deferred to advanced use later. Morten noted the existing combustion system can be adapted to this interface and that the machinery is broad, so the team should focus only on the parts needed for explosions first.

### Rendering
The renderer should meet or exceed Houdini Karma and is considered close — smoke with an HDRI already looks great (Dale's environment work called out). Needs: emissive volumes for fire, an explicit particulate-based smoke material vs. a separate vapor/cloud material/algorithm, and fire-induced scattering. JUR's work is considered essentially done and will be pulled into the MVP.

### Sourcing
Keep MVP sourcing simple with basic primitive shapes. Nick advocated dropping CSG noise-blend shapes (performance cost, rarely used) in favor of modulating parameters with baked IlluGen noise, giving ranges instead of on/off values; Jason was on board provided the same results are achievable. Particles are powerful for sourcing but are out of the MVP (they'll come in full EG2); dynamic fuel can instead emerge from two components mixing.

### Scene graph / outliner idea
Nick floated moving always-present scene objects (skybox, ground, lights, cameras) out of the node graph and into an outliner, "promoting" an item to a node only when you need to transform it — to declutter the graph, especially with Dale's whole-world mesh imports. Explicitly not for the MVP; raised for future consideration, with caution about not making EG2 feel unlike EmberGen.

### Transforms
Deferred. Despite reportedly ~100 hours of side discussion, the team agreed transforms aren't worth debating for the MVP; EG1's behavior is considered fine for now. Nick's only preference: a unified "transform" data type/pin.

### Process / cycle
Jeremiah outlined timing: current cycle ends this week (finish in-flight work), followed by a 2-week cooldown during which leads assign people and build milestones, planned per cycle. No hard MVP deadline was set beyond a 2026 goal, with an emphasis on focus and discipline.

## Open Questions

- Where does the Combustion Lab live in the UI — inside the sim node (double-click), a separate tab, or a sub-graph? (deferred as a usability detail)
- Are ChemLab rules per-voxel, or do they affect neighboring voxels? Nick's intuition is per-voxel, but it's flagged as a Morten question.
- Do components need explicit starting states for the sim to run, or is the graph sufficient? (Nick thinks not, but unsure)
- Said's doubt: is EG2's current unusability really due to the lack of a ChemLab, or mainly parameter tuning producing wrong temperature? (ChemLab agreed as worthwhile regardless)
- Final name for the system — "Combustion Lab" vs. "ChemLab" vs. a floated "Pyro Lab."
- Exact component limit (Morten to confirm; ~16 discussed).
