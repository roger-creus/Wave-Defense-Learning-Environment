import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, img_path, width, height):
        super().__init__()

        self.original_surf = pygame.image.load(img_path)
        self.original_surf = pygame.transform.scale(self.original_surf, (width, height)) 
        self.surf = self.original_surf
        self.rect = self.surf.get_rect(center=(320,200))
        self.angle = 0

    def rotate(self, angle):
        self.angle += angle 
        self.angle = self.angle % 360 
        self.surf = pygame.transform.rotate(self.original_surf, self.angle)
        self.rect = self.surf.get_rect(center=(320,200))

    def shoot(self, x, y):
        bullet = Bullet(self.angle, x, y)
        return bullet
