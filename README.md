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
- [ ] Full 3D written from scratch in GLSL
  - [X] Perspective camera
  - [X] Gouraud shading
  - [X] Oren-Nayar reflectance
  - [X] Distance fog
  - [ ] Bump mapping
- [ ] Chunks and chunk loading
- [ ] Procedural generation
  - [ ] Based on Worley noise
  - [ ] Possible deformation calculated ahead of time
- [ ] A motion planner for flybacks
  - [ ] Based around virtual potential fields
  - [ ] Powered by a reverse-mode autodiff engine
  - [ ] Used by a 5D planner
  - [ ] With a fallback mode for flying out of local minima

# Requirements

The following command installs everything you need (it works on Debian 11):

```sh
python -m pip install numpy glcontext moderngl moderngl_window glfw
```
