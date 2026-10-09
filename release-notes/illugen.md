# 1.2.0

## New Additions
- Added an Accumulate node that combines a range of timeline frames into a single image, supporting grayscale, color, UV and normal textures
- Added a custom curve mode and weighted scale for the accumulation in the Sheet Encode node; this also fixes a scaling issue in the sample weight, and old presets keep their behavior
- Added a histogram overlay to the 2D viewport (toolbar button or Ctrl+Shift+5); shows the 256-level distribution of grayscale images or of the red, green, blue and alpha channels of color images
- Added an Equalize node that equalizes the histogram of an image so every level is equally represented, with Luminance and Per Channel modes for color images and a Strength control
- Renderer gained three tonemapping operators: GT7 (Gran Turismo 7), AgX and Khronos PBR Neutral
- Color Interpolate and Color Gradient nodes gained OKLCh, Spectral, HSV Smooth, CIELAB, RYB and Beer-Lambert interpolation modes
- Added a Geo Subdivide node that applies up to 6 levels of Catmull-Clark subdivision to geometry; hard edges are kept sharp (creased)
- Grid node gained a Tileable option; the hexagonal grid now tiles seamlessly at any width, and its islands output merges hexagons split across edges into single islands
- Added a Snap to angle option to the rotation randomization of the Grayscale Fractal, Color Fractal, Grayscale Polar Scatter, Islands to Gradient and Islands to UV nodes (snaps the random rotation to the nearest multiple of the given angle, 0 disables it); the Grayscale Tiler Snap rotation dropdown gained a matching Custom option
- Added a Viewport Dithering preference that reduces 8-bit color banding in the 2D and 3D viewports (on by default)
- Added an Image to Material node that extracts albedo (de-lit), height (with optional edge-preserving denoise) and roughness maps from a photo; supports tiling so the maps stay seamless for a seamless input (heuristic, frequency-based; best for flat-lit material photos)
- UV Noise node gained an Add Z axis option with Z position and Z layers for animatable noise that loops seamlessly (Z position 0% and 100% match)
- Tile node techniques gained a Blend mode option: Linear, OKLab (avoids muddy seams), or Soft Blend (keeps detail and contrast — per-frequency on Mirror/Scale, variance-preserving on Voronoi)
- Added snap-to-frames support to the timeline
- Geo Shapes:
  - Cone gained a Top radius option
  - Torus now uses dedicated Minor radius parameters; old presets are migrated automatically
  - Added a Pivot at bottom option
  - Added a Geodesic Sphere primitive (subdivided icosahedron)
- Added a Geo Complex Shapes node:
  - Supershape — organic/star-like forms from the Gielis superformula
  - Torus Knot — a tube swept along a (P, Q) knot curve
  - Helix — a tube swept along a coil
- Added a Geo Honeycomb Shapes node:
  - Spline-sweep mode: connect control points and the node wraps a honeycomb strip along the spline (uses the points' orientation to roll the tube when present, otherwise a rotation-minimizing frame)
  - Sphere
  - Plane (with Bend X and Bend Y options to bend up to a torus)
  - Hexagonal patch
  - All of the above with an adjustable gap between cells and a cell height for raising cells into spikes or sinking them into holes, plus an option to bake a per-cell pivot, orientation and id
- Added per-node timings to the node graph (can be enabled from the preferences under `Show GPU Timings`)
- Added graph frame rate and UI frame rate to stats
- Added interpolation mode selection for all keys at once in the curve menu
- Added a Keep relative center position option to the Auto Crop node, with an adjustable Pivot gizmo

## Improvements
- Improved the 3D viewport bloom:
  - Anamorphic radii (for horizontal or vertical streaks)
  - Dirt/dust masks, with support for normal maps
  - A much larger maximum bloom radius
  - Frequency modification (effectively allowing you to change the blur's falloff shape)
  - Firefly/sparkle reduction
  - Up to 2x faster than before on Apple Silicon
- Improved load balancing performance and stability for graphs that require high amounts of GPU time
- Optimizations:
  - Directional Blur node optimized, output is identical
  - Blur node uses a two-pass filter when its radius isn't modulated, output is close to the previous version
  - Grayscale Filter blur (Gaussian/Sharpen/High-pass) uses a faster mip-bounded separable Gaussian, output is close to the previous version
  - Glow node uses a separable multi-scale bloom, output is close to the previous version

## Changes
- Renamed the Auto Crop node's Uniform cropping option to Keep aspect ratio

## Fixes
- Fixed Color Gradient alpha being gamma-corrected in the RGB and OKLab modes; alpha now interpolates linearly
- Fixed 'autolink' for dangling reroute nodes
- Fixed the Import Model node forgetting which mesh layer was selected when reloading a project
- Fixed the color picker not working on macOS
- Fixed Auto Crop node cropping for non-square sizes and mismatched resolutions
