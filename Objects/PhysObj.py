import pygame
import math

class PhysObj():
    # Constructor
    # x y: coordinates
    # weight: weight of the object
    def __init__(self, x, y, angle, speed, weight) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.weight = weight

    # Moves Object
    # Speed: Pixels to move per call
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    # Causes obj to bounce
    # Width: screen width
    # Height: screen height
    # Size: size object from origin
    # TODO, swap width/height checks with wall collision
    def bounce(self, width, height, size):
        if self.x > width - size:
            self.x = 2 * (width - size) - self.x
            self.angle = -self.angle
        elif self.x < size:
            self.x = 2* size - self.x
            self.angle = -self.angle

        if self.y > height - size:
            self.y = 2 * (height - size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < size:
            self.y = 2 * size - self.y
            self.angle = math.pi - self.angle

# Remove/move to a separate file eventually
# Meant to test PhysObj class
import random
class TestObj(PhysObj):
    def __init__(self, screen, x, y, weight, radius) -> None:
        self.screen = screen
        super().__init__(x, y, random.uniform(0, math.pi*2), 2, weight)
        self.radius = radius
        self.color = (0, 0, 255)

    def draw(self):
        super().move()
        super().bounce(1280, 720, self.radius)
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.radius}"