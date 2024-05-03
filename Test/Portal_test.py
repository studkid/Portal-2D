import pygame
from sys import exit
from Utils.Game_settings import *
from Utils.Portal_gun import *
from Utils import GlobalVariables
from Utils.Platform import Platform

pygame.init()

pygame.display.set_caption("Portal 2D - Portal Test")
#tab/window settings
(width, height) = (1280, 720)
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))
clock = pygame.time.Clock()

#loads colors
WHITE = pygame.color.Color( '#ffffff' )
BLACK = pygame.color.Color( '#0a0a0a' )

platforms = [Platform( 100, 300, 700, 50, True, 0 )]
gun = Pgun(True)

async def PortalTest():
    running = True
    while running:
        keys = pygame.key.get_pressed()
        if keys[ pygame.K_w ]:
            gun.hitbox_rect.y += -8
        if keys[ pygame.K_s ]:
            gun.hitbox_rect.y += 8
        if keys[ pygame.K_d ]:
            gun.hitbox_rect.x += 8
        if keys[ pygame.K_a ]:
            gun.hitbox_rect.x += -8

    #lets you quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun.is_shooting()
                
        screen.fill(WHITE)
        platforms[0].draw(screen)
        gun.update(platforms)
        gun.draw(screen)
        gun.drawHitbox(screen)
        
        # screen.blit( bullet_var, ( bullet_pos ) )

        # all_sprites_group.draw(screen)
        # all_sprites_group.update()
        pygame.display.update()
        clock.tick( FPS )
