# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw
#: import moderngl

class GameWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (3840//3, 2160//3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('world_vertex.glsl', 'r') as f:
            vertex_shader = f.read()
        with open('world_fragment.glsl', 'r') as f:
            fragment_shader = f.read()  
        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )
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
    
    def render(self, *_):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render()

mglw.run_window_config(GameWindow)
