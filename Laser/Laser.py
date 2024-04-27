import pygame
import math

class Laser:
    def __init__(self, start_pos, direction, obstacles, screen, color=(255, 0, 0)):
        self.start_pos = start_pos
        self.direction = direction
        self.obstacles = obstacles
        self.screen = screen
        self.color = color
        self.end_pos = self.calculate_end_pos()
        self.bounding_rect = pygame.Rect(self.start_pos, (1, 1)).union(pygame.Rect(self.end_pos, (1, 1)))

    def calculate_end_pos(self):
        x, y = self.start_pos
        angle = self.direction
        length = 1280  # ajust to the scale of the game is needed
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y + length * math.sin(math.radians(angle))

        # temporary endpoint before collision detection
        closest_point = (int(end_x), int(end_y))

        # create a line from start_pos to the calculated far end
        dx = end_x - x
        dy = end_y - y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize direction vector
        for step in range(int(dist)):
            # incrementally check for collision
            check_x = int(x + dx * step)
            check_y = int(y + dy * step)
            ##if any(obstacle.collidepoint(check_x, check_y) for obstacle in self.obstacles):
                ##closest_point = (check_x, check_y)
                ##break

        return closest_point

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.start_pos, self.end_pos, 2)