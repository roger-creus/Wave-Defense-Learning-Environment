import pygame
import numpy as np

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, x, y, screen_width, screen_height, mov_speed = 2.5):
        super().__init__()
        self.surf = pygame.Surface((8, 8))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(screen_width/2,screen_height/2))
        self.angle = angle
        self.mov_speed = mov_speed


    def step_forward(self):
        self.rect.x += np.cos(np.deg2rad(self.angle)) * self.mov_speed
        self.rect.y -= np.sin(np.deg2rad(self.angle)) * self.mov_speed

    def check_collision(self, another):
        if np.sqrt( (self.rect[0] - another.rect[0])**2 + (self.rect[1] - another.rect[1])**2 ) <= 15:
            return 1
        return 0