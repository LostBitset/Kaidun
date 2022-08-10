# Kaidun
A 3D game made in Python with moderngl

## Gameplay

> All you know is that you were placed into cryopreservation against your own will,
> that this planet was once a thriving metropolis instead of a hostile wasteland,
> and of course, that you're awake now.

- [ ] You're on a strange alien planet, with a complex network of interconnected mountains and flat valleys
- [ ] The valleys are deep caverns that are practically impossible to escape from
- [ ] You traverse the mountains (you can choose which path to take at forks)
- [ ] Some ground is weak, you can tell based on how light the color of the soil is
- [ ] Only reddish ground is perfectly safe, for everything else, avalanches are possible
- [ ] These will send you tumbling into a deadly valley
- [ ] When this happens, your space suit will use the last of its power to keep you alive
- [ ] There isn't quite enough power for magic shields and remembering your recent progress, so you'll have to try again
- [ ] Or you can just move on if you want, it's up to you, you can even come back later

In other words, "What if temple run was a soulslike on a desolate alien planet?".

## Complexity
- [X] A simple 3D engine
    - [X] Invokes ModernGL (an OpenGL interface) from `cmu_112_graphics`
    - [X] Scenes that define geometry and when to update it
    - [X] Controllers to handle events and shader code setup
    - [X] Automatic reallocation of GPU vertex buffer when tri count changes
    - [X] Full 3D written from scratch in GLSL
        - [X] Perspective camera implemented from scratch
        - [X] Lambertian component (Phong shading) 
        - [X] Oren-Nayar reflectance (Gouraud shading)
        - [X] Distance fog (calculated per-pixel using the z-buffer)
        - [X] Bump mapping (finite-difference method)
        - [X] Procedural heightmaps for terrain surfaces
    - [X] Simple physics so you don't fall through the floor
- [ ] Procedural terrain generation
    - [ ] Heightmaps based on Worley noise
- [ ] Mostly realistic avalanches
    - [ ] Deformation of existing terrain
    - [ ] Persistence of terrain modification (deltas stored in save data)

## Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window 
```

## Partial to-do list

- [ ] Make a `Graph` class
- [ ] Get follow to work along an edge
- [ ] Get switching to work
- [ ] Generate Delaunay triangulation

