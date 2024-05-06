import pygame
import math
import sys
import os

class CubeDropper(pygame.sprite.GroupSingle):
    def __init__(self, x, y, rotation, size):
        super().__init__(self)
        self.image = pygame.image.load(os.path.join(sys.path[0], './Assets/Cube_Spawner.png'))

        self.rotation = rotation % 360
        self.image = pygame.transform.scale(self.image, (26 * size, 32 * size))
        self.image = pygame.transform.rotate(self.image, self.rotation)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def spawnCube(self):
        self.sprite.rect.center = self.rect.center
        self.sprite.speed = 1.5
        self.sprite.angle = math.pi / 180 * (360 - self.rotation)

    def spawnCubeAway(self):
        self.sprite.rect.x = -500
        self.sprite.rect.y = 5000
        self.sprite.speed = 0
        self.sprite.angle = math.pi / 180 * (360 - self.rotation)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)
        for _, obj in enumerate(super().sprites()):
            obj.drawHitbox(screen)