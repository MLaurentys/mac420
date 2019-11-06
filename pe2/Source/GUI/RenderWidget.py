import os
import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Graphics.Renderer import Renderer

class RenderWidget(QWidget):

    def __init__(self, parent=None, **kwargs):
        super(RenderWidget, self).__init__(parent)

        self._font = kwargs.get("font", QFont())
        self.setFont(self._font)

        ## create render window
        self._parent = parent
        self._renderer = Renderer(self, antialiasing=True, **kwargs)

        self._mainLayout = QVBoxLayout()
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(3)

        ## create viewer
        self._mainLayout.addWidget(self._renderer)

        ## create bottom layout
        self._bottomLayout = QHBoxLayout()
        self._bottomLayout.setContentsMargins(3, 0, 3, 0)
        self._bottomLayout.setSpacing(3)

        ## create view sublayout
        self._viewLayout = QHBoxLayout()
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.setSpacing(3)

        # Adding actor selector
        label = QLabel("Object Sources: ")
        self._bottomLayout.addWidget(label)
        self.actorCombo = QComboBox()
        self.actorCombo.currentIndexChanged.connect(self._renderer.changeActor)
        self._bottomLayout.addWidget(self.actorCombo)
        self.actorCombo.addItem("Select To Create")
        #gets list of available objects
        files = []
        available = []
        o_dir = "obj-models/buildings/"
        for file in os.listdir(o_dir):
            if (file.endswith(".obj")):
                if (file.strip("obj") + "mtl" in files):
                    available.append(file.strip(".obj"))
                else:
                    files.append(file)
            elif (file.endswith(".mtl")):
                if (file.strip("mtl") + "obj" in files):
                    available.append(file.strip(".mtl"))
                else:
                    files.append(file)
        available = list(set(available))
        for i in range(len(available)): self.actorCombo.addItem(available[i])
        #for i in range(len(available)): available[i] = o_dir + available[i] + ".obj"
        self._renderer.setActors(available)
        ## register view functions
        self._viewFunc = [
            self._renderer.viewLeft,
            self._renderer.viewRight,
            self._renderer.viewTop,
            self._renderer.viewBottom,
            self._renderer.viewFront,
            self._renderer.viewBack]

        label = QLabel("Axis: ")
        label.setFont(self._font)
        self._viewLayout.addWidget(label)
        self._viewCombo = QComboBox(self)
        self._viewCombo.addItem("+x")
        self._viewCombo.addItem("-x")
        self._viewCombo.addItem("+y")
        self._viewCombo.addItem("-y")
        self._viewCombo.addItem("+z")
        self._viewCombo.addItem("-z")
        self._viewCombo.setFont(self._font)
        self._viewCombo.activated.connect(self.viewDirectionChanged)
        self._viewLayout.addWidget(self._viewCombo)

        self._bottomLayout.addLayout(self._viewLayout)

        ## create camera sublayout
        self._cameraLayout = QHBoxLayout()
        self._cameraLayout.setContentsMargins(0, 0, 5, 0)
        self._cameraLayout.setSpacing(3)

        label = QLabel(" Camera: ")
        label.setFont(self._font)
        self._cameraLayout.addWidget(label)
        self._cameraLensCombo = QComboBox(self)
        self._cameraLensCombo.addItem("Perspective")
        self._cameraLensCombo.addItem("Ortographic")
        self._cameraLensCombo.setFont(self._font)
        self._cameraLensCombo.activated.connect(self._renderer.cameraLensChanged)
        self._cameraLayout.addWidget(self._cameraLensCombo)

        self._cameraCombo = QComboBox(self)
        self._cameraCombo.addItem("Store")
        self._cameraCombo.addItem("Recall")
        self._cameraCombo.addItem("Reset")
        self._cameraCombo.setFont(self._font)
        self._cameraCombo.activated.connect(self.cameraOperationChanged)
        self._cameraLayout.addWidget(self._cameraCombo)

        self._bottomLayout.addLayout(self._cameraLayout)

        self._renderLayout = QHBoxLayout()
        self._renderLayout.setContentsMargins(0, 0, 5, 0)
        self._renderLayout.setSpacing(3)
        label = QLabel(" Style: ")
        label.setFont(self._font)
        self._renderLayout.addWidget(label)
        self._drawStyleCombo = QComboBox(self)
        self._drawStyleCombo.addItem("Points")
        self._drawStyleCombo.addItem("Wireframe")
        self._drawStyleCombo.addItem("Solid")
        self._drawStyleCombo.addItem("Solid with edges")
        self._drawStyleCombo.setFont(self._font)
        self._drawStyleCombo.activated.connect(self._renderer.drawStyleChanged)
        self._drawStyleCombo.setCurrentIndex(2)
        self._renderLayout.addWidget(self._drawStyleCombo)

        label = QLabel(" Quality: ")
        label.setFont(self._font)
        self._renderLayout.addWidget(label)
        self._shadingCombo = QComboBox(self)
        self._shadingCombo.addItem("Low")
        self._shadingCombo.addItem("High")
        self._shadingCombo.setFont(self._font)
        self._shadingCombo.activated.connect(self._renderer.shadingChanged)
        self._shadingCombo.setCurrentIndex(1)
        self._renderLayout.addWidget(self._shadingCombo)

        self._bottomLayout.addLayout(self._renderLayout)

        menu = QMenu()
        menu.setFont(self._font)
        lightingAction = QAction("Lighting", self)
        lightingAction.setCheckable(True)
        lightingAction.setChecked(True)
        lightingAction.triggered.connect(self._renderer.lightingChanged)
        menu.addAction(lightingAction)        
        
        profilingAction = QAction("Profiling", self)
        profilingAction.setCheckable(True)
        profilingAction.setChecked(True)  
        profilingAction.triggered.connect(self.profilingChanged)         
        menu.addAction(profilingAction)
        
        menu.addSeparator() 
        animateAction = QAction("Animate", self)
        animateAction.setCheckable(True)
        animateAction.setChecked(False)
        animateAction.triggered.connect(self.animateChanged)                  
        menu.addAction(animateAction)       

        self._options = QPushButton()
        self._options.setText("Options")
        self._options.setFont(self._font)
        self._options.setMenu(menu)
        self._renderLayout.addWidget(self._options)


        self._delete = QPushButton()
        self._delete.setText("Delete")
        self._delete.setFont(self._font)
        self._renderLayout.addWidget(self._delete)
        self._delete.clicked.connect(self.delActor)
        self._delete.setDisabled(True)
        
        self._bottomLayout.addStretch(1)

        self._mainLayout.addLayout(self._bottomLayout)
        self.setLayout(self._mainLayout)

    def mousePressEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse click."""
        print("MOUSE")
        super(RenderWidget, self).mousePressEvent(event)
        if event.isAccepted():
            return
        render = self._renderer
        if event.buttons() & Qt.LeftButton:
            point = render._pixelPosToViewPos(event.localPos())
            render._trackball.press(point, QQuaternion())
            render._trackball.start()
            event.accept()
            if not render.isAnimating():
                render.update()
            if (render._shift_isPressed):
                wd = render._world
                ob = wd.pick(point)
                if (ob[0] != None):
                    if (wd.selectedActor() == None):
                        self._delete.setDisabled(False)
                    wd.selectActor(ob[0])
                    render.currentActor_ = ob[0]
                    print("AEE")
                else:
                    if (wd.selectedActor() != None):
                        self._delete.setDisabled(True)
                        wd.selectActor(None)
                        render.currentActor_ = None
                    print("nops")
                print("ok")
        elif event.buttons() & Qt.RightButton:
            render.pan(render._pixelPosToViewPos(event.localPos()), state='start')
            render.update()

    def keyPressEvent(self, QKeyEvent):
        super(RenderWidget, self).keyPressEvent(QKeyEvent)
        if (QKeyEvent.key() == Qt.Key_Shift):
            self._renderer.shiftPressed()
    def keyReleaseEvent(self, QKeyEvent):
        super(RenderWidget, self).keyReleaseEvent(QKeyEvent)
        if (QKeyEvent.key() == Qt.Key_Shift):
            self._renderer.shiftReleased()
        
    def delActor(self):
        self._delete.setDisabled(False)
        self._renderer.delActor()

    def clear(self):
        """Clear viewer"""
        self._renderer.clear()


    def updateViewer(self):
        """Refresh viewer"""
        self._renderer.update()


    def viewDirectionChanged(self, index):
        """Called upon a change in view direction"""
        self._viewFunc[index]()


    def cameraOperationChanged(self, index):
        """Called upon a chnage in camera operation"""
        if index == 0:
            self.storeViewerCamera()
        elif index == 1:
            self.recallViewerCamera()
        else:
            self.resetViewerCamera()


    def storeViewerCamera(self):
        """Ask the the viewer to store active camera parameters"""
        self._renderer.storeCamera()


    def recallViewerCamera(self):
        """Ask the viewer to recall previously stored camera parameters"""
        self._renderer.recallCamera()
        self._cameraLensCombo.setCurrentIndex(self._renderer.activeSceneCamera().lens)


    def resetViewerCamera(self):
        """Ask viewer to reset the active camera parameters"""
        self._renderer.resetCamera()
        self._cameraLensCombo.setCurrentIndex(self._renderer.activeSceneCamera().lens)


    def profilingChanged(self, state):
        """Turn on or off rendering profiling"""
        if state:
            self._renderer.enableProfiling(True)
            self._parent.restartTimer()
        else:
            self._renderer.enableProfiling(False)
            self._parent.stopTimer()
            self._parent.clearStatistics()


    def animateChanged(self, state):
        """Turn on or off animation"""
        self._renderer.enableAnimation(state)


    def renderTimeEstimates(self):
        """Ask viewer for current render time estimates"""
        return self._renderer.renderTimeEstimates()


    def sizeHint(self):
        return QSize(1280, 800)





