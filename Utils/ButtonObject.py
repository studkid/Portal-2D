import pygame

class ButtonObject:
    # Constructor
    # x y: coordinates
    # type: what can interact with it
    #       0 = Both player and cube
    #       1 = Only cube
    #       2 = Only player
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.Active = False

    # Draws button
    def draw(self, screen):
        if self.Active:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.x, self.y + 10, 40, 5))
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 40, 15))

    # TODO - Add check for player and button type
    def checkActive(self, objList):
        hitbox = pygame.Rect(self.x, self.y, 40, 15)
        for obj in objList:
            rect = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
            if hitbox.colliderect(rect):
                self.Active = True
                return
            
        self.Active = False
            
