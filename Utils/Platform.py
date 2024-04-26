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
        self.surface = pygame.Surface((width, length))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isPortable = isPortable
        self.collision = collision
        self.active = True

    # Draws wall
    def draw(self, screen):
        if not self.active:
            return

        if self.collision == 1:
            self.surface.fill((255, 0, 0))
            self.surface.set_alpha(128)
        elif self.collision == 2:
            self.surface.fill((3, 155, 229))
            self.surface.set_alpha(128)
        elif self.isPortable:
            self.surface.fill((150, 150, 150))
            self.surface.set_alpha(255)
        else:
            self.surface.fill((10, 10, 10))
            self.surface.set_alpha(255)

        screen.blit(self.surface, (self.rect.x, self.rect.y))