import prefabs
from prefabs.normal_enemy import NormalEnemy
from prefabs.player import Player
from prefabs.enemy_spawner import EnemySpawner

import pygame
from pygame.locals import *
import numpy as np
import time

# Init and define screen
pygame.init()
width = 640
height = 400
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("./resources/sprites/black.jpg")
bg = pygame.transform.scale(bg, (width, height)) 

# Init clock
clock = pygame.time.Clock()

# Instantiate player
player = Player("./resources/sprites/player.png", 45, 30)

# Create sprite groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Instantiate enemy spawner
spawner = EnemySpawner(width, height, player, enemies)

# Game loop
init = time.time()
max_spawn_time = 1
running = True
while running:
    # Check for events                
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                running = False
            if event.key == K_a:
                player.rotate(10)
            if event.key == K_d:
                player.rotate(-10)
            if event.key == K_SPACE:
                bullet = player.shoot(player.rect[0], player.rect[1])
                bullets.add(bullet)
    
        elif event.type == QUIT:
            running = False

    # Continuosly handle enemy spawners
    current = time.time()
    if current - init > max_spawn_time:
        enemy = spawner.spawn_enemy()
        enemies.add(enemy)
        init = current
        current = 0

    # Clear canvas once every frame before blitting everything
    clear = False
    if not clear:
        screen.blit(bg,(0,0))
        clear = True

    # Step all enemies towards player and blit them
    for enemy in enemies:
        enemy.step_towards_player()
        screen.blit(enemy.surf,  enemy.rect)
    
    # Step all bullets forward
    for bullet in bullets:
        bullet.step_forward()
        screen.blit(bullet.surf,  bullet.rect)
        
    # Plot player and update display
    screen.blit(player.surf, player.rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()