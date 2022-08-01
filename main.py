# Kaidun (by HktOverload)

from http.client import MOVED_PERMANENTLY
from turtle import onkey
import numpy as np
import moderngl_window as mglw
import moderngl

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
        L = [
            0, 0, 0, 1, 0, 0, 1, 1, 0,
            0, 0, 0, 0, 1, 0, 1, 1, 0,
            0, 0, 1, 1, 0, 1, 1, 1, 1,
            0, 0, 1, 0, 1, 1, 1, 1, 1,

            0, 0, 0, 0, 1, 0, 0, 1, 1,
            0, 0, 0, 0, 0, 1, 0, 1, 1,
            1, 0, 0, 1, 1, 0, 1, 1, 1,
            1, 0, 0, 1, 0, 1, 1, 1, 1,

            0, 0, 0, 0, 0, 1, 1, 0, 1,
            0, 0, 0, 1, 0, 0, 1, 0, 1,
            0, 1, 0, 0, 1, 1, 1, 1, 1,
            0, 1, 0, 1, 1, 0, 1, 1, 1,
        ]
        # OpenGL / Vertex data
        self.vertBuf = self.ctx.buffer(
            np.array(L, dtype='f4')
        )
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vertBuf, '3f', 'vert')
            ]
        )
        # Camera
        self.cam_ctr = (0.0, 1.0, -2.0)
        self.d_cam_ctr = (0.0, 0.0, 0.0)
        self.cam_rot = (0.0, 0.0, 0.0) # (yaw, pitch, roll)
        self.d_cam_rot = (0.0, 0.0, 0.0)
        self.cam_far = 4.0
        self.cam_near = 1.0
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
        }
        keyrelease = {
            **movementOnKeyrelease,
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
        #self.ctx.depth_func = '<'
        self.vao.render()
        self.frame()

    def key_event(self, key, action, _):
        if action == self.wnd.keys.ACTION_PRESS:
            handler = 'keypress'
        elif action == self.wnd.keys.ACTION_RELEASE:
            handler = 'keyrelease'
        self.handlers[handler].get(key, lambda: None)()

    def setupShaderInvocation(self):
        self.prog['cam_ctr'].value = self.cam_ctr
        (
            self.prog['cam_yaw'].value,
            self.prog['cam_pitch'].value,
            self.prog['cam_roll'].value,
        ) = \
            self.cam_rot

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
