import pygame, sys

class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,speed, screen_height):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.image.fill('white')
		self.rect = self.image.get_rect(center=pos)
		self.speed = speed
		self.screen_height = screen_height

	def move(self, dir):
		if dir == 'up':
			self.rect.y += self.speed
		else:
			self.rect.y -= self.speed

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.screen_height+50:
			self.kill()
			print('Bullet is gone')
			pygame.quit()
			sys.exit()

	def update(self, dir):
		self.move(dir)
		self.destroy()