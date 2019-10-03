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
        uvplane = {}

        ver_step = math.pi/self._ver_res
        hor_step = 2*math.pi/self._hor_res
        cur_hor = 0
        cur_ver = 0
        r = self._radius
        tp = math.pi*2
        pi = math.pi
        #vertices = np.empty((int(2*self._hor_res*self._ver_res), 3))
        vertices = []
        indices = []
        #build uvplane
        theta = -math.pi/2.0
        #topo da esfera fica encima (z = r)
        top = [0.0, 0.0, r]
        bot = [0.0, 0.0, -r]
        self.addVertex(top, vertices)
        self.addVertex(bot, vertices)
        parity = self._ver_res%2
        for i in range (self._hor_res):
            uvplane[(i, math.floor(self._ver_res/2))] = (0, (0.0, 1.0))
            uvplane[(i, -math.floor(self._ver_res/2) - parity)] = (1, (0.0, 0.0))
        i = 0
        j = 0
        while(i < math.floor(self._ver_res/2)):  
        
            up = theta + i * ver_step + parity*(ver_step/2.0)
            down = theta - i * ver_step - parity*(ver_step/2.0)
            while(j < self._hor_res):
                phi = j * hor_step
                pair = (phi/tp, 1.0 + up/pi)
                pairB = (phi/tp, 1.0 + down/pi)
                vertex = [r*math.sin(up)*math.cos(phi),
                          r*math.sin(up)*math.sin(phi),
                          r*math.cos(up)]
                vertexB = [r*math.sin(down)*math.cos(phi),
                           r*math.sin(down)*math.sin(phi),
                           r*math.cos(down)]
                sz = len(vertices)
                self.addVertex(vertex, vertices)
                self.addVertex(vertexB, vertices)
                uvplane[(j, i)] = (sz, pair)
                uvplane[(j, -i -parity)] = (sz + 1, pairB)
                j += 1
            # self.addVertex(top, vertices)
            # self.addVertex(bot, vertices)
            # uvplane[(self._hor_res, i)] = (len(vertices) - 2, top)
            # uvplane[(self._hor_res, -i)] = (len(vertices) - 1, bot)
            j = 0
            i += 1
        if(parity == 1):
            for j in range(self._hor_res - 1):
                a = uvplane[(j, 0)][0]
                b = uvplane[(j + 1, 0)][0]
                c = uvplane[(j, -1)][0]
                d = uvplane[(j+1, -1)][0]
                indices += [[a, b, c]]
                indices += [[b, c, d]]
            a = uvplane[(self._hor_res - 1, 0)][0]
            b = uvplane[(0, 0)][0]
            c = uvplane[(self._hor_res - 1, -1)][0]
            d = uvplane[(0, -1)][0]
            indices += [[a, b, c]]
            indices += [[b, c, d]]
        for i in range(math.floor(self._ver_res/2)):
            for j in range(self._hor_res - 1):
                #phi = j * hor_step
                a = uvplane[(j, i)][0]
                b = uvplane[(j + 1, i)][0]
                c = uvplane[(j, i+1)][0]
                d = uvplane[(j+1, i+1)][0]
                e = uvplane[(j, -i - parity)][0]
                f = uvplane[(j+1, -i - parity)][0]
                g = uvplane[(j, -i - 1 - parity)][0]
                h = uvplane[(j+1, -i - 1 - parity)][0]
                indices += [[a, b, c]]
                indices += [[b, c, d]]
                indices += [[e, g, f]]
                indices += [[f, g, h]]
            a = uvplane[(self._hor_res - 1, i)][0]
            b = uvplane[(0, i)][0]
            c = uvplane[(self._hor_res - 1, i + 1)][0]
            d = uvplane[(0, i+1)][0]
            e = uvplane[(self._hor_res - 1, -i - parity)][0]
            f = uvplane[(0, -i - parity)][0]
            g = uvplane[(self._hor_res - 1, -i-1 - parity)][0]
            h = uvplane[(0, -i-1 - parity)][0]
            indices += [[a, b, c]]
            indices += [[b, c, d]]
            indices += [[e, g, f]]
            indices += [[f, g, h]]

                #indices += [[b, c, d]]
                #indices += [[e, a, f]]
                #indices += [[f, a, b]]
                # a = (phi, theta)
                # b = (phi + hor_step, theta)
                # c = (phi, up)
                # d = (phi + hor_step, up)
                # e = (phi, down)
                # f = (phi + hor_step, down)
                #a = (A[0]/tp, 1.0 + A[1]/pi)
                #b = (B[0]/tp, 1.0 + B[1]/pi)
                #c = (C[0]/tp, 1.0 + C[1]/pi)
                #d = (D[0]/tp, 1.0 + D[1]/pi)
                #e = (E[0]/tp, 1.0 + E[1]/pi)
                #f = (F[0]/tp, 1.0 + F[1]/pi)
                # indices += [[uvplane[(a[0], a[1])][0], uvplane[(b[0],b[1])[0]],
                #              uvplane[(c[0], c[1])][0], uvplane[(d[0], d[1])[0]]]]
                # indices += [[uvplane[(a[0], a[1])][0], uvplane[(b[0],b[1])[0]],
                #              uvplane[(e[0], e[1])][0], uvplane[(f[0], f[1])[0]]]]

        

        self._normals = np.array(vertices, dtype=np.float32)
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

    