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
		
		self.DialogueUI = ResourceLoader.load("res://main/UIscene/DialogueUI.tscn").instance()
		self.add_child(self.DialogueUI)
		
		self.TypingUI = self.get_node("TypingUI")
		pass

	def showUI(self,getdamage):
		self.DialogueUI.aftergameplay(getdamage)
		
	def send_damage(self,getdamage):
		self.healthbar = self.get_node("healthbar.tscn")
		self.healthbar.damage(getdamage)
