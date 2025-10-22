from godot import exposed, export
from godot import *
from ..preload_resources import DialogueScene

@exposed
class WizardScene(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(0)
		
		
	def changescene(self):
		self.get_tree().change_scene("res://main/VillageScene/VillageScene.tscn")
