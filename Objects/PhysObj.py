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
    def bounce(self, width, height, size, dt):
        if self.x > width - size:
            self.x = 2 * (width - size) - self.x
            self.angle = -self.angle
            self.speed *= self.elasticity
        elif self.x < size:
            self.x = 2* size - self.x
            self.angle = -self.angle
            self.speed *= self.elasticity

        if self.y > height - size:
            self.y = 2 * (height - size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
        elif self.y < size:
            self.y = 2 * size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

def collide(obj1, obj2):
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y 

    distance = math.hypot(dx, dy)
    if distance < obj1.size + obj2.size:
        tangent = math.atan2(dy, dx)
        obj1.angle = 2 * tangent - obj1.angle
        obj2.angle = 2 * tangent - obj2.angle

        obj1.speed, obj2.speed = obj2.speed, obj1.speed
        obj1.speed *= obj1.elasticity
        obj2.speed *= obj2.elasticity

        angle = 0.5 * math.pi + tangent
        obj1.x += math.sin(angle)
        obj1.y -= math.cos(angle)
        obj2.x -= math.sin(angle)
        obj2.y += math.cos(angle)

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
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.size}"