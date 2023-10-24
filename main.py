import pygame, sys
from player import Player
import obstacle
from bullet import Bullet
from enemy import Enemy

#Todo
#each enemy has diff dir? 
#level system?
#bullet destroyer?

class Game:
	def __init__(self):
		#player
		#Player(pos,speed,constraint)
		player_sprite = Player((screen_width/2,screen_height), 5, screen_width) 
		self.player = pygame.sprite.GroupSingle(player_sprite)

		#blocks
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		#blocks creation
		#Block(screen_width/15, y, x_offset)
		#self.create_obstacle(screen_width/15, 30, 0)
		#self.create_obstacle(screen_width/15, 30, 65)
		pos_x = 0
		for i in range(8):
			self.create_obstacle(screen_width/15, 50, pos_x)
			pos_x += 65
		#...............

		#bullet
		self.bullets = pygame.sprite.Group()
		self.change_dir = True
		self.dir = 'up'
		self.ready = True

		#Enemy
		self.enemies = pygame.sprite.Group()
		self.enemy_dir = 1
		#enemy creation
		#Enemy(color, x, y)
		pos_x = 0
		pos_y = 100
		color = ''
		for j in range(6):
			if j%2 == 0:
				color = 'yellow'
			else:
				color = 'green'
			for i in range(8):
				self.create_enemy(color, pos_x, pos_y)
				pos_x += 65
			pos_y += 65
			pos_x = 0
		#...............

		#level
		#self.level_no = 1

		#HUD
		self.score = 0
		self.font = pygame.font.Font('font/Pixeled.ttf', 20)
		self.bullet_amount = 1

		#Audio
		music = pygame.mixer.Sound('audio/music.wav')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.bullet_sound = pygame.mixer.Sound('audio/laser.wav')
		self.bullet_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

	def shoot_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.ready:
			#print('bullet')
			self.shoot_bullet()
			self.ready = False
			self.bullet_sound.play()

	def shoot_bullet(self):
		self.bullet_amount -= 1
		x = self.player.sprite.rect.x+30
		y = self.player.sprite.rect.y-10
		#print(x)
		#Bullet(pos,speed,screen_height)
		self.bullets.add(Bullet((x,y), -6, screen_height)) 

	def create_enemy(self, color, x, y):
		self.enemies.add(Enemy(color, x, y))

	def enemy_pos_checker(self):
		all_enemies = self.enemies.sprites()
		for enemy in all_enemies:
			if enemy.rect.left <= 0:
				self.enemy_dir = 1
				self.enemy_move_down(2)
			elif enemy.rect.right >= screen_width:
				self.enemy_dir = -1
				self.enemy_move_down(2)

	def enemy_move_down(self, distance):
		if self.enemies: 
			for enemy in self.enemies.sprites():
				enemy.rect.y += distance

	def create_obstacle(self, x_start, y_start, offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index, col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size, (241,79,80), x, y)
					self.blocks.add(block)

	def collision_detection(self):
		bullets = self.bullets
		
		if bullets:
			for bullet in bullets:
				#block collision
				if pygame.sprite.spritecollide(bullet, self.blocks, True):
				#up dir
					self.dir = 'down'
					#bullet.move('down')
					self.change_dir = False
					#print('collided')
				#change dir
				elif self.change_dir:
					#bullet.move('up')
					self.dir = 'up'
				
				#player collision
				if pygame.sprite.spritecollide(bullet, self.player, False):
					self.dir = 'up'
					self.change_dir = True
					self.ready = True
					bullet.kill()
					self.bullet_amount += 1

				#enemy collision
				if pygame.sprite.spritecollide(bullet, self.enemies, True):
					print('killed')
					#bounce back from enemies
					self.dir = 'down'
					self.change_dir = False
					self.score += 200
					self.explosion_sound.play()
					#.......................

		#enemy collision
		enemies = self.enemies
		if enemies:
			for enemy in enemies:
				if pygame.sprite.spritecollide(enemy, self.player, False):

					print('u r dead')
					pygame.quit()
					sys.exit()

	def display_score(self):
		score_surface = self.font.render(f'score: {self.score}', False, 'white')
		score_rect = score_surface.get_rect(topleft = (10,-10))
		screen.blit(score_surface,score_rect)

	def display_bullet_amount(self):
		bullet_surface = self.font.render(f'Bullet: {self.bullet_amount}', False, 'white')
		bullet_rect = bullet_surface.get_rect(topright = (screen_width-10,-10))
		screen.blit(bullet_surface,bullet_rect)

	def display_victory_message(self):
		if not self.enemies.sprites():
			print("win")
			victory_surface = self.font.render('Victory', False, 'white')
			victory_rect = victory_surface.get_rect(center = (screen_width/2, screen_height/2))
			screen.blit(victory_surface, victory_rect)

	def run(self):
		#update
		self.player.update()
		self.shoot_input()
		self.collision_detection()
		self.bullets.update(self.dir)
		self.enemies.update(self.enemy_dir)
		self.enemy_pos_checker()
		#HUD update
		self.display_score()
		self.display_bullet_amount()
		self.display_victory_message()

		#draw
		self.player.draw(screen)
		self.bullets.draw(screen)
		self.blocks.draw(screen)
		self.enemies.draw(screen)

if __name__ == '__main__':
	pygame.init()
	screen_width = 600
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.fill((30,30,30))
		game.run()

		pygame.display.flip()
		clock.tick(60)