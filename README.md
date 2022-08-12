# Kaidun
A 3D game made in Python with moderngl

## Gameplay in one sentence

What if Temple Run was a flight simulator?

## Gameplay

The game mechanics are inspired by Temple Run. In this version you fly over
desert mountains on an alien planet, and try to travel as far as you can without
failing checkpoints (shown as red triangles). You can use a and d to adjust the
roll of your alien space-plane, and the try to match it with the roll of the
checkpoint marker (the marker should appear as horizontal as possible). If you fail,
the plane starts shaking and crashes. Start and stop by pressing the enter key.

## Running it

- Just run `python main.py`
    - Use the arrow keys to look around
    - Toggle following the mountains with the enter key
- Files ending in `.test.py` are tests
- Files ending in `.vtest.py` are "visual tests" for me to make sure things look right
- Files ending in `.vert` or `.frag` are OpenGL shaders
- The `SAVEFILE.json` file is where your scores are stored (it's not tracked by git)

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
- [X] Following edges of a graph
    - [X] Use t-values to determine position and derive heading
    - [X] Randomly switch to possible new edges at the end
    - [X] Rotation done using a P-controller
    - [X] Keeps track of how far you've traveled
- [X] Procedural terrain generation
    - [X] Heightmaps derived from a graph where mountains are edges
    - [X] A triangulation data structure
    - [X] Delaunay Triangulation with Bowyer-Watson
    - [X] Finding the incenter using barycentric coordinates
    - [X] Creating a random Delaunay Triangulation
    - [X] Expanding it until all incenters are far enough away from sides
    - [X] Conversion of triangulations into graphs
- [X] Checkpoints
    - [X] Generation of checkpoints for each edge
    - [X] Rendered without bump mapping
    - [X] Rotated properly along all three rotation axes
    - [X] Detect when checkpoints have been failed
    - [X] Fall down and start camera shake when you fail
    - [X] Restart when you crash

## Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window pyopengltk pynput
```

Massive credit goes to the library authors for allowing this project to run at more than 2 FPS.

