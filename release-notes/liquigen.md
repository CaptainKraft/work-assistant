# 1.0.6

- Fixed occasional garbage in path tracer output
- Made PT geometry twice as much memory-efficient and faster to reallocate
- Improved UI's string truncation to truncate in the middle instead of the end -- this should improve the readability of long file path
- Added support for zooming individual axis on Node Detail's curve editor
- Added sliders on context menu for Node Detail's curve editor keys
- Improved `Frequency` parameter on modulator nodes
    - Divisions of the loop region, frames and seconds are now supported as units for this parameter
- Fixed issue of application not entering power saving mode when task manager was open
- Made `Node Details` panel content resize dynamically based on panel width
- Fixed some elements overlapping when panels were made very narrow
- Changed the default camera to be a normal node on the node graph
- Fixed bug when `Ctrl+Click`ing to select two nodes on the node graph
- Changed export preview to play by default
- Added splashscreen on Windows and Linux
- Improved auto-scrolling when dragging off the edge of a panel (eg. when selecting nodes)
- Added timeline lane visibility "unsolo" support when shift-clicking a solo'd lane
- Fix using animated imports as transforms on Alembic exports
- Support using primitive shapes as transforms for exports
- Made "NEW" badge show on What's New section of homescreen when there are changes
- Add tonemapping options
- Made Ctrl+N and Ctrl+O for new / open project work on homescreen
- Fix missing extension when saving project file on Linux

# 1.0.5

## Fixes
- Fixed a licensing bug that was preventing some users from activating their license

# 1.0.4

## New Additions
- Added normal map export pass
- Added "Absolute Frames" in "Export Image". This makes the frame count start from the "absolute" frame count seen in the timeline rather than 0
- Added "UI Brightness" setting to preferences
- Added viewport resolution to stats
- Added support for out-of-bound values from modulator output preview
- Added target engine option for VAT exports

## Improvements
- Improved path tracer performance for large scenes
- Improved SDF generation for meshes with planar sides
- Made content of group show in node menu if only one group is present

## Changes
- Changed the default filename for "Export Particles" and "Export Mesh" nodes
- Updated UI layout when searching node menu
- VAT exports use FBX or glTF formats depending on target engine.

## Fixes
- Fixed an issue with inverted colliders being hollow when using imported meshes
- Fixed flickering shadows in the rasterizer
- Fixed wrong emissive material indexing in the path tracer
- Fixed erroneous context menu on gradient preset browser special categories
- Fixed how strict camera bindings were
    - It's now possible to remain in a camera mode (Pan, Orbit, etc) after pressing the necessary input, and then releasing all keys
- Fixed a bug where camera modifiers (Shift for fine-tuning, QE/WASD/Arrows for flying) would incorrectly trigger a binding
- Fixed clicking off textbox on Node Details panel sometimes not registering the new value
- Fixed a memory leak related to exporting
- Fixed an issue with missing images from an export
- Fixed an issue with "Simulation Preemption" under "Preferences" which should improve UI responsiveness
- Fixed rare bug where exiting textbox state might have resulted in a crash
- Fixed an issue where "Freeze Simulation" would prevent cameras and other animated imports from animating
- Fixed an issue where otherwise empty models containing animated cameras wouldn't work
- Fixed some issues with VAT exports.
- Fixed wrong transform on VDB exports

# 1.0.3

## New Additions
- Added `Shift+D` shortcut to toggle diagnostics panel
- Mesh Flipbooks now export metadata in a JSON file

## Improvements
- Improved clarity of several tooltips in the Render and Export Image nodes
- Improved error messages on `Export: Image` node's camera selector
- Improved UI of Force Masks parameters

## Changes
- Made shortcut key name in preferences expand when resizing window and added tooltip
- The noise viewer in the Force Noise Node is now affected by the rotation parameter
- Removed Inherit Sun Color from the Light: Directional node
- Removed Falloff from the Light: Directional node

## Fixes
- Fixed accumulation not accumulation for sample 2
- Fixed black pixels appearing in the viewport
- Fixed a crash caused by exporting a capture type that doesn't output anything on its own, but receives inputs
- Fixed integer values sometimes showing as different when multi-editing nodes
- Fixed default number of samples of Export Image node

# 1.0.2

## New Additions
- Added support for dropping multiple files onto the node graph
- Added copy + paste support to curves and gradients
- Added many tooltips for Camera Preferences

