import asyncio
import pygame
from Objects.PhysObj import *

background_color = (255, 255, 255)
(width, height) = (1280, 720)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_color)

    pygame.display.flip()

    running = True
    while running:
        # exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        
        await asyncio.sleep(0)

asyncio.run(main())