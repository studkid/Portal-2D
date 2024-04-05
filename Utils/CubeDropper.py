import pygame
import math
import sys
import os

class CubeDropper(pygame.sprite.GroupSingle):
    def __init__(self, x, y, rotation):
        super().__init__(self)
        self.image = pygame.image.load(os.path.join(sys.path[0], './Assets/Cube_Spawner.png'))

        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def spawnCube(self):
        self.sprite.rect.center = self.rect.center
        self.sprite.speed = 2
        self.sprite.angle = math.pi / 180 * self.rotation 

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)