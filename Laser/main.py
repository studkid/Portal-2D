import pygame
import sys
import Laser

# used to initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# create random obstacles
obstacles = [
    pygame.Rect(300, 100, 200, 50),
    pygame.Rect(500, 400, 50, 150)
]

# instantiate the laser
laser = Laser.Laser((100, 300), 45, obstacles, screen)

# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))  # clear screen

    # draw the obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (123, 123, 123), obstacle)

    # draw laser
    laser.draw()

    pygame.display.flip()  # update screen

pygame.quit()
sys.exit()