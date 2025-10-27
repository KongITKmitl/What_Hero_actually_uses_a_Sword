from godot import exposed, export
from godot import *

monster_healthlist = {
		1:800,
		2:1600,
		3:3200,
		4:4800,
		5:8000,
		6:12000,
		7:15000
	}
base_mon = 1

@exposed
class healthbar(Control):
	def _ready(self):
		global base_mon
		
		self.DialogueUI = self.get_tree().get_current_scene().get_node('dialogueUI')
		
		self.progress_bar = self.get_node("MonsterBar")
		self.monster_health = monster_healthlist[base_mon]
		self.progress_bar.max_value = monster_healthlist[base_mon]
		self.progress_bar.value = monster_healthlist[base_mon]

		self.mcprogress_bar = self.get_node("MCHealthBar")
		self.mc_health = ((monster_healthlist[base_mon]) / 4) * 5
		self.mcprogress_bar.max_value = ((monster_healthlist[base_mon]) / 4) * 5
		self.mcprogress_bar.value = ((monster_healthlist[base_mon]) / 4) * 5

		self.monEffect = self.get_tree().get_current_scene().get_node('MonsterDMG_effect') #Node ของที่แสดง Effect monster ตอนถูกโจมตี

	def take_damage(self, damage):
		global base_mon
		self.monster_health -= damage
		self.mc_health -= damage + (0.03 * damage)

		if self.monster_health < 0:
			self.monster_health = 0
			
			self.DialogueUI.aftergameplay()
			self.queue_free()

		elif self.mc_health < 0:
			self.mc_health = 0
			self.get_tree().change_scene("res://main/VillageScene/VillageScene.tscn")
			
		self.update_health_bar()
		
		self.monEffect.play_animation() #แสดง animation มอนเต้อถูกโจมตี

		print(f"💥Monster HP = {self.monster_health}")
		print(f"💥MC HP = {self.mc_health}")
		
		if self.monster_health > 0:
			self.update_health_bar()
			self.spawn_typing_ui()
		else:
			base_mon += 1
			print("monster_die")
			
	def update_health_bar(self):
		# อัปเดตค่าหลอดเลือดใน ProgressBar
		self.progress_bar.value = self.monster_health
		self.mcprogress_bar.value = self.mc_health
	
	def spawn_typing_ui(self):
		typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
		self.get_tree().get_root().add_child(typingUI)
		print("next_damage")
