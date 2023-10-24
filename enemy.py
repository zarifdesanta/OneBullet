import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'graphics/'+color+'.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft=(x,y))

	def move(self,dir):
		self.rect.x += dir

	def update(self,dir):
		self.move(dir)