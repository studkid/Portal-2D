import asyncio
import pygame
import random
import math

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Utils.PhysObj import CubeObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform
from Utils.CubeDropper import CubeDropper

backgroundColor = (255, 255, 255)
plaformColor = (41, 41, 41)
(width, height) = (1280, 720)

# dropper = pygame.sprite.Group()
wallList = [
    Platform(0, height - 20, width, 20, True, None),
    Platform(200, 300, 100, 20, True, None),
    Platform(700, 500, 20, 200, False, None),
]

# Meant to test PhysObj class
# import random
# class TestObj(PhysObj):
#     def __init__(self, x, y, size, weight, elasticity) -> None:
#         super().__init__(x, y, random.uniform(0, math.pi*2), 2, weight, elasticity)
#         self.size = size
#         self.color = (0, 0, 255)

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

#     def toString(self) -> str:
#         return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.size}"
    
#     def collide(self, objList):
#         for obj2 in objList:
#             super().collide(obj2)

#     def bounce(self, width, height, wallList):
#         super().bounce(width, height, wallList)

async def PhysTest():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)
    selectedObj = None
    clock = pygame.time.Clock()

    dropper = CubeDropper(1130, 0, 135, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()

    button = ButtonObject(230, 285, 0)
    pygame.display.update()

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            # Exit handler
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if event.button == 1:
                    selectedObj = findObject(dropper.sprites(), mouseX, mouseY)
                elif event.button == 3:
                    dropper.spawnCube()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        
        # Move Object
        if selectedObj:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selectedObj.rect.x
            dy = mouseY - selectedObj.rect.y
            selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
            selectedObj.speed = math.hypot(dx, dy) * 0.1
            selectedObj.rect.x = mouseX
            selectedObj.rect.y = mouseY

        screen.fill(backgroundColor)

        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj:
                obj.move(dt)
            obj.bounce(1280, 720, wallList)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)
        dropper.drawHitbox(screen)

        button.checkActive(dropper.sprites())
        button.draw(screen)
        
        for wall in wallList:
            wall.draw(screen)
        pygame.display.flip()
        
        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.rect.x-x, obj.rect.y-y) <= obj.size:
            return obj
    return None