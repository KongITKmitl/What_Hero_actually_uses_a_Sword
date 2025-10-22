from godot import exposed, export
from godot import *
from ..preload_resources import DialogueScene

@exposed
class Farmscene(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		# รอ plugin init เสร็จก่อน
		self.get_tree().create_timer(0.2).connect("timeout", self, "_load_ui")

	def _load_ui(self):
		self.DialogueUI = DialogueScene.instance()  # instance จะ bind Python class
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(38)     
	def changescene(self):
		self.get_tree().change_scene("res://main/FarmScene/Farmscene.tscn")
