import sys
import pygame
import os
from Utils import GlobalVariables

class ExitDoor():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.closed_door = pygame.image.load(os.path.join(sys.path[0], './Assets/ExitDoor_Closed.png')).convert_alpha()
        self.closed_door = pygame.transform.scale(self.closed_door, (50, 150))
        self.opened_door = pygame.image.load(os.path.join(sys.path[0], './Assets/ExitDoor_Open.png')).convert_alpha()
        self.opened_door = pygame.transform.scale(self.opened_door, (100, 150))
        self.image = self.closed_door
        self.opened = False

    def update(self, screen):
        return screen.blit(self.image, (self.x, self.y))
    
    def door_status(self, button):
        if button.active:
            self.image = self.opened_door
            self.opened = True
        else:
            self.image = self.closed_door
            self.opened = False
    
    def can_exit(self, player, pressed_keys):
        if self.opened:
            if pressed_keys[pygame.K_e]:
                if player.x > self.x and player.x < self.x + 100:
                    if player.y > self.y and player.y < self.y - 150:
                        return True

        return False