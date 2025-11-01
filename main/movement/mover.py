from godot import exposed, Vector2, AudioStreamPlayer, AudioStreamSample, ResourceLoader
from godot.bindings import Node2D
from godot import AnimatedSprite

@exposed
class Mover(Node2D):
	target_x = 0.0
	target_y = 0.0
	speed = 50.0
	flip = False
	target_x_active = False
	target_y_active = False
	anim_locked = False
	current_anim = ""

	def _ready(self):
		self.set_process(True)
		self.SFXpath = 'res://item/SoundEffect/SFXgrasswalking.ogg'
		self.anim = self.get_node("AnimatedSprite")

	def move_to(self, new_x, flip=False, new_speed=None):
		self.target_x = new_x
		self.flip = flip
		self.target_x_active = True
		if new_speed is not None:
			self.speed = new_speed
		self.play_sound(self.SFXpath)
		
		if self.anim:
			self.anim.play("walk")

	def move_to_y(self, new_y):
		self.target_y = new_y
		self.target_y_active = True
		
		if self.anim:
			self.anim.play("walk")

	def _process(self, delta):
		new_x = self.position.x
		new_y = self.position.y

		# X movement
		if self.target_x_active:
			direction_x = 1 if self.target_x > self.position.x else -1
			distance_x = abs(self.target_x - self.position.x)
			move_x = min(self.speed * delta, distance_x)
			new_x = self.position.x + direction_x * move_x
			if distance_x == 0:
				self.target_x_active = False  # reached target
				self.sound.stop()

		# Y movement
		if self.target_y_active:
			direction_y = 1 if self.target_y > self.position.y else -1
			distance_y = abs(self.target_y - self.position.y)
			move_y = min(self.speed * delta, distance_y)
			new_y = self.position.y + direction_y * move_y
			if distance_y == 0:
				self.target_y_active = False  # reached target

		self.position = Vector2(new_x, new_y)

		# Flip horizontally
		if self.flip:
			self.scale = Vector2(-abs(self.scale.x), self.scale.y)
		else:
			self.scale = Vector2(abs(self.scale.x), self.scale.y)
			
		moving = self.target_x_active or self.target_y_active
		if not moving and self.anim and not self.anim_locked:
			if self.current_anim != "default":
				self.play_animation("default")

	def play_sound(self, path):
		self.sound = AudioStreamPlayer.new()
		self.sound.stream = ResourceLoader.load(path)
		self.add_child(self.sound)

		self.sound.play()

	def change_walk_sound(self,path):
		self.SFXpath = path
	
	def play_animation(self, anim_name):
		if self.anim:
			self.anim.play(anim_name)
			self.current_anim = anim_name
			self.anim_locked = True
			print("🎬 Playing animation:", anim_name)
		else:
			print("⚠️ No AnimatedSprite found in MCSprite!")
	
	def stop_animation(self):
		self.play_animation("default")
		self.anim_locked = True
		
