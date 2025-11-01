from godot import exposed, export
from godot import *
from godot import AnimatedSprite

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
		self.playerEffect = self.get_tree().get_current_scene().get_node('PlayerDMG_effect')
		self.healEffect = self.get_tree().get_current_scene().get_node('PlayerHEAL_effect')

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
		
		# เสียงทั้งหมด
		self.mc_die_sound = self.get_node("mc_die")
		self.mon_damage = self.get_node("montakedamage")   # เสียงมอนโดนโจมตี
		self.mc_damage = self.get_node("mctakedamage")     # เสียง MC โดนโจมตี
		self.priest_heal = self.get_node("heal")           # เสียงตอนฮีล

		print("[LOG] Ready complete")


	def take_damage(self, damage):
		global base_mon
		prev_health = self.monster_health
		self.monster_health -= damage
		self.progress_bar.value = max(self.monster_health, 0)

		# เอฟเฟกต์และเสียงตอนมอนโดนโจมตี
		self.monEffect.play_animation()
		self.mon_damage.play()
		print(f"[LOG] Monster took {damage} damage → {self.monster_health}/{self.progress_bar.max_value}")

		# ดาเมจที่ MC จะได้รับ = ดาเมจจริงที่มอนโดน × 1.5
		actual_damage = prev_health - self.monster_health
		self.pending_mc_damage += actual_damage * 1.5

		# เริ่มนับดีเลย์ 1.5 วิ เพื่อให้มอนสวนกลับ
		if self.delay_timer.is_stopped():
			self.delay_timer.start(1.5)

		# ถ้ามอนตาย
		if self.monster_health <= 0:
			self.monster_health = 0
			self.DialogueUI.aftergameplay()
			print("[LOG] Monster died — next base_mon =", base_mon + 1)
			base_mon += 1
			self.queue_free()


	def _on_delay_timeout(self):
		self.delay_timer.stop()
		self.mc_health -= self.pending_mc_damage
		self.pending_mc_damage = 0
		self.mcprogress_bar.value = max(self.mc_health, 0)

		# เอฟเฟกต์และเสียงตอน MC โดนโจมตี
		self.playerEffect.play_animation()
		self.mc_damage.play()
		print(f"[LOG] MC took damage → {self.mc_health}/{self.mcprogress_bar.max_value}")

		# ถ้า MC ตาย
		if self.mc_health <= 0:
			self.mc_health = 0
			self.die_lable.show()
			self.mc_die_sound.play()
			print("[LOG] MC died — showing DIE label, will wait 3s then change scene")
			self.get_tree().create_timer(3.0).connect("timeout", self, "_on_die_timeout")
		else:
			# ดีเลย์ 2 วิ ก่อนฮีล
			self.get_tree().create_timer(2.0).connect("timeout", self, "_on_heal_delay")


	def _on_heal_delay(self):
		self.heal_mc_if_low()
		if self.monster_health > 0 and self.mc_health > 0:
			self.spawn_typing_ui()


	def heal_mc_if_low(self):
		max_mc_health = ((monster_healthlist[base_mon]) / 4) * 5
		threshold = max_mc_health * 0.1  # 10% ของ HP สูงสุด

		if self.mc_health < threshold and self.mc_health > 0:
			heal_amount = max_mc_health * 0.15
			self.mc_health += heal_amount
			self.mcprogress_bar.value = min(self.mc_health, self.mcprogress_bar.max_value)

			# เอฟเฟกต์และเสียงตอนฮีล
			self.priest = self.get_tree().get_current_scene().get_node("priest")
			self.priest.play_animation("heal")
			self.get_tree().create_timer(1.50).connect("timeout", self, "_on_stop_priest_anim")

			print(f"[LOG] MC healed (HP <10%) — heal +{heal_amount}, new HP = {self.mc_health}")


	def _on_die_timeout(self):
		current_scene = self.get_tree().get_current_scene()
		scene_path = current_scene.filename
		print(f"[LOG] Reloading scene: {scene_path} with base_mon = {base_mon}")
		self.get_tree().change_scene(scene_path)
		self.queue_free()


	def spawn_typing_ui(self):
		typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
		self.get_tree().get_root().add_child(typingUI)
		print("[LOG] Spawned TypingUI for next battle")
	
	def _on_stop_priest_anim(self):
			self.healEffect.play_animation()
			self.priest_heal.play()
			self.priest.stop_animation()
			print("[LOG] Priest animation stopped after heal")
