from godot import exposed, export
from godot import *


@exposed
class healthbar(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	hp = 100

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
	def damage(self,damage):
		hp -= damage
		print(damage)
