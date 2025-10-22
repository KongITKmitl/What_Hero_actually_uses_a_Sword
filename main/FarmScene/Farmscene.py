from godot import exposed, export
from godot import *

@exposed
class Farmscene(Node2D):

	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.get_tree().create_timer(0.2).connect("timeout", self, "_load_ui")

	def _load_ui(self):
		# โหลด DialogueScene จากไฟล์ tscn โดยตรง
		dialogue_scene_res = ResourceLoader.load("res://main/UIscene/DialogueScene.tscn")
		if dialogue_scene_res:
			dialogue_scene = dialogue_scene_res.instance()
			self.add_child(dialogue_scene)

			# ตรวจว่า node มีฟังก์ชัน setup_dialogue ก่อนเรียก
			if hasattr(dialogue_scene, "setup_dialogue"):
				dialogue_scene.setup_dialogue(38)
		else:
			print("❌ ไม่พบ DialogueScene.tscn ที่ระบุไว้!")

	def changescene(self):
		self.get_tree().change_scene("res://main/FarmScene/Farmscene.tscn")
