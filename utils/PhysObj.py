import pygame
import math

# Code based off of: https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/
class PhysObj():
    # Constructor
    # x y: coordinates
    # weight: weight of the object
    # elasticity: "bounciness" of the object
    def __init__(self, x, y, angle, speed, weight, elasticity) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.weight = weight
        self.elasticity = elasticity

    # Moves Object
    # Speed: Pixels to move per call
    def move(self, dt):
        self.angle, self.speed = addVectors(self.angle, self.speed, math.pi, self.weight)
        self.x += math.sin(self.angle) * self.speed * dt
        self.y -= math.cos(self.angle) * self.speed * dt
        self.speed *= 0.999

    # Causes obj to bounce
    # Width: screen width
    # Height: screen height
    # Size: size object from origin
    # TODO, swap width/height checks with wall collision
    def bounce(self, width, height, size):
        rect = pygame.Rect(self.x, self.y, size, size)
        if rect.right > width:
            self.x = width - size
            self.angle = -self.angle
            self.speed *= self.elasticity
        elif rect.left < 0:
            self.x = 0
            self.angle = -self.angle
            self.speed *= self.elasticity

        if rect.bottom > height:
            self.y = height - size
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
        elif rect.top < 0:
            self.y = 0
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

    # Causes obj to collide with other objects
    # obj: object to collie with
    def collide(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y 

        distance = math.hypot(dx, dy)
        if distance < self.size + obj.size:
            tangent = math.atan2(dy, dx)
            self.angle = 2 * tangent - self.angle
            obj.angle = 2 * tangent - obj.angle

            self.speed, obj.speed = obj.speed, self.speed
            self.speed *= self.elasticity
            obj.speed *= obj.elasticity

            angle = 0.5 * math.pi + tangent
            self.x += math.sin(angle)
            self.y -= math.cos(angle)
            obj.x -= math.sin(angle)
            obj.y += math.cos(angle)
        

def addVectors(ang1, len1, ang2, len2):
    x = math.sin(ang1) * len1 + math.sin(ang2) * len2
    y = math.cos(ang1) * len1 + math.cos(ang2) * len2 
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

# Remove/move to a separate file eventually
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
        super().bounce(width, height, self.size)