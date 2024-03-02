import asyncio
import pygame
import random
from Objects.PhysObj import TestObj

backgroundColor = (255, 255, 255)
(width, height) = (1280, 720)

objList = []

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)

    for _ in range(20):
        size = random.randint(20, 30)
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
        objList.append(TestObj(screen, x, y, 5, size))

    pygame.display.flip()

    running = True
    while running:
        # exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(backgroundColor)
        for obj in objList:
            obj.draw()
        pygame.display.flip()
        
        await asyncio.sleep(0)

asyncio.run(main())