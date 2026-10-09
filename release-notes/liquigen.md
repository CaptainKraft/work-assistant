# 1.1.0

## New Additions
- Added support for node presets (top-right dropdown menu on the Node Details panel)
- Added support for connection reroute and wireless connections
- Added support for subgraphs to the node graph
- Added a dedicated **Meshing** node, moving all mesh-generation controls out of the Simulation node into a node you can insert between Simulation and Scene/Export
- Added adaptive particle radius and a minimum-neighbors filter to mesh generation, helping fill holes, stabilize isolated particles temporally, and cull stray floating droplets

## Improvements
- Improved the thickness render pass to render more layers
- Improved the 'Higher quality meshing' mode that doubles the mesh resolution and unlocks a full surface post-processing pipeline:
  - **Smooth SDF**: averages the surface to remove bumps and noise, with reshaping, depth limiting, and velocity/vorticity/density masks
  - **Curvature Flow (MCF)**: geometry-aware smoothing that targets noise while preserving flat areas, thin sheets, and fine strands, with much better volume preservation than plain smoothing
  - **Reshape**: dilate/erode and open/close operations to grow/shrink the surface and fill or remove small features
  - **Smooth Mesh**: vertex smoothing with two algorithms — Bilateral (preserves sharp edges like wave crests and splashes) and Weighted Laplacian (aggressively flattens bulk surfaces while particle density protects droplets)
  - **Snap to Colliders**: pulls mesh vertices onto nearby collider surfaces so liquid sits flush against solids (e.g. water against the inside of a glass), with configurable distance, iterations, and margin
  - **Clipping**: remove solid faces at liquid/collider boundaries, and clip the mesh against connected primitives or imported meshes via a new 'Clipping geometry' input

## Changes
- Merged the Simulation node's 'Particles' and 'Mesh' output pins into a single 'Liquid' pin that connects to the new Meshing node and the Export: Particles and Export: VDB inputs
- Renamed the Scene node's 'Liquid Mesh' input to 'Mesh', matching the Meshing node's output
- Removed the Scene node's 'Liquid Particles' input
- Removed processing of geometry files dropped on the viewport; they now only work when dropped on the graph

## Fixes
- Fixed issues with exporting ground plane alpha
- Fixed mask selection not working when used for emitters and colliders
- Fixed mask selection visibility not being refreshed
