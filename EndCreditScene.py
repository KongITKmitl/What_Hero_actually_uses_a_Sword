from godot import exposed, export
from godot import *


@exposed
class EndCreditScene(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		
		self.content = self.get_node('content')
		self.content.move_to_y(-1300)
		self.get_tree().create_timer(15).connect("timeout", self, "end")
	
		pass
	
	def end(self):
		self.get_tree().change_scene("res://main/StartScene/start1.tscn")
