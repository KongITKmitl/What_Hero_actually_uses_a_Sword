from godot import exposed, Vector2
from godot.bindings import Node2D, AnimatedSprite

@exposed
class Mover(Node2D):
	target_x = 0.0
	target_y = 0.0
	speed = 50.0
	flip = False
	target_x_active = False
	target_y_active = False

	def _ready(self):
		self.set_process(True)
		self.sprite = self.get_node("AnimatedSprite")
		self.sprite.play("default") 

	def move_to(self, new_x, flip=False, new_speed=None):
		self.target_x = new_x
		self.flip = flip
		self.target_x_active = True
		if new_speed is not None:
			self.speed = new_speed

	def move_to_y(self, new_y):
		self.target_y = new_y
		self.target_y_active = True

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
