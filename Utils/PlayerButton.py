import pygame
import sys
import os

class PlayerButton:
    def __init__(self, x, y, timer) -> None:
        self.inactiveSprite = pygame.image.load(os.path.join(sys.path[0], './Assets/Player_Button.png'))
        self.activeSprite = pygame.image.load(os.path.join(sys.path[0], './Assets/Player_Button_Active.png'))
        self.rect = self.activeSprite.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.timerConst = timer
        self.timer = 0
        self.active = False

    def draw(self, screen):
        if self.timer > 0:
            self.timer -= 1
            screen.blit(self.activeSprite, (self.rect.x, self.rect.y))
        else:
            self.active = False
            screen.blit(self.inactiveSprite, (self.rect.x, self.rect.y))

    def activate(self) -> bool:
        if not self.active:
            self.timer = self.timerConst
            self.active = True
            return True
        return False

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)