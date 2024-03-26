import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import test_code
import connection
import levels
from Utils import GlobalVariables

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))


buttons: Dict[str, MenuButton] = {
    "connect_button":  MenuButton(50, 120, "Connection", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "levels_button":  MenuButton(50, 170, "Levels", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "test_button": MenuButton(50, 220, "Test your code", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    ### may need to add login button
}

async def main():
    while True:
        screen.blit(background, (0,0))

        clock.tick(GlobalVariables.FPS)

        mouse_pos = pygame.mouse.get_pos()

        title_text = GlobalVariables.font(50).render("Portal 2D", True, GlobalVariables.Text_Forecolor)
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
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["levels_button"].check_click(mouse_pos):
                    await levels.level_screen()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["test_button"].check_click(mouse_pos):
                    await test_code.test_screen()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())