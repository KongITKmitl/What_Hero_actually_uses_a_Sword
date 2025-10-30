from godot import exposed, export
from godot import *
from main.preload_resources import DialogueScene

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
		
		self.MCSprite = self.get_node('MCSprite')
		self.Sensei = self.get_node('Sensei')
		
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(0)
		
		self.monster = self.get_node('monster')
		self.dissapear = self.get_node('DissapearEffect')
		self.sdissapear = self.get_node('SenseiDissapearEffect')

	def done_dialogue(self):
		self.dissapear.play_animation()
		self.monster.queue_free()
		self.get_tree().create_timer(2).connect("timeout", self, "bf_change_scene")

		
	def bf_change_scene(self):
		self.MCSprite.move_to(700)
		
		self.Sensei.queue_free()
		self.sdissapear.play_animation()

		self.get_tree().create_timer(10).connect("timeout", self, "change_scene")
		
	def change_scene(self):
		self.get_tree().change_scene("res://main/VillageScene/VillageScene.tscn")
