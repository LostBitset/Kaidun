# Kaidun
A 3D game made in Python with moderngl

# Gameplay

- You're on a strange alien planet, with a complex network of interconnected mountains and flat valleys
- Your goal is to cover as much ground as you can, in order to collect data about this mysterious world
- You have to stay on top of the mountains, but there are "weak sites" that will cause you to fall into the valley
- If you fall into the valley, the toxic gases begin harming your EVA suit, but you can't just run back up
- These flat valleys, known as "islands" have stealth mechanics, and will fall down if you move too suddenly
- Islands also just fall randomly, and your emergency jetpacks will fly you back to your ship
- These "flybacks" use buckets of power, and some samples will be irreperably damaged

# Complexity
- [ ] A simple 3D engine
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
        - [X] Procedural heightmaps for terrain surfaces *need to fix rotation artifact*
    - [ ] Simple physics so you don't fall through the floor
- [ ] Procedural terrain generation
    - [ ] Terrain heightmaps based on Worley noise
    - [ ] Automated classification of terrain features
    - [ ] Automated classification of potential avalanche sites
- [ ] Mostly realistic avalanches
    - [ ] Deformation of existing terrain
    - [ ] Persistence of terrain modification (deltas stored in save data)
- [ ] A motion planner for flybacks
  - [ ] Based around virtual potential fields
  - [ ] Powered by a reverse-mode autodiff engine
  - [ ] With a fallback mode for flying out of local minima

# Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window 
```
