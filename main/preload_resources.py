from godot import ResourceLoader

# preload tscn ตอน import module
DialogueScene = ResourceLoader.load("res://main/UIscene/DialogueUI.tscn")

print("DialogueScene:", DialogueScene)

