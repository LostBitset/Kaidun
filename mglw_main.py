# Kaidun (by HktOverload)

import time

import numpy as np
import moderngl_window as mglw
import moderngl

import events
import terrain
import scenes as s
from vbo_utils import VertBufRef

'''
This class is essentially a very heavily modified version of the very basic
example that displays a single triangle given at:

[: Citation (a big one) https://github.com/moderngl/moderngl/blob/master/examples/basic_simple_color_triangle.py :]

Pretty much all of the other information I used was found in the moderngl docs:
[: Citation (another big one) https://moderngl.readthedocs.io/en/latest/ :]
'''

class GameWindow(mglw.WindowConfig):
    title = 'Unnamed Window'
    gl_version = (3, 3)
    window_size = (3840//3, 2160//3)

    frame_callback = None
    init_callback = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if GameWindow.init_callback != None:
            (GameWindow.init_callback)(self)
        # Setup gamedata and scene
        self.gamedata = dict()
        self.scene = s.WorldScene
        self.geometryState = None
        # Frame times
        self.ftimeLast = time.time()
        # OpenGL / Shader code
        # [: Citation https://github.com/KhronosGroup/glslang :]
        with open('world.glsl.vert', 'r') as f:
            vertex_shader = f.read()
        with open('world.glsl.frag', 'r') as f:
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
        # World geometry
        followGraph = terrain.genTestGraph()
        worldGeometry = terrain.fromGraph(followGraph)
        # Camera
        zeroVec3 = (0, 0, 0)
        followEdge = next( i for i in followGraph.edges() )
        followEdge = followEdge.toDirectedND()
        print(followEdge)
        self.gamedata.update({
            '<wnd>': self.wnd,
            'cam_ctr': (followEdge.src[0], followEdge.src[1], 0.5),
            'd_cam_ctr': zeroVec3,
            'cam_rot': (np.pi/2, 0.0, 0.0),
            'd_cam_rot': zeroVec3,
            'cam_near': 0.01,
            'follow_graph': followGraph,
            'follow_edge': followEdge,
            'is_following': False,
            'world_geometry': worldGeometry,
        })
        # Everything after this point is a uniform for shader code
        # Please read the documentation in the shader code itself
        # for citations
        self.prog['cam_near'].value = self.gamedata['cam_near']
        self.prog['cam_dist'].value = 59.0
        # Lighting
        self.prog['lighting_ambient'].value = 0.2
        self.prog['lighting_maxsc'].value = 1.15
        self.prog['lighting_light_ctr'] = (2.0, 2.0, 2.0)
        self.prog['lighting_light_brightness'] = 100.0
        # Lighting / Surface info
        # Information about albedo values for planets in the solar system:
        # [: Citation https://astronomy.swin.edu.au/cosmos/a/Albedo :]
        # Information about how to interpret that information:
        # [: Citation http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/albedo.html :]
        self.prog['surf_albedo'].value = 0.09
        self.prog['surf_roughness'].value = 0.1
        # Distance fog
        self.fog_color = (0.2, 0.2, 0.2)
        self.prog['fog_color'].value = self.fog_color
        self.prog['fog_attenuation_coef'].value = 3.1
        # Terrain and gravity
        self.gamedata.update({
            'player_height': 1.5,
            'current_terrain_height': 1.0,
            'vel_gravity': 0.0,
        })

    def render(self, *_):
        self.setupShaderInvocation()
        self.ctx.clear(*self.fog_color)
        # This has C code, so I translated it into this line
        # which uses the modergl bindings and not the actual
        # OpenGL C library
        # All I got from this was basically just the name of
        # the flag
        # [: Citation https://learnopengl.com/Advanced-OpenGL/Depth-testing :]
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
                (
                    self.vbr.buf,  # TARGET
                    '3f 3f 3f',    # FORMAT
                    'vert', 'drv_surf_normal', 'aux_rgb',
                )
            ]
        )

    def frame(self):
        self.scene.getController(self.gamedata).frame(
            self.gamedata,
            time.time() - self.ftimeLast,
        )
        self.ftimeLast = time.time()
        if GameWindow.frame_callback != None:
            (GameWindow.frame_callback)()

def main(load_hook=None):
    if load_hook != None:
        load_hook(GameWindow)
    mglw.run_window_config(GameWindow, args=('--window', 'tk'))

if __name__ == '__main__':
    main()

