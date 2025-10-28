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
	"So thou hast come at last… O chosen Hero.", #---------StartBoss scene------ index 66
	"Pray, tell—", #l
	"Where dost thou keep the Princess?", #l
	"Hm?",#cg ? index 69
	"Dost that not fall to thee to utter, brave one?",
	"Nay, 'tis of no import now. The Princess, thou seekest?",
	"See with thine own eyes, and judge for thyself.",
	"                                                               ", #เลื่อนไปดูกรง # cage cg index 73
	"Then come—let us bring this tale to its turning point.", #start typing index 74
	"...",
	"Alas...",
	"This hath dragged on far longer than mine expectation.",
	"Know this: I seized the Princess not from malice,",
	"but in accordance with ancient rite and custom.",
	"What a tiresome affair...",
	"Let us end this folly, swiftly and without further delay!", #Fight phase 2 index 81
	"Urgh… No more…",
	"Thou hast bested me, O silent one.",
	"I yield. The Princess is thine to reclaim.",
	"At long last, I may take my leave—perhaps to lands unknown,",
	"to taste a fleeting moment of peace…",
	"What?", #l index 87
	"Is that all?", #l
	"Hath the tale come to its end?", #l
	"Aye.",
	"Now be swift, and leave this place, ere I rethink my mercy.", #จากนั้นกรงหล่นทับ
	"        ", #pan camera index 92
	"...",
	"…Wait a moment.",
	"Wha—!?",
	"...",
	"A-As this hath been my first time donning the mantle of the Demon Lord,",
	"I shall bestow upon thee a token — a gift most rare —",
	"for being the first to lay me low.",
	"Take this, and may fate guide thy steps henceforth.",
	"Fare thee well, noble Hero.",
	"Thou hast obtained: Reviving Draught ×1", # Blackscreen? index 102
	"A choice now lieth before thee...",
	"Only one soul may return to the realm of the living.",
	"Choose wisely, for fate shall not grant thee this mercy twice." ,#display choice by going into new scene index 105
	"My deepest condolences, noble Hero.", #start Ending: The Princess index 106
	"Your companion was truly courageous.",
	"Those words would come to be spoken to the Hero",
	"more often than any other.",
	"Truly… I am sorry, my Hero.",
	"And yet, I am grateful — so very grateful — that you chose me.",
	"Thank you.",
	"...Hmm.",
	"Beneath the warm, amber sky,",
	"they offered their silent prayers for the great sacrifice that had been made.",
	"A single bouquet was laid upon the resting place.",
	"Two figures stood quietly before the grave —",
	"united in both grief and remembrance.",
	"Ending: The Princess", #blackscreen ---> credit index 119
	"A-Are you certain about this…? My Hero?", #start Ending: The Priest index 120
	"I can scarcely believe you would choose me.",
	"Aye… yet it seems our time draws short.",
	"Our fate, perhaps, was sealed long ago. Heh…",
	"I can tell just by looking at us…",
	"But, you know… this is the first time I’ve heard you speak.",
	"Truly? Heh…",
	"Amidst the curses and cries that filled the air,",
	"only two voices remained —",
	"soft laughter, shared between companions,",
	"echoing faintly through the chaos.",
	"Ending: The Priest", #blackscreen --> credit index 131
	"END", #index 132
]

text_speed = 0.0001

			
@exposed
class DialogueUI(Control):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def setup_dialogue(self,start_dialogue_order):
		self.current_dialogue_order = start_dialogue_order
		self.current_text = dialogue_list[self.current_dialogue_order]
		self.current_char = 0
		self.Ingame = False
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
		if Input.is_action_just_pressed("Pressed_Enter"):
			if not self.waiting and not self.gameplaytrigger and not self.Ingame:
				self.next_dialogue()
			elif not self.waiting and self.gameplaytrigger and not self.Ingame:
				self.start_gameplay()

	def next_dialogue(self):
		if not self.waiting and not self.gameplaytrigger and self.current_dialogue_order < len(dialogue_list) - 1:
			self.current_dialogue_order += 1
			self.current_text = dialogue_list[self.current_dialogue_order]
			self.label.text = ''
			self.timer_setup()

			self.check_newscene()
			self.check_dialogue_display()
			self.change_cg()
			self.check_if_gameplay()


	def start_gameplay(self):
		if not self.waiting and self.gameplaytrigger:
			self.Ingame = True
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
		self.Ingame = False
		self.current_text = dialogue_list[self.current_dialogue_order]
		
		self.check_dialogue_display()
		self.change_cg()
		self.timer_setup()
	
	def check_dialogue_display(self):
		if self.current_dialogue_order in (0,102,103,104,105,119,131):
			self.create_blackscreen()
		elif 1 <= self.current_dialogue_order <= 4 or 22 <= self.current_dialogue_order <= 37 \
		or 106 <= self.current_dialogue_order <= 118 or 120 <= self.current_dialogue_order <= 130:
			self.create_cg()
		elif self.current_dialogue_order in (41,42,43,46,47,48,52,53,54,58,64,65,67,68,87,88,89): 
			self.create_left()
		else:
			self.create_right()
			if self.current_dialogue_order in (73,92):
				self.get_tree().get_current_scene().pan_camera()
				self.RightDialogueBox.visible = False
				self.get_tree().create_timer(4.5).connect("timeout", self, "auto_change_dialogue")
			
	def auto_change_dialogue(self):
		if self.current_dialogue_order in (73,92):
			self.next_dialogue()
		
	def check_if_gameplay(self):
		"""เมื่อถึงบทพูด index = .... ให้เข้า gameplay typing"""
		if self.current_dialogue_order in (13,40,50,57,63,74,81):
			self.gameplaytrigger = True
		else:
			self.gameplaytrigger = False

	def check_newscene(self):
		if self.current_dialogue_order in (22,38,42,54,59,66,106,120,132):
			self.get_tree().get_current_scene().done_dialogue()
			self.queue_free()

	def change_cg(self):
		if self.current_dialogue_order == 0:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG1_Wizard.png")
		if self.current_dialogue_order == 22:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG1_villageScene.png")
		if self.current_dialogue_order == 106:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG_EndingPrincess.png")
		if self.current_dialogue_order == 120:
			self.cg.texture = ResourceLoader.load("res://item/SpriteAndMore/CG_EndingPriest.png")

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
