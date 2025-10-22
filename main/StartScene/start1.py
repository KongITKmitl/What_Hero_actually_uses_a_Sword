from godot import exposed, export
from godot import *


@exposed
class start1(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
	
	def _on_StartButton_pressed(self):
		self.get_tree().change_scene("res://main/WizardScene/WizardScene.tscn")
	
	def _on_QuitButton_pressed(self):
		self.get_tree().quit()