## Changes
- Removed "WASD Fly Plane" settings for each camera operation
    - "Fly Plane" can still be set for the "Fly" and "Pan" modes
- Renamed "Camera Rotate" to "Orbit"
- Renamed "Camera Rotate First Person" to "Fly"

## Fixes
- Fixed a bug preventing presets from being launched on the home page
- Fixed issues with UI animation being dependant on framerate
- Fixed "Show" attribute in Shape forces not hiding imported meshes when disabled
- Fixed "Show Masks" not showing masks when enabled
- Fixed crash on VDB exports
- Fixed wrong frame rate when exporting Alembic with compensation enabled
- Fixed invalid particles showing outside the world domain

# 1.0.1

- Fixed path tracer sometimes not correctly finishing rendering with preemption on
- Fixed a bug causing a black screen on startup and other rendering issues

# 1.0.0

LiquiGen is now production ready and has gained substantial improvements to both usability and stability. The core simulator has gained per-emitter viscosity which was highly requested. We have added new export types such as mesh flipbooks and VAT's for games, as well as the ability to export liquid thickness maps. The camera system has changed to mimic industry standard control schemes and we've added useful tools such as solver tuners and a very helpful simulation diagnostics panel.

## Added
- Added a new camera control system, primarily controlled by pressing `alt`, with features such as zoom to cursor and pan around cursor: This was done to prevent gizmos interaction from affecting camera positioning
- Added high viscosity solver support: Coiling, buckling and more are now supported
- Added support for exporting Vertex Animated Textures (VAT)
- Added support for exporting mesh flipbook: This allows you to export a single FBX file with all frames packed into it and separated by vertex color
- Added a new material system which supports more realistic material profiles for liquids and surfaces: We currently have a few presets such as water, iron, gold, copper, plastic and so on.
- Added more rasterized export passes (Thickness, Diffuse, Reflection, Refraction)
- Added `Models > Show SDF` to diagnostics panel: This helps diagnose issues with imported models and with choosing a good voxel resolution
- Added higher quality meshing that can be enabled via a checkbox in the `simulation node`
- Added isotropic and anisotropic kernel modes: Think of these as spherical particles vs elongated particles
- Added morphological operators for high quality meshing (dilate, erode, open, close)
- Added SDF smoothing
- Added normals smoothing
- Added a `Diagnostics Panel` to visualize simulation data (sim domain, force fields, velocity fields, liquid mesh and particles): Can be found by clicking the `water droplets icon` at the top right of the viewport.
- Added support for using `Ctrl+C` to copy dialog box messages to clipboard
- Added support for searching in dropdown menus
- Added default shortcut key `H` for creating a notes in the node graph
- Added Step Back Once button to timeline (note: this steps back the timeline for animation previews and not the simulation)
- Added support for importing animated cameras
- Added per emitter stickiness: Stickiness is now defined in the emitter vs simulation node
- Added new options to allow for different levels of simulation accuracy
- Added the ability to export velocity fields to VDB format
- Added decay to whitewater bubbles
- Added a splash screen to startup
- Added `Shift + RMB` to pan to help laptop users as a secondary binding
- Added the ability to trigger a `Fill just once` emitter multiple times by unchecking and checking the `Emitter activity` parameter
- Added a repeat-frames marker to timeline when `Reset Simulation` is enabled for feature parity compared to EmberGen.
- Added a tooltip when hovering over the `Export Now` button

## Improved
- Improved bounding box granularity
- Improved interactions with smaller liquids: For things like surface tension and viscosity to work without using extremely large values, you will need to use real scales such as 0.01 voxel size. LiquiGen now excels at small, medium, and large simulations
- Improved when white water particles spawn: You used to have to input a shape for white water particles to spawn from and now you only need to add a shape if you want to limit their spawn area. By default you only need to add a white water emitter and that is enough to have white water particles spawn within your entire simulation
- Improved visualization of the "Drag Force" in the diagnostics panel
- Improved normalization and scaling of arrows in the diagnostics "Velocity" and "Force" visualizer
- Improved memory management
- Improved many tooltip descriptions
- Improved liquid's boundary conditions
- Improved reflectivity is now defined by F0+F90, metalness has departed the building due to the new material system mentioned above
- Improved naming of the "Projection" tab to "Pressure" in the simulation node
- Improved consistency of `max number of whitewater particles` parameter location from `whitewater node` to `simulation node`
- Improved how the virtual domain bounding box is rendered
- Improved Export passes so that "Alpha", "Depth" and "Normals" now export using the rasterizer instead of the path tracer
- Improved default values for some force nodes
- Improved path tracing denoiser
- Improved how key bindings can be made on Mac & Linux
- Improved how HDRI's load: If the HDRI is still loading we will fall back to atmospheric rendering temporarily
- Improved Warnings so that if you click them, it will now take you to the parameter that's causing concern
- Improved the interaction between changing things such as voxel size and ensuring that the simulation automatically resets upon application of new values

