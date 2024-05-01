import pygame
from sys import exit
from Utils.Game_settings import *
from Utils.Portal_gun import *
from Utils import GlobalVariables

pygame.init()

pygame.display.set_caption("Portal 2D - Portal Test")
#tab/window settings
(width, height) = (1280, 720)
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))
clock = pygame.time.Clock()

#loads colors
WHITE = pygame.color.Color( '#ffffff' )
BLACK = pygame.color.Color( '#0a0a0a' )

platforms = [pygame.Rect( 100,300,700,50 )]
gun = Pgun(0)

async def PortalTest():
    running = True
    while running:
        keys = pygame.key.get_pressed()
        print(keys)
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
                
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, platforms[0])
        gun.update(platforms)
        gun.draw(screen)
        gun.drawHitbox(screen)
        
        # screen.blit( bullet_var, ( bullet_pos ) )

        # all_sprites_group.draw(screen)
        # all_sprites_group.update()
        pygame.display.update()
        clock.tick( FPS )
