# Kaidun
A 3D game made in Python with moderngl

## Gameplay

The game mechanics are inspired by Temple Run. In this version you fly over
desert mountains on an alien planet, and try to collect artifacts without
failing checkpoints.

## Complexity
- [X] A simple 3D engine
    - [X] Invokes ModernGL (an OpenGL interface) from `cmu_112_graphics`
    - [X] Scenes that define geometry and when to update it
    - [X] Controllers to handle events and shader code setup
    - [X] Automatic reallocation of GPU vertex buffer when necessary
    - [X] Full 3D written from scratch in GLSL
        - [X] Perspective camera implemented from scratch
        - [X] Lambertian component (Phong shading) 
        - [X] Oren-Nayar reflectance (Gouraud shading)
        - [X] Distance fog (calculated per-pixel using the z-buffer)
        - [X] Bump mapping (finite-difference method)
        - [X] Procedural heightmaps for terrain surfaces
    - [X] Simple physics so you don't fall through the floor
    - [X] Terrain organized into chunks, and generated from a heightmap
    - [X] A chunk loading system
- [ ] Following edges of a graph
    - [X] Use t-values to determine position and derive heading
    - [X] Randomly switch to possible new edges at the end
    - [X] Rotation done using a P-controller
    - [ ] Keeps track of how far you've traveled
- [X] Procedural terrain generation
    - [X] Heightmaps derived from a graph where mountains are edges
    - [X] A triangulation data structure
    - [X] Delaunay Triangulation with Bowyer-Watson
    - [X] Finding the incenter using barycentric coordinates
    - [X] Creating a random Delaunay Triangulation
    - [X] Expanding it until all incenters are far enough away from sides
    - [X] Conversion of triangulations into graphs
- [ ] Checkpoints
    - [ ] Detect when checkpoints have been failed
    - [ ] Change color when missed once
    - [ ] If you miss twice, have gravity begin to act
    - [ ] Restart when you fall down

## Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window pyopengltk 
```

