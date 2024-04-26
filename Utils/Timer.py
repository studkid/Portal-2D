import pygame
import sys

# initialize pygame
pygame.init()

# the set up screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Platformer")

# color(s)
WHITE = (255, 255, 255)

# the font(s)
font = pygame.font.Font(None, 36)

# timer variables
timer_started = False
start_time = 0
elapsed_time = 0

def start_timer():
    global timer_started, start_time
    timer_started = True
    start_time = pygame.time.get_ticks()

def stop_timer():
    global timer_started, elapsed_time
    if timer_started:
        elapsed_time = pygame.time.get_ticks() - start_time
        timer_started = False

# main game loop
running = True
while running:
    screen.fill(WHITE)

    # check for the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # press 'space' to stop the timer
                stop_timer()

    # start the timer when the level is loaded i.e. the start of the game
    if not timer_started:
        start_timer()

    # display the timer in the top-right corner of the screen
    if timer_started:
        current_time = pygame.time.get_ticks() - start_time
        timer_text = font.render("Time: " + str(current_time // 1000) + "s", True, (0, 0, 0))
        screen.blit(timer_text, (screen_width - 200, 20))

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()