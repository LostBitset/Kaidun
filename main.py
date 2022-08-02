# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw
import moderngl

import scenes

def triNormal(tri):
    a1 = tri[3] - tri[0]
    a2 = tri[4] - tri[1]
    a3 = tri[5] - tri[2]
    b1 = tri[6] - tri[0]
    b2 = tri[7] - tri[1]
    b3 = tri[8] - tri[2]
    return (
        (a2*b3) - (a3*b2),
        (a3*b1) - (a1*b3),
        (a1*b2) - (a2*b1),
    )

class GameWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (3840//3, 2160//3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # OpenGL / Shader code
        with open('world_vertex.glsl', 'r') as f:
            vertex_shader = f.read()
        with open('world_fragment.glsl', 'r') as f:
            fragment_shader = f.read()  
        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )
        cube = [
            (0, 0, 0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1, 1, 0),
            (0, 0, 1, 1, 0, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1, 1, 1, 1),

            (0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 0, 1, 1),
            (1, 0, 0, 1, 1, 0, 1, 1, 1), (1, 0, 0, 1, 0, 1, 1, 1, 1),

            (0, 0, 0, 0, 0, 1, 1, 0, 1), (0, 0, 0, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 0, 1, 1, 0, 1, 1, 1),
        ]
        L = []
        for tri in cube:
            normal = triNormal(tri)
            for i in range(0, 9, 3):
                coord = tri[i : i + 3]
                L.extend(coord)
                L.extend(normal)
        self.cube = np.array(L, dtype='f4')
        # OpenGL / Vertex data
        self.vertBuf = self.ctx.buffer(
            np.zeros((216,), dtype='f4')
        )
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vertBuf, '3f 3f', 'vert', 'aux_surf_normal')
            ]
        )
        # Camera
        self.cam_ctr = (0.0, 1.0, -2.0)
        self.d_cam_ctr = (0.0, 0.0, 0.0)
        self.cam_rot = (0.0, 0.0, 0.0) # (yaw, pitch, roll)
        self.d_cam_rot = (0.0, 0.0, 0.0)
        self.prog['cam_near'].value = 1.0
        self.prog['cam_dist'].value = 50.0
        # Lighting
        self.light_ctr = (2.0, 2.0, 2.0)
        self.brightness = 3.0
        self.d_brightness = 0.0
        self.prog['lighting_ambient'].value = 0.2
        self.prog['lighting_maxsc'].value = 1.15
        # Lighting / Surface info
        self.prog['surf_albedo'].value = 0.09
        # Event handlers
        self.handlers = {
            'keypress': {},
            'keyrelease': {},
        }
        # Event handlers / Keyboard / Movement
        tspeed, rspeed = 0.1, 0.03
        movement = {
            'w':        (0, 0, +tspeed, 0, 0, 0),
            'a':        (+tspeed, 0, 0, 0, 0, 0),
            's':        (0, 0, -tspeed, 0, 0, 0),
            'd':        (-tspeed, 0, 0, 0, 0, 0),
            'e':        (0, +tspeed, 0, 0, 0, 0),
            'c':        (0, -tspeed, 0, 0, 0, 0),
            'up':       (0, 0, 0, +rspeed, 0, 0),
            'down':     (0, 0, 0, -rspeed, 0, 0),
            'left':     (0, 0, 0, 0, +rspeed, 0),
            'right':    (0, 0, 0, 0, -rspeed, 0),
            'o':        (0, 0, 0, 0, 0, +rspeed),
            'p':        (0, 0, 0, 0, 0, -rspeed),
        }
        movementOnKeypress, movementOnKeyrelease = {}, {}
        def moveOnKeypress(*args):
            return lambda: \
                self.updateCameraMove(*[
                    float(i) \
                        for i in args
                ])
        def moveOnKeyrelease(*args):
            return lambda: \
                self.updateCameraMove(*[
                    (0.0 if i == 0 else None) \
                        for i in args
                ])
        for k, args in movement.items():
            movementOnKeypress[k] = moveOnKeypress(*args)
            movementOnKeyrelease[k] = moveOnKeyrelease(*args)
        # Event handlers / Keyboard
        keypress = {
            **movementOnKeypress,
            'l': lambda: \
                setattr(self, 'd_brightness', +1.0),
            'k': lambda: \
                setattr(self, 'd_brightness', -1.0),
        }
        keyrelease = {
            **movementOnKeyrelease,
            'l': lambda: \
                setattr(self, 'd_brightness', 0.0),
            'k': lambda: \
                setattr(self, 'd_brightness', 0.0),
        }
        for k, v in keypress.items():
            key = getattr(self.wnd.keys, k.upper())
            self.handlers['keypress'][key] = v
        for k, v in keyrelease.items():
            key = getattr(self.wnd.keys, k.upper())
            self.handlers['keyrelease'][key] = v
    
    def render(self, *_):
        self.setupShaderInvocation()
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.vao.render()
        self.frame()

    def key_event(self, key, action, _):
        if action == self.wnd.keys.ACTION_PRESS:
            handler = 'keypress'
        elif action == self.wnd.keys.ACTION_RELEASE:
            handler = 'keyrelease'
        self.handlers[handler].get(key, lambda: None)()

    def setupShaderInvocation(self):
        self.vertBuf.write(self.cube)
        self.prog['cam_ctr'].value = self.cam_ctr
        (
            self.prog['cam_yaw'].value,
            self.prog['cam_pitch'].value,
            self.prog['cam_roll'].value,
        ) = \
            self.cam_rot
        self.prog['lighting_light_ctr'].value = self.light_ctr
        self.prog['lighting_light_brightness'].value = self.brightness

    def frame(self):
        self.cam_ctr = (
            self.cam_ctr[0] + self.d_cam_ctr[0],
            self.cam_ctr[1] + self.d_cam_ctr[1],
            self.cam_ctr[2] + self.d_cam_ctr[2],
        )
        self.cam_rot = (
            self.cam_rot[0] + self.d_cam_rot[0],
            self.cam_rot[1] + self.d_cam_rot[1],
            self.cam_rot[2] + self.d_cam_rot[2],
        )
        self.light_ctr = self.cam_ctr
        self.brightness += self.d_brightness
    
    def updateCameraMove(self, x, y, z, a, b, c):
        self.d_cam_ctr = (
            (self.d_cam_ctr[0] + x) if x != None else 0.0,
            (self.d_cam_ctr[1] + y) if y != None else 0.0,
            (self.d_cam_ctr[2] + z) if z != None else 0.0,
        )
        self.d_cam_rot = (
            (self.d_cam_rot[0] + a) if a != None else 0.0,
            (self.d_cam_rot[1] + b) if b != None else 0.0,
            (self.d_cam_rot[2] + c) if c != None else 0.0,
        )

mglw.run_window_config(GameWindow)
