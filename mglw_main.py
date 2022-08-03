# Kaidun (by HktOverload)

import numpy as np
import moderngl_window as mglw
import moderngl

import events
import scenes

class VertBufRef(object):
    __slots__ = 'buf', 'size'

    def __init__(self, size, alloc_fn=None):
        self.buf = alloc_fn(size)
        self.size = size

    def reset(self, newData, alloc_fn=None, alloc_hook=None):
        if alloc_fn == None:
            raise Exception(
                'VertBufRef.reset needs an alloc_fn specified'
                + ' (it does not have an OpenGL/moderngl context'
            )
        self.buf.release()
        newSize = len(newData.tobytes())
        if self.size != newSize:
            self.buf = alloc_fn(newSize)
            self.size = newSize
            if alloc_hook != None:
                alloc_hook()
        self.buf.write(newData)
        
    @classmethod
    def makeAllocFn(cls, ctx):
        def inner(desiredSize):
            return ctx.buffer(reserve=desiredSize)
        return inner

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
    title = 'Unnamed Window'
    gl_version = (3, 3)
    window_size = (3840//3, 2160//3)

    frame_callback = None

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
        self.alloc = VertBufRef.makeAllocFn(self.ctx)
        self.vbr = VertBufRef(
            1024,
            alloc_fn=self.alloc
        )
        self.updateVAO()
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
        self.prog['fog_attenuation_coef'].value = 1.9
    
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
            newGeometry = self.scene.buildGeometry(newGeometryState)
            self.vbr.reset(
                newGeometry,
                alloc_fn=self.alloc,
                alloc_hook=self.updateVAO,
            )
            self.geometryState = newGeometryState
    
    def updateVAO(self):
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbr.buf, '3f 3f', 'vert', 'aux_surf_normal')
            ]
        )

    def frame(self):
        self.scene.getController().frame(self.gamedata)
        if GameWindow.frame_callback != None:
            (GameWindow.frame_callback)()

def main(load_hook=None):
    if load_hook != None:
        load_hook(GameWindow)
    mglw.run_window_config(GameWindow, args=('--window', 'tk'))

if __name__ == '__main__':
    main()
