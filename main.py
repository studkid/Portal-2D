import pygame
import asyncio
from Utils.Player import Player

background = pygame.Surface((640, 400))
background.fill((255, 255, 255))

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

player = Player(50, 270, Width, Height)

platform_color = (41,41,41)
platforms = [
    pygame.Rect(0, Height - 20, Width, 20), ## the main platform
    pygame.Rect(200, 300, 100, 20), ## a random platform - low platform
    pygame.Rect(50, 200, 100, 20), ## a random platform - middle platform
    pygame.Rect(200, 100, 100, 20), ## a random platform = high platform
]

async def main():
    global Width
    global Height
    global FPS

    while True:
        screen.blit(background,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        dt = clock.tick(60)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        player.move(pressed_keys, platforms, dt)
        player.jump(platforms, dt)
        player.update(platforms, dt)

        for platform in platforms: 
            pygame.draw.rect(screen, platform_color, platform)
            
        pygame.draw.rect( screen, (255,0,0), player.rect() )

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())