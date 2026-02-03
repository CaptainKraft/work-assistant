# 1.1.2

- Improved UI's string truncation to truncate in the middle instead of the end -- this should improve the readability of long file paths
- Fixed "Export complete" dialog sometimes not showing
- Added Slope Blur node, useful to simulate edge damaged on heightmaps.
- Added flip face option to transform node. Useful when applying negative scale transforms
- Improved `Frequency` parameter on modulator nodes
  - Divisions of the loop region, frames and seconds are now supported as units for this parameter
- Improved backwards compatibility handling for node presets
- Fixed issue of application not entering power saving mode when task manager was open
- Made `Node Details` panel content resize dynamically based on panel width
- Previewing a texture node will now show the texture applied to best matching geometry rather than a flat plane
- Texture antialiasing option renamed to HQ supersampling
- Fixed some elements overlapping when panels were made very narrow
- Improve Cartesian to polar node :
  - HQ supersampling option added
  - Aperture angle and width to define the coverage of the full disk
  - Option to clamp of out of range texels
  - Added Distance option (Euclidean, Chebyshev and Squircle ) + Pinch and perspective
- Improve texture Transform node :
  - HQ supersampling option added
  - Optional safe transform toggle that allows any rotation angle and any scale when tiling is active
  - Fixed flip options when tiling was higher than 1
- Added splashscreen on Windows and Linux
- Added High pass filter option to the grayscale filter node.
- Fixed bug when `Ctrl+Click`ing to select two nodes on the node graph
- Added Color Meter to the 2D viewport, which can be toggled with the 'Toggle Color Meter' button.
  - The color meter shows in a magnified view of the pixels under the cursor as well as the value of the pixel under the mouse cursor.
  - You can lock the color inspector to a specific pixel in the viewport by left clicking the viewport. It can be then unlocked by clicking the viewport again.
  - Color textures will show the value of the RGBA channels in sRGB space
  - Grayscale textures will show the value in both RGB and sRGB space
  - UV textures will show the absolute UV value as well as its relative offset from the inspected pixel
  - Normal textures will show the normal direction
  - Island textures will the island ID and size
- Fixed Copy and Transform Y flipped pivot position and better label naming.
- Improved auto-scrolling when dragging off the edge of a panel (eg. when selecting nodes)
- Added timeline lane visibility "unsolo" support when shift-clicking a solo'd lane
- Added Utils Advect node that will advect/move textures along UV each frame of animation.
- Fixed Directional blur not tiling and noise.
- Improved import streaming quality of life by trying to auto detect the filename formatting
- Fixed exposing a parameter as a pin on "multi" nodes
- Made "NEW" badge show on What's New section of homescreen when there are changes
- Added Operator selection in Threshoold node (Greater than - legacy, Less than, In range, Out of range).
- Added 'Duplicate from' in the option of GeoUV to duplicate a UV set to another one
- Added Geo Render Camera Control node to control Geo Render To Texture node
- Fix missing extension when saving project file on Linux
- Added Geo delete points node that delete points using a mask selection
- Added Geo fuse points node that can merge points in the same position in space

# 1.1.1

## Fixes
- Fixed a licensing bug that was preventing some users from activating their license

# 1.1.0

## New Additions
- We've released the first version of our material functions for Unreal Engine 5 and Unity, which are useful for loading in our VAT textures, Optical Flowmaps, and more
  - Download them from the `Game Materials` menu option for your engine of choice
- Added Geometry masks. They are defined using Geo Combine Mask and can be applied to all Geometry nodes modifying the geometry
- Added VAT Encode and VAT Decode nodes :
  - You can encode per vertex position, normal, tangent and color in texture
  - Position can be encoded as a single pixel or split in high/low bits in two pixels
  - Position is encoded as normalized value, you need to define the maximum scale of your animation.
- Added more displacement mode in Geo noise : Along normal, 3D world (legacy), 3D local and on tangent plane and option to use point orientation or vertices normal and tangent
- Added Super sampling AA option to spritesheet encoding, edge extension for looping textures
- Added import streaming to import nodes
  - Import nodes can now stream in multiple files over time that match the current timeline frame
- Added support for variables in the import node's filename
  - This can for example allow you to import files relative to the project's directory
- Added wrap mode to renderer
- Added srgb view for grayscale. This allows you to view grayscale nodes in an encoding similar to color nodes
- Added Opacity mask input and vertex color alpha opacity in geo render to texture node
- Blend node will now account for the alpha channel when blend mode is set to 'alpha'
  - Grayscale blend mode 'alpha' will blend the inputs like the alpha channel of color blend
  - Previous behaviour of blend mode 'alpha' can be performed by using the new blend mode 'mix'
- Added 'UI Brightness' setting to preferences
- Added 'Invert Y channel' to 'Export: UV', 'UV to Color', 'Color to UV', 'UV Split' and 'UV Merge'
- Added Optical Flow node:
  - Analyses how pixels move from one frame to another
  - Can be used to produce flowmaps for smooth flipbook playback
