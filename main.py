import pygame
import asyncio
from Utils.MenuButton import MenuButton
import test_code
import connection
import levels

Width, Height = 640, 400

background = pygame.Surface((Width, Height))
background.fill((41, 41, 41))

pygame.display.set_caption("Portal 2D")

FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

def font(size):
    return pygame.font.SysFont("Consolas", size)

color = (255, 255, 255)
hover_color = (0, 255 ,255)

async def main():
    global FPS

    while True:
        screen.blit(background, (0,0))

        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()

        title_text = font(50).render("Portal 2D", True, (255, 255, 255))
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        connection_button = MenuButton(50, 120, "Connect", font(30), color, hover_color)
        level_button = MenuButton(50, 170, "Levels", font(30), color, hover_color)
        test_room_button = MenuButton(50, 220, "Test your code", font(30), color, hover_color)

        screen.blit(title_text, title_rect)

        for button in [connection_button, level_button, test_room_button]:
            button.check_hover(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if connection_button.check_click(mouse_pos):
                    await connection.connect_screen()
                if level_button.check_click(mouse_pos):
                    await levels.level_screen()
                if test_room_button.check_click(mouse_pos):
                    await test_code.test_screen()

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())