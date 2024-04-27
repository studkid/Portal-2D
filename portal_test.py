import pygame
from sys import exit
from Utils.Game_settings import *
from Utils.Portal_gun import *
from Utils.GlobalVariables import *

pygame.init()

#tab/window settings
screen = pygame.display.set_mode( ( Width, Height ) )
pygame.display.set_caption( "2D Portal" )
clock = pygame.time.Clock()

#loads colors
WHITE = pygame.color.Color( '#ffffff' )
BLACK = pygame.color.Color( '#0a0a0a' )



while True:
    keys = pygame.key.get_pressed()

#lets you quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, platform)
    screen.blit( portal_var, ( portal_pos ) )
    screen.blit( bullet_var, ( bullet_pos ) )


    all_sprites_group.draw(screen)
    all_sprites_group.update()
    pygame.display.update()
    clock.tick( FPS )
