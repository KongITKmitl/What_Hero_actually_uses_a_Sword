from godot import exposed
from godot import *
import random

@exposed
class EffectPlayer(AnimatedSprite):

	def _ready(self):
		self.hide()

	def play_animation(self):
		if not self.frames:
			return

		# get all animation names
		animations = self.frames.get_animation_names()
		self.animation = random.choice(animations)
		self.show()
		self.play()

		self.connect("animation_finished", self, "finished")

	def finished(self):
		self.disconnect("animation_finished", self, "finished")
		self.hide()
