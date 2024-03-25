import pygame
import asyncio
from Utils.Player import Player
from Utils.Platform import Platform

Width, Height = 1280, 720

background = pygame.Surface((Width, Height))
background.fill((255, 255, 255)) ## change bg color if you want to for testing

pygame.display.set_caption("Portal 2D - Player Test")

Width, Height = 1280, 720
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

async def PlayerTest():
    global FPS

    platform_color = (41,41,41)
    platforms = [
        Platform(0, Height - 20, Width, 20, True, None), ## the main platform
        Platform(200, Height - 100, 100, 20, True, None),
        Platform(400, Height - 200, 100, 20, True, None),
        Platform(600, Height - 300, 100, 20, True, None),
        Platform(800, Height - 400, 100, 20, True, None),
        Platform(1000, Height - 500, 100, 20, True, None),
    ]

    player = Player(50, 270, Width, Height)

    running = True
    while running:
        screen.blit(background, (0,0))

        ### your test code here

        dt = clock.tick(60)
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