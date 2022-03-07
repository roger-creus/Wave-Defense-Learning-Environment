import pygame
import numpy as np

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, x, y, mov_speed = 10):
        super().__init__()
        self.surf = pygame.Surface((5, 10))
        self.surf.fill((255, 0, 0))
        self.rect = (320,200)
        self.angle = angle
        self.mov_speed = mov_speed

    def step_forward(self):
        self.rect = (self.rect[0] + np.cos(self.angle), self.rect[1] + np.sin(self.angle))