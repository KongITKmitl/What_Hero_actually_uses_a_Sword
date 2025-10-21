from godot import exposed, export, signal
from godot import *
import random
import time

magiclist = {
	"magic20": ["Eat this! avadakeda-", "Giggity carb giggity", "Wingardium leviosa!!", "Harry!! Is that you!", "I forgot ma spells!!"],
	"magic40": ["I will take this potato chip and eat it.", "Look at the calendar, see that deadline?", "Let your sin weigh upon your mortal soul", "The weeds in my garden gives more grief.", "Knowledge was the measure of all things."],
	"magic60": ["Come closer and get a shot! Let's see how daring you are", "Smoke with Fire, Mist with Water and the Power with Magic!!!", "Fairy barely carry the vary, Wary rally parry pastry moldy", 'This is the spell to make you HAPPY Every day, "Eudaimonia".', "Silver moon, silver moon, peal the wounds with sacred light."],
	"magic80": ["By the Grand Sorcerer's will, the sacred force shields all I love from all harm.", "In the name of the Moon, I shall punish you for all the evil you have done.", "Power, faith, and hope—unite as one light! I will fight to protect every single dream.", "All my life’s learning shall not bring sorrow to my teacher; I wield my magic now.", "Om, let the demon's binding chains be utterly shattered by the full power of my magic!"],
	"magic100": ["2 o'clock , temperature 37 Celsius, gun force 32, humid 22. sweep right and fire for an effect,BOOM!", "I am the Bone of my magic, Steel is my Body and Fire is my Blood, as I Pray, Unlimited 9 millimetre!", "A destructive force return all creation to cinders, from the abyss, the ultimate attack magic 9mm!!!", "The time of awakening cometh. Justice, fallen upon the infallible boundary, appear now as a 9mm!!!!!", "The time has come! Now, awaken from your slumber, and by my madness, be wrought! Strike forth…9mm!!!"]
}


@exposed
class TypingUI(Control):

	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		
		self.healthbar = self.get_node('../healthbar')
		self.word_display = self.get_node("GridContainer/Panel2/word")
		self.current_char = self.get_node("GridContainer/Panel/currentChar")
		self.timer = self.get_node("Timer")
		self.progress_bar = self.get_node("ProgressBar")
		self.stats_label = self.get_node("StatsLabel")
		self.damage_label = self.get_node("damageLabel")
		self.timer2 = self.get_node("Timer2")  # ✅ Timer2 สำหรับซ่อนข้อความดาเมจ

		self.timer.connect("timeout", self, "_on_Timer_timeout")

		num = random.randrange(1, 101)
		if 1 <= num <= 99:
			num = random.choice(["magic20", "magic40", "magic60", "magic80"])
			self.text = random.choice(magiclist[num])
		else:
			self.text = random.choice(magiclist["magic100"])

		self.points = 0
		self.c = 0
		self.correct = 0
		self.start_time = time.time()

		self.word_display.text = self.text[1:]
		self.current_char.text = self.text[0]
		self.progress_bar.value = 0
		self.stats_label.text = "WPM: 0 | Accuracy: 100%"
		self.damage_label.text = ""
		self.timer.start()

	def _input(self, event):
		"""function  ที่รับinput จากแป้นพิมพ์"""
		if self.c < len(self.text):
			if event.unicode != 0:
				char = chr(event.unicode)
				expected = self.text[self.c]

				if char == expected:
					self.points += 10
					self.current_char.add_color_override("font_color", Color(0, 1, 0))
				else:
					self.current_char.add_color_override("font_color", Color(1, 0, 0))

				self.c += 1

				if self.c < len(self.text):
					self.current_char.text = self.text[self.c]
					self.word_display.text = self.text[self.c + 1:]
				else:
					self._show_summary()
					self.timer.stop()

				self.calculate_wpm()

	def calculate_wpm(self):
		"""function ที่คำนวนค่าตัวเลขต่างๆ"""
		progress = (self.c / len(self.text)) * 100
		self.progress_bar.value = progress

		accuracy = (self.correct / self.c) * 100 if self.c > 0 else 100
		elapsed = time.time() - self.start_time
		self.minutes = elapsed / 60
		self.wpm = (self.c / 5) / self.minutes if self.minutes > 0 else 0
		self.stats_label.text = f"WPM: {int(self.wpm)} | Accuracy: {int(accuracy)}%"

	def _show_summary(self):
		"""Show summary after typing each round"""
		self.damage = self.points * (self.wpm * 0.05)

		print("✅--Typing Complete!--")
		print(f"Score: {self.points}")
		print(f"WPM: {round(self.wpm, 1)}")
		print(f"Damage: {round(self.damage, 1)}")

		self.damage_label.text = f"Damage: {round(self.damage, 1)}"

		#ตั้ง Timer2 ให้ซ่อนข้อความหลัง 2 วิ
		self.timer2.wait_time = 1.0
		self.timer2.one_shot = True
		if not self.timer2.is_connected("timeout", self, "_hide_damage"):
			self.timer2.connect("timeout", self, "_hide_damage")
		self.timer2.start()

	
	def _hide_damage(self):
		"""หลังจาก function show summary จบ"""
		self.damage_label.text = ""
		self.healthbar.take_damage(self.damage)
		#self.get_tree().current_scene.showUI() #แสดงdialog

		self.queue_free()
