from godot import exposed, export
from godot import *
import asyncio #เพื่อจะได้ใช้ Await ได้
dialogue_list = [
	"Good morning my dear disciple.",
	"Eventually, this day has come.",
	"The day that I'm going to pass by my greatest spell to you.",
	"Behold!!",
	"Nice",
	"Now, use those spell to save the world",
	"And may be find the partner of your life."
]

text_speed = 0.03
waiting = False
			
@exposed
class DialogueUI(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		
		self.current_dialogue_order = 0
		self.current_text = dialogue_list[self.current_dialogue_order]
		self.current_char = 0
		self.gameplaytrigger = False

		self.RdialogueContent = self.get_node("RightDialogueBox/RightDialogueContent")
		
		self.timer_setup()
	
	
	def timer_setup(self):
		gameplaytrigger = False

		self.RdialogueContent.text = ''
		self.current_char = 0

		self.timer = Timer.new()
		self.timer.wait_time = text_speed
		self.timer.one_shot = True
		self.add_child(self.timer)
		self.timer.connect("timeout",self,"_on_timer_timeout")
		
		self.timer.start()

	def _process(self,delta):
		"""Always run"""

		if Input.is_action_just_pressed("Pressed_Enter") and not waiting and not self.gameplaytrigger\
		and self.current_dialogue_order < len(dialogue_list)-1:
			
			self.current_dialogue_order += 1
			self.current_text = dialogue_list[self.current_dialogue_order]

			self.timer_setup()
			
			"""เมื่อถึงบทพูด index = .... ให้เข้า gameplay typing"""
			if self.current_dialogue_order == 3:
				self.gameplaytrigger = True
			else:
				self.gameplaytrigger = False

		elif Input.is_action_just_pressed("Pressed_Enter") and not waiting and self.gameplaytrigger:
			
			typingUI = ResourceLoader.load("res://main/UIscene/TypingUI.tscn").instance()
			self.get_tree().get_root().add_child(typingUI)
			self.hide()
		

	def _on_timer_timeout(self):
		
		if self.current_char < len(self.current_text):
			self.RdialogueContent.text += GDString(self.current_text[self.current_char])
			self.current_char += 1
			self.timer.start()
			waiting = True
		else:
			print(self.current_dialogue_order)
			self.timer.queue_free()
			waiting = False
			
	def aftergameplay(self,*args):
		self.show()
		self.current_dialogue_order += 1
		gameplaytrigger = False
		self.current_text = dialogue_list[self.current_dialogue_order]
		self.timer_setup()
		

