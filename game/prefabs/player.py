import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, img_path, width, height, screen_width, screen_height):
        super().__init__()

        self.original_surf = pygame.image.load(img_path)
        self.original_surf = pygame.transform.scale(self.original_surf, (width, height)) 
        self.surf = self.original_surf
        self.rect = self.surf.get_rect(center=(screen_width/2,screen_height/2))
        self.angle = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def rotate(self, angle):
        self.angle += angle 
        self.angle = self.angle % 360 
        self.surf = pygame.transform.rotate(self.original_surf, self.angle)
        self.rect = self.surf.get_rect(center=(self.screen_width/2, self.screen_height/2))

    def shoot(self, x, y):
        bullet = Bullet(self.angle, x, y, self.screen_width, self.screen_height)
        return bullet
