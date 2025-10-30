from godot import exposed, export
from godot import *
from main.preload_resources import DialogueScene

@exposed
class EndingScene(Node2D):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.Bprincess = self.get_node('Bprincess')
		self.Bpriest = self.get_node('Bpriest')
		pass

	def _on_Bprincess_button_down(self):
		self.chose = 106
		self.get_tree().create_timer(0.5).connect("timeout", self, "start_dialogue")
	
	def _on_Bpriest_button_down(self):
		self.chose = 120
		self.get_tree().create_timer(0,5).connect("timeout", self, "start_dialogue")
		
	def start_dialogue(self):
		self.Bprincess.queue_free()
		self.Bpriest.queue_free()
		
		self.DialogueUI = DialogueScene.instance()
		print(self.DialogueUI)
		self.add_child(self.DialogueUI)
		self.DialogueUI.setup_dialogue(self.chose)   

	def done_dialogue(self):
		self.change_scene()
		
	def change_scene(self):
		self.get_tree().change_scene("res://main/EndCreditScene/EndCreditScene.tscn")