- Added Flow Blend node:
  - Blends 2 images together using a flowmap
- Added support for out-of-bound values from modulator output preview
- Added neutral tonemapper to the tonemapping options of the renderer node
- Added derivative options to the uv from grayscale node
- Added support for zooming individual axis on Node Detail's curve editor
- Added sliders on context menu for Node Detail's curve editor keys
- Added 'Linear to sRGB' and 'sRGB to Linear' presets in node Levels

## Improvements
- Improved export performance in various cases
- Improved Sheet Decode to decode multiple frames at once and to have a frame perfect mode
  - To decode another frame enable 'Decode next frame'
  - To enable frame perfect playback set the 'Playback mode' to 'Standard'
- Improved timeline playback and scrubbing to make animated parameters more reproducible
- Enabled node preset support for all nodes
- Updated UI layout when searching node menu

## Changes
- BREAKING: All combine nodes have been renamed and modified to expose parameters in a clearer way:
  - Geo Combine Transform -> Geo XForm
  - Geo Combine Scale -> Geo Scale Points
  - Geo Combine Color -> Geo Color
- Changed exporting to export textures at the input nodes resolution rather than the project resolution
- Made content of group show in node menu if only one group is present

## Fixes
- BREAKING: Fixed orientation inconsistencies with pivots
- Fixed fractal nodes randomization degenerating on extreme scaling
- Fixed erroneous context menu on gradient/curve preset browser special categories
- Fixed clicking off textbox on Node Details panel sometimes not registering the new value
- Fixed clicking off textbox on Node Details panel sometimes not registering the new value
- Fixed copy and transform pivot baking
- Fixed aspect ratio in geo render to texture node
- Fixed rare bug where exiting textbox state might have resulted in a crash
- Fixed alpha channel being dropped with blend nodes
- Fixed export progress bar exceeding 100% progress
- Fixed Sheet Encode
  - to encode the first frame rather than last frame of a sequence when in stride mode
  - to be frame perfect
  - to be pixel perfect
- Fixed issues with backwards compatibility handling when subgraphs were used
- Fixed Geo UV node
  - Bad UV generation with triangle geometry
  - Incoherent UI in 'keep current' mode + exposing mirror and rotations
- Fixed background color being inconsistent when the grid is on
- Fixed point orientation in geo copy to points, geo copy and transform, geo points shape
- Fixed geo copy and transform node
  - Jitter position was not aligned to point orientation when points pin was used
  - Distribution and skip last are removed when points pin was used
- Fixed directional blur uv filtering
- Fixed point orientation in geo space warp
- Fixed alpha channel being displayed in the wrong color space when using RGBA toggles in the viewport

- Added grayscale Tiler node that generates regular patterns of shapes.

# 1.0.3

## New Additions
- Added option in Geo sweep to transfer point color to vertex color
- Added Geo Render to Texture node:
  - Color: Vertex color, Point color, 3D positions uniform, 3D position scaled per axis
  - UV: vertex UV0 -> UV3, point UV, Reflection distortion, Refraction distortion, Normal to UV
  - Grayscale: Depth, Mask, Fresnel, Diffuse lighting
  - Normal (screen or world): Vertex normal, Point normal, Reflection vector, Refraction vector
- Added Multi packer node to easily create atlases
- Added Pixelizer node to reduce and quantize textures
- Added the ability to select a custom resolution for Export Viewport node
- Added new techniques to the Edge Detect node

## Improvements
- Improved Geo copy and transform by adding pre rotation, pre scale, extent or spacing distribution as well as curves
- Improved rendering of geometry when only the emissive pin is used

## Changes
- Made shortcut key name in preferences expand when resizing window and added tooltip

## Fixes
- Fixed import model to work with larger sized models
- Fixed integer values sometimes showing as different when multi-editing nodes
- Fixed fractal nodes randomization degenerating on extreme scaling
- Fixed space warp node unwanted translation when moving origin

# 1.0.2

## New Additions
- Added geometry self shadowing
- Added intensity parameter to color to normal node
- Added maximum smoothness intensity to Polar Scatter node and Grayscale Fractal nodes
- Added support for dropping multiple files onto the node graph
- Added automatic capture of thumbnails for projects
- Added geo displacement node, this removes the displacement pin in the renderer
- Added a scale reference to grayscale shape node to define the texture axis used to define the size of the shape
- Added preset to all nodes missing them
- Added color to normal intensity slider
- Added copy + paste support to curves and gradients
- Added a 'regular' chaos type to UV radial

## Improvements
- Improved floating viewport when a panel is fullscreen to display all viewport modes
- Improved grid shadow to work with opacity keying and displacement
- Improved geometry and point node types. you can now use all geo nodes with any type of geometry
- Improved anisotropy in utils transform node which has been replaced with non uniform scale - horizontal and vertical scales
- Improved graph undo/redo stability
- Improved workload balancing on weaker GPUs
- Improved geometry lighting
- Improved auto view when working with 2D heavy project
- Improved chaos in UV radial : 3D noise, rotation, contrast and bias control

