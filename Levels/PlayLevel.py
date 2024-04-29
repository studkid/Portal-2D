import pygame
from Levels import level_one
from Levels import level_two
from Levels import level_three
from Levels import level_four
from Levels import level_five

async def play_level(level):
    pygame.display.flip()
    pygame.event.pump()
    pygame.time.wait(100) 
    if level == 1:
        await level_one.Level()
    elif level == 2:
        await level_two.Level()
    elif level == 3:
        await level_three.Level()
    elif level == 4:
        await level_four.Level()
    elif level == 5:
        await level_five.Level()