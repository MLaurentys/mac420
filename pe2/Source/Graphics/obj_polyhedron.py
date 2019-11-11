import os
import sys
from shutil import copyfile
from PyQt5.QtGui import QVector3D
from PIL import Image
sys.path.append('../..')
import math
import numpy as np
from Source.Graphics.Material import Material
from triangulate_obj_faces import processFace
from OpenGL import GL
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
from Source.Graphics.Actor import Actor

# def read_texture(filename):
#     glutInit()
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     img = Image.open(filename)
#     img_data = np.array(list(img.getdata()), np.int8)
#     texture_id = glGenTextures(1)
#     glBindTexture(GL_TEXTURE_2D, texture_id)
#     glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
#     glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0,
#                  GL_RGB, GL_UNSIGNED_BYTE, img_data)
#     return texture_id


class Obj_Polyhedron(Actor):

    ## initialization
    def __init__(self, renderer, filename, **kwargs):
        """Initialize actor."""
        super(Obj_Polyhedron, self).__init__(renderer, **kwargs)

        # Init basic object variables
        # if (os.path.exists("redtexture.png")):
        #     self.setTexture(data.get("redtexture.png"))
        self._selectable = True
        self._obj_file = filename + '.obj'
        self._mtl_file = filename + '.mtl'
        self._scale = 0.15 # obj file is too large
        self.setPickFactor(1.10)
        self._vertices = None
        self._normals = None
        self._faces = None

        ## create actor
        self.initialize()

    def generateGeometry(self):
        # Init local variables
        obj_file = 'temp.obj'
        mtl_file = 'temp.mtl'
        fout_path = 'Source/Graphics/'
        fin_path = 'obj-models/buildings/'
        vertices = []
        faces = {}
        indices = []
        normals = []
        names = []
        textures = []
        ranges = {}
        materials = {None: Material()}
        #
        # Prepares files for I/O
        #
        if (not os.path.exists(fout_path + obj_file)):
            os.mknod(fout_path + obj_file)
        if (os.path.exists(fout_path + mtl_file)):
            os.remove(fout_path + mtl_file)
        open(fout_path + obj_file, 'w').close() #erases content
        copyfile(fin_path + self._mtl_file, fout_path + mtl_file) #copy whole file
        #
        # Gets mtl information from file
        #
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
                                               shininess=16)
        #
        # Gets obj geometry from file
        #
        processFace(fin_path + self._obj_file, fout_path + obj_file, self._scale)
        with open(fout_path + obj_file, "r") as f:
            curr_name = None
            min_max = [0,0]
            maxi = 0
            aux_all = []
            for line in f:
                data = line.split()
                if len(data) < 1:
                    pass
                elif data[0] == "f":
                    maxi += 3
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
                    textures.append([data[1], data[2]])
                elif data[0] == "vn":
                    normals.append([[data[1], data[2], data[3]]])
                elif data[0] == "vp":
                    continue
                elif data[0] == "l":
                    print ("l not implemented")
                elif data[0] == "usemtl":
                    a = min_max[1]
                    b = maxi
                    names.append(curr_name)
                    ranges[curr_name] = [a, b]
                    faces[curr_name] = aux_all
                    min_max = [a,b]
                    aux_all = []
                    curr_name = data[1]
        #
        # Creates the object properties
        #
        v_aux = []
        n_aux = []
        for m in names:
            for j  in range(len(faces[m])):
                for i in range(3):
                    v_aux.append(vertices[faces[m][j][3*i] - 1])
                    n_aux.append(normals[faces[m][j][3*i + 2] - 1])
        self._vertices = np.array(v_aux, dtype="float32")
        self._normals = np.array(n_aux, dtype="float32")
        self._materials = materials
        self._num_vertices = len(self._vertices)
        self._num_normals = len(self._normals)
        self._names = names
        self._texCoords = np.array(textures, dtype="float32")
        self._ranges = ranges

    def initialize(self):
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, 
                    colors=None,
                    normals=self._normals,
                    texcoords=self._texCoords)


    def render(self):
        for m in self._names:
            self._active_shader.setUniformValue('material.emission' , self._materials[m].emissionColor )
            self._active_shader.setUniformValue('material.ambient'  , self._materials[m].ambientColor )
            self._active_shader.setUniformValue('material.diffuse'  , self._materials[m].diffuseColor )
            self._active_shader.setUniformValue('material.specular' , self._materials[m].specularColor)
            self._active_shader.setUniformValue('material.shininess', self._materials[m].shininess    )
            GL.glDrawArrays(GL.GL_TRIANGLES, self._ranges[m][0], self._ranges[m][1] - self._ranges[m][0])