## Changes
- Changed graph align options to support shortcuts
- Changed timeline key align to support shortcuts
- Changed renderer node parameter "emissive" to "emissive intenisty"
- Moved ground grid and shadow to per-project settings

## Fixes
- Fixed a bug preventing presets from being launched on the home page
- Fixed issues with ui animation being dependant on framerate
- Fixed crash/freeze while the node graph is processing geometry
- Fixed geometry merge to support different attributes configuration to be merged
- Fixed broken curvature node
- Fixed caustic tiling even when tiling option was off
- Fixed geo noise missing shard and gabor noises
- Fixed grayscale spline when uv input is connected
- Fixed Caustic looking drastically different when changing resolutions
- Fixed fractal nodes breaking the tiling when quincunx was active
- Fixed grid node not generating tileable islands
- Fixed geometry tangents when using geo uv node
- Fixed nodes not updating properly when dependent on timeline frame
- Fixed geo node stats not updating properly when animated
- Fixed undo undoing too many things in a single action
- Fixed modulatable range slider when inputting for "Max" value
- Fixed undo resetting the entire lattice for the lattice warp node
- Fixed first frame of export being wrong in many cases

# 1.0.1

- Fixed a bug causing a black screen on startup and other rendering issues

# 1.0.0

IlluGen is a real-time procedural VFX asset generator for both 2D and 3D assets. This is the first public release and unlike a standard changelog, we will list the major features, and nodes as they currently exist.

## Included Nodes
- [camera]: camera, look at
- [color]: adjust, fractal, hue spread, interpolate, ramp, replace, uniform
- [export]: color, mask, mesh, multimask, normal, viewport, warp
- [geometry]: accumulate, bake, combine color, combine scale, combine transform, copy and transform, copy to points, extract points, merge, noise, points shape, promote, shapes, space warp, sweep, transform, UV
- [grayscale]: AO, caustics, curvature, curve, dilate, filter, fractal, gradient, noise, polar scatter, shape, slice, spline, threshold, uniform, xdog
- [import]: model, texture
- [islands]: generate, padding, to color, to gradient, to grayscale, to uv
- [normal]: combine, create
- [particle]: 2D render, point attributes
- [renderer]: renderer
- [utils]: alpha merge, alpha split, anisotropic kuwahara, auto crop, bilateral filter, blend, blur, cartesian to polar, color to normal, color to uv, copy and transform, denoise, directional blur, distance, edge detect, fxaa, glow, grid, hsva to rgba, lattice, levels, multi blend, multi switch, normal merge, normal split, normal to color, polar to cartesian, rgba merge, rgba split, rgba to hsva, rgb to grayscale, sheet decode, sheet encode, softblend, tile, transform, uv merge, uv split, uv to color
- [uv]: blend, blur, cartesian to polar, directional, flow, from grayscale, identity, noise, radial, rotational, spline, transform

## Features
- Real-time Node Previews for individual nodes.
- 2D and 3D Viewports for cleaner editing and separation of asset types.
- Author procedural 2D and 3D assets within the same graph for ultimate convenience.
- Preview individual color channels, and full color with alpha within our 2D viewport.
- Conveniently check for texture tiling with our tiling texture preview
- Switch between bilinear and point filtering as needed
- Preview normal maps, UV warp coordinates (these are used to warp textures), 2D images, grayscale, color, alpha, flowmaps, flipbooks, 3D meshes,  3D mesh points, vertices, UV's, faces, triangles, quads and a ton more.
- Alpha is not a separate concept in IlluGen like other some tools. Anything can be packed as an alpha channel and can be authored like any other RGB or HSV color channel.
- Brand new node search system when dragging off of a pin: Allows you to easily type the name of a node or node preset.
- Smart and context appropriate node suggestions based on your most commonly used nodes in a given situation.
- Reroute pins: Drag off of any active connection to create a reroute node. This is also the proper way to move a bundle of connections to another pin.
- Animation timeline complete with keyframing, a full curve editor, repeating, looping, and more.
- Easily load and edit existing flipbook textures on a per frame basis.
- Export Mesh Flipbooks, 2D Flipbooks, 2D Images, Non-Square textures, and more.
- Subgraph support: For commonly used sets of nodes, use subgraphs to make reusable functions out of them and simplify your workflows.
- Curve profile and color gradient presets can be stored in custom folders and be shared amongst teams.
- Any node can become a preset by clicking the dropdown at the top right of the node info window. This is useful in a case where you may have a very cool custom noise texture that you've generated and would like to easily reuse it as a starting point in the future. Once named, you could search for this preset and spawn it right within the node context window (right click).
- Basic PBR rendering support
- Standard shading model support for VFX asset types: Alpha, Opaque, multiply, translucent.
