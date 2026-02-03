# 0.5.4-beta

- Fixed "Export complete" dialog sometimes not showing
- Added support for zooming individual axis on Node Detail's curve editor
- Added sliders on context menu for Node Detail's curve editor keys
- Improved `Frequency` parameter on modulator nodes
    - Divisions of the loop region, frames and seconds are now supported as units for this parameter
- Improved backwards compatibility handling for node presets
- Fixed issue of application not entering power saving mode when task manager was open
- Made `Node Details` panel content resize dynamically based on panel width
- Fixed some elements overlapping when panels were made very narrow
- Fixed bug when `Ctrl+Click`ing to select two nodes on the node graph
- Added splashscreen on Windows and Linux
- Improved auto-scrolling when dragging off the edge of a panel (eg. when selecting nodes)
- Added timeline lane visibility "unsolo" support when shift-clicking a solo'd lane
- Made "NEW" badge show on What's New section of homescreen when there are changes
- Made Ctrl+N and Ctrl+O for new / open project work on homescreen
- Fix missing extension when saving project file on Linux

# 0.5.3-beta

## Fixes
- Fixed a licensing bug that was preventing some users from activating their license

# 0.5.2-beta

## New Additions
- Added support for dropping multiple files onto the node graph
- Added copy + paste support to curves and gradients
- Added new preset browser for gradients and curves
- Added 'UI Brightness' setting to preferences
- Added support for out-of-bound values from modulator output preview

## Improvements
- Made shortcut key name in preferences expand when resizing window and added tooltip
- Updated UI layout when searching node menu
- Made content of group show in node menu if only one group is present

## Changes
- Changed graph align options to support shortcuts
- Changed timeline key align to support shortcuts

## Fixes
- Fixed crash/freeze during node graph geometry processing
- Fixed integer values sometimes showing as different when multi-editing nodes
- Fixed erroneous context menu on gradient preset browser special categories
- Fixed clicking off textbox on Node Details panel sometimes not registering the new value
- Fixed rare bug where exiting textbox state might have resulted in a crash
- Fixed issues with backwards compatibility handling when subgraphs were used
- Fixed planet micro craters node

# 0.5.1-beta

- Fixed a bug causing a black screen on startup and other rendering issues

# 0.5.0-beta

- Mac support
- Added center-to-active shortcut to camera
- Fixed control points of exported mesh terrain surface and boundaries not being welded
- Fixed exported mesh boundaries having an invalid UV projection
- Fixed terrain exporting color vertex maps when no texture connected to input color pin
- Fixed open-edged seam in exported planet mesh
- Added support for searching in dropdown menus
- Added `Step Back Once` button to timeline
- Fix timeline region length

# 0.4.1-beta

- Fixed a bug causing the camera to get stuck in fly mode

# 0.4.0-beta

- Changed the default camera orbit/rotation control to `Alt + Left Mouse Button`
- Added the Warp Flow node that resolves pressure for computing obstacle avoidance
- Added the Heightmap Store and Heightmap Recall nodes to allow feedback loops
- Added preference option to invert camera panning
- Added tooltips to toolbar buttons
- Added status bar messages for spline tool and camera
- Added option to flip imported mesh along Z-axis
- Added a Repeat option to the Import: Heightmap node
- Fixed mesh exporter writing vertex normals to vertex color output channel
- Fixed mesh importer not reading vertex colors from FBX files
- Mesh importer output color values can now be read from a texture input pin
- Added uniform fill shape to mask/heightmap shape nodes
- Mesh exporter no longer silently fails when only the color input pin is connected
- Fixed mesh importer reload button not functioning
- Fixed mesh import node not loading OBJ files
- Fixed blank images being exported when using Unity mapping
- Mesh reduction is now also applied to water layers exported by the model writer
- Added PNG16 read support
- Added a bounding box to imported meshes
- Added a shortcut to toggle water rendering in the Renderer node
- Added the Export: Warp node
- Added the Export Variations option in the File menu
- Added a node-processing progress bar to the viewport
- Added copy+paste support for color-gradient handles
- Added "copy" button next to color picker's HEX value
- Added the `Numbering offset` parameter to export nodes
- Added support for using Ctrl+C to copy dialog box message to clipboard
- Fixed shadow mask not updating when link-to-sun is enabled for the first time
- Improved speed of 16-bit PNG writer and set it as default format for heightmap exports
- Added status message to image importers' parameter list
- Improved performance and responsiveness of mesh and image exporters
- Improved viewport camera stability when zoomed out
- Improved the performance and quality of water and fog rendering
- Improved the flow output generated by water filter
- Improved domain warping preview
- Improved fluvial erosion by using bicubic filtering and having proper details erosion
- Improved the Oren Nayar implementation to reduce unwanted anisotropy in diffuse lighting
- Improved various error messages
- Mesh importer output color values can now be read from a texture input pin
- Set heightmap export PNG precision to 16-bit by default
- EXR files are now exported with 32-bit precision
- Set multimask default srgb values to false
- Spline join now bridges two disconnected nodes instead of merging them
- Interior values of closed heightmap splines are now clamped at the spline boundary to avoid values from spiking
- Made preferences and project settings searchable
- Updated the Oscillator node's curve editor when using custom waveform
- Made license key hidden-by-default in the license manager

