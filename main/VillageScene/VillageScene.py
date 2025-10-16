from godot import exposed, export
from godot import *


@exposed
class VillageScene(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""	
		
		DialogueUI = ResourceLoader.load("res://main/UIscene/DialogueUI.tscn").instance()
		self.add_child(DialogueUI)


		pass

	
