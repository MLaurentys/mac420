import os
import sys
from shutil import copyfile
from PyQt5.QtGui import QVector3D
sys.path.append('../..')
import math
import numpy as np
from Source.Graphics.Material import Material
from triangulate_obj_faces import processFace
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Obj_Polyhedron(Actor):

    ## initialization
    def __init__(self, renderer, filename, **kwargs):
        """Initialize actor."""
        super(Obj_Polyhedron, self).__init__(renderer, **kwargs)

        self._obj_file = filename + '.obj'
        self._mtl_file = filename + '.mtl'
        self._vertices = None
        self._normals = None
        self._faces = None

        ## create actor
        self.initialize()

    def generateGeometry(self):
        # init variables
        vt_toggle = False
        obj_file = 'temp.obj'
        mtl_file = 'temp.mtl'
        fout_path = 'Source/Graphics/'
        fin_path = 'obj-models/buildings/'
        vertices = []
        faces = {}
        indices = []
        normals = []
        names = []
        materials = {None: Material()}
        #prepares files
        if (not os.path.exists(fout_path + obj_file)):
            os.mknod(fout_path + obj_file)
        if (os.path.exists(fout_path + mtl_file)):
            os.remove(fout_path + mtl_file)
        open(fout_path + obj_file, 'w').close() #erases content
        copyfile(fin_path + self._mtl_file, fout_path + mtl_file) #copy whole file

        #makes materials
        with open(fout_path + mtl_file, 'r') as file:
            f = file.readlines()
            i = 0
            while (i < len(f)):
                line = f[i].split()
                i+=1
                if(len(line) < 1): continue
                if (line[0] == 'newmtl'):
                    name = line[1]
                    ns = ka = kd = ks = ke = ni = d = illum = None
                    while (i < len(f)):
                        line = f[i].split()
                        if(len(line) < 1): break
                        if (line[0] == 'Ns'):
                            ns = float(line[1])
                        elif (line[0] == 'Ka'):
                            ka = QVector3D(float(line[1]), float(line[2]), float(line[3]))
                        elif (line[0] == 'Kd'):
                            kd = QVector3D(float(line[1]), float(line[2]), float(line[3]))
                        elif (line[0] == 'Ks'):
                            ks = QVector3D(float(line[1]), float(line[2]), float(line[3]))
                        elif (line[0] == 'Ke'):
                            ke = QVector3D(float(line[1]), float(line[2]), float(line[3]))
                        elif (line[0] == 'Ni'):
                            ni = float(line[1])
                        elif (line[0] == 'd'):
                            d = float(line[1])
                        elif (line[0] == 'illum'):
                            illum = int(line[1])
                        else:
                            break
                        i += 1
                    materials[name] = Material(emission=ke,
                                               ambient=ka,
                                               diffuse=kd,
                                               specular=ks,
                                               shininess=illum)

        #gets obj geometry
        processFace(fin_path + self._obj_file, fout_path + obj_file, 1.0)
        with open(fout_path + obj_file, "r") as f:
            curr_name = None
            aux_all = []
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
                    aux = [a[0], a[1], a[2], 
                            b[0], b[1], b[2],
                            c[0], c[1], c[2]]
                    aux_all.append([int(el) for el in aux])
                elif data[0] == "v":
                    vertices.append([data[1], data[2], data[3]])
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
                elif data[0] == "usemtl":
                    names.append(curr_name)
                    faces[curr_name] = aux_all
                    aux_all = []
                    curr_name = data[1]


        v = {}
        n = {}
        v_aux = []
        n_aux = []
        for m in names:
            v[m] = []
            n[m] = []
            for j  in range(len(faces[m])):
                for i in range(3):
                    y = faces[m][j][3*i]
                    x = vertices[y - 1]
                    v[m].append(x)
                    n[m].append(normals[faces[m][j][3*i + 2] - 1])
                    v_aux.append(vertices[faces[m][j][3*i] - 1])
                    n_aux.append(vertices[faces[m][j][3*i + 2] - 1])
            v[m] = np.array(v[m], dtype="float32")
        self._vertices = np.array(v_aux, dtype="float32")
        self._normals = np.array(n_aux, dtype="float32")
        self._materials = materials
        self._num_vertices = len(self._vertices)
        self._num_normals = len(self._normals)
        self._names = names
        self._vertices_m = v

    def initialize(self):
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, 
                    colors=None,
                    normals=self._normals)


    def render(self):
        for m in self._names:
            self._material = self._materials[m]
            self._vertices = self._vertices_m[m]
            amt = len(self._vertices)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0 , amt)

    