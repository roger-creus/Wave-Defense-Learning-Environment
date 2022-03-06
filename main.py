from prefabs.normal_enemy import NormalEnemy
from prefabs.player import Player
import pygame
from pygame.locals import *
import prefabs
import numpy as np

# Init and define screen
pygame.init()
screen = pygame.display.set_mode((640, 400))
bg = pygame.image.load("./resources/sprites/black.jpg")
bg = pygame.transform.scale(bg, (640, 400)) 

clock = pygame.time.Clock()


player = Player("./resources/sprites/player.png", 45, 30)
player.rect = (320, 200)

normal_enemy = NormalEnemy()
normal_enemy.rect = (600,300)

# create sprite groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)
enemies.add(normal_enemy)

running = True
while running:       
    for enemy in enemies:
        deltaX = player.rect[0] - enemy.rect[0]
        deltaY = player.rect[1] - enemy.rect[1]

        angle = np.arctan2(deltaY, deltaX)
        
        pos_x = enemy.rect[0] + np.cos(angle) 
        pos_y = enemy.rect[1] + np.sin(angle)
        
        enemy.rect = (pos_x, pos_y)
        screen.blit(bg,(0,0))
        screen.blit(enemy.surf,  enemy.rect)

                
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                running = False
        elif event.type == QUIT:
            running = False
    
    screen.blit(player.surf, player.rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()