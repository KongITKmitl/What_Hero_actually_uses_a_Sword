from godot import exposed, export
from godot import *

import random
import time

# ----------------------------
# เวทมนตร์
# ----------------------------
magiclist = {
	"magic20": [
		"Eat this! avadakeda-",
		"Giggity carb giggity",
		"Wingardium leviosa!!",
		"Harry!! Is that you!",
		"I forgot ma spells!!"
	],

	"magic40": [
		"I will take this potato chip and eat it.",
		"Look at the calendar, see that deadline?",
		"Let your sin weigh upon your mortal soul",
		"The weeds in my garden gives more grief.",
		"Knowledge was the measure of all things."
	],

	"magic60": [
		"Come closer and get a shot! Let's see how daring you are",
		"Smoke with Fire, Mist with Water and the Power with Magic!!!",
		"Fairy barely carry the vary, Wary rally parry pastry moldy",
		'This is the spell to make you HAPPY Every day, "Eudaimonia".',
		"Silver moon, silver moon, peal the wounds with sacred light."
	],

	"magic80": [
		"By the Grand Sorcerer's will, the sacred force shields all I love from all harm.",
		"In the name of the Moon, I shall punish you for all the evil you have done.",
		"Power, faith, and hope—unite as one light! I will fight to protect every single dream.",
		"All my life’s learning shall not bring sorrow to my teacher; I wield my magic now.",
		"Om, let the demon's binding chains be utterly shattered by the full power of my magic!"
	],
	
	"magic100": [
		"2 o'clock , temperature 37 Celsius, gun force 32, humid 22. sweep right and fire for an effect,BOOM!",
		"I am the Bone of my magic, Steel is my Body and Fire is my Blood, as I Pray, Unlimited 9 millimetre!",
		"A destructive force return all creation to cinders, from the abyss, the ultimate attack magic 9mm!!!",
		"The time of awakening cometh. Justice, fallen upon the infallible boundary, appear now as a 9mm!!!!!",
		"The time has come! Now, awaken from your slumber, and by my madness, be wrought! Strike forth…9mm!!!"
	]
}


# ----------------------------
# คลาสหลักของเกม Typing UI
# ----------------------------
@exposed
class TypingUI(Control):

	# ตัวแปรที่สามารถตั้งค่าได้จาก Editor ของ Godot
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""ฟังก์ชันนี้จะถูกเรียกเมื่อ Node ถูกโหลดเข้าฉาก"""
		# ดึง Node ลูกที่อยู่ใน Scene มาใช้งาน
		self.word_display = self.get_node("GridContainer/Panel2/word")     # แสดงตัวอักษรถัดไป
		self.current_char = self.get_node("GridContainer/Panel/currentChar")  # ตัวอักษรที่ต้องพิมพ์ตอนนี้
		self.timer = self.get_node("Timer")									# ตัวจับเวลา
		self.progress_bar = self.get_node("ProgressBar")					# แถบความคืบหน้า
		self.stats_label = self.get_node("StatsLabel")						# แสดง WPM และ Accuracy
		self.damage_label = self.get_node("damageLabel")					#เลขดาเมจ

		# เชื่อมสัญญาณเมื่อ timer หมดเวลา
		self.timer.connect("timeout", self, "_on_Timer_timeout")

		# ----------------------------
		# สุ่มข้อความเวทมนตร์ 1 อันจาก magiclist
		# ----------------------------
		num = random.randrange(1, 101)
		if 1 <= num <= 99:
			num = random.choice(["magic20", "magic40", "magic60", "magic80"])
			self.text = random.choice(magiclist[num])
		else:
			self.text = random.choice(magiclist["magic100"])

		# ค่าเริ่มต้นต่าง ๆ
		self.points = 0           # คะแนนรวม
		self.c = 0                # จำนวนอักษรที่พิมพ์แล้ว
		self.correct = 0          # จำนวนอักษรถูก
		self.start_time = time.time()  # เวลาเริ่มต้นพิมพ์

		# ตั้งค่า UI เริ่มต้น
		self.word_display.text = self.text[1:]    # แสดงอักษรถัดไป
		self.current_char.text = self.text[0]     # อักษรแรกที่ต้องพิมพ์
		self.progress_bar.value = 0
		self.stats_label.text = "WPM: 0 | Accuracy: 100%"

		# เริ่มนับเวลา
		self.timer.start()

	def _input(self, event):
		"""ตรวจจับการพิมพ์ของผู้เล่น"""
		if self.c < len(self.text):
				if event.unicode != 0:
					char = chr(event.unicode)       # ตัวอักษรที่ผู้ใช้พิมพ์
					expected = self.text[self.c]    # ตัวอักษรที่ควรพิมพ์

					# ตรวจว่าถูกหรือผิด
					if char == expected:
						self.points += 10
						self.correct += 1
						self.current_char.add_color_override("font_color", Color(0, 1, 0))  # เขียว = ถูก
					else:
						self.current_char.add_color_override("font_color", Color(1, 0, 0))  # แดง = ผิด

					self.c += 1  # เพิ่มจำนวนตัวอักษรที่พิมพ์แล้ว

					# ----------------------------
					# อัปเดต UI หลังพิมพ์แต่ละครั้ง
					# ----------------------------
					if self.c < len(self.text):
						self.current_char.text = self.text[self.c]       # ตัวต่อไปที่ต้องพิมพ์
						self.word_display.text = self.text[self.c + 1:]  # ส่วนที่เหลือ
					else:
						# ถ้าพิมพ์ครบแล้ว ให้โชว์สรุปผล
						self._show_summary()
						self.timer.stop()

					# อัปเดตแถบ progress bar
					progress = (self.c / len(self.text)) * 100
					self.progress_bar.value = progress

					# คำนวณ Accuracy และ WPM
					accuracy = (self.correct / self.c) * 100 if self.c > 0 else 100
					elapsed = time.time() - self.start_time
					minutes = elapsed / 60
					wpm = (self.c / 5) / minutes if minutes > 0 else 0  # สูตร WPM (1 คำ = 5 ตัวอักษร)
					
					# แสดงผลทางหน้าจอ
					self.stats_label.text = f"WPM: {int(wpm)} | Accuracy: {int(accuracy)}%"

	def _show_summary(self):
		"""สรุปผลหลังพิมพ์ครบ"""
		elapsed = time.time() - self.start_time
		minutes = elapsed / 60
		wpm = (len(self.text) / 5) / minutes       # คำนวณ WPM จริงทั้งหมด
		damage = self.points * (wpm * 0.05)        # สมมุติเป็นดาเมจที่เกิดขึ้นตามคะแนนและความเร็ว
		print("✅ Typing Complete!")
		print(f"Score: {self.points}")
		print(f"WPM: {round(wpm, 1)}")
		print(f"Damage: {round(damage, 1)}")
		self.damage_label.text = f"Damage: {round(damage, 1)}"

