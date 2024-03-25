import asyncio
import pygame
import random
import math

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Utils.PhysObj import PhysObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform

backgroundColor = (255, 255, 255)
plaformColor = (41, 41, 41)
(width, height) = (1280, 720)

objList = []
wallList = [
    Platform(0, height - 20, width, 20, True, None),
    Platform(200, 300, 100, 20, True, None),
    Platform(700, 500, 20, 200, False, None),
]

# Meant to test PhysObj class
import random
class TestObj(PhysObj):
    def __init__(self, x, y, size, weight, elasticity) -> None:
        super().__init__(x, y, random.uniform(0, math.pi*2), 2, weight, elasticity)
        self.size = size
        self.color = (0, 0, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.size}"
    
    def collide(self, objList):
        for obj2 in objList:
            super().collide(obj2)

    def bounce(self, width, height, wallList):
        super().bounce(width, height, wallList)

async def PhysTest():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)
    selectedObj = None
    clock = pygame.time.Clock()

    for _ in range(1):
        size = random.randint(40, 50)
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
        objList.append(TestObj(x, y, size, 0.0999, 0.2))

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
                    selectedObj = findObject(objList, mouseX, mouseY)
                elif event.button == 3:
                    size = random.randint(40, 50)
                    objList.append(TestObj(mouseX, mouseY, size, 0.0999, 0.2))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
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

        for wall in wallList:
            wall.draw(screen)
        for i, obj in enumerate(objList):
            if obj != selectedObj:
                obj.move(dt)
            obj.bounce(1280, 720, wallList)
            obj.collide(objList[i+1:])
            obj.draw(screen)
        button.checkActive(objList)
        button.draw(screen)
        pygame.display.flip()
        
        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.x-x, obj.y-y) <= obj.size:
            return obj
    return None