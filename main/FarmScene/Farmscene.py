from godot import exposed, export
from godot import *
from main.preload_resources import DialogueScene
@exposed
class Farmscene(Node2D):

	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.MCSprite = self.get_node("MCSprite")
		self.MCSprite.play("walk")
		self.MCSprite.move_to(212)
		#print(type(self.MCSprite))
		
		#บาทหลวงเดินเข้ามา
		self.priest = self.get_node("priest")
		self.priest.move_to(152)
		
		self.snake = self.get_node('snake')
		self.dissapear = self.get_node('DissapearEffect')
		self.get_tree().create_timer(4).connect("timeout", self, "showmonster")
		

	def showmonster(self):
		self.snake.move_to_y(252)
		self.get_tree().create_timer(2).connect("timeout", self, "start_dialogue")
		
	def start_dialogue(self):
		# โหลด DialogueScene จากไฟล์ tscn โดยตรง
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(38)   

	def done_dialogue(self):
		self.dissapear.play_animation()
		self.snake.queue_free()
		
		self.priest.move_to(700)
		self.MCSprite.move_to(700)
		self.get_tree().create_timer(10).connect("timeout", self, "change_scene")
		
	def change_scene(self):
		self.get_tree().change_scene("res://main/ForestScene/forestscene.tscn")
