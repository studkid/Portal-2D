import pygame
import sys
import os

class PlayerButton:
    def __init__(self, x, y, timer) -> None:
        self.inactiveSprite = pygame.image.load(os.path.join(sys.path[0], './Assets/Player_Button.png'))
        self.activeSprite = pygame.image.load(os.path.join(sys.path[0], './Assets/Player_Button_Active.png'))

        self.x = x
        self.y = y
        self.timerConst = timer

        self.timer = 0
        self.active = False

    def draw(self, screen):
        if self.timer > 0:
            self.active = True
            self.timer -= 1
            screen.blit(self.activeSprite, (self.x, self.y))
        else:
            self.active = False
            screen.blit(self.inactiveSprite, (self.x, self.y))

    def activate(self):
        if not self.active:
            self.timer = self.timerConst
        