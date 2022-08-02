# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw
import moderngl

import events
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
        # Setup gamedata and scene
        self.gamedata = dict()
        self.scene = scenes.CubeScene
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
        self.prog['lighting_ambient'].value = 0.2
        self.prog['lighting_maxsc'].value = 1.15
        self.prog['lighting_light_ctr'] = (2.0, 2.0, 2.0)
        self.prog['lighting_light_brightness'] = 50.0
        # Lighting / Surface info
        self.prog['surf_albedo'].value = 0.09
        self.prog['surf_roughness'].value = 0.1
        self.vertBuf.write(self.scene.buildGeometry("I'm a cube!"))
    
    def render(self, *_):
        self.setupShaderInvocation()
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.vao.render()
        self.frame()

    def key_event(self, key, action, *_):
        if action == self.wnd.keys.ACTION_PRESS:
            kind = 'key_event/PRESS'
        elif action == self.wnd.keys.ACTION_RELEASE:
            kind = 'key_event/RELEASE'
        self.scene.getController().handle(
            self.gamedata,
            events.Event(
                kind,
                {
                    'key': key,
                },
                self.wnd)
        )

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
