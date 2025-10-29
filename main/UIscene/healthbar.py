from godot import exposed, export
from godot import *

# -------------------------------
# ตารางเลือดของมอนสเตอร์แต่ละเลเวล
# -------------------------------
monster_healthlist = {
	1: 800,
	2: 1600,
	3: 3200,
	4: 4800,
	5: 8000,
	6: 12000,
	7: 15000
}

# ตัวแปรเก็บเลเวลของมอนสเตอร์ปัจจุบัน (ใช้ร่วมกันทุกซีน)
base_mon = 1

@exposed
class healthbar(Control):
	"""สคริปต์ healthbar ใช้ควบคุมระบบเลือดของมอนสเตอร์และผู้เล่น"""

	def _ready(self):
		global base_mon
		print("[LOG] _ready() called — base_mon =", base_mon)

		# ดึง node ที่จำเป็นจากซีนหลัก
		self.DialogueUI = self.get_tree().get_current_scene().get_node('dialogueUI')
		self.monEffect = self.get_tree().get_current_scene().get_node('MonsterDMG_effect')

		# รีเซ็ตค่าพลังชีวิตเริ่มต้น
		self.monster_health = monster_healthlist[base_mon]
		self.mc_health = ((monster_healthlist[base_mon]) / 4) * 5  # MC มีเลือดมากกว่ามอน
		self.pending_mc_damage = 0

		# ProgressBar ของมอนสเตอร์
		self.progress_bar = self.get_node("MonsterBar")
		self.progress_bar.max_value = self.monster_health
		self.progress_bar.value = self.monster_health

		# ProgressBar ของ MC
		self.mcprogress_bar = self.get_node("MCHealthBar")
		self.mcprogress_bar.max_value = self.mc_health
		self.mcprogress_bar.value = self.mc_health

		# Label "DIE" สำหรับตอน MC ตาย
		self.die_lable = self.get_node("DIE")
		self.die_lable.hide()

		# Timer ดีเลย์หักเลือด MC หลังมอนโดนโจมตี
		self.delay_timer = self.get_node("Delay")
		self.delay_timer.connect("timeout", self, "_on_delay_timeout")
		self.delay_timer.stop()

		print("[LOG] Ready complete")

	def take_damage(self, damage):
		"""เรียกตอนมอนโดนโจมตี"""
		global base_mon
		prev_health = self.monster_health
		self.monster_health -= damage
		self.progress_bar.value = max(self.monster_health, 0)

		# แสดงอนิเมชันมอนโดนตี
		self.monEffect.play_animation()

		# ดาเมจที่ MC จะได้รับ = ดาเมจจริงที่มอนโดน × 1.5
		actual_damage = prev_health - self.monster_health
		self.pending_mc_damage += actual_damage * 1.5

		# ถ้ายังไม่มี timer ให้เริ่มนับดีเลย์
		if self.delay_timer.is_stopped():
			self.delay_timer.start(1.5)

		# ถ้ามอนตาย
		if self.monster_health <= 0:
			self.monster_health = 0
			self.DialogueUI.aftergameplay()  # แจ้งจบฉากการต่อสู้
			self.queue_free()  # ลบ healthbar ออกจากซีน
			base_mon += 1
			print("monster_die")

	def _on_delay_timeout(self):
		"""เรียกเมื่อครบเวลา delay จะเอา damage ที่ค้างไว้ไปหักเลือด MC"""
		self.delay_timer.stop()
		self.mc_health -= self.pending_mc_damage
		self.pending_mc_damage = 0

		# ดีเลย์ 2 วิ ก่อนฮีล
		self.get_tree().create_timer(2.0).connect("timeout", self, "_on_heal_delay")

		self.mcprogress_bar.value = max(self.mc_health, 0)

		# ถ้า MC ตาย
		if self.mc_health <= 0:
			self.mc_health = 0
			self.die_lable.show()  # แสดงคำว่า DIE
			print("[LOG] MC died — showing DIE label, will wait 3s then change scene")
			self.get_tree().create_timer(3.0).connect("timeout", self, "_on_die_timeout")
		else:
			# ถ้ายังไม่ตาย ให้สร้าง UI พิมพ์ใหม่
			if self.monster_health > 0:
				self.spawn_typing_ui()

	def _on_heal_delay(self):
		"""หลังดีเลย์ 2 วิ จะค่อยเรียกฮีล"""
		self.heal_mc_if_low()

	def heal_mc_if_low(self):
		"""ฮีล MC ถ้าเลือดเหลือน้อยกว่า 100"""
		if 1 <= self.mc_health <= 100:
			max_mc_health = ((monster_healthlist[base_mon]) / 4) * 5
			heal_amount = max_mc_health * 0.32
			self.mc_health += heal_amount
			print(f"[LOG] MC healed after 2s delay — heal +{heal_amount}, new HP = {self.mc_health}")
			self.mcprogress_bar.value = min(self.mc_health, self.mcprogress_bar.max_value)

	def _on_die_timeout(self):
		"""หลังจากดีเลย์ 3 วิ จะรีเซ็ต base_mon และเปลี่ยนซีนกลับไปเริ่มต้น"""
		global base_mon
		base_mon = 1
		self.get_tree().change_scene("res://main/StartScene/start1.tscn")
		self.queue_free()

	def spawn_typing_ui(self):
		"""สร้าง UI พิมพ์ (TypingUI) ขึ้นมาใหม่"""
		typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
		self.get_tree().get_root().add_child(typingUI)
