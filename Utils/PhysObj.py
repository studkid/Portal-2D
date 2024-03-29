import pygame
import math
import sys
import os

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
    def bounce(self, width, height, wallList):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)

        for plat in wallList:
            wall = plat.rect
            if rect.colliderect(wall):
                if rect.right > wall.left and rect.right < wall.left + 40:
                    self.x = wall.left - self.size
                    self.angle = -self.angle
                    self.speed *= self.elasticity
                elif rect.left < wall.right and rect.left > wall.right - 40:
                    self.x = wall.right
                    self.angle = -self.angle
                    self.speed *= self.elasticity

                if rect.bottom > wall.top and rect.bottom < wall.top + 40:
                    self.y = wall.top - self.size
                    self.angle = math.pi - self.angle
                    self.speed *= self.elasticity
                elif rect.top < wall.bottom and rect.top > wall.bottom - 40:
                    self.y = wall.bottom
                    self.angle = math.pi - self.angle
                    self.speed *= self.elasticity
        if rect.right > width:
            self.x = width - self.size
            self.angle = -self.angle
            self.speed *= self.elasticity
        elif rect.left < 0:
            self.x = 0
            self.angle = -self.angle
            self.speed *= self.elasticity

        if rect.bottom > height:
            self.y = height - self.size
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
        elif rect.top < 0:
            self.y = 0
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

    # Causes obj to collide with other objects
    # obj: object to collide with
    def collide(self, obj):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect2 = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
        
        if rect.colliderect(rect2):
            if rect.bottom > rect2.top and rect.bottom < rect2.top + 20:
                self.y = rect2.top - self.size + 1

                self.angle = math.pi - self.angle
                obj.angle = math.pi - obj.angle

                self.speed, obj.speed = obj.speed, self.speed
                self.speed *= self.elasticity
                obj.speed *= obj.elasticity
            elif rect.top < rect2.bottom and rect.top > rect2.bottom - 20:
                obj.y = rect.top - self.size - 1

                self.angle = math.pi - self.angle
                obj.angle = math.pi - obj.angle

                self.speed, obj.speed = obj.speed, self.speed
                self.speed *= self.elasticity
                obj.speed *= obj.elasticity
            elif rect.left < rect2.right and rect.left > rect2.right - 20:
                self.x = rect2.right - 1
                
                self.angle = math.pi - self.angle
                obj.angle = math.pi - obj.angle

                self.speed, obj.speed = obj.speed, self.speed
                self.speed *= self.elasticity
                obj.speed *= obj.elasticity
            elif rect.right > rect2.left and rect.right > rect2.left + 20:
                self.x = rect2.right - self.size + 1
                
                self.angle = math.pi - self.angle
                obj.angle = math.pi - obj.angle

                self.speed, obj.speed = obj.speed, self.speed
                self.speed *= self.elasticity
                obj.speed *= obj.elasticity

def addVectors(ang1, len1, ang2, len2):
    x = math.sin(ang1) * len1 + math.sin(ang2) * len2
    y = math.cos(ang1) * len1 + math.cos(ang2) * len2 
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

class CubeObj(PhysObj, pygame.sprite.Sprite):
    def __init__(self, x, y, weight, elasticity) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sys.path[0], './Assets/CompanionCube_Asset.png'))
        self.rect = self.image.get_rect()

        # pygame.draw.rect(self.image, (0, 0, 255), pygame.Rect(x, y, 32, 32))

        PhysObj.__init__(self, x, y, 0, 0, weight, elasticity)
        self.size = 32
        self.color = (0, 0, 255)
        print(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))
        # pygame.draw.

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.size}"
    
    def collide(self, objList):
        for obj2 in objList:
            super().collide(obj2)

    def bounce(self, width, height, wallList):
        super().bounce(width, height, wallList)