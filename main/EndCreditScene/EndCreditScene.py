from godot import exposed, export
from godot import *


@exposed
class EndCreditScene(Node2D):

	speed = export(float, default=50.0)
	target_y = export(float, default=-1500.0)

	def _ready(self):
		self.content = self.get_node("content")
		self.start_y = self.content.rect_position.y
		self.set_process(True)

	def _process(self, delta):
		pos = self.content.rect_position
		if pos.y > self.target_y:
			pos.y -= self.speed * delta
			self.content.rect_position = pos
		else:
			self.end()
			self.queue_free()
	
	def end(self):
		self.get_tree().change_scene("res://main/StartScene/start1.tscn")
