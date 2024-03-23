import asyncio
import pygame
import random
import math
from Utils.PhysObj import PhysObj

backgroundColor = (255, 255, 255)
plaformColor = (41, 41, 41)
(width, height) = (1280, 720)

objList = []
wallList = [
    pygame.Rect(0, height - 20, width, 20),
    pygame.Rect(200, 300, 100, 20),
    pygame.Rect(700, 500, 20, 200),
]

# Meant to test PhysObj class
import random
class TestObj(PhysObj):
    def __init__(self, screen, x, y, size, weight, elasticity) -> None:
        self.screen = screen
        super().__init__(x, y, random.uniform(0, math.pi*2), 2, weight, elasticity)
        self.size = size
        self.color = (0, 0, 255)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.size}"
    
    def collide(self, objList):
        for obj2 in objList:
            super().collide(obj2)

    def bounce(self, width, height, wallList):
        super().bounce(width, height, wallList)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(backgroundColor)
    selectedObj = None
    clock = pygame.time.Clock()

    for _ in range(1):
        size = random.randint(40, 50)
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
        objList.append(TestObj(screen, x, y, size, 0.0999, 0.2))

    pygame.display.update()

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

        for wall in wallList:
            pygame.draw.rect(screen, plaformColor, wall)
        for i, obj in enumerate(objList):
            if obj != selectedObj:
                obj.move(dt)
            obj.bounce(1280, 720, wallList)
            obj.collide(objList[i+1:])
            obj.draw()
        pygame.display.flip()
        
        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.x-x, obj.y-y) <= obj.size:
            return obj
    return None

asyncio.run(main())