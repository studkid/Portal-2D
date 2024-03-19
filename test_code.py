import pygame
import asyncio
from Utils.Player import Player

background = pygame.Surface((640, 400))
background.fill((255, 255, 255)) ## change bg color if you want to for testing

pygame.display.set_caption("Portal 2D - Test")

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

async def test_screen():
    global FPS

    platform_color = (41,41,41)
    platforms = [
        pygame.Rect(0, Height - 20, Width, 20), ## the main platform
        pygame.Rect(200, 300, 100, 20), ## a random platform - low platform
        pygame.Rect(50, 200, 100, 20), ## a random platform - middle platform
        pygame.Rect(200, 100, 100, 20), ## a random platform = high platform
    ]

    player = Player(50, 270, Width, Height)

    while True:
        screen.blit(background, (0,0))

        ### your test code here

        dt = clock.tick(60)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        player.move(pressed_keys, platforms, dt)
        player.jump(dt)
        player.update(platforms, dt)

        for platform in platforms: 
            pygame.draw.rect(screen, platform_color, platform)
            
        pygame.draw.rect( screen, (255,0,0,0), player.rect() )

        ### end of test code

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.update()

        await asyncio.sleep(0)