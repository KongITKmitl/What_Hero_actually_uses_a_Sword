
from godot import *
from ..preload_resources import DialogueScene

@exposed
class VillageScene(Node2D):

	def _ready(self):
		# รอ plugin init เสร็จก่อน
		self.get_tree().create_timer(2).connect("timeout", self, "_load_ui")

	def _load_ui(self):
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(22)     
	def changescene(self):
		self.get_tree().change_scene("res://main/FarmScene/Farmscene.tscn")