## Bugfixes
- Mesh exporter no longer silently fails when only the color input pin is connected
- Fixed "Node Details" panel drag handle not working when not on the first tab
- Fixed bug which caused node graph tree-view to disappear when dragged too far to the right
- Fixed bug which prevented dialog provider changes to be saved
- Fixed parameter override cycler showing while multi-editing on non-overridable parameters
- Fixed lighting errors when having render details enabled
- Fixed mesh importer reload button not functioning
- Fixed mesh exporter writing vertex normals to vertex color output channel
- Fixed imported textures being flipped
- Fixed convert to sediment in sediment filter
- Fixed mesh importer not reading vertex colors from FBX files
- Fixed blank images being exported when using Unity mapping
- Fixed height ways water flow showing uneven pattern in filter water
- Fixed snow mask scale not matching the emitted amount of snow. Default snow amount increased to 1 meter
- Fixed sediment mask scale not matching the emitted amount of sediment
- Fixed large warp intensity by setting default to 100% for nodes that support warping
- Fixed seam artifacts in Tile Heightmap & Mask nodes
- Fixed bug when the same subgraph node preset was used multiple times in a project
- Fixed camera transformation state not being applied to automation timeline
- Fixed memory leaks in gizmos
- Spline join now bridges two unconnected nodes instead of merging them
- Interior values of closed heightmap splines are now clamped at the spline boundary to avoid values from spiking
- Added error dialog when a project fails to load
- Added dialog box listing errors if there were problems loading a project
- Fixed "Node Details" panel drag handle not working when not on the first tab
- Added support for variation export (File -> Export Variations...)
- Fixed bug which caused node graph tree-view to disappear when dragged too far to the right
- Made preferences and project settings searchable
- Fixed bug which prevented dialog provider changes to be saved
- Updated `Oscillator` node's curve editor when using custom waveform
- Improved viewport's stat UI
- Added node-processing progress bar to viewport
- Made license key hidden-by-default on licence manager
- Added copy+paste support for color-gradient handles
- Added "copy" button next to color picker's HEX value
- Added `Numbering offset` parameter to export nodes
- Improved error reporting on "Export Variations"
- Fixed parameter override cycler showing while multi-editing on non-overridable parameters
- Added support for using Ctrl+C to copy dialog box message to clipboard

# 0.3.1-beta

- Fixed `Convert To Subgraph` inputs when used with multiple nodes connected to the same output pin
- Fixed a bug related to using the same subgraph node preset multiple times in a project
- Fixed issues related to AMD graphics cards
- Fixed file dialogs for Linux users

# 0.3.0-beta

- WARNING: due to significant changes in this release, presets from previous versions are not guaranteed to work

- Added support for subgraphs
- Added Ground relief noise parameters to the Shape node
- Rock Node:
    - Removed 'Maximum height' in favor of 'Squeeze height'
    - Improved 'Orientation from slope' behavior to control how much the rocks are tilted along the ground
    - Masks are no longer deformed by the domain input in order to be more consistent with the Scatter node
    - Added anisotropy parameter for non uniform grids
- Scatter Node:
    - Made size distribution consistent with the Rock node
    - Improved 'Orientation from slope' behavior to control how much the relief is tilted along the ground
    - Added the 'Underlying ground detail level' parameter to match Rock node behavior
    - Added anisotropy parameter for non uniform grids
- The Adjust node's Heightmap output now works for planets
- The Noise and Fractal nodes' Heightmap can now directly blend on top of an input heightmap
- Added the Directional Blur Color node
- Added the Warp only option to the Base node
    - This exposes only the height variation generated by the warp
- Added the Smooth border option to the Height Noise, Height Fractal, and Height Spline
- Added the ability to delete all image dimension presets
- Added ambient occlusion to the preview and final render
	- The resolution can be adjusted in settings
- Added the 'Mask blur' node
- Added Mask height Use Full Range option
- Added a directional blur pass prior to the regular blur pass of the Warp blur node
- Added 'Accurate slopes' to the 'Voronoi distance type' parameter of the Warp Noise node
	- This gives more regular shapes when using 'Difference' in the 'Voronoi result' parameter
