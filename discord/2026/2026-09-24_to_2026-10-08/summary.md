# Discord catch-up: Sep 24 – Oct 8, 2026

- Server: JangaFX Dev Team
- Sections: Operations, JangaFX HQ, Software Development, Other Development
- Messages read: 2,027

Names: Discord display names, with real names where the chat made them clear:
jmpep = Javier, Perlind = Lucas, Solomai = Seb, Gaxil = Gil.

## Needs your attention

- **Internal builds are unsigned while you're away.** Shirk hit a Windows block opening an
  internal build and asked again for a dev launcher / release tool. Mike told people signed
  internal builds will resume when you're back. (#gen-application, Sep 25–28)
- **Discord meeting reminders aren't firing.** Lucas, Jan, Dale and Seb didn't get one for the
  Oct 7 meeting. Shirk got it during the meeting. With daylight saving, the meeting is now 11pm
  for Lucas (he usually sleeps at 10). (#lounge, Oct 7–8)
- **IlluGen 2.0 is about one week from release.** Gil is pushing back on late changes: QA started
  three weeks ago and he doesn't want another PR next week. He suggested a **2.1 milestone in
  GitHub** for deferred items. Seb asked where "small annoyance" issues should go. Mike said to
  file them as low-priority issues. This lines up with the git-tracked milestones plan.
  (#ig-bugs-feedback, Oct 8)
- **ChemLab scope.** Jesse proposed moving ChemLab to the EG 2.0 release candidate, or even 2.1,
  since the rest of EG 2.0 is more mature than people think. Dale said to drop it entirely.
  Shirk asked what would replace it for artist-friendly, non-physical sims. Dale's answer was
  "simtuition". No decision yet. Confirm whether ChemLab is Combustion Lab. (#embergen-dev, Oct 7)
- **The Odin update is stuck.** Bill's Odin update PR (jangafx/EmberGen#5994) has waited months
  for testers. Alvaro and Mike want to hold it until after the release (under two weeks). Bill
  says he can't just merge it anymore with this many products and branches, and needs a test
  process. (#odin-dev, Sep 28–29)
- **Two friction points between people.**
  - Javier spent a weekend on octahedral HDRI work. Dale then said the unified renderer won't use
    it. Javier was annoyed because he had asked up front whether it was needed. (#liquigen-dev,
    Sep 26–27)
  - Gil is frustrated about the late shape-node feedback (see the IlluGen release item above).
- **Mac minimum spec is undecided.** Will and Nick asked for EG and LG system requirements and
  supported chips. Rough agreement: all M-series chips on paper. Oliver suggested ~300 GB/s memory
  bandwidth as the recommended spec. The team agrees not to support A-chip Macs (the new Mac Neo).
  Nobody owns the final answer. (#mac-dev, Oct 6–7)
- **Print ad deadline has passed.** Born Digital (Japanese reseller) needs 4K+ IlluGen images for
  a CGWorld print ad that runs Nov 10. The original ask was due Sep 20. Jason is covering EG, LG
  and GG. IlluGen images are still unassigned. (#marketing, Oct 5)

## EmberGen 2

- **Big build on Oct 1.** Dale posted a build with export work (flipbooks, image sequences,
  multi-layer EXR, VDB, TIF), Tungsten scene import, better FBX material support, directional
  shadows, overscan, much faster imports (Bistro 3+ min → ~3 s), much lower texture VRAM
  (5 GiB → 200 MiB on the car scan), anti-aliased primitive wireframes and viewport hover/click.
- **Nick tested it the same day** and found problems: no export or render-pass previews, slow
  Bistro import on his PC, shadow acne, a kaboom scene, and drag-and-drop FBX losing textures
  (backslash paths). Dale fixed most of these within hours. Jesse took drag-and-drop, including
  Linux support.
- **Old memory leak fixed.** Since 2023, release builds leaked memory in the texture pool: an
  `assert` wrapped a destroy call, and release builds strip it. Later texture-count changes made
  it churn every frame, which may also explain a recent slowdown. Fixed in jangafx/EmberGen#6318.
- **Jesse's EG 2.0 gap list:** export background color semantics, a warning for unapplied sim
  changes (LiquiGen-style), a material manager, per-pass export formats, and quick model-scale
  presets. Morten and Dale agreed the default should be premultiplied alpha. Jesse is adding the
  option.
- **Wireframes merged to development.** Jan finds them too bright. Mike suggested a toggle in the
  View menu.
- **Mesh SDFs** (Dale): working but heavy. One 4.7M-triangle mesh uses about 2 GiB VRAM, and some
  sign bugs remain. Morten cares more about VRAM than speed and wants scaling measurements. Dale
  also suspects his GPU is failing (desktop corruption while the sim runs).
- **Still open:**
  - A combustion velocity blow-up (Morten will look when he can).
  - Flicker tied to preemption and adaptive tonemappers on the 5090 (Jan).
- **Long-term EG 3.0 sim direction** (Morten): lift the 64K tile limit, per-component sparsity,
  hash-map indirection, block encoding, and more memory aliasing. Dale added async compute and
  eventually going fully bindless or Vulkan-only.

## IlluGen

- **Release builds:** Gil posted IG 2.0 builds on Sep 26, Sep 29, Oct 1, Oct 5 and Oct 6.
  - Fixes include fracture, crashes, tiling and distance nodes.
  - Mike's new node menu is in.
  - All node defaults were reworked, and the shipped "default" preset files were removed after
    Mike objected (those are meant for users' own defaults).
  - The 2.0 presets were finished Oct 8.
- **Nick's preset feedback:** fracture presets need a grid texture, and static presets should
  have static thumbnails. Gil has done both.
- **Bugs:**
  - Multi-select wrong-connection bug found by Seb: fixed by Mike (Oct 7).
  - Heavy geometry can crash the GPU (Windows TDR). Gil reduced it but won't do the full fix
    before release.
  - Exports are ~10× slower than playback. Lucas says compression needs pipelining.
- **Shape node:** default parameters look bad for some shapes. Agreed to fix in 2.1, not now.
- **MCP experiment** (Javier): a working Claude ↔ IlluGen bridge that builds decent materials with
  a lot of guidance. Mike strongly objected to anything user-facing with AI because of how artists
  see it. Nick: "zero percent chance we are releasing this." Gil and Mike see value for AI-driven
  QA.
- **Ideas raised:** a layer stack / PSD import node (Shirk); code/shader node support (Lucas is on
  it); TIF writing now in JAM (Dale).

## LiquiGen

- **Mac path tracer bug on Oliver's M3 (QA, Cycle 5 Team 4):** geometry disappears. BVH2 mode
  works and BVH8 doesn't. Diagnostics show the BVH8 build itself is broken. Dale found two side
  issues along the way (radix-sort undefined behavior, unsafe min/max on Metal). The root cause
  was still unfound as of Sep 27.
- **HDRI orientation:** Javier fixed the HDRI orientation to match Blender, with backward
  compatibility. Mike reviewed it, and it merged with `dale/jsa-destutter` into development
  (jangafx/EmberGen#6311).
- **FOV tooltip is wrong in every app:** it says vertical FOV, but it's actually horizontal. Dale
  wants to switch to focal length + sensor size.
- **Snap (Specs Inc) feedback** came in through Zach. Jesse answered most of it and asked
  follow-ups: why they want per-particle random velocity and mass, plus a ticket for meshes
  vanishing abruptly when particles die.
- **Nick needed a Mac LiquiGen build for a customer.** Lucas said the signed one is in
  #internal-builds.

## Shared tech (camera, JRI, Mac, Odin, Bridge)

- **New camera** (Jesse) in LiquiGen: pivot-to-cursor is now opt-in, there's a "Classic" pivot
  mode, and scroll-zoom now flies forward. Feedback is positive. Nick and Jason don't think the
  new toolbar is needed. Shirk wants a visible speed readout. The plan is to bring the same camera
  to GeoGen and IlluGen.
- **JRI:**
  - Dale built fully analytic anti-aliased wireframe shapes (Vitalii's design).
  - He wants to merge the four separate gizmo systems into one.
  - He posted a backplate design (keep the plate out of the scene and blend it at display time).
  - Lucas will do the Metal side of stutter-free texture uploads.
- **Mac:** Dale and Lucas fixed a Metal depth-blit validation error that broke primitive
  hover/click on Lucas's machine. Merged to dev.
- **Odin (Bill's cooldown work):**
  - Compile times are 1.5–2.7× faster.
  - Odin now defaults to `radlink` on Windows.
  - Bill concluded incremental builds won't help.
  - He's now adding escape analysis to catch bugs.
- **Bridge / JPI** (Bill): JPI shipped for IlluGen Sep 24 but crashed for Nick. Bill filed
  UI/icon issues jangafx/EmberGen#6277 through jangafx/EmberGen#6281 for Vitalii, who has started
  mockups. Starting Monday Oct 12, Bill will bring the whole Bridge to EmberGen 2.0.
- **Said** fixed a directory-creation bug on fresh Windows installs (jangafx/EmberGen#6310).
- **UI/UX:**
  - Request for a per-node visibility toggle icon (Jason). Vitalii mocked it up. Mike wants it
    always visible, not hover-only.
  - Display rotation flips our apps upside down. Dale says it's a ~10-minute SDL fix and it isn't
    done yet.

## Business and marketing

- **Nick's week:**
  - A video for Born Digital's Japanese clients.
  - Advice calls with Day III Studios.
  - A Claude-built sales CRM that scans FastSpring receipts for license-tier violations and
    upsell targets.
  - The first biweekly marketing meeting.
  - Heavy IG2/EG2 bug hunting.
  - A call with MadVFX about teaching IlluGen exclusively.
- **Case study leads:** Gears of War: E-Day (IMAFX), LEGO Batman, GSC Game World (Nick is
  following up), High on Life 2 / Squanch (Nick will build one).
- **BlenderCon (Jason and Daniel):**
  - Strong contacts: Pokémon Company, GSC, Polyfjord (wants to collaborate), Skoda, Egosoft, and
    several YouTubers.
  - A Belgian school asked Daniel to teach a masterclass.
  - Jason also figured out how to get LiquiGen whitewater into Unreal.
- **Feature requests:** SpaceMouse support (again); text meshes in EmberGen from Born Digital. The
  team leans toward an IlluGen → EmberGen live link instead.
- **Crash reports:** many IlluGen 1.2.1 crashes, mostly from one user, in preset-browser loading
  (likely a corrupt file). Lucas asked for assert details in crash reports.

## People

- **Francisco's** daughter was born Oct 1. **Daniel's** son Jonas was born Oct 4.
- **Vitalii** was sick from Oct 5 (fever), and also took Oct 2 off.
- **Gil** is at school some days (Oct 7, plus a tech-art jam).
- **Lucas** was working from Sydney for a few days from Oct 1.
- **Bill's** Doppelbock won third place in a CAMRA competition.
