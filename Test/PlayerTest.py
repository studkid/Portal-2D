import pygame
import asyncio
from Utils.Player import Player
from Utils.Platform import Platform
from Utils import GlobalVariables

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Player Test")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def PlayerTest():
    platform_color = (41,41,41)
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, True, None), ## the main platform
        Platform(200, GlobalVariables.Height - 100, 100, 20, True, None),
        Platform(400, GlobalVariables.Height - 200, 100, 20, True, None),
        Platform(600, GlobalVariables.Height - 300, 100, 20, True, None),
        Platform(800, GlobalVariables.Height - 400, 100, 20, True, None),
        Platform(1000, GlobalVariables.Height - 500, 100, 20, True, None),
    ]

    player = Player(50, 270, GlobalVariables.Width, GlobalVariables.Height)

    running = True
    while running:
        screen.blit(background, (0,0))

        ### your test code here

        dt = clock.tick(GlobalVariables.FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        player.move(pressed_keys, platforms, dt)
        player.jump(dt)
        player.update(platforms, dt)

        for platform in platforms: 
            pygame.draw.rect(screen, platform_color, platform)
            
        pygame.draw.rect( screen, (255,0,0,0), player.rect() )

        ### end of test code

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

        await asyncio.sleep(0)