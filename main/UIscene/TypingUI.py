from godot import exposed, export
from godot import *

import random
import time

magiclist = {
	"magic20" : ["Eat this! avadakeda-",
				"Giggity carb giggity",
				"Wingardium leviosa!!",
				"Harry!! Is that you!",
				"I forgot ma spells!!"],
	"magic40" : ["I will take this potato chip and eat it.",
				"Look at the calendar, see that deadline?",
				"Let your sin weigh upon your mortal soul",
				"The weeds in my garden gives more grief.",
				"Knowledge was the measure of all things."],

	"magic60" : ["Come closer and get a shot! Let's see how daring you are",
				"Smoke with Fire, Mist with Water and the Power with Magic!!!",
				"Fairy barely carry the vary, Wary rally parry pastry moldy",
				'This is the spell to make you HAPPY Every day, "Eudaimonia".',
				"Silver moon, silver moon, peal the wounds with sacred light."],

	"magic80" : ["By the Grand Sorcerer's will, the sacred force shields all I love from all harm.",
				"In the name of the Moon, I shall punish you for all the evil you have done.",
				"Power, faith, and hope—unite as one light! I will fight to protect every single dream.",
				"All my life’s learning shall not bring sorrow to my teacher; I wield my magic now.",
				"Om, let the demon's binding chains be utterly shattered by the full power of my magic!"],
	
	"magic100" : ["2 o'clock , temperature 37 Celsius, gun force 32, humid 22. sweep right and fire for an effect,BOOM!",
				"I am the Bone of my magic, Steel is my Body and Fire is my Blood, as I Pray, Unlimited 9 millimetre!",
				"A destructive force return all creation to cinders, from the abyss, the ultimate attack magic 9mm!!!",
				"The time of awakening cometh. Justice, fallen upon the infallible boundary, appear now as a 9mm!!!!!",
				"The time has come! Now, awaken from your slumber, and by my madness, be wrought! Strike forth…9mm!!!"]
}


@exposed
class TypingUI(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""Called when the node enters the scene tree for the first time."""
		self.word_display = self.get_node("GridContainer/Panel2/word")
		self.current_char = self.get_node("GridContainer/Panel/currentChar")

		#random magic to cast
		num = random.randrange(1,101)
		print(num)
		if 1 <= num <= 99:
			#normal spell
			num = random.choice(['magic20','magic40','magic60','magic80']) #'magic20','magic40','magic60','magic80'
			self.text = random.choice(magiclist[num])
		else:
			self.text = random.choice(magiclist["magic100"])
		
		self.points = 0
		self.c = 0

		# Show the initial characters
		self.word_display.text = self.text[1:]
		self.current_char.text = self.text[0]
		
		self.start_time = time.time()

	def _input(self, event):
		"""Handle key input"""
		if self.c < len(self.text):
			if isinstance(event, InputEventKey) and event.pressed and not event.echo:
				if event.unicode != 0:

					char = chr(event.unicode)
					expected = self.text[self.c]

					if char == expected:
						print(f"{char} (Correct) +10p")
						self.points += 10
					else:
						print(f"{char} (Wrong)")

					# Update UI
					self.c += 1
					if self.c < len(self.text):
						self.current_char.text = self.text[self.c]
						self.word_display.text = self.text[self.c + 1:]
					else:
						self.current_char.text = ""
						self.word_display.text = ""
						print("End")
						
						"""Calculate wpm by WPM = (Total Char Typed / 5) / minutes you type"""
						self.end_time = time.time()
						type_minute = (self.end_time - self.start_time) / 60
						
						self.wpm = (len(self.text) / 5) / type_minute
						self.damage = self.points * (self.wpm *0.05)
						
						print('Raw damage = '+ str(self.points))
						print('WPM = ' + str(self.wpm))
						print('Damage (RawDamage * WPM) = ' + str(self.damage) )
						
						self.get_tree().current_scene.showUI()
						self.queue_free()



