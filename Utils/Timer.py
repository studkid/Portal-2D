import pygame

# initialize pygame
pygame.init()

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