## Fixed
- Fixed the ground plane showing up in all render passes, now its only shown in the "Render Viewport" render pass (including the viewport itself)
- Fixed an issue where an imported mesh would cause liquids to explode when moving
- Fixed an issue where there was no liquid emission from an animated alembic file while `animate` was unchecked in the `import` node
- Fixed issues where the camera node's near and far planes where never used: Note that with perspective projection only the near plane is used, but with orthographic projection both near and far planes are used
- Fixed issue with stationary meshes having non-zero velocities for high timerates / substeps
- Fixed a bug where the camera node's "Display Dimensions" was being ignored when exporting, resulting it the "Preview" tab not matching the actual exported view: This also allows varying source aspect ratios to be scaled/stretched to any other arbitrary destination aspect ratio while exporting by using the "Display Resolution" to set the aspect ratio
- Fixed timeline region length
- Fixed a bug where two forces with the same name could not be selected in the diagnostics panel
- Fixed a bug where high velocities would cause the "Value" color scheme in the diagnostics panel to go out of range
- Fixed a bug with continuous emitters not working properly with high flow rates
- Fixed a bug with emitters not working properly when substepping
- Fixed a bug where being in the Export tab would likely delay loading a project until switching to the Scene tab or Preview tabs
- Fixed a bug with velocity transfer being affected by disabled modulators
- Fixed parameter override cycler showing while multi-editing on non-overridable parameters
- Fixed memory leaks in the export process, exports now use significantly less memory
- Fixed animation not updating on substeps
- Fixed an issue where point lights and area lights combined would cause rendering issues
- Fixed liquid explosions when using `ctrl-Z` to undo parameter changes
- Fixed a memory leak in the camera node

## Removed
- Removed unimplemented options from the View Menu (show entity icons, show masking)
- Removed "Enforce particles distance" option from Simulation node, since it was always needed when compensating compression / decompression.
- Removed collider's velocity transfer: Use force drag to slow down collisions if needed, and emitters still have the ability to transfer velocity
- Removed an unused `Reflective Ground` parameter

# 0.3.2-alpha

- Fixed a bug causing a crash for certain exports
- Fixed some timeline interactions not updating parameter values
- Added the "Units" type to the Ground node

# 0.3.1-alpha

### Import/Export
- Export writing speeds have been greatly improved
- Added "compensate framerate" option to Export Mesh node. This option lowers the framerate of the export to compensate for the frame stride
- Changed export preview to use linear sampling
- Increased the memory limit for the local SDF for imported meshes

### Simulation and Rendering
- Improved collisions with the ground
- Improved solver so that whitewater has less of an impact in simulation times when far from the main liquid
- Improved path tracing + photon mapping performance and their denoising

### UI/UX
- Improved error message when the maximum amount of unique meshes/masks linked to forces is reached
- Added warning message when the liquid reaches the bounds of the virtual domain
- Several whitewater UX changes
  - Whitewater Emitters are now called Whitewater Sources. If they are not masked they act globally. But:
  - Whitewater node defines a global source already, so for most scenarios it's the only node needed to have whitewater
  - Whitewater can now use the same drains as the main liquid's simulation but also its own
- Improved UI responsiveness when rendering more complex scenes
- Removed unused parameters from Ground node
- User interface color updates
- Changed asset paths to work relative to the current project
- Added dialog box listing errors if there were problems loading a project
- Moved the "Show" found on various nodes to the bottom of their respective tab sections
- Added "Shapes" toggle to the View dropdown, which can hide or show all shapes with one click
- Shape visibility now works the same way as it does in EmberGen: as long as a shape is connected, the connected node has "Show" enabled, and the "Shapes" toggle in View is enabled then the shape will be shown
- Removed "All input shapes when paused" toggle from the View dropdown
- Added `Import...` option to file menu
- Made preferences and project settings searchable
- Updated `Oscillator` node's curve editor when using custom waveform
- Made license key hidden-by-default on licence manager
- Added copy+paste support for color-gradient handles
- Added "copy" button next to color picker's HEX value
- Added `Numbering offset` parameter to export nodes

