from godot import exposed, export
from godot import *
@exposed
class Start1(Node2D):

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.sound = self.get_node('buttonSound')
		pass
	
	def _on_StartButton_pressed(self):
		self.sound.play()
		self.get_tree().create_timer(0.7).connect("timeout", self, "start")
		
	def start(self):
		self.get_tree().change_scene("res://main/WizardScene/WizardScene.tscn")
	
	def _on_QuitButton_pressed(self):
		self.get_tree().quit()

