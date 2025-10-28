from godot import exposed, export
from godot import *
from ..preload_resources import DialogueScene
@exposed
class BossScene(Node2D):

	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.MCSprite = self.get_node("MCSprite")
		self.MCSprite.move_to(212)
		#print(type(self.MCSprite))
		
		#บาทหลวงเดินเข้ามา
		self.priest = self.get_node("priest")
		self.priest.move_to(152)
		
		self.monster = self.get_node('monster')
		
		self.camera = self.get_node('Camera2D')

		self.get_tree().create_timer(5).connect("timeout", self, "start_dialogue")
		
		

	def showmonster(self):
		self.monster.move_to_y(252)
		self.get_tree().create_timer(2).connect("timeout", self, "start_dialogue")
		
	def start_dialogue(self):
		self.DialogueUI = DialogueScene.instance()
		
  
		print(type(self.DialogueUI))

		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(66)   

	def done_dialogue(self):
		self.change_scene()
		
	def change_scene(self):
		self.get_tree().change_scene("res://main/EndingScene/EndingScene.tscn")
	
	def pan_camera(self):
		self.camera.move_to(100,False,120)
		self.get_tree().create_timer(4).connect("timeout", self, "reset_camera")
	def reset_camera(self):
		self.camera.move_to(0,False,120)

