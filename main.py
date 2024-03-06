import pygame
import asyncio
from Utils.Player import Player

background = pygame.Surface((640, 400))
background.fill((30, 90, 120))

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

player = Player(50, 270, Width, Height)

async def main():
    global Width
    global Height
    global FPS

    while True:
        screen.blit(background,(0,0))
        pygame.draw.rect( screen, (0,0,255), player.rect() )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        clock.tick(FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        player.move(pressed_keys)
        player.jump()
        player.update()
        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())