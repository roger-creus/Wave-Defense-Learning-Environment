import time
import random
from .normal_enemy import NormalEnemy

class EnemySpawner():
    def __init__(self, width, height, player, enemies, enemy_mov_speed=1.5, seed = 1):
        super(EnemySpawner, self).__init__() 
        self.init = time.time()
        self.player = player
        self.enemies = enemies
        self.width = width
        self.height = height
        self.enemy_mov_speed = enemy_mov_speed
        
        random.seed(seed)

    def spawn_enemy(self):
        if random.randint(0,1) == 0:
            if random.randint(0,1):
                pos_x = self.width + 5
                pos_y = random.randint(0, self.height)           
            else:
                pos_x = -5
                pos_y = random.randint(0, self.height)
        else:
            if random.randint(0,1):
                pos_y = self.height + 5
                pos_x = random.randint(0, self.width)
            else:
                pos_y = -5
                pos_x = random.randint(0, self.width)

        normal_enemy = NormalEnemy(self.player, pos_x, pos_y, mov_speed = self.enemy_mov_speed)
        return normal_enemy