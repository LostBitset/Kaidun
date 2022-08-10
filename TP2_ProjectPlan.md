# Project Plan (as of TP2)

## Original Project Plan

#### Project Description

The project will be a 3D adventure game that takes place on a faraway desolate planet where you try to explore as much of the world as possible, while avoiding avalanches and asteroid strikes. 

#### Structual Plan

The `Scene` class stored as `app.scene` handles events, draws extra stuff in `redrawAll`, and returns a list of geometry to render. Geometry that has been defined as `Geom` objects can be assigned lighting algorithms by passing it into `@diffuseShadingAlgorithm` functions, which return a new `Geom` object. Functions decorated with `@renderer` turn `Geom` objects into `(renderer, geometry)` tuples. A function that takes `app` and returns `(renderer, geometry)` pairs is known as a geomsrc.

A `Viewport` actually renders the `Scene`, and it contains lights, a camera, and a geomsrc. This is called in `redrawAll`.

The `Scene` classes that are being used can be found in `scenes.py`, helper functions they use are `scene_components.py`, and geometries used are in `scene_geometry.py`. This pattern is mirrored for `generation.py`, which handles world generation. 

#### Algorithmic Plan

The perspective camera model is used, and coordinates are converted into homogenous form, passed into a matrix, and then converted back into 2D coordinates. Screen-space coordinates are found at the last minute, when the flat shading function is called. 

All triangles are drawn in order, sorted by the distance between the camera and their centroids (aka the Painter's algorithm). The image plane is calculated in terms of a point and a normal vector, and only triangles with vertices on the front side of the image plane are rendered. 

For lighting, lights are stored as a property of `Viewport` objects, and passed into the appropriate lighting function by the flat shading function. The Lambertian reflectance model is used.

Most of the complexity of this project can be found in the 3D renderer.

#### Version Control Plan

Everything is stored on GitHub, and this codebase can be found [here](https://github.com/HktOverload/Garbage3D).

## TP2 Update

#### Structural Plan Update

A new (similar, and very MVP-like) design pattern has been used for the OpenGL version that is currently being used. There are still `Scene` classes that play the same role they did previously, but scene controllers are now implemented using the mixin system defined in `mix.py`. 

Files and what they do:
- `cpu_geom.py`: Geometry stored on the CPU
- `cpu_geom_utils.py`: Helper functions that involve geometry and don't involve the GPU
- `cpu_linalg.py`: A simple linear algebra system
- `events.py`: A class representing `moderngl` events, which for now are only keypresses
- `graphs.py`: Graphs and special functions for nodes that exist in 2D space
- `main.py`: The `cmu_112_graphics`-based entry point
- `mglw_main.py`: Where the actual interaction with `moderngl` and `moderngl_window` is done
- `mix.py`: The mixin-like system used for extensible scene controllers
- `mix.test.py`: A simple test for `mix.py`
- `scene_controllers.py`: All of the scene controllers, which act every frame, handle events, and update OpenGL uniforms
- `scene_groups.py`: A simple mechanism to combine scenes
- `scenes.py`: Scenes, and where they are all defined
- `splash.png`: An image I made that's used as the splash screen
- `terrain.py`: Generation of the terrain
- `terrain_graphs.py`: The network of mountains is represented as a graph, and these functions deal with that
- `terrain_graphs.vtest.py`: A handy test that shows some functions in `terrain_graphs.py` working so I can sanity check them
- `vbo_utils.py`: A wrapper class that adds an extra layer of indirection to accessing OpenGL vertex buffers, and reallocates them when necessary
- `world.glsl.vert`: The OpenGL vertex shader that runs on the GPU and operates on each vertex
- `world.glsl.frag`: The OpenGL fragment shader that runs on the GPU and operates on each pixel (mostly)

#### Algorithmic Plan Update

Adjustments to algorithmic components that already existed:
- The new 3D system has the following components:
  - A simple 3D engine
    - Invokes ModernGL (an OpenGL interface) from `cmu_112_graphics`
    - Scenes that define geometry and when to update it
    - Controllers to handle events and shader code setup
    - Automatic reallocation of GPU vertex buffer when tri count changes
    - Full 3D written from scratch in GLSL
        - Perspective camera implemented from scratch
        - Lambertian component (Phong shading) 
        - Oren-Nayar reflectance (Gouraud shading)
        - Distance fog (calculated per-pixel using the z-buffer)
        - Bump mapping (finite-difference method)
        - Procedural heightmaps for terrain surfaces
- OpenGL allowed me to switch from the Painter's algorithm to the less complex but more efficient z-buffering method

New algorithmic components:
- Gravity and jumping
- The heightmap is based on the minimum distance to a mountain edge
- The structure of mountains you traverse is represented as a planar graph, and various properties need to be checked to ensure that it works in the context of the game
  - The heightmap must be evaluated at the minimum point, which is the incenter in this case
  - The two possibilities to switch to must be on different sides of the initial side
