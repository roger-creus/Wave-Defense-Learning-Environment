import pygame

class NormalEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(NormalEnemy, self).__init__() 
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()