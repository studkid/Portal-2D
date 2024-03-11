import pygame
from sys import exit
import math
from game_settings import *
from portal_gun import *

pygame.init()

#tab/window settings
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( "2D Portal" )
clock = pygame.time.Clock()

#loads images
background = pygame.transform.scale(pygame.image.load( "img/background/background.png" ).convert(), ( WIDTH, HEIGHT ) )

while True:
    keys = pygame.key.get_pressed()

#lets you quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit( background, ( 0, 0 ) )


    all_sprites_group.draw(screen)
    all_sprites_group.update()
    pygame.display.update()
    clock.tick( FPS )
