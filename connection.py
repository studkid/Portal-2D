import pygame
import asyncio

background = pygame.Surface((640, 400))
background.fill((255, 0, 0)) ## change bg color if you want to for testing

pygame.display.set_caption("Portal 2D - Connect")

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

async def connect_screen():
    global FPS

    while True:
        screen.blit(background, (0,0))

        ### connection screen code

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.update()

        await asyncio.sleep(0)