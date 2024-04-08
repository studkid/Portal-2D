import sys
import pygame
import os
from Utils import GlobalVariables

class ExitDoor():

    def __init__(self, x, y):
        self.x = x
        self.opened_x = self.x - 75
        self.closed_x = self.x
        self.y = y
        self.closed_door = pygame.image.load(os.path.join(sys.path[0], './Assets/ExitDoor_Closed.png')).convert_alpha()
        self.closed_door = pygame.transform.scale(self.closed_door, (75, 150))
        self.opened_door = pygame.image.load(os.path.join(sys.path[0], './Assets/ExitDoor_Open.png')).convert_alpha()
        self.opened_door = pygame.transform.scale(self.opened_door, (150, 150))
        self.image = self.closed_door
        self.opened = False

    def update(self, screen):
        return screen.blit(self.image, (self.x, self.y))
    
    def door_status(self, button):
        if button.Active:
            self.image = self.opened_door
            self.opened = True
            self.x = self.opened_x
        else:
            self.image = self.closed_door
            self.opened = False
            self.x = self.closed_x
    
    def try_exit(self, player, pressed_keys):
        if self.opened:
            if pressed_keys[pygame.K_e]:
                if (player.x > self.x + 75 and player.x < self.x + 150) or (player.x + player.size_x > self.x + 75 and player.x + player.size_x < self.x + 150):
                    if player.y > self.y:
                        print("Player tried to exit!!!!!!!!!!")
                        return True

        return False