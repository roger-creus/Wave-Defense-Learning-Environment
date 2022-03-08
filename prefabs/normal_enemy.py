import pygame
import numpy as np

class NormalEnemy(pygame.sprite.Sprite):
    def __init__(self, player,x, y, mov_speed=1, damage_distance = 100):
        super(NormalEnemy, self).__init__() 
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect(center=(x,y))
        self.player = player
        self.mov_speed = mov_speed
        self.damage_distance = damage_distance

    def step_towards_player(self):
        if np.sqrt((self.rect[0] - self.player.rect[0])**2 + (self.rect[1] - self.player.rect[1])**2) > self.damage_distance:
            deltaX = self.player.rect[0] - self.rect[0]
            deltaY = self.player.rect[1] - self.rect[1]

            angle = np.arctan2(deltaY, deltaX)
            
            pos_x = self.rect[0] + np.cos(angle) * self.mov_speed
            pos_y = self.rect[1] + np.sin(angle) * self.mov_speed 

            self.rect = (pos_x, pos_y, 25, 25)