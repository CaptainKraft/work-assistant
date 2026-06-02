# Team Glossary

Canonical spellings of JangaFX product names, people, and domain jargon, with the common
speech-to-text mis-hearings to watch for (in parentheses).

Used two ways:

- **Summaries must use these spellings.** When writing `notes/summary.md`, correct the ASR
  mis-hearings below to the canonical term.
- **Transcription hinting (optional/future).** This list can seed faster-whisper's
  `initial_prompt` to make the raw transcript itself spell these terms correctly.

Keep this list growing as new terms come up. Entries marked **(confirm)** need verification.

## Products & tools

- **EmberGen** / **EmberGen 2** (**EG2**) — JangaFX's real-time volumetric fire/smoke/explosion tool. (ASR: "Embergen", "Ambergen", "Emergen", "Emberton", "Enbridge N2")
- **IlluGen** (**IG**) — JangaFX's node-based procedural tool; its node UI framework is being ported into EG2. (ASR: "Illusion", "Illusions", "IG's UI")
- **LiquiGen** — JangaFX's real-time liquid simulation tool. (ASR: "Liquid Gen", "liquid gin")
- **JangaFX** — the company. (ASR: "Jenga", "Janga")
- **Craig** — the Discord bot used to record these meetings.
- **Claude** — Anthropic's AI; Nick and Vitalii used it to prototype interactive Combustion Lab mockups. (ASR: "clod")

## People

Correct spellings for references that appear inside the spoken text. (Speaker attribution
itself is handled by `people.json`.)

- **Nick** — EG2 product lead; speaks from the Discord account `jangafx`.
- **Morten** — simulation lead. (ASR: "Morton", "Martin")
- **Vitalii** — engineer; Combustion Lab design with Nick.
- **Dale** — rendering / environment renderer.
- **Mike** — UI; porting the IlluGen UI into EG2.
- **Jan** — path tracer.
- **Daniel**, **Jason** — artists / testers.
- **Said** — engineer.
- **Jeremiah** — manager.

## Domain terms

- **Combustion Lab** — EG2's simplified per-component "chemistry" system: components have triggers (e.g. temperature) that produce products (flames, smoke, …). Also called **ChemLab**; a name **"Pyro Lab"** was floated. (ASR: "cam lab", "chem-like") **(confirm canonical name)**
- **component** / **material** — EG2 concept: a *component* (e.g. "fuel A") contains a *material* (a rendering preset).
- **VDB** — OpenVDB volume format (an export target).
- **flipbook**, **EXR / image sequence** — export formats.
- **HDRI** — image-based lighting. (ASR: "HDR eyes")
- **advection** / **advected** — transport of a quantity by the velocity field. (ASR: "infected")
- **voxel**, **sparse simulation**, **buoyancy**, **vorticity**, **dissipation**, **diffusion** — simulation terms.
- **ray march** — volume rendering technique. (ASR: "raymarch")
- **scattering**, **emissive**, **density**, **six-point lighting**, **holdout**, **straight / premultiplied alpha** — render passes and channels.
- **CSG** — constructive solid geometry. **SDF** — signed distance field.
- **modulator / modulation** — varying a parameter with baked noise instead of on/off CSG shapes.
- **Noita** — game referenced for grain / per-voxel simulation.
- **Houdini** / **Karma** — SideFX Houdini and its renderer (benchmark / competitor reference).

## To confirm

- **JUR** — referenced as something "more or less done" being pulled into the MVP; unclear whether it's a person, a tool, or an acronym.
- Canonical name for the **Combustion Lab** (Combustion Lab vs ChemLab vs "Pyro Lab", and its spelling).
