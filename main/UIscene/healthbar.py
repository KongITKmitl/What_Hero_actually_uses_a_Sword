from godot import exposed, export
from godot import *

# ตารางค่าพลังชีวิตของมอนสเตอร์แต่ละเลเวล
monster_healthlist = {
	1: 800,
	2: 1600,
	3: 3200,
	4: 4800,
	5: 8000,
	6: 12000,
	7: 15000
}

# ตัวแปรระดับมอนสเตอร์ปัจจุบัน
base_mon = 1

@exposed
class healthbar(Control):

	def _ready(self):
		global base_mon
		print("[LOG] _ready() called — base_mon =", base_mon)
		self.DialogueUI = self.get_tree().get_current_scene().get_node('dialogueUI')

		self.monEffect = self.get_tree().get_current_scene().get_node('MonsterDMG_effect') #Node ของที่แสดง Effect monster ตอนถูกโจมตี
		
		# รีเซ็ตค่าพลังชีวิตทุกครั้งที่ Scene โหลด
		self.monster_health = monster_healthlist[base_mon]
		self.mc_health = ((monster_healthlist[base_mon]) / 4) * 5
		self.pending_mc_damage = 0

		print(f"[LOG] Reset monster_health={self.monster_health}, mc_health={self.mc_health}")

		# ProgressBar ของมอน
		self.progress_bar = self.get_node("MonsterBar")
		self.progress_bar.max_value = self.monster_health
		self.progress_bar.value = self.monster_health

		# ProgressBar ของ MC
		self.mcprogress_bar = self.get_node("MCHealthBar")
		self.mcprogress_bar.max_value = self.mc_health
		self.mcprogress_bar.value = self.mc_health

		# Label DIE
		self.die_lable = self.get_node("DIE")
		self.die_lable.hide()

		# Timer ดีเลย์ลดเลือด MC
		self.delay_timer = self.get_node("Delay")
		self.delay_timer.connect("timeout", self, "_on_delay_timeout")
		self.delay_timer.stop()

		print("[LOG] Ready complete")

	def take_damage(self, damage):
		global base_mon
		print(f"[LOG] take_damage() called — damage = {damage}")

		prev_health = self.monster_health
		self.monster_health -= damage
		self.progress_bar.value = max(self.monster_health, 0)

		self.monEffect.play_animation() #แสดง animation มอนเต้อถูกโจมตี

		actual_damage = prev_health - self.monster_health
		self.pending_mc_damage += actual_damage * 2
		print(f"[LOG] actual_damage={actual_damage}, pending_mc_damage now = {self.pending_mc_damage}")

		if self.delay_timer.is_stopped():
			print("[LOG] Starting delay_timer for MC damage")
			self.delay_timer.start(1.5)

		if self.monster_health <= 0:
			self.monster_health = 0
			print("[LOG] Monster died — calling DialogueUI.aftergameplay() and queue_free()")
			self.DialogueUI.aftergameplay()
			self.queue_free()
			print("monster_die")

		print(f"[LOG] end of take_damage — monster_health = {self.monster_health}")

	def _on_delay_timeout(self):
		print("[LOG] _on_delay_timeout() fired")
		self.delay_timer.stop()

		self.mc_health -= self.pending_mc_damage
		print(f"[LOG] MC health reduced by pending_mc_damage => mc_health now {self.mc_health}")
		self.pending_mc_damage = 0

		self.heal_mc_if_low()

		self.mcprogress_bar.value = max(self.mc_health, 0)
		print(f"[LOG] MC progress bar set => {self.mcprogress_bar.value}")

		if self.mc_health <= 0:
			self.mc_health = 0
			self.die_lable.show()
			print("[LOG] MC died — showing DIE label and changing scene")
			self._on_die_timeout()
		else:
			if self.monster_health > 0:
				print("[LOG] MC alive & monster still alive — spawn typing UI")
				self.spawn_typing_ui()

	def heal_mc_if_low(self):
		if self.mc_health <= 100:
			max_mc_health = ((monster_healthlist[base_mon]) / 4) * 5
			heal_amount = max_mc_health * 0.1
			self.mc_health += heal_amount
			print(f"[LOG] MC HP restored by 10% => heal_amount = {heal_amount}, mc_health now {self.mc_health}")

	def _on_die_timeout(self):
		global base_mon
		print(f"[LOG] _on_die_timeout() — resetting base_mon from {base_mon} to 1, then changing scene")
		base_mon = 1
		self.get_tree().change_scene("res://main/StartScene/start1.tscn")
		self.queue_free()

	def spawn_typing_ui(self):
		print("[LOG] spawn_typing_ui() called")
		typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
		self.get_tree().get_root().add_child(typingUI)
		print("next_damage")
