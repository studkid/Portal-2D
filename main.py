import asyncio
import pygame
import random
import math
from Objects.PhysObj import TestObj, collide

backgroundColor = (255, 255, 255)
(width, height) = (1280, 720)

objList = []

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)
    selectedObj = None
    clock = pygame.time.Clock()

    for _ in range(20):
        size = random.randint(20, 30)
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
        objList.append(TestObj(screen, x, y, size, 0.005, 0.2))

    pygame.display.flip()

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            # Exit handler
            if event.type == pygame.QUIT:
                running = False
            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                selectedObj = findObject(objList, mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                selectedObj = None
        
        # Move Object
        if selectedObj:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selectedObj.x
            dy = mouseY - selectedObj.y
            selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
            selectedObj.speed = math.hypot(dx, dy) * 0.1
            selectedObj.x = mouseX
            selectedObj.y = mouseY

        screen.fill(backgroundColor)
        for i, obj in enumerate(objList):
            if obj != selectedObj:
                obj.move(dt)
            obj.bounce(1280, 720, obj.size, dt)
            for obj2 in objList[i+1:]:
                collide(obj, obj2)
            obj.draw()
        pygame.display.flip()
        
        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.x-x, obj.y-y) <= obj.size:
            return obj
    return None

asyncio.run(main())