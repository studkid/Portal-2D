import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import host
from Utils import GlobalVariables

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
    user_input = "enter room code"
    textbox = pygame.Rect(GlobalVariables.Width / 2 - 150, GlobalVariables.Height / 2 + 50, 300, 50)
    textbox_active = False
    textbox_border_color = GlobalVariables.Text_Hovercolor

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = GlobalVariables.font(50).render("Connection", True, (255, 255, 255))
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

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
                if textbox.collidepoint(event.pos):
                    textbox_active = True
                else:
                    textbox_active = False
            if event.type == pygame.KEYDOWN:
                if textbox_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        if len(user_input) < 10:
                            user_input += event.unicode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if textbox_active:
            textbox_border_color = (0, 255, 255)
            
            if user_input == "enter room code":
                user_input = ""
        else:
            textbox_border_color = (255, 255, 255)
            if len(user_input) == 0:
                user_input = "enter room code"

        pygame.draw.rect(screen, textbox_border_color, textbox, 2)
        text = GlobalVariables.font(25).render(user_input, True, (255, 255, 255))
        text_x = textbox.x + (textbox.width - text.get_width()) / 2
        text_y = textbox.y + (textbox.height - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))

        pygame.display.update()

        await asyncio.sleep(0)