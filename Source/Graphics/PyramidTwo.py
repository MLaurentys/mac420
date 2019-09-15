import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Pyramid(Actor):
	def __init__(self, renderer, **kwargs):
		super(Pyramid, self).__init__(renderer, **kwargs)

		self.height_ = kwargs.get("height", 1.0)

		self.vertices_ = None
		self.initialize()

	def generateGeometry(self):
		h = self.height_

		vertices = [
			# BASE
			-0.5, 0.0, -0.5,	 0.5, 0.0, -0.5,  -0.5, 0.0,  0.5,
			 0.5, 0.0, -0.5,	 0.5, 0.0,  0.5,  -0.5, 0.0,  0.5,	
			# TOP 
			-0.5, 0.0, -0.5,  -0.5, 0.0,  0.5,     0,   h,    0,
			-0.5, 0.0, -0.5,   0.5, 0.0, -0.5,     0,   h,    0,
			 0.5, 0.0, -0.5,   0.5, 0.0,  0.5,     0,   h,    0,
			 0.5, 0.0,  0.5,  -0.5, 0.0,  0.5,     0,   h,    0
		]

		normals = [
			# BASE
			0, -1, 0,     0, -1, 0,   0, -1, 0,
			0, -1, 0,     0, -1, 0,   0, -1, 0,
			# TOP
			-1, 0, 0,    -1, 0, 0,   -1, 0, 0,
			 0, 0,-1,     0, 0,-1,    0, 0,-1,
			 1, 0, 0,     1, 0, 0,    1, 0, 0,
			 0, 0, 1,     0, 0, 1,    0, 0, 1 ]

		self.vertices_ = np.array(vertices, np.float32)
		self.normals_ = np.array(normals, np.float32)		
		
	def initialize(self):
		if self.vertices_ is None:
			self.generateGeometry()

		self.create(self.vertices_, normals=self.normals_)

	def render(self):
		GL.glDrawArrays(self._render_mode, 0, len(self.vertices_))

		self._normal_visualizing_shader.bind()
		self._normal_visualizing_shader.setUniformValue("modelMatrix", self._transform)
		self._normal_visualizing_shader.setUniformValue("viewMatrix", self._scene.camera.viewMatrix)
		self._normal_visualizing_shader.setUniformValue("projectionMatrix", self._scene.camera.projectionMatrix)
		self._normal_visualizing_shader.setUniformValue("normalMatrix", self._transform.normalMatrix())
		
		GL.glDrawArrays(self._render_mode, 0, len(self.vertices_))
		self._normal_visualizing_shader.release()
