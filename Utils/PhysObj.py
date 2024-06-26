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
    def __init__(self, rect, angle, speed, weight, elasticity) -> None:
        self.rect = rect
        self.angle = angle
        self.speed = speed
        self.weight = weight
        self.elasticity = elasticity

    # Moves Object
    # Speed: Pixels to move per call
    def move(self, dt):
        self.angle, self.speed = addVectors(self.angle, self.speed, math.pi, self.weight)
        self.rect.x += math.sin(self.angle) * self.speed * dt
        self.rect.y -= math.cos(self.angle) * self.speed * dt
        self.speed *= 0.999

    # Causes obj to bounce
    # Width: screen width
    # Height: screen height
    # Size: size object from origin
    # TODO, swap width/height checks with wall collision
    def bounce(self, width, height, wallList):
        if self.rect.left > -100 and self.rect.top > -100:
            for plat in wallList:
                wall = plat.rect
                if self.rect.colliderect(wall) and plat.active and not plat.collision == 1:
                    if self.rect.bottom > wall.top and self.rect.bottom < wall.top + 30:
                        self.rect.bottom = wall.top
                        self.angle = math.pi - self.angle
                        self.speed *= self.elasticity
                    elif self.rect.top < wall.bottom and self.rect.top > wall.bottom - 30:
                        self.rect.top = wall.bottom
                        self.angle = math.pi - self.angle
                        self.speed *= self.elasticity
            
                    elif self.rect.right > wall.left and self.rect.right < wall.left + 30:
                        self.rect.right = wall.left
                        self.angle = -self.angle
                        self.speed *= self.elasticity
                    elif self.rect.left < wall.right and self.rect.left > wall.right - 30:
                        self.rect.left = wall.right
                        self.angle = -self.angle
                        self.speed *= self.elasticity


            if self.rect.right > width:
                self.rect.right = width
                self.angle = -self.angle
                self.speed *= self.elasticity
            elif self.rect.left < 0:
                self.rect.left = 0
                self.angle = -self.angle
                self.speed *= self.elasticity

            if self.rect.bottom > height:
                self.rect.bottom = height
                self.angle = math.pi - self.angle
                self.speed *= self.elasticity
            elif self.rect.top < 0:
                self.rect.top = 0
                self.angle = math.pi - self.angle
                self.speed *= self.elasticity


    # Causes obj to collide with other objects
    # obj: object to collide with
    def collide(self, obj):
        rect2 = obj.rect
        if self.rect.left > -100 and self.rect.top > -100:
            if self.rect.colliderect(rect2):
                if self.rect.bottom > rect2.top and self.rect.bottom < rect2.top + 20:
                    self.rect.y = rect2.top - self.size + 1

                    self.angle = math.pi - self.angle
                    obj.angle = math.pi - obj.angle

                    self.speed, obj.speed = obj.speed, self.speed
                    self.speed *= self.elasticity
                    obj.speed *= obj.elasticity
                elif self.rect.top < rect2.bottom and self.rect.top > rect2.bottom - 20:
                    obj.rect.y = self.rect.top - self.size - 1

                    self.angle = math.pi - self.angle
                    obj.angle = math.pi - obj.angle

                    self.speed, obj.speed = obj.speed, self.speed
                    self.speed *= self.elasticity
                    obj.speed *= obj.elasticity
                elif self.rect.left < rect2.right and self.rect.left > rect2.right - 20:
                    self.rect.x = rect2.right - 1
                    
                    self.angle = math.pi - self.angle
                    obj.angle = math.pi - obj.angle

                    self.speed, obj.speed = obj.speed, self.speed
                    self.speed *= self.elasticity
                    obj.speed *= obj.elasticity
                elif self.rect.right > rect2.left and self.rect.right > rect2.left + 20:
                    self.rect.x = rect2.right - self.size + 1
                    
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
        self.size = self.image.get_rect().width * 2
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        PhysObj.__init__(self, self.image.get_rect(), 0, 0, weight, elasticity)
        self.x = x
        self.y = y

        self.runPhysics = True
        self.warpCooldown = 0

    def update(self):
        if self.warpCooldown > 0:
            self.warpCooldown -= 1

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)

    def toString(self) -> str:
        return f"({self.rect.x}, {self.rect.y}) Weight: {self.weight} Radius: {self.size}"
    
    def collide(self, objList):
        for obj2 in objList:
            super().collide(obj2)

    def bounce(self, width, height, wallList):
        super().bounce(width, height, wallList)

    def portalWarp(self, portals):
        touchedPortal = False
        for portal in portals:
            if self.rect.colliderect(portal):
                touchedPortal = True
                if self.warpCooldown > 0 or not self.runPhysics:
                    return
                if portal.playerNum == 0:
                    self.rect.center = portals[1].rect.center
                    self.angle = (270 - portals[1].angle) % 360 * math.pi / 180
                    self.warpCooldown = 20
                    return
                elif portal.playerNum == 1:
                    self.rect.center = portals[0].rect.center
                    self.angle = (270 - portals[0].angle) % 360 * math.pi / 180
                    self.warpCooldown = 20 
                    return
        if not touchedPortal:
            self.warpCooldown = 0