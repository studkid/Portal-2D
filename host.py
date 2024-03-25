import pygame
import asyncio

Width, Height = 1280, 720

background = pygame.Surface((Width, Height))
background.fill((41, 41, 41))

pygame.display.set_caption("Portal 2D - Levels")

FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

async def host_screen():
    global FPS

    running = True
    while running:
        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

        await asyncio.sleep(0)