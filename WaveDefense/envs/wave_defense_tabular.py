import gym
from .prefabs.normal_enemy import NormalEnemy
from .prefabs.player import Player
from .prefabs.enemy_spawner import EnemySpawner

import pygame
from pygame.locals import *
import numpy as np
import time
import os

class WaveDefenseTabular(gym.Env):
    def __init__(self):
            this_dir, this_filename = os.path.split(__file__)

            # this is set when calling make_env() wrapper (see /models)
            self._seed = 1

            self.screen_width = 800
            self.screen_height = 800

            # Define Observation and Action spaces for RL
            self.action_space = gym.spaces.Discrete(3)
            self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(35,), dtype=np.float)
            
            # Define screen settings
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

            # Instantiate player and customize it
            self.player_width = 45
            self.player_height = 30
            self.max_shooting_time = 1
            self.shoot_init = time.time()

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
            self.spawner = EnemySpawner(self.screen_width, self.screen_height, self.player, self.enemies, enemy_mov_speed = 2.5, seed = self.seed)
            self.current_enemies = 0
            self.max_enemies = 6
            
            self.current_bullets = 0
            self.max_bullets = 10

            # Game variables
            self.player_hp = 10

            self.init = time.time()
            self.max_spawn_time = 3

            self.init_damage = time.time()
            self.max_damaging_time = .5

            self.score = 0


    def get_current_game_state(self):

        input_vec = [self.player.angle / 360, self.player_hp / 10]
       
        if self.current_shoot - self.shoot_init > self.max_shooting_time:
            input_vec += [1]
        else:
            input_vec += [0]
           

        # Add info of all enemies in game (either pos x and pos y or angle and distance)
        enemies_to_pad = self.max_enemies - len(self.enemies) 
        for enemy in self.enemies:
            #pos_x = enemy.rect[0] / self.screen_width
            #pos_y = enemy.rect[1] / self.screen_height
            delta_x, delta_y, _ = enemy.distance_to_player()
            dist = (np.abs(delta_x) / self.screen_width) + (np.abs(delta_y) / self.screen_height)
            angle = np.abs(np.rad2deg(enemy.angle_to_player()) -  180) / 360
            input_vec += [dist, angle]
        
        for i in range(enemies_to_pad):
            input_vec += [0, 0]          

        # Add info of all bullets in game
        bullets_to_pad = self.max_bullets - len(self.bullets)
        for bullet in self.bullets:
            pos_x = bullet.rect[0] / self.screen_width
            pos_y = bullet.rect[1]  / self.screen_height
            input_vec += [pos_x, pos_y]

        for i in range(bullets_to_pad):
            input_vec += [0, 0]


        return np.array(input_vec)


    def step(self, action):
        reward = 1
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
            #else:
                # -5 reward if trying to shoot when "reloading"
                #reward -= 5

        # Clear canvas once every frame before blitting everything
        self.screen.fill((0,0,0))


        # Step all enemies towards player and blit them
        count_damaging_enemies = 0
        for enemy in self.enemies:
            enemy.step_towards_player()      
            self.screen.blit(enemy.surf,  enemy.rect)

            # for each enemy we give negative reward depending on how close it is to the player
            delta_x, delta_y, _ = enemy.distance_to_player()
            enemy_dist = (np.abs(delta_x) / self.screen_width) + (np.abs(delta_y) / self.screen_height)
            enemy_reward = enemy_dist - 1
            reward += enemy_reward
            
            if enemy_dist <= 0.12:
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
                    # Reward for killing an enemy
                    reward += 30
            self.screen.blit(bullet.surf,  bullet.rect)

        self.screen.blit(self.player.surf, self.player.rect)

        ### At this point all objects are drawn in the screen ###
        next_state = self.get_current_game_state()

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
        self.current_bullets = 0
        self.current_enemies = 0
        
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
        state = self.get_current_game_state()

        return np.array(state)

    def render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.player.surf, self.player.rect)

        # Blit all enemies
        for enemy in self.enemies:
            self.screen.blit(enemy.surf,  enemy.rect)

        for bullet in self.bullets:
           self.screen.blit(bullet.surf,  bullet.rect)

        state = self.get_current_game_state()

        pygame.display.update()
        return pygame.surfarray.array3d(self.screen)

    def seed(self, seed):
        self._seed = seed
        self.spawner = EnemySpawner(self.screen_width, self.screen_height, self.player, self.enemies, enemy_mov_speed = 2.5, seed = self._seed)