### Bugfixes
- Fixed file dialogs for Linux users
- Fixed an issue where attempting to export without a Skybox node would result in an error message "Could not set renderer input"
- Fixed an issue where deleting the Sky node, or disabling the current HDRI wouldn't actually make the sky dark
- Fixed error dialog not showing when loading project fails
- Fixed bug which may have caused a changed backplate not to be reloaded
- Fixed drag+drop of camera backplates onto graph and viewport
- Fixed crash relating to using an invalid path for the backplates
- Fixed "Node Details" panel drag handle not working when not on the first tab
- Fixed an issue where Voxel Size, Substeps and Timestep were being updated in the simulation internally regardless of clicking the "Apply" button
- Fixed issue with HDRI file dropped on skybox node not being accepted
- Fixed `Export: Image` node initialising with frame values of -NaN
- Fixed project initializing in dirty state
- Fixed undo/redo not settings parameters controlled by modulators while paused
- Fixed bug which caused node graph tree-view to disappear when dragged too far to the right
- Fixed bug which prevented dialog provider changes to be saved

# 0.3.0-alpha

- WARNING: due to significant changes in this release, presets from previous versions are not guaranteed to work

### Simulation
- The simulation solver has gone through a complete overhaul, and that comes with tons of major improvements! Here's an overview of what you can expect:
  - Surface tension
  - Whitewater Node
    - Three types of whitewater particles
      - Spray, which falls down from the liquid
      - Foam, which follows the liquid surface movements
      - Bubbles, which rise to the surface of the liquid
    - Emitter: Whitewater nodes can be used to emit whitewater based on different criteria
    - Force Nodes can be connected to apply forces only to whitewater particles
  - Whitewater View Options
    - Wave crest, this displays the wave crests of the liquid where whitewater particle will spawn if enabled
    - Trapped air, this displays the regions where air is getting trapped by the liquid whitewater particle will spawn if enabled
  - Moved from APIC to a PIC/FLIP solver
  - Volume conservation improvements[, especially when using compensation]
  - Projection improvements to create a smoother liquid surface [(specially when mesh isovalue >= 0.3)]
  - Improvements to the spatial accuracy of the emission
