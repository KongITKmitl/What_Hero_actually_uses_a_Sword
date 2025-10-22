from godot import ResourceLoader
def get_healthbar():
	return ResourceLoader.load("res://main/UIscene/healthbar.tscn")

def get_typing_ui():
	return ResourceLoader.load("res://main/UIscene/TypingUI.tscn")
