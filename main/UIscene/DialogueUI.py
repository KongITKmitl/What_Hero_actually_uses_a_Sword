from godot import exposed, export
from godot import *
from ..preload_resources2 import get_healthbar, get_typing_ui
dialogue_list = [
	"Thou awakeneth, stirred by a gentle yet mischievous voice.", # Black screen
	"Hey~~ Thou there, awake already, will thee?", #cg
	"’Tis nigh unto noon, sleepyhead~!",
	"The time for training hath arrived! Come now, ",
	"up with thee, before I drag thee out myself~!", # end cg
	"Thou hast studied beneath mine wing for many a year now, sweet apprentice~",
	"And lo, the hour hath come for thee to step forth upon thine own path",
	"To face the world and take on thy very first quest!",
	"But ere that, I shall test thee once more—to see if thou truly rememberest all I hath taught thee. Heehee~",
	"Now then, let us begin from the very basics.",
	"When thou casteth a spell, thou must utter the incantation with utmost care.",
	"For a single misplaced word may lessen thy power, yet a perfect chant shall rend mountains asunder!",
	"So keep thy focus sharp, hmm?",
	"Very well then begin!" ,#fight--------- 13
	"Well done, my dear !",
	"Thou hast done splendidly. Methinks thou art ready for what lieth ahead.",
	"Now then, about thy mission~",
	"This one cometh straight from His Majesty the King himself!",
	"He requesteth that thou rescue a certain princess",
	"Though I confess I quite forget which number she is—from the dread Demon Lord who hath spirited her away.",
	"Truth be told, ’twas I who should have gone... but alas, I find myself dreadfully lazy this day.",
	"So~ I entrust this noble task to thee, my capable pupil! Fare thee well—", #---------------------end scene 1----(index :21)
	"Blessings be upon thee, O weary traveler.",#---------scene village---------
	"I am but a humble servant of the Light…",
	"though the Light may take many forms.",
	"I sense within thee a rare flame —",
	"radiant, yet perilous if untamed.",
	"Pray, wouldst thou grant me the honor",
	"of walking beside thee —",
	"to see what fate the Light hath woven?",
	"Ah… so thou wouldst permit my company.",
	"How gracious of thee.",
	"The path ahead is veiled in shadow —",
	"yet in darkness the Light burneth brightest.",
	"Walk beside me, and may courage dwell in thy heart.",
	"May fortune smile upon thy cause.",
	"Go forth, traveler,",
	"and may thy journey be guided by wisdom and mercy.",#----------end scene village------(index 37)
	"Sss… I want to sleep, sss…", #-------scene farm------
	"don’t step on my grass, sss…",
	"no passing, sss…",
	"Well done, traveler… thy bravery is most delightful, and I cannot help but be intrigued by thy daring.",  # left dialogue -----------end farm scene(index41)
	"What the hell is that supposed to be…?",#l-------scene forest----------
	"A Rattlepiranha? Seriously!?", #l 43
	"Why so startled ?",
	"This is a fantasy world, after all. Didst thou expect only rabbits and butterflies?",
	"By the Light… it speaks!", #l
	"And with wit sharper than its fangs, I daresay.", #l
	"You’ve gotta be kidding me. What’s next, a talking potato with wings?", #l 48
	"Mock me while thou still draw breath, mortal.",
	"When my tail rings… it tolls for thee. Cling-cling-cling!",#Typing game start!-------- index 50
	"Heh… may thy courage not sink as swiftly as I do… glub…",
	"Rest easy, creature. Even monsters may find peace in the great current beyond.", #l
	"Well fought, my Hero. Perhaps the waters favor thee yet.", #-------End scene forest index 53
	"hat in the blazes…? Something’s rising from the ground!" ,#l  ------Demon town scene---------
	"So... a mortal dares tread upon my hallowed ground.",
	"Know this — none who enter shall ever depart!",
	"Take it, and embrace your fate — the Bone Shard of Death!", # start game index 57
	"Heh, some “Bone Shard of Death” you turned out to be. Just bones, nothing more.", #l -----end scene demon town index 58
	"Well, well... an uninvited guest, how delightful.",#------- Castle gate scene------
	"From afar, I can scarce tell — art thou man or maid?",
	"If a maiden, thy flesh must be sweet indeed...",
	"If not, the taste may be foul, yet filling all the same.",
	"Either way... I shall feast. Heh-heh-heh...", #start game index 63
	"A pig demon, how precious… and utterly vile.",#l
	"Touch me, and I’ll be scratching till I need a restoration elixir from the arcane merchant!",#l -------end scene castle gate index 65
	
]

