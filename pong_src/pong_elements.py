#!/usr/bin python
from pyprocessing import *

class Ball:

	def __init__(self, x, y, scaleX, scaleY, speedX, speedY):
		self.x = x
		self.y = y
		self.scaleX = scaleX
		self.scaleY = scaleY
		self.speedX = speedX
		self.speedY = speedY

	def update(self):
		def collision():
			if self.y <= 0 + self.scaleY/2:
				self.speedY *= -1
			elif self.y >= height - self.scaleY/2:
				self.speedY *= -1 
		self.x += self.speedX
		self.y += self.speedY

		collision()

	def display(self):
		fill(255)
		ellipse(self.x, self.y, self.scaleX, self.scaleY)


class Racket:

	def __init__(self, x, y, scaleX, scaleY):
		self.x = x
		self.y = y
		self.scaleX = scaleX
		self.scaleY = scaleY

	def moveUp(self):
		self.y -= 20

	def moveDown(self):
		self.y += 20

	def display(self):
		fill(255)
		rect(self.x, self.y, self.scaleX, self.scaleY)
