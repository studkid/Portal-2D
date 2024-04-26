import pygame

class Platform():
    # Constructor
    # x, y, width, length for Rect constructor
    # isPortable: determines if platform can have a portal
    # collision: determines what can interact with the platform
    #       0 = Both player and cube
    #       1 = Only cube
    #       2 = Only player
    # active: determins if the platform should be rendered/collided with
    def __init__(self, x, y, width, length, isPortable, collision):
        self.rect = pygame.Rect(x, y, width, length)
        self.isPortable = isPortable
        self.collision = collision
        self.active = True

    # Draws wall
    def draw(self, screen):
        if not self.active:
            return

        if self.collision == 1:
            color = (255, 0, 0)
        elif self.collision == 2:
            color = (3, 155, 229)
        elif self.isPortable:
            color = (150, 150, 150)
        else:
            color = (10, 10, 10)

        pygame.draw.rect(screen, color, self.rect)