import gym
from .prefabs.normal_enemy import NormalEnemy
from .prefabs.player import Player
from .prefabs.enemy_spawner import EnemySpawner

import pygame
from pygame.locals import *
import numpy as np
import time
import os

class WaveDefenseNoReward(gym.Env):
    def __init__(self):

            self._seed = 1

            self.screen_width = 256
            self.screen_height = 256

            # Define Observation and Action spaces for RL
            self.action_space = gym.spaces.Discrete(3)
            self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.screen_height, self.screen_width, 3), dtype=np.uint8)
            
            # Define screen settings
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

            # Instantiate player and customize it
            self.player_width = 30
            self.player_height = 20
            self.max_shooting_time = 1
            self.shoot_init = time.time()

            this_dir, this_filename = os.path.split(__file__)
            DATA_PATH = os.path.join(this_dir, "player.png")

            self.player = Player(DATA_PATH, self.player_width, self.player_height, self.screen_width, self.screen_height)
            self.rotation_angle = 10
            self.current_shoot = 0

            # Init clock
            self.clock = pygame.time.Clock()
            
            # Create sprite groups
            self.enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()

            # Instantiate enemy spawner
            self.spawner = EnemySpawner(self.screen_width, self.screen_height, self.player, self.enemies, enemy_mov_speed = 1, seed = self.seed)
            self.current_enemies = 0
            self.max_enemies = 6

            self.current_bullets = 0
            self.max_bullets = 6

            # Game variables
            self.player_hp = 10

            self.init = time.time()
            self.max_spawn_time = 5

            self.init_damage = time.time()
            self.max_damaging_time = 1

            self.score = 0


    def step(self, action):
        reward = 0
        done = False

        # Handle the spawners
        current_spawn = time.time()
        if current_spawn - self.init > self.max_spawn_time or self.current_enemies == 0:
            if self.current_enemies + 1 <= self.max_enemies:
                enemy = self.spawner.spawn_enemy()
                self.enemies.add(enemy)
                self.current_enemies += 1
                self.init = current_spawn
                current_spawn = 0

        # Process action        
        if action == 0:
            self.player.rotate(self.rotation_angle)
        elif action == 1:
            self.player.rotate(-self.rotation_angle)
        elif action == 2:
            self.current_shoot = time.time()
            # Shoot maximum every 1s
            if self.current_shoot - self.shoot_init > self.max_shooting_time and len(self.bullets) < self.max_bullets:
                bullet = self.player.shoot(self.player.rect[0], self.player.rect[1])
                self.bullets.add(bullet)
                self.current_bullets += 1
                self.shoot_init = self.current_shoot
                self.current_shoot = 0

        # Clear canvas once every frame before blitting everything
        self.screen.fill((0,0,0))

        # Step all enemies towards player and blit them
        count_damaging_enemies = 0
        for enemy in self.enemies:
            enemy.step_towards_player()      
            self.screen.blit(enemy.surf,  enemy.rect)

            delta_x, delta_y, _ = enemy.distance_to_player()
            enemy_dist = (np.abs(delta_x) / self.screen_width) + (np.abs(delta_y) / self.screen_height)
            
            if enemy_dist <= 0.2:
                count_damaging_enemies += 1

        # Step all bullets forward
        for bullet in self.bullets:
            bullet.step_forward()
            if bullet.rect.x >= self.screen_width or bullet.rect.x < 0 or bullet.rect.y < 0 or bullet.rect.y > self.screen_height:
                self.bullets.remove(bullet)
                self.current_bullets -= 1
            for enemy in self.enemies:
                if bullet.check_collision(enemy):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.current_enemies -= 1
                    self.current_bullets -= 1

            self.screen.blit(bullet.surf,  bullet.rect)
        
        self.screen.blit(self.player.surf, self.player.rect)

        ### At this point all objects are drawn in the screen ###
        next_state = pygame.surfarray.array3d(self.screen)
        next_state = next_state.swapaxes(0,1)

        # Count the damage received in the current frame
        current_damage = time.time()
        if current_damage - self.init_damage > self.max_damaging_time:
            self.player_hp -= count_damaging_enemies
            if self.player_hp <= 0:
                return next_state, reward, True, {} 
            self.init_damage = current_damage
            current_damage = 0
        
        self.clock.tick(60)

        return next_state, reward, False, {}

    def reset(self):
        # Empty all enemies and bullets in game
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.current_enemies = 0
        self.current_bullets = 0
        
        # Reset player health points and score
        self.player_hp = 10
        self.score = 0

        # Reset spawn, damage and shooting timers
        self.init = time.time()
        self.init_damage = time.time()
        self.shoot_init = time.time()

        # Draw empty board with only the player
        self.screen.fill((0,0,0))
        self.screen.blit(self.player.surf, self.player.rect)
        
        # Transform surface to numpy image
        state = pygame.surfarray.array3d(self.screen)
        state = state.swapaxes(0,1)

        return state

    def render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.player.surf, self.player.rect)

        # Blit all enemies
        for enemy in self.enemies:
            self.screen.blit(enemy.surf,  enemy.rect)

        for bullet in self.bullets:
           self.screen.blit(bullet.surf,  bullet.rect)

        pygame.display.update()
        return pygame.surfarray.array3d(self.screen)

    def seed(self, seed):
        self._seed = seed
        self.spawner = EnemySpawner(self.screen_width, self.screen_height, self.player, self.enemies, enemy_mov_speed = 1, seed = _self.seed)
