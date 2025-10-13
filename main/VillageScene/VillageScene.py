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
		pass
	
	def _on_TestGameplayButton_pressed(self):
		self.get_node("TestGameplayButton").hide()
		typingUI = ResourceLoader.load("res://main/Test(AnythingRandomGoesHere)/TypingUI.tscn").instance()
		self.add_child(typingUI)

		