text_speed = 0.03

			
@exposed
class DialogueUI(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def setup_dialogue(self,start_dialogue_order):
		self.current_dialogue_order = start_dialogue_order
		self.current_text = dialogue_list[self.current_dialogue_order]
		self.current_char = 0
		self.gameplaytrigger = False
		self.waiting = False
		
		self.check_dialogue_display()
		self.change_cg()
		self.timer_setup()

	def _ready(self):
		
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.blackscreen = self.get_node('blackscreen')
		self.blackscreenlabel = self.get_node('blackscreenLabel')
		
		self.RightDialogueBox = self.get_node('RightDialogueBox')
		self.RightDialogueContent = self.get_node('RightDialogueContent')
		
		self.LeftDialogueBox = self.get_node('LeftDialogueBox')
		self.LeftDialogueContent = self.get_node('LeftDialogueContent')
		
		self.cgLabel = self.get_node('cgLabel')
		self.cg = self.get_node('cg')
		


	def timer_setup(self):
		self.gameplaytrigger = False

		self.label.text = ''
		self.current_char = 0

		self.timer = Timer.new()
		self.timer.wait_time = text_speed
		self.timer.one_shot = True
		self.add_child(self.timer)
		self.timer.connect("timeout",self,"_on_timer_timeout")
		
		self.timer.start()

	def _process(self,delta):
		"""Always run"""

		if Input.is_action_just_pressed("Pressed_Enter") and not self.waiting and not self.gameplaytrigger\
		and self.current_dialogue_order < len(dialogue_list)-1:
			
			self.current_dialogue_order += 1
			self.current_text = dialogue_list[self.current_dialogue_order]
			self.label.text = ''
			self.timer_setup()
			
			self.check_newscene()
			self.check_dialogue_display()
			self.change_cg()
			self.check_if_gameplay()
			

		elif Input.is_action_just_pressed("Pressed_Enter") and not self.waiting and self.gameplaytrigger:
			self.label.text = ''
			
			
			self.healthbar_ui = get_healthbar().instance()
			self.get_tree().get_root().add_child(self.healthbar_ui)

			self.typing_ui = get_typing_ui().instance()
			self.get_tree().get_root().add_child(self.typing_ui)
			
			self.hide()
		

	def _on_timer_timeout(self):
		
		if self.current_char < len(self.current_text):
			self.label.text += GDString(self.current_text[self.current_char])
			self.current_char += 1
			self.timer.start()
			self.waiting = True
		else:
			print(self.current_dialogue_order)
			self.timer.queue_free()
			self.waiting = False
			

	def aftergameplay(self):
		self.show()

		self.current_dialogue_order += 1
		self.gameplaytrigger = False
		self.current_text = dialogue_list[self.current_dialogue_order]
		
		self.check_dialogue_display()
		self.change_cg()
		self.timer_setup()
	
	def check_dialogue_display(self):
		if self.current_dialogue_order == 0:
			self.create_blackscreen()
		elif 1 <= self.current_dialogue_order <= 4 or 22 <= self.current_dialogue_order <= 37:
			self.create_cg()
		elif self.current_dialogue_order in (41,42,43,46,47,48,52,53,54,58,64,65): 
			self.create_left()
		else:
			self.create_right()
			
	def check_if_gameplay(self):
		"""เมื่อถึงบทพูด index = .... ให้เข้า gameplay typing"""
		if self.current_dialogue_order in (13,40,50,57,63):
			self.gameplaytrigger = True
		else:
			self.gameplaytrigger = False

	def check_newscene(self):
		if self.current_dialogue_order in (22,38,42,54,59,66):
			self.get_tree().get_current_scene().done_dialogue()
			self.queue_free()

	def change_cg(self):
		if self.current_dialogue_order == 0:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG1_Wizard.png")
		if self.current_dialogue_order == 22:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG1_villageScene.png")

	def create_blackscreen(self):
		self.label = self.blackscreenlabel
		
		self.cg.visible = False
		self.blackscreen.visible = True
		self.RightDialogueBox.visible = False
		self.LeftDialogueBox.visible = False
	
	def create_cg(self):
		self.label = self.cgLabel

		self.cg.visible = True
		self.blackscreen.visible = False
		self.RightDialogueBox.visible = False
		self.LeftDialogueBox.visible = False
	def create_right(self):
		self.label = self.RightDialogueContent
		
		self.cg.visible = False
		self.blackscreen.visible = False
		self.RightDialogueBox.visible = True
		self.LeftDialogueBox.visible = False
		
	def create_left(self):
		self.label = self.LeftDialogueContent
		
		self.cg.visible = False
		self.blackscreen.visible = False
		self.RightDialogueBox.visible = False
		self.LeftDialogueBox.visible = True
