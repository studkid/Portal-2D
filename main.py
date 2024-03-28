import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import connection
import levels
import test_code
import account
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
}

async def main():
    
    sign_up_button = MenuButton(GlobalVariables.Width - 150, 50, "Sign up", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)
    log_in_button = MenuButton(GlobalVariables.Width - 150, 90, "Log in", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)
    log_off_button = MenuButton(GlobalVariables.Width - 150, 90, "Log off", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)

    sign_up_button.rect.right = GlobalVariables.Width - 50
    log_in_button.rect.right = GlobalVariables.Width - 50
    log_off_button.rect.right = GlobalVariables.Width - 50

    while True:
        logged = GlobalVariables.Account_Username is not ""

        screen.blit(background, (0,0))

        clock.tick(GlobalVariables.FPS)

        mouse_pos = pygame.mouse.get_pos()

        title_text = GlobalVariables.font(50).render("Portal 2D", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        user_text = GlobalVariables.font(30).render("Welcome, " + GlobalVariables.Account_Username, True, GlobalVariables.Text_Forecolor)
        user_rect = user_text.get_rect(right=GlobalVariables.Width - 50, top=50)

        screen.blit(title_text, title_rect)

        if logged:
            log_off_button.active = True
            sign_up_button.active = False
            log_in_button.active = False

            screen.blit(user_text, user_rect)
            log_off_button.check_hover(mouse_pos)
            log_off_button.update(screen)

        else:
            log_off_button.active = False
            sign_up_button.active = True
            log_in_button.active = True

            sign_up_button.check_hover(mouse_pos)
            sign_up_button.update(screen)
            log_in_button.check_hover(mouse_pos)
            log_in_button.update(screen)

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
                if sign_up_button.check_click(mouse_pos) and sign_up_button.active == True:
                    await account.sign_up()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if log_in_button.check_click(mouse_pos) and log_in_button.active == True:
                    await account.log_in()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if log_off_button.check_click(mouse_pos) and log_off_button.active == True:
                    GlobalVariables.Account_ID = ""
                    GlobalVariables.Account_Username = ""
                    logged = False

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())