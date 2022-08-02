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
        self.geometryState = None
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
        zeroVec3 = (0.0, 0.0, 0.0)
        self.gamedata.update({
            'cam_ctr': (0.0, 1.0, -2.0),
            'd_cam_ctr': zeroVec3,
            'cam_rot': zeroVec3,
            'd_cam_rot': zeroVec3,
        })
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
        # Distance fog
        self.fog_color = (0.2, 0.2, 0.2)
        self.prog['fog_color'].value = self.fog_color
        self.prog['fog_attenuation_coef'].value = 0.002
    
    def render(self, *_):
        self.setupShaderInvocation()
        self.ctx.clear(*self.fog_color)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.vao.render()
        self.frame()

    def key_event(self, key, action, *_):
        if action == self.wnd.keys.ACTION_PRESS:
            kind = 'key_event/PRESS'
        elif action == self.wnd.keys.ACTION_RELEASE:
            kind = 'key_event/RELEASE'
        controller = self.scene.getController(self.gamedata)
        controller.handle(
            self.gamedata,
            events.Event(
                kind,
                {
                    'key': key,
                },
                self.wnd,
            ),
        )

    def setupShaderInvocation(self):
        controller = self.scene.getController(self.gamedata)
        updates = controller.shaderUpdates(self.gamedata)
        for k, v in updates.items():
            self.prog[k].value = v
        newGeometryState = self.scene.geometryState(self.gamedata)
        if self.geometryState != newGeometryState:
            self.vertBuf.write(
                self.scene.buildGeometry(newGeometryState)
            )
            self.geometryState = newGeometryState

    def frame(self):
        self.scene.getController().frame(self.gamedata)

mglw.run_window_config(GameWindow)
