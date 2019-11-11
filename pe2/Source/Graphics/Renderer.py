import math
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OpenGL import GL
from Source.Graphics.Trackball import Trackball
from Source.Graphics.Light import Light
from Source.Graphics.Camera import Camera
from Source.Graphics.Material import Material
from Source.Graphics.Scene import Scene
from Source.Graphics.Actor import Actor
from Source.Graphics.Cone import Cone
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Cube import Cube
from Source.Graphics.Group import Group
from Source.Graphics.Gnomon import Gnomon
from Source.Graphics.World import World

# import actors
from Source.Graphics.obj_polyhedron import Obj_Polyhedron
from Source.Graphics.Icosahedron import Icosahedron
from Source.Graphics.Floor import Floor

from enum import IntEnum

class Renderer(QOpenGLWidget):

    ## initialization
    def __init__(self, parent=None, **kwargs):
        """Initialize OpenGL version profile."""
        super(Renderer, self).__init__(parent)
        self._parent = parent

        self._transforming = False
        self._prevPoint = QPointF(0.0, 0.0)
        self.axis_selected = False
        ## deal with options
        self._lighting = kwargs.get("lighting", True)
        self._antialiasing = kwargs.get("antialiasing", False)
        self._statistics = kwargs.get("statistics", True)

        ## define home orientation
        self._home_rotation = QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 25.0) * QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -50.0)

        ## define scene trackball
        self._trackball = Trackball(velocity=0.05, axis=QVector3D(0.0, 1.0, 0.0), mode=Trackball.TrackballMode.Planar, rotation=self._home_rotation, paused=True)
        
        ## create main scene
        self._world = World(self, home_position=QVector3D(0, 0, 3.5))

        ## do not animate
        self._animating = True

        ## not yet initialized
        self._initialized = False

        self.setAutoFillBackground(False)

        self.currentActor_ = None
        self._shift_isPressed = False

    def shiftPressed(self):
        self._shift_isPressed = True
    def shiftReleased(self):
        self._shift_isPressed = False

    def printOpenGLInformation(self, format, verbosity=0):
        print("\n*** OpenGL context information ***")
        print("Vendor: {}".format(GL.glGetString(GL.GL_VENDOR).decode('UTF-8')))
        print("Renderer: {}".format(GL.glGetString(GL.GL_RENDERER).decode('UTF-8')))
        print("OpenGL version: {}".format(GL.glGetString(GL.GL_VERSION).decode('UTF-8')))
        print("Shader version: {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('UTF-8')))
        print("Maximum samples: {}".format(GL.glGetInteger(GL.GL_MAX_SAMPLES)))
        print("\n*** QSurfaceFormat from context ***")
        print("Depth buffer size: {}".format(format.depthBufferSize()))
        print("Stencil buffer size: {}".format(format.stencilBufferSize()))
        print("Samples: {}".format(format.samples()))
        print("Red buffer size: {}".format(format.redBufferSize()))
        print("Green buffer size: {}".format(format.greenBufferSize()))
        print("Blue buffer size: {}".format(format.blueBufferSize()))
        print("Alpha buffer size: {}".format(format.alphaBufferSize()))
            #print("\nAvailable extensions:")
            #for k in range(0, GL.glGetIntegerv(GL.GL_NUM_EXTENSIONS)-1):
            #    print("{},".format(GL.glGetStringi(GL.GL_EXTENSIONS, k).decode('UTF-8')))
            #print("{}".format(GL.glGetStringi(GL.GL_EXTENSIONS, k+1).decode('UTF-8')))



    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions.""" 	
        if not self._initialized:
            self.printOpenGLInformation(self.context().format())
        
            ## create gnomon
            self._gnomon = Gnomon(self)
            
            ## update cameras
            self._world.camera.setRotation(self._trackball.rotation().inverted())
            self._gnomon.camera.setRotation(self._trackball.rotation().inverted())

  
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_DEPTH_CLAMP)
            #GL.glEnable(GL.GL_CULL_FACE)
            GL.glEnable(GL.GL_MULTISAMPLE)
            GL.glEnable(GL.GL_FRAMEBUFFER_SRGB)
            
            ## attempt at line antialising
            if self._antialiasing:
        
                GL.glEnable(GL.GL_POLYGON_SMOOTH)
                GL.glEnable(GL.GL_BLEND)

                GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
                GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
                GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)

                GL.glPointSize(5)
                GL.glLineWidth(1)

            ## clear color
            GL.glClearColor(0.75, 0.76, 0.76, 0.0)

            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()

            ## timer for immediate update
            self._timer = QTimer(self)
            self._timer.setTimerType(Qt.PreciseTimer)
            self._timer.timeout.connect(self.updateScene)
            self._timer.start()

            ## timer for measuring elapsed time
            self._elapsed_timer = QElapsedTimer()
            self._elapsed_timer.restart()
            self._frameElapsed = 0
            self._gpuElapsed = 0

            xform1 = QMatrix4x4()
            aux =  Obj_Polyhedron(self._world, "1", transform=xform1)

            self._world.addActor(aux)
            
            self._initialized = True

        else:
            
            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()


        ## initialize OpenGL timer
        self._query = GL.glGenQueries(1)


    def clear(self):
        """Clear scene"""
        self._world.clear()
        self.update()

    def renderTimeEstimates(self):
        return [self._frameElapsed, self._gpuElapsed]

    def selectActor(self, actor):
        self.RemoveLines()
        self.currentActor_ = actor
        self._world.selectActor(actor)

    @property
    def lighting(self):
        return self._lighting


    def setDrawStyle(self, style):
        self._draw_style = style


    def activeSceneCamera(self):
        """Returns main scene camera"""
        return self._world.camera


    def setAnimating(self, value):
        """Sets continuous update"""
        self._animating = value


    def isAnimating(self):
        """Returns whether continous update is active"""
        return self._animating


    def updateScene(self):
        """Schedule an update to the scene"""
        if self.isAnimating():
            self.update()


    def renderScene(self):
        """Draw main scene"""

        ## set scene rotation
        self._world.camera.setRotation(self._trackball.rotation().inverted())
        self._gnomon.camera.setRotation(self._trackball.rotation().inverted())

        self._world.render()

        ## render gnomon
        self._gnomon.render()

    
    def paintGL(self):
        """Draw scene"""

        ## record render time statistics
        if self._statistics:

            ## begin GPU time query
            GL.glBeginQuery(GL.GL_TIME_ELAPSED, self._query)

            ## render scene
            self.renderScene()

            ## finish GPU time query
            GL.glEndQuery(GL.GL_TIME_ELAPSED)

            ## record render time statistics, need to stall the CPU a bit
            ready = False 
            while not ready:
                ready = GL.glGetQueryObjectiv(self._query, GL.GL_QUERY_RESULT_AVAILABLE)
            self._gpuElapsed = GL.glGetQueryObjectuiv(self._query, GL.GL_QUERY_RESULT ) / 1000000.0

            ## delete query object
            #GL.glDeleteQueries( self._query )

        else:

            ## render scene
            self.renderScene()

        self._frameElapsed = self._elapsed_timer.restart()


    def resizeGL(self, width, height):
        """ Called by the Qt libraries whenever the window is resized"""
        self._world.camera.setAspectRatio(width / float(height if height > 0.0 else 1.0))


    def pan(self, point, state='start'):
        """Move camera according to mouse move"""
        if state == 'start':
            self._lastPanningPos = point
        elif state == 'move':
            delta = QLineF(self._lastPanningPos, point)
            self._lastPanningPos = point
            direction = QVector3D(-delta.dx(), -delta.dy(), 0.0).normalized()
            newpos = self._world.camera.position + delta.length()*2.0 * direction
            self._world.camera.setPosition(newpos)
    

        
    def mouseMoveEvent(self, event):
        """Called by the Qt libraries whenever the window receives a mouse move/drag event."""
        super(Renderer, self).mouseMoveEvent(event)
        
        if event.isAccepted():
            return

        if event.buttons() & Qt.LeftButton:
            self._trackball.move(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            event.accept()
            if not self.isAnimating():
                self.update()

        elif event.buttons() & Qt.RightButton:
            self.pan(self._pixelPosToViewPos(event.localPos()), state='move')
            self.update()




    def wheelEvent(self, event):
        """Process mouse wheel movements"""
        super(Renderer, self).wheelEvent(event)
        self.zoom(-event.angleDelta().y() / 950.0)
        event.accept()
        ## scene is dirty, please update
        self.update()


    def zoom(self, diffvalue):
        """Zooms in/out the active camera"""
        multiplicator = math.exp(diffvalue)

        ## get a hold of the current active camera
        camera = self._world.camera
        
        if camera.lens == Camera.Lens.Orthographic:
            # Since there's no perspective, "zooming" in the original sense
            # of the word won't have any visible effect. So we just increase
            # or decrease the field-of-view values of the camera instead, to
            # "shrink" the projection size of the model / scene.
            camera.scaleHeight(multiplicator)

        else:
        
            old_focal_dist = camera.focalDistance
            new_focal_dist = old_focal_dist * multiplicator

            direction = camera.orientation * QVector3D(0.0, 0.0, -1.0)
            newpos = camera.position + (new_focal_dist - old_focal_dist) * -direction

            camera.setPosition(newpos)
            camera.setFocalDistance(new_focal_dist)


    def viewFront(self):
        """Make camera face the front side of the scene"""
        self._trackball.reset(QQuaternion())
        self.update()
        

    def viewBack(self):
        """Make camera face the back side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 180.0))
        self.update()


    def viewLeft(self):
        """Make camera face the left side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -90.0))
        self.update()


    def viewRight(self):
        """Make camera face the right side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 90.0))
        self.update()


    def viewTop(self):
        """Make camera face the top side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 90.0))
        self.update()


    def viewBottom(self):
        """Make camera face the bottom side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), -90.0))
        self.update()

    
    def createGridLines(self):
        """Set gridlines"""
        self.makeCurrent()
        self._world.createGridLines()
        self.doneCurrent()


    def cameraLensChanged(self, lens):
        """Switch world's. camera lens"""
        self._world.setCameraLens(lens)
        self._gnomon.setCameraLens(lens)
        self.update()


    def storeCamera(self):
        """Store world's camera parameters"""
        self._world.storeCamera()


    def recallCamera(self):
        """Recall camera parameters"""
        self._world.recallCamera()
        self._trackball.reset(self._world.camera.rotation.inverted())
        self.update()


    def resetCamera(self):
        """Reset world's camera parameters"""
        self._world.resetCamera()
        self._trackball.reset(self._home_rotation)
        self.update()


    def drawStyleChanged(self, index):
        self._world.setDrawStyle(Scene.DrawStyle.Styles[index])
        self.update()

    def setActors(self, objects):
        self._objs = objects

    def lightingChanged(self, state):
        self._world.setLighting(state)
        self.update()

    
    def shadingChanged(self, index):
        self._world.setShading(Scene.Shading.Types[index])
        self.update()


    def headLightChanged(self, state):
        self._world.light.setHeadLight(state)
        self.update()


    def directionalLightChanged(self, state):
        self._world.light.setDirectional(state)
        self.update()

    
    def enableProfiling(self, enable):
        self._statistics = enable


    def enableAnimation(self, enable):
        self.setAnimating(enable)
        if not enable:
            self._trackball.stop()

    def _pixelPosToViewPos(self, point):
        return QPointF(2.0 * float(point.x()) / self.width() - 1.0, 1.0 - 2.0 * float(point.y()) / self.height())

    def changeActor(self, index):
        if (index == 0): return
        if (index > len(self._objs)):
            print("!!!!! Fora da Lista !!!!!!")
            return
        self.makeCurrent()
        xform1 = QMatrix4x4()
        aux =  Obj_Polyhedron(self._world, self._objs[index - 1], transform=xform1)
        self._world.addActor(aux)

    def delActor(self):
        self.RemoveLines()
        self._world.removeActor(self.currentActor_)
    
    def generateScalingLines(self):
        self.makeCurrent()
        self.RemoveLines()
        cur = self.currentActor_
        if (type(cur) is not Obj_Polyhedron): pass
        cur._state = 1
        sc = cur._scale
        asc = sc * 2.5 # axis scale
        dist = 5.0 * asc * 3

        # x cube
        matrix = QMatrix4x4()
        matrix.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        xl = Cube(self._world, name="sxc",
                material=Material(diffuse=QVector3D(1.0, 0.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
                shininess=76.8), transform=matrix)
        # y cube
        matrix = QMatrix4x4()
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        yl = Cube(self._world, name="syc",
                material=Material(diffuse=QVector3D(0.0, 1.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        # z cube
        matrix = QMatrix4x4()
        matrix.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        zl = Cube(self._world, name="szc",
                material=Material(diffuse=QVector3D(0.0, 0.47, 0.78), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        # x cylinder
        matrix = QMatrix4x4()
        matrix.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/4.0, 0.0)
        xlc = Cylinder(self._world, name="txc", height=dist/2.0, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(1.0, 0.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)
        # y cylinder
        matrix = QMatrix4x4()
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/4.0, 0.0)
        ylc = Cylinder(self._world, name="tyc", height=dist/2.0, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(0.0, 1.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        # z cylinder
        matrix = QMatrix4x4()
        matrix.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/4.0, 0.0)
        zlc = Cylinder(self._world, name="tzc", height=dist/2.0, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(0.0, 0.47, 0.78), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        newlines = [xl, yl, zl, xlc, ylc, zlc]
        self.currentActor_._lines = newlines
        for l in newlines:
            self._world.addActor(l)
    def generateRotatingLines(self):
        pass
    def generateTranslatingLines(self):
        self.makeCurrent()
        self.RemoveLines()
        cur = self.currentActor_
        if (type(cur) is not Obj_Polyhedron): pass
        sc = cur._scale
        cur._state = 3
        asc = sc * 2.5 # axis scale
        dist = 5.0 * asc * 3
        ## x axis cone
        matrix = QMatrix4x4()
        matrix.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist, 0.0)
        xl = Cone(self._world, name="tx",
            resolution=12, material=Material(diffuse=QVector3D(1.0, 0.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        ## y axis cone
        matrix = QMatrix4x4()
        matrix.scale(asc, asc, asc)        
        matrix.translate(0.0, dist, 0.0) ##6.0
        yl = Cone(self._world, name="ty",
            resolution=12, material=Material(diffuse=QVector3D(0.0, 1.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        ## z axis cone
        matrix = QMatrix4x4()
        matrix.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        matrix.scale(asc, asc, asc)        
        matrix.translate(0.0, dist, 0.0)
        zl = Cone(self._world, name="tz",
            resolution=12, material=Material(diffuse=QVector3D(0.0, 0.47, 0.78), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        # x cylinder
        matrix = QMatrix4x4()
        matrix.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        xlc = Cylinder(self._world, name="txc", height=dist, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(1.0, 0.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)
        # y cylinder
        matrix = QMatrix4x4()
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        ylc = Cylinder(self._world, name="tyc", height=dist, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(0.0, 1.0, 0.0), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        # z cylinder
        matrix = QMatrix4x4()
        matrix.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        matrix.scale(asc, asc, asc)
        matrix.translate(0.0, dist/2.0, 0.0)
        zlc = Cylinder(self._world, name="tzc", height=dist, radius=sc,
            resolution=12, material=Material(diffuse=QVector3D(0.0, 0.47, 0.78), specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=matrix)

        newlines = [xl, yl, zl, xlc, ylc, zlc]
        self.currentActor_._lines = newlines
        for l in newlines:
            self._world.addActor(l)
    
    def selectX(self):
        self.axis_selected = True
        self.currentActor_._axis = 1
        self.currentActor_._lines[0].setHighlighted(True)
        self.currentActor_._lines[1].setHighlighted(False)
        self.currentActor_._lines[2].setHighlighted(False)
    def selectY(self):
        self.axis_selected = True
        self.currentActor_._axis = 2
        self.currentActor_._lines[0].setHighlighted(False)
        self.currentActor_._lines[1].setHighlighted(True)
        self.currentActor_._lines[2].setHighlighted(False)
    def selectZ(self):
        self.axis_selected = True
        self.currentActor_._axis = 3
        self.currentActor_._lines[0].setHighlighted(False)
        self.currentActor_._lines[1].setHighlighted(False)
        self.currentActor_._lines[2].setHighlighted(True)

    def IsAxisSelected(self): return self.axis_selected

    def RemoveLines(self):
        self.axis_selected = False
        self._transforming = False
        if (type(self.currentActor_) is not Obj_Polyhedron): return
        old = self.currentActor_._lines
        if (old != None): 
            for l in old:
                self._world.removeActor(l)
        self.currentActor_._lines = None

    def TransformActor(self, amt):
        if (self.currentActor_._state == 1):
            self.scale(amt)
        elif (self.currentActor_._state == 2):
            pass
        elif (self.currentActor_._state == 3):
            self.translate(amt)

    def scale (self, amt):
        if (amt < 0):
            amt = -1/amt
        cur = self.currentActor_
        initialPos = cur.position()
        cur.translate(-initialPos)
        cur.scale(amt)
        cur.translate(initialPos)

    def translate (self, amt):
        cur = self.currentActor_
        if(cur._axis == 1):
            cur.translate(QVector3D(amt, 0.0, 0.0))
        elif(cur._axis == 2):
            cur.translate(QVector3D(0.0, amt, 0.0))
        elif(cur._axis == 3):
            cur.translate(QVector3D(0.0, 0.0, amt))

    def startTransforming(self, point):
        if (self._transforming): return
        self._transforming = True
        self._prevPoint = point
        
    def finishTransforming(self, point):
        moved = self._prevPoint - point
        norm = math.sqrt(moved.x()**2 + moved.y()**2)
        self._transforming = False
        norm *= 3.0
        if (self._prevPoint.x() > point.x()):
            norm = -norm
        self.TransformActor(norm)



    def mouseReleaseEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse release."""
        super(Renderer, self).mouseReleaseEvent(event)
        print("yup, here")
        if event.isAccepted():
            return

        if (event.button() == Qt.LeftButton):
            event.accept()
            print("mouse left released")
            point = self._pixelPosToViewPos(event.localPos())
            if (self.IsAxisSelected()):
                self.finishTransforming(point)
            else:
                self._trackball.release(point, QQuaternion())
                if not self.isAnimating():
                    self._trackball.stop()
                    self.update()
