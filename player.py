import pygame
#from bullet import Bullet

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,speed, max_x):
		super().__init__()
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=pos)
		self.speed = speed
		self.max_x = max_x

		#bullet
		#self.bullet = pygame.sprite.Group()
		#self.ready = True
		#print(self.ready)
		
	def get_input(self):
		#print(self.ready)
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] and self.rect.right <= self.max_x:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT] and self.rect.left >= 0:
			self.rect.x -= self.speed

	
			
	def update(self):
		self.get_input()
		#self.bullet.update()
