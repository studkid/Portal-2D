import asyncio
import pygame
import pygbag
import random

backgroundColor = (255, 255, 255)
(width, height) = (1280, 720)

objList = []

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)
    selectedObj = None

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            # Exit handler
            if event.type == pygame.QUIT:
                running = False
        print("running!")

        await asyncio.sleep(0)

asyncio.run(main())