import pygame
import numpy as np

class NormalEnemy(pygame.sprite.Sprite):
    def __init__(self, player,x, y, mov_speed=1.5, damage_distance = 35):
        super(NormalEnemy, self).__init__() 
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect(center=(x,y))
        self.player = player
        self.mov_speed = mov_speed
        self.damage_distance = damage_distance

    def step_towards_player(self):
        _, _, distance_to_player = self.distance_to_player()
        
        if distance_to_player > self.damage_distance:
            angle = self.angle_to_player()
            
            pos_x = self.rect[0] + np.cos(angle) * self.mov_speed
            pos_y = self.rect[1] + np.sin(angle) * self.mov_speed 

            self.rect = (pos_x, pos_y, 20, 20)            
            

    def distance_to_player(self):
        delta_X = self.rect[0] - self.player.rect[0]
        delta_Y = self.rect[1] - self.player.rect[1]
        distance_to_player = np.sqrt(delta_X**2 + delta_Y**2)
        return delta_X, delta_Y, distance_to_player

    def angle_to_player(self):
        deltaX = self.player.rect[0] - self.rect[0]
        deltaY = self.player.rect[1] - self.rect[1]
        angle = np.arctan2(deltaY, deltaX)
        return angle