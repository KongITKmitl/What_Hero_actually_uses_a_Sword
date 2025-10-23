from godot import ResourceLoader
from main.preload_resources3 import healthbar, typingUI
def get_healthbar():
	return healthbar

def get_typing_ui():
	return typingUI
	
print("helth:" , healthbar , "tping" , typingUI)
