import pygame
import asyncio

Width, Height = 640, 400

background = pygame.Surface((Width, Height))
background.fill((41, 41, 41))

pygame.display.set_caption("Portal 2D - Levels")

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

async def level_screen():
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