from godot import exposed, export
from godot import *


@exposed
class healthbar(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.TypingUI = self.get_node('../TypingUI')
		self.hp = 1000
		pass
		
		"""หลังพิมพ์จบ 1 รอบ เขียนไว้ว่าให้เรียกใช้ function take_damage แล้วก้ส่ง damage ของรอบนั้นมาให้"""
	def take_damage(self,damage):
		self.damage = damage
		
		self.hp -= self.damage
		print('hp - damage =' , self.hp)
