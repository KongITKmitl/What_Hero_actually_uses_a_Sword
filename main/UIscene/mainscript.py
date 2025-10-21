from godot import exposed, export
from godot import *


@exposed
class mainscript(Node):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def main():
			healthbar = ResourceLoader.load("res://main/UIscene/healthbar.tscn").instance()
			self.get_tree().get_root().add_child(healthbar)
			
			typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
			self.get_tree().get_root().add_child(typingUI)
			
			
