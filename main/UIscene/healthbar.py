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
		self.progress_bar = self.get_node("MonsterBar")
		self.monster_health = monster_healthlist[base_mon]

	def take_damage(self, damage):
		self.monster_health -= damage
		if self.monster_health < 0:
			self.monster_health = 0
			base_mon += 1
		self.update_health_bar()
		print(f"💥Monster HP = {self.monster_health}")

	def update_health_bar(self):
		# อัปเดตค่าหลอดเลือดใน ProgressBar
		self.progress_bar.value = self.monster_health
