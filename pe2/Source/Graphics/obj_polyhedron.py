import os
import sys
sys.path.append('../..')
import math
import numpy as np
from triangulate_obj_faces import processFace
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Obj_Polyhedron(Actor):

    ## initialization
    def __init__(self, renderer, filename, **kwargs):
        """Initialize actor."""
        super(Obj_Polyhedron, self).__init__(renderer, **kwargs)

        self._file = filename
        self._vertices = None
        self._normals = None
        self._faces = None

        ## create actor
        self.initialize()

    def generateGeometry(self):
        """Generate geometry"""
        vt_toggle = False
        file = 'temp.obj'
        fpath = 'Source/Graphics/'
        vertices = []
        faces = []
        indices = []
        normals = []
        if (not os.path.exists(file)):
            os.mknod(file)
        open(file, 'w').close() #erases content
        processFace(self._file, fpath + file, 1.0)
        with open(fpath + file, "r") as f:
            for line in f:
                data = line.split()
                if len(data) < 1:
                    pass
                elif data[0] == "f":
                    a = data[1]
                    a = a.split('/')
                    b = data[2]
                    b = b.split('/')
                    c = data[3]
                    c = c.split('/')
                    aux = [[a[0], a[1], a[2], 
                            b[0], b[1], b[2],
                            c[0], c[1], c[2]]]
                    faces.append(aux)
                elif data[0] == "v":
                    vertices.append([[data[1], data[2], data[3]]])
                elif data[0] == "vt":
                    if (not vt_toggle):
                        print ("vt not implemented")
                        vt_toggle = True
                elif data[0] == "vn":
                    normals.append([[data[1], data[2], data[3]]])
                elif data[0] == "vp":
                    print ("vp not implemented")
                elif data[0] == "vt":
                    print ("vt not implemented")
                elif data[0] == "l":
                    print ("l not implemented")

        self._vertices = np.array(vertices, dtype="float32")
        self._normals = np.array(normals, dtype="float32")
        self._faces = np.array(faces, dtype="int32")
        for i in range (0, len(self._faces)-3, 3):
            aux = []
            for j in range (i, i + 3):
                aux.append(self._faces[j][0])
            indices.append([aux])
        self._indices = np.array(indices, dtype="int")

    def initialize(self):
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, 
                    colors=None,
                    normals=self._normals,
                    indices=self._indices,
                    faces=self._faces)


    def render(self):
        a = 10
        GL.glDrawElements(GL.GL_TRIANGLES, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)

    