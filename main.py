# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw

class GameWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (3840//3, 2160//3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # OpenGL shader code
        with open('world_vertex.glsl', 'r') as f:
            vertex_shader = f.read()
        with open('world_fragment.glsl', 'r') as f:
            fragment_shader = f.read()  
        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )
        # OpenGL data
        self.vertBuf = self.ctx.buffer(
            np.array([
                0.2, -0.8, 0.0,
                0.4, 0.9, 0.5,
                -0.5, 0.3, 0.3,
            ], dtype='f4')
        )
        self.prog['cam_ctr'].value = (0.0, 1.0, -2.0)
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vertBuf, '3f', 'vert')
            ]
        )
        # Event handlers
        self.handlers = {
            'keypress': {
                'A': lambda: print('tacos'),
            },
            'keyrelease': {
                'A': lambda: print('no tacos'),
            },
        }
        self.handlers['keypress'] = {
            getattr(self.wnd.keys, k.lower()): v \
                for k, v in self.handlers['keypress'].items()
        }
        self.handlers['keyrelease'] = {
            getattr(self.wnd.keys, k.lower()): v \
                for k, v in self.handlers['keyrelease'].items()
        }
    
    def render(self, *_):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render()

    def key_event(self, key, action, _):
        if action == self.wnd.keys.ACTION_PRESS:
            handler = 'keypress'
        elif action == self.wnd.keys.ACTION_RELEASE:
            handler = 'keyrelease'
        self.handlers[handler].get(key, lambda: None)()

mglw.run_window_config(GameWindow)
