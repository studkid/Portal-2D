import pygame

class Platform():
    # Constructor
    # x, y, width, length for Rect constructor
    # isPortable: determines if platform can have a portal
    # collision: Object blacklist for what can collide with it.  None for all objects
    def __init__(self, x, y, width, length, isPortable, collision):
        self.rect = pygame.Rect(x, y, width, length)
        self.isPortable = isPortable
        self.collision = collision

    # Draws wall
    def draw(self, screen):
        if self.isPortable:
            color = (150, 150, 150)
        else:
            color = (10, 10, 10)

        pygame.draw.rect(screen, color, self.rect)