
from godot import *
from main.preload_resources import DialogueScene
@exposed
class VillageScene(Node2D):
	speed = 50
	def _ready(self):
		# รอ plugin init เสร็จก่อน
		
		#MC เดินเข้ามา
		self.MCSprite = self.get_node("MCSprite")
		self.MCSprite.move_to(250)
		#print(type(self.MCSprite))
		
		#บาทหลวงเดินเข้ามา
		self.priest = self.get_node("priest")
		self.priest.move_to(300)

		self.get_tree().create_timer(10).connect("timeout", self, "start_dialogue")
		
	def start_dialogue(self):
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(22)     
		
		
	def done_dialogue(self):
		self.get_tree().create_timer(10).connect("timeout", self, "change_scene")
		self.MCSprite.move_to(700)
		self.get_tree().create_timer(2).connect("timeout", self, "wait_walk")
		
		
	def change_scene(self):
		self.get_tree().change_scene("res://main/FarmScene/Farmscene.tscn")
		
	def wait_walk(self):
		self.priest.move_to(700,True)
