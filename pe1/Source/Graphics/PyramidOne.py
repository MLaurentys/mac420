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
		vertices = [
			-0.5, 0.0, -0.5,
			 0.5, 0.0, -0.5,
			-0.5, 0.0,  0.5,
			 0.5, 0.0,  0.5,
			 0.0, self.height_, 0.0]

		normals = [
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, +1.0, 0.0]

		indices = [ 
			0, 1, 2,   1, 2, 3,  # base
			0, 2, 4,   0, 1, 4,   1, 3, 4,    2, 3, 4  # top
		]

		self.vertices_ = np.array(vertices, np.float32)
		self.normals_ = np.array(normals, np.float32)		
		self.indices_ = np.array(indices, np.uint32)


	def initialize(self):
		if self.vertices_ is None:
			self.generateGeometry()

		self.create(self.vertices_, normals=self.normals_, indices=self.indices_)

	def render(self):
		GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Pyramid(Actor):
	def __init__(self, renderer, **kwargs):
		super(Pyramid, self).__init__(renderer, **kwargs)

		self.height_ = kwargs.get("height", 1.0)

		self.vertices_ = None
		self.initialize()

	def generateGeometry(self):
		vertices = [
			-0.5, 0.0, -0.5,
			 0.5, 0.0, -0.5,
			-0.5, 0.0,  0.5,
			 0.5, 0.0,  0.5,
			 0.0, self.height_, 0.0]

		normals = [
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, -1.0, 0.0,
			0.0, +1.0, 0.0]

		indices = [ 
			0, 1, 2,   1, 2, 3,  # base
			0, 2, 4,   0, 1, 4,   1, 3, 4,    2, 3, 4  # top
		]

		self.vertices_ = np.array(vertices, np.float32)
		self.normals_ = np.array(normals, np.float32)		
		self.indices_ = np.array(indices, np.uint32)


	def initialize(self):
		if self.vertices_ is None:
			self.generateGeometry()

		self.create(self.vertices_, normals=self.normals_, indices=self.indices_)

	def render(self):
		GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)