- Improved sticky boundary conditions with rotating geometry [(a bit. It's still not great)]
- Increased the maximum number of particles supported
- There are now four possible export options in the Particles Export node: liquid, foam, spray, and bubble
- Removed "Redistribute tight particles" from Simulation Node
- Force nodes have gone through several changes and additions, here's an overview of what you can expect:
  - Added a line force node, affecting both the simulation and whitewater
  - Added a toroidal force node, affecting both the simulation and whitewater
  - Turbulence node was reworked, params and inner workings are now similar to Embergen's noise node
  - Added noise preview to the turbulence node
  - Improved shape forces with imported meshes
  - Fixed some crashes resulting from interations between import nodes and force masks pins
- Added lifetime to particles
- Added the "target divergence" option to the projection
  - The solver will now adapt to achieve a given "quality" instead of running the same number of iterations all the time

### Rendering
- Improved rasterized directional light's shadowmap range
- Added refraction for liquids and geometry when using rasterized rendering
- Added liquid transmission color when using rasterized rendering
- Pathtracing now respects inverted shapes
- Pathtraced materials now have an emissive property, so any geometry can be a light source (even the liquid)
- Pathtraced point lights can now have a radius (they become a sphere light with a nonzero radius)
- All color inputs are now gamma-correct
- Allow coloring particles by attribute

### UI/UX
- Added gizmo/parameter live-recording to timeline (Shift+R)
- Added support for snapping-to-frame on the timeline
  - Enable by using the "magnet" icon at the top right of the timeline
- Made internal floating windows resizable from any corner
- Improved line rendering across the entire UI
- Improved the stats in the viewport with more relevant information
- Split and renamed Divergence Control into "Compensante compression" and "Compensate decompression"
- Added shortcut to randomize parameters (Ctrl+Alt+R)
- Added shortcut to show liquid simulation tiles (Alt+B)
- Added shortcut to show liquid simulation bounding box (B)
- Fixed long submenus sometimes not handling mouse click correctly

### Bugfixes
- Fixed volumetric emitters always generating zero velocity on the interior when used with imported meshes
- Fixed volumetric emitters always resetting interior velocities
- Fixed several bugs related to performance
- Fixed issues with velocity transfer of imported meshes
- Fixed vertex winding order for alembic imports
- Fixed issues with the transfer of collider velocities to the liquid
- Fixed issues with isolated droplets being removed
- Fixed important issues with the liquid-air interface
- Fixed collisions adding energy into the system
- Fixed a bug related to velocity transfer for imported meshes
- Fixed a window maximizing bug on Linux
- Fixed an issue where 'View -> Bounds' (B) didn't do anything
- Fixed an issue where in "Whitewater - Trapped Air" or "Whitewater - Wave crests" viewing modes, the liquid would be rendered with refraction even though it inhibited the usability of these modes

# 0.2.1-pre-alpha

- Added ability to export transforms applied to import nodes in Alembic caches
- Added ability to select a list of meshes from an import node
- Added ability to select a list of meshes or bones to act as a mask on an import node
- Added warning when drains are removing newly created particles
- Added support for exporting default camera using `Export: Image` node
- Improved mesh import performance
- Moved New Project and Open Project to the top-left of the Home screen
- Embedded "Appearance" parameters directly on nodes
- Made it possible to delete all image dimension presets
- Updated graph to move camera inputs from `Export: Image` to `Scene`
- Fixed scroll wheel not waking application while sleeping from inactivity
- Fixed a bug causing LiquiGen to crash when enabling path tracing
- Fixed previous value sometimes being copied when switching between range sliders
- Re-enable backplates
- Fixed skybox node toggling
- Fixed various mesh import bugs

# 0.2.0-pre-alpha

- Added support for exporting velocity on mesh vertices and added a frame stride option
- Added the Relative Resolution parameter for imported models
- The Scene and Render tabs should now look the same
- Fixed the units of particle velocities to be in physical units rather than grid units
- Fixed artifacts showing up when pathtracing that would show up under certain circumstances
- Fixed velocity transfer for imports
- Fixed some crashes when switching between projects on Windows
- Fixed some crashes for AMD GPU users
- Fixed a bug that caused exports to continue when they should have stopped after running out of resources
- Fixed a bug causing a crash when deleting the Simulation node
- Fixed a bug causing user-defined resource limits to be ignored
- Fixed various memory leaks
- Improved and fixed a bug related to powersaving
- Removed the "Preview" section from the Camera node since you can preview the camera in the Render tab
- Reordered some parameters for more continuity
- Hid backplates in the Render node until they are fully implemented
- Reduced some explosiveness related to imported meshes

# 0.1.0-pre-alpha

LiquiGen pre-alpha has been released!
This is a closed alpha and the first version of LiquiGen publicly available.

## Features
- Real-time sparse liquid solver (Pseudo-Boundless APIC)
- Rasterized renderer for fast previz
- Pathtraced renderer for high quality renders
  - Rudimentary material system
- Real-time liquid meshing
  - Alembic exports
  - Particle exports
- Animated mesh support for colliders and emitters
- Forces: Constant, Shape, Turbulence, Drag
- Lighting: HDRI, Directional, Area, Point

## Known issues
- Enabling the path tracer with more than 30M triangles can lead to a crash
- Resizing the viewport too small or exporting too small of a texture can lead to corrupted textures
- Loading a preset directly can sometimes result in a completely black viewport. This can be fixed by loading the default preset first
- Path tracing is broken on AMD GPUs on Linux
- Path tracing can make Linux desktops unresponsive

## Known limitations
- Currently the previz renderer has no transparency (so it ignores Appearance properties about it)
- Only 8 meshes can be imported at this time
- Only "very well-behaved" meshes are likely to work (in particular they need to be watertight manifolds)
- Drains can be shapes but not imported meshes (yet)
- Intel GPUs are unsupported

## Upcoming features
- Better projection (should improve the surface of the fluid among other things)
- Surface tension
- Foam, spray and bubbles
- Meshing at a higher resolution
- Mask based emission from meshes
- Subsurface scattering for pathtraced materials (milk/blood/goo)
- True viscosity
- More simulation