- Added 'Randomized difference' and 'Edges' in 'Voronoi result' dropdown of the Warp Noise node
- Added toggleable lighting to the Mask, Domain and Color previews (shift-L)
- Added a Base node option for multiple octaves with randomized scale, height, and offset
- Added reverse Voronoi noise for generating cracks
- Added spline node variants for heightmap, mask and warp
- Added option to bake out a high frequency normal map from the export mesh node
- Added shortcut to randomize parameters (ctrl+alt+r)
- Added pop-out curve editor to curve editor widgets
    - Accessible using the button to the right of the curve editor widget
- Added support for snapping-to-frame on the timeline
    - Enable by using the magnet icon at the top right of the timeline
- Added blending to the Transform node
- Added gizmos to various nodes for more control in the viewport
- Improved default rendering which now uses bilinear filtering
    - The bicubic sharpening option can be used to revert back to legacy high quality rendering settings
- Improved preview rendering and basic raymarching
	- Added a convolution pass to the atmosphere LUT
- Improved line rendering across the entire UI
- Improved ground noise on the Heightmap base node
- Improved the quality of smooth min/max blending for Heightmaps
- Improved shadows in both raytraced and pathtraced rendering
- Improved volumetric atmosphere rendering
- Optimized Vornoi noise
- Made internal floating windows resizable from any corner
- Changed parameters in the Directional Mask Blur and Directional Blur nodes to match the Color Blur node
- Fixed bugs related to EXR and RAW imports
- Fixed bugs related to link replacement from reroute nodes
- Fixed previous value sometimes being copied when switching between range sliders
- Fixed scroll wheel not waking application while sleeping from inactivity
- Fixed autokeying on timeline when using the manipulators
- Fixed Soft alpha blending mode
- Fixed incorrect brightness in the last step of pathtracing
- Fixed long submenus sometimes not handling mouse click correctly
- Fixed Rock node and Scatter node scaling with terrain size

# 0.2.1-alpha

- [Breaking] Snow node has been improved and behave less like liquid and more like snow
    - New slop limit parameters added, Snow hardness parameter removed
    - Snow hardness mask intensity parameter added
- Improved fluvial erosion node
    - Humidity limit parameter added. This reduces the erosion where less water is flowing
    - Better filtering when doing particles projection, resulting in smoother, less angular results
    - HQ mode added
    - Jitter added on projection, which can help smoothing too sharp erosion
    - Strength over lifetime curve added
- Ground style added for final preview (Checkerboard, Faded grid and None)
- Flip horizontal & vertical added to model import
- Fractal nodes added (Heightmap, Mask). These nodes are a mixed blend of noise and scatter with much more control

# 0.2.0-alpha

- Check out the new presets!
- [Breaking] The crumbling node was completely rewritten, optimized, and made to be deterministic
    - Proper collisions and stacking parameters were added
- [Breaking change] Improved the behavior of the fluvial mask and filter fluvial erosion
    - Results are now coherent when changing resolution
    - All presets using these should be retuned, because the range of values are quite different now
- Added local extreme parameter on mask cavity, mask curvature, mask occlusion, mask orientation, and mask slope to favor sharper results
- Optimized of all the particle based nodes (crumble, fluvial, crease)
- Improved export UI:
    - Directory, filename, and extension are now all separate fields
    - Text fields support variables
    - "Open Folder" button has been added to open the folder of the export
    - The png bitcount parameter has been updated to be an 8/16 bit selector
    - Nodes can export via the "Export" button in the top right
    - All nodes can be exported at the same time by using the "Export" option in the file menu
    - Selected nodes can be exported at once
- Added the ability to reroute Graph nodes
    - Clicking a link will allow you to insert a "Reroute Node" or normal node
    - "Extract Delete" has been added to allow removal of nodes or reroute nodes without severing the connection
- Added sequence export to all export nodes
- Added a viewport export node
    - This is currently limited to the viewport resolution, but we will implement custom resolutions later
- Fixed edges being improperly exported in textures
- Added toggle for the timeline, mapped by default to Ctrl-Shift-T
- Added a warp modulation parameter to Ridge and Bulge to modulate the intensity according to the alignment of the warp direction with the terrain normal
- Added animation of waves using wave phase
- Added viewport capture to clipboard
    - This is mapped to f12 by default
    - This is not currently supported in Linux builds
- Fixed saving gradients to .png
- Improved export speeds

# 0.1.4-alpha

- Fixed issues when DOF focus distance was zero
- Fixed Heightmap and Mask adjust nodes
    - Offset was applied at the wrong time, and frequencies were sometimes wrong
    - Added minimal mip level parameter
