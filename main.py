import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import test_code
import connection
import levels

Width, Height = 1280, 720

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

buttons: Dict[str, MenuButton] = {
    "connect_button":  MenuButton(50, 120, "Connection", font(30), color, hover_color),
    "levels_button":  MenuButton(50, 170, "Levels", font(30), color, hover_color),
    "test_button": MenuButton(50, 220, "Test your code", font(30), color, hover_color),
    ### may need to add login button
}

async def main():
    global FPS

    while True:
        screen.blit(background, (0,0))

        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()

        title_text = font(50).render("Portal 2D", True, (255, 255, 255))
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["connect_button"].check_click(mouse_pos):
                    await connection.connect_screen()
                    pygame.display.set_mode((Width,Height))
                if buttons["levels_button"].check_click(mouse_pos):
                    await levels.level_screen()
                    pygame.display.set_mode((Width,Height))
                if buttons["test_button"].check_click(mouse_pos):
                    await test_code.test_screen()
                    pygame.display.set_mode((Width,Height))

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())