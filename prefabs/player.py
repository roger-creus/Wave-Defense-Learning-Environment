import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, img_path, width, height):
        super().__init__()

        self.surf = pygame.image.load(img_path)
        self.surf = pygame.transform.scale(self.surf, (width, height)) 
        self.rect = self.surf.get_rect(center=(0,0))