- Fixed proper progression indicator in the viewport
- Fixed bug with Scatter node having a warp node connected
- Fixed hard limit of 128 curves in the graph
- Added double click to preview node / double click on renderer for full render
- Added Mask levels node
- Added the option of mask preview colors in preferences
- Added the option of mask out of bounds stripes in preferences
- Added timeline (no animation export yet)
- Heightmap preview mode is now available for planets and can be configured in preferences
- Fixed Denoise node search bug
- Fixed major flaw in water filter, emission mask was not working
- Fixed emission time logic in snow, sediment and water filters
- Added water filter denoise parameter
- Added shard noise and gabor noise to terrains and planets (height, mask & warp)
- Renamed the Dent node to Warp blur
- Added flow direction and blur mode parameters in warp blur node
- Renamed the Color pin to Vertex color in export mesh node
- Fixed texture not being refreshed before being exported
- Multimask exports now output RGB if no alpha pin is connected when exporting
- Added Mask fluvial node which is particle-based
    - Similar to fluvial erosion, without the erosion
- Disabled the ability to create more than one active Render node
- Fixed a bug when too many gradients were displayed
- Increased the maximum number of allowed gradient presets

# 0.1.3-alpha

- Added the mask transform node
- Renamed the propagation background mask to Source Mask
- Fixed inconsistencies with horizontal and vertical orientation of some textures
- Fixed issue with the snow filter when using a high frequencies mask as active mask
- Fixed issue where position was modified when changing terrain size
- Fixed missing blending mask weight for mask delta, mask height, mask propagation, and mask shape
- Improved rendering performance
- Added viewport quality settings for heightmaps
- Improved water rendering quality
- Added atlas generation in 3D model import node
- Removed the black terrain preview with export nodes
- Changed default values for fade distance in transform nodes
- Changed the order of domain warping and filters in menu
- Roughness now has its own input pin in the renderer node
- Added an option to toggle the temporal antialiasing in the preferences
- Fixed an issue in the PBR shading that was causing bright spots

# 0.1.2-alpha

- [Breaking Change]: Fixed the position of some nodes being influenced by scale
- Fixed the Planet Transform node to correctly use the input mask for blending weight and the output mask to return the area that has been modified by the node
- Fixed the visible seams in cavity, curvature, occlusion and edge detect for planet mode
    - Improved the quality of the masks as well
- Fixed unwanted holes in occlusion masks
- Fixed emissive for planets
- Fixed jagged edges in preview mode rendering for terrains
- Fixed multimask export bug
    - Export nodes are now forced to wait for the input texture to be rebuilt
- The top menu bar in the viewport now allows changing terrain and planet resolution separately
- Added the Modulation mask to the Denoise node
- Added the world partition landscape size mode to texture export nodes
- Improved texture filtering on mask curvature, cavity, occlusion, slope and orientation (bicubic instead of bilinear)
- Improved the quality of the preview rendering for planets
- Added bloom as a rendering post process
- Improved waves rendering on water in terrain mode
- Mask adjust node now behaves like the height adjust node

# 0.1.1-alpha

- Fixed issues with AMD GPUs related to Rocks, Scatter and Crumbling filter nodes
- Added a water toggle option when previewing node
    - ctrl+shift+w by default
- Changed the default preview mode for heightmap to monochrome instead of rainbow
- Removed `Import...` and `Export...` from the main menu as they were not used
- Set the default shadows quality to High
- Improved parameter naming in warp noise and warp shapes

# 0.1.0-alpha

This is the initial alpha release of GeoGen. Release notes will contain the list of all fixes and new features that we will implement from now on.

Have fun!

- Fully featured node-graph based procedural generation
- Powerful mask based system for absolute control
    - Masks based on Height, Curvature, Occlusion, Slope, Shadow, etc.
    - Familiar blend operations to leverage the strength of masks
    - Easy chaining of mask nodes
- Broad range of Heightmap operators such as Terrace, Faulting, Craters, Crystallizer, Ridge & Buldge, etc.
- Advanced erosion filters
    - Grid based and particle based
    - Work in multiple resolutions at once for finer control
    - Includes mask extraction
- Water, snow, and sediment simulations with advanced level of detail control
- Terrain and Planet generation
    - Terrain up to 8km by 8km, with a texture resolution of up to 8192x8192
    - Planets of arbitrary scale with full atmosphere support
- Intuitive curve and color gradient controls
- Mesh, Heightmap, and Texture Import and Export
- Raymarched, Lightmapped, and Path Traced rendering for both speed and quality
- Robust look-dev renderer
    - Fully simulated atmosphere with parametric controls
    - Clouds, Water, Depth Of Field, Lighting, Atmosphere, and Texture Details
