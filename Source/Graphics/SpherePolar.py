import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class SpherePolar(Actor):

    ## initialization
    def __init__(self, renderer, radius=1.0, horRes=20, verRes=20, **kwargs):
        """Initialize actor."""
        super(SpherePolar, self).__init__(renderer, **kwargs)

        self._radius = radius
        self._hor_res = horRes
        self._ver_res = verRes
        self._vertices = None
        self._normals = None
        ## create actor
        self.initialize()
        

    @property
    def radius(self):
        """Returns the bottom radius of the Sphere"""
        return self._radius


    @property
    def hor_Resolution(self):
        """Returns the horizontal resolution of this cone"""
        return self._hor_res
        
    @property
    def ver_Resolution(self):
        """Returns the vertical resolution of this cone"""
        return self._ver_res

    def addVertex(self, v, vertices):
        """Add a vertex into the array"""
        norm = np.linalg.norm(v)
        if(norm != 0):
            vn = v / norm * self._radius
        else:
            vn = [0.0,0.0,0.0]
        vertices += [[vn[0], vn[1], vn[2]]]
        return len(vertices)-1

    def generateGeometry(self):
        """Generate geometry"""
        
        ver_step = math.pi/self._ver_res
        hor_step = 2*math.pi/self._hor_res
        cur_hor = 0
        cur_ver = 0
        r = self._radius

        #vertices = np.empty((int(2*self._hor_res*self._ver_res), 3))
        vertices = []
        indices = []

        normals = np.empty((int(2*self._hor_res*self._ver_res), 3))
        center = [0.0,0.0,0.0]
        self.addVertex(center, vertices)

        nnext = [r, 0.0, 0.0]
        for i  in range(1, self._hor_res):
            self.addVertex(nnext, vertices)
            cur_hor += hor_step
            nnext[0] = r * math.cos(i * hor_step)
            nnext[1] = r * math.sin(i * hor_step)

        for i in range(1, len(vertices)-1):
            if (i <= (len(vertices)/2)):
                indices += [[0, i, i + 1]]
            else:
                indices += [[0, i+ 1, i]]

        indices += [[0, len(vertices) - 1, 1]]

        self._normals = np.array([[0.0, 0.0, 1.0]] * len(vertices), dtype=np.float32)
        self._vertices = np.array(vertices, dtype=np.float32)
        self._indices = np.array(indices, dtype=np.uint32)

    def initialize(self):
        """Creates cone geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, 
                    colors=None,
                    normals=self._normals, 
                    indices=self._indices)


    def render(self):
        """Render Sphere"""
        GL.glDrawElements(GL.GL_TRIANGLES, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)

    