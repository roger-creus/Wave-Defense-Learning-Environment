import envs.prefabs
from envs.prefabs.normal_enemy import NormalEnemy
from envs.prefabs.player import Player
from envs.prefabs.enemy_spawner import EnemySpawner

import pygame
from pygame.locals import *
import numpy as np
import time
from IPython import embed

# Init and define screen
pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load("./wave_defense/envs/resources/sprites/black.jpg")
bg = pygame.transform.scale(bg, (screen_width, screen_height)) 

# Init clock
clock = pygame.time.Clock()

# Instantiate player
player_width = 45
player_height = 30
max_shooting_time = 0.5
shoot_init = time.time()
player = Player("./wave_defense/envs/resources/sprites/player.png", player_width, player_height, screen_width, screen_height)

# Create sprite groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Instantiate enemy spawner
spawner = EnemySpawner(screen_width, screen_height, player, enemies)

# Game loop
player_hp = 10

init = time.time()
max_spawn_time = 3

init_damage = time.time()
max_damaging_time = 1

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
                # Shoot maximum every 0.5s
                current_shoot = time.time()
                if current_shoot - shoot_init > max_shooting_time:
                    bullet = player.shoot(player.rect[0], player.rect[1])
                    bullets.add(bullet)
                    shoot_init = current_shoot
                    current_shoot = 0

        elif event.type == QUIT:
            running = False

    # Continuosly handle enemy spawners
    current_spawn = time.time()
    if current_spawn - init > max_spawn_time:
        enemy = spawner.spawn_enemy()
        enemies.add(enemy)
        init = current_spawn
        current_spawn = 0

    # Clear canvas once every frame before blitting everything
    clear = False
    if not clear:
        screen.blit(bg,(0,0))
        clear = True

    # Step all enemies towards player and blit them
    count_damaging_enemies = 0
    for enemy in enemies:
        damaging = enemy.step_towards_player()
        screen.blit(enemy.surf,  enemy.rect)
        if damaging:
            count_damaging_enemies += 1

    current_damage = time.time()
    if current_damage - init_damage > max_damaging_time:
        player_hp -= count_damaging_enemies
        if player_hp <= 0:
            print("you lost")
        init_damage = current_damage
        current_damage = 0
    
    # Step all bullets forward
    for bullet in bullets:
        bullet.step_forward()
        for enemy in enemies:
            if bullet.check_collision(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
        screen.blit(bullet.surf,  bullet.rect)
        
    # Plot player and update display
    screen.blit(player.surf, player.rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()