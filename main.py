# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw

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
        # OpenGL / Vertex data
        self.vertBuf = self.ctx.buffer(
            np.array([
                0.2, -0.8, 0.0,
                0.4, 0.9, 0.5,
                -0.5, 0.3, 0.3,
            ], dtype='f4')
        )
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vertBuf, '3f', 'vert')
            ]
        )
        # Camera
        self.cam_ctr = (0.0, 1.0, -2.0)
        self.dcam = (0.0, 0.0, 0.0)
        # Event handlers
        self.handlers = {
            'keypress': {},
            'keyrelease': {},
        }
        # Event handlers / Keyboard
        keypress = {
            'w': lambda: \
                self.updateCameraMove(0.0, 0.0, +0.5),
        }
        keyrelease = {
            'w': lambda: \
                self.updateCameraMove(0.0, 0.0, None),
        }
        for k, v in keypress.items():
            seq = k if isinstance(k, tuple) else (k,)
            for k in seq:
                key = getattr(self.wnd.keys, k.upper())
                self.handlers['keypress'][key] = v
        for k, v in keyrelease.items():
            seq = k if isinstance(k, tuple) else (k,)
            for k in seq:
                key = getattr(self.wnd.keys, k.upper())
                self.handlers['keyrelease'][key] = v
    
    def render(self, *_):
        self.forwardToGPU()
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render()
        self.frame()

    def key_event(self, key, action, _):
        if action == self.wnd.keys.ACTION_PRESS:
            handler = 'keypress'
        elif action == self.wnd.keys.ACTION_RELEASE:
            handler = 'keyrelease'
        self.handlers[handler].get(key, lambda: None)()

    def forwardToGPU(self):
        self.prog['cam_ctr'] = self.cam_ctr

    def frame(self):
        self.cam_ctr = (
            self.cam_ctr[0] + self.dcam[0],
            self.cam_ctr[1] + self.dcam[1],
            self.cam_ctr[2] + self.dcam[2],
        )
    
    def updateCameraMove(self, x, y, z):
        self.dcam = (
            (self.dcam[0] + x) if x != None else 0.0,
            (self.dcam[1] + y) if y != None else 0.0,
            (self.dcam[2] + z) if z != None else 0.0,
        )

mglw.run_window_config(GameWindow)
