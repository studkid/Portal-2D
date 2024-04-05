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
        self.opened_door = pygame.transform.scale(self.opened_door, (50, 150))
        self.image = self.closed_door
        self.exit = False

    def update(self, screen):
        return screen.blit(self.image, (self.x, self.y))
    
    def open(self, button):
        return
    
    def player_exit(self, player, pressed_keys):
        return