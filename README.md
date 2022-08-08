# Kaidun
A 3D game made in Python with moderngl

## Gameplay

> All you know is that you were placed into cryopreservation against your own will,
> that this planet was once a thriving metropolis instead of a hostile wasteland,
> and of course, that you're awake now.

- [ ] You're on a strange alien planet, with a complex network of interconnected mountains and flat valleys
- [ ] The valleys are pools of molten rock that regularly self-assembles large rocks that fly up and fall down
- [ ] There are artifacts of the history of this planet scattered about the mountains, and these reveal the story
- [ ] You traverse the mountains, but some ground (lighter-colored ground specifically) is weaker than others
- [ ] Only reddish ground is perfectly safe, for everything else, avalanches are possible
- [ ] These will send you tumbling into a valley, and you land on a currently forming rock
- [ ] You have to get back up before you get involuntarily launched into the atmosphere
- [ ] When this happens, you'll land nearby, but your space suit will use the last of its power to keep you alive
- [ ] There isn't quite enough power for magic shields and remembering your recent progress, so you'll have to try again
- [ ] Or you can just move on if you want, it's up to you, you can even come back later
- [ ] Eventually, you collect an ancient radio transmitter, and massive magnetic fields appear in the upper atmosphere
- [ ] The quasi-meteorites begin targeting you with greater and greater accuracy
- [ ] You're suit still saves you when hit, but large swaths of land will be dropped from memory 

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
- [ ] Mostly realistic avalanches
    - [ ] Deformation of existing terrain
    - [ ] Persistence of terrain modification (deltas stored in save data)

## Interaction

- [X] Switching between `cmu_112_graphics` and `moderngl` windows
- [X] Basic movement
  - [X] Seeing the 3D world
  - [X] Looking around
  - [X] Moving relative to the direction you're facing
- [ ] The interface you see when resting (this uses `cmu_112_graphics`)

## Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window 
```

