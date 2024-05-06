import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
from Utils.InputTextBox import InputBox
from Utils import GlobalVariables
import host

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Connect")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

buttons: Dict[str, MenuButton] = {
    "host_button":  MenuButton(GlobalVariables.Width / 2 - 38, GlobalVariables.Height / 2 - 75, "HOST", GlobalVariables.font(40), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "connect_button":  MenuButton(GlobalVariables.Width / 2 - 73, GlobalVariables.Height / 2 , "CONNECT", GlobalVariables.font(40), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
}

async def connect(user_input):
    ### TODO - implement this method so connects with room code from user_input
    return

async def connect_screen():
    default_txt = "enter room code"

    textbox = InputBox(GlobalVariables.Width / 2 - 150, GlobalVariables.Height / 2 + 50, 300, 50, default_txt)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = GlobalVariables.font(50).render("Connection", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        esc_text = GlobalVariables.font(24).render("back - ESC", True, GlobalVariables.Text_Forecolor)
        screen.blit(esc_text, (GlobalVariables.Width - 190, 50))

        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

        textbox.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["host_button"].check_click(mouse_pos):
                    await host.host_screen()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["connect_button"].check_click(mouse_pos):

                    ### TODO - add a statement that calls connect()

                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            textbox.handle_event(event)

        textbox.update()

        pygame.display.update()

        await asyncio.sleep(0)