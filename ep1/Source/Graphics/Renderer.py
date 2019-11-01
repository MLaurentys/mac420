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
from Source.Graphics.Group import Group
from Source.Graphics.Gnomon import Gnomon
from Source.Graphics.World import World

# import actors
from Source.Graphics.Cone import Cone
from Source.Graphics.Cube import Cube
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Icosahedron import Icosahedron
from Source.Graphics.Floor import Floor
import Source.Graphics.PyramidOne as PyramidOne
import Source.Graphics.PyramidTwo as PyramidTwo
from Source.Graphics.SpherePolar import SpherePolar
from Source.Graphics.SphereIcos import SphereIcos

from enum import IntEnum

class Renderer(QOpenGLWidget):
    class ActorType(IntEnum):
        CONE = 0,  
        CUBE = 1,
        CYLINDER = 2,
        FLOOR = 3, 
        ICOSAHEDRON = 4, 
        PYRAMID_1 = 5, 
        PYRAMID_2 = 6
        SPHERE_POLAR = 7,
        SPHERE_ICOS = 8,

    ## initialization
    def __init__(self, parent=None, **kwargs):
        """Initialize OpenGL version profile."""
        super(Renderer, self).__init__(parent)

        self._parent = parent

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

            self._initialized = True

            ###
            ### Creates Scenes
            ###
            SCENE = 0 #polar spheres
            #SCENE = 1 #tessalation spheres
            #SCENE = 2 #test scene
            if(SCENE == 0):
                xform1 = QMatrix4x4()
                xform2 = QMatrix4x4()
                xform3 = QMatrix4x4()
                xform1.translate(2.0, 0.0, 0.0)
                xform2.translate(-3.0, 0.0, 0.0)
                xform3.translate(0.0, 0.0, 0.0)
                self._actor1 = SpherePolar(self._world, 1.0, 7, 7, transform=xform1)
                self._actor2 = SpherePolar(self._world, 2.0, 12, 15, transform=xform2)
                self._actor3 = SpherePolar(self._world, 1.0, 40, 40, transform=xform3)
                self._world.addActor(self._actor1)
                self._world.addActor(self._actor2)
                self._world.addActor(self._actor3)
            elif(SCENE == 1):
                xform1 = QMatrix4x4()
                xform2 = QMatrix4x4()
                xform3 = QMatrix4x4()
                xform1.translate(2.0, 0.0, 0.0)
                xform2.translate(-3.0, 0.0, 0.0)
                xform3.translate(0.0, 0.0, 0.0)
                self._actor1 = SphereIcos(self._world, radius=1.0, innerLevel=2, outerLevel=2, transform=xform1, mode=GL.GL_PATCHES)
                self._actor2 = SphereIcos(self._world, radius=2.0, innerLevel=4, outerLevel=4, transform=xform2, mode=GL.GL_PATCHES)
                self._actor3 = SphereIcos(self._world, radius=1.0, innerLevel=5, outerLevel=5, transform=xform3, mode=GL.GL_PATCHES, colors=True)
                self._world.addActor(self._actor1)
                self._world.addActor(self._actor2)
                self._world.addActor(self._actor3)
            elif(SCENE == 2):
                xform1 = QMatrix4x4()
                xform1.translate(0.0, 0.0, 0.0)
                #self._actor1 = Icosahedron(self._world, transform=xform1, colors=True)
                self._actor1 = SphereIcos(self._world, radius=1.0,
                                    innerLevel=1, outerLevel=5, transform=xform1,
                                    mode=GL.GL_PATCHES, colors=True)
                self._world.addActor(self._actor1)

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
    

    def mousePressEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse click."""
        super(Renderer, self).mousePressEvent(event)
        
        if event.isAccepted():
            return

        if event.buttons() & Qt.LeftButton:
            self._trackball.press(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            self._trackball.start()
            event.accept()
            if not self.isAnimating():
                self.update()

        elif event.buttons() & Qt.RightButton:
            self.pan(self._pixelPosToViewPos(event.localPos()), state='start')
            self.update()


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


    def mouseReleaseEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse release."""
        super(Renderer, self).mouseReleaseEvent(event)
        
        if event.isAccepted():
            return

        if event.button() == Qt.LeftButton:
            self._trackball.release(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            event.accept()
            if not self.isAnimating():
                self._trackball.stop()
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
        self.makeCurrent()
        self.currentActor_.destroy()
        self._world.removeActor(self.currentActor_)

        xform = QMatrix4x4()        
        if index  == Renderer.ActorType.CONE:
            xform.translate(0, 1, 0)
            self.currentActor_ = Cone(self._world)
        elif index == Renderer.ActorType.CUBE:            
            xform.translate(0, 0.5, 0)
            self.currentActor_ = Cube(self._world, transform=xform)
        elif index == Renderer.ActorType.CYLINDER:
            xform.translate(0, 1, 0)
            self.currentActor_ = Cylinder(self._world, transform=xform)
        elif index == Renderer.ActorType.FLOOR:            
            self.currentActor_ = Floor(self._world, transform=xform)
        elif index == Renderer.ActorType.ICOSAHEDRON:
            xform.translate(0, -2.0, 0)
            self.currentActor_ = Icosahedron(self._world, transform=xform)
        elif index == Renderer.ActorType.PYRAMID_1:
            self.currentActor_ = PyramidOne.Pyramid(self._world)
        elif index == Renderer.ActorType.PYRAMID_2:
            self.currentActor_ = PyramidTwo.Pyramid(self._world)
        elif index == Renderer.ActorType.SPHERE_ICOS:
            self.currentActor_ = SphereIcos(self._world, radius=1.0, innerLevel=2, outerLevel=2, transform=xform, mode=GL.GL_PATCHES)
        elif index == Renderer.ActorType.SPHERE_POLAR:
            self.currentActor_ = SpherePolar(self._world, 1.0, 40, 40, transform=xform)
        self._world.addActor(self.currentActor_)
        

