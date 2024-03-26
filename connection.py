import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import host

Width, Height = 1280, 720

background = pygame.Surface((Width, Height))
background.fill((41, 41, 41))

pygame.display.set_caption("Portal 2D - Connect")

FPS = 60

def font(size):
    return pygame.font.SysFont("Consolas", size)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

color = (255, 255, 255)
hover_color = (0, 255 ,255)

buttons: Dict[str, MenuButton] = {
    "host_button":  MenuButton(Width / 2 - 38, Height / 2 - 75, "HOST", font(40), color, hover_color),
    "connect_button":  MenuButton(Width / 2 - 73, Height / 2 , "CONNECT", font(40), color, hover_color),
}

async def connect(user_input):
    ### TODO - implement this method so connects with room code from user_input
    return

async def connect_screen():
    global FPS

    user_input = "enter room code"
    textbox = pygame.Rect(Width / 2 - 150, Height / 2 + 50, 300, 50)
    textbox_active = False
    textbox_border_color = (255,255,255)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = font(50).render("Connection", True, (255, 255, 255))
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
                    pygame.display.set_mode((Width,Height))
                if buttons["connect_button"].check_click(mouse_pos):

                    ### TODO - add a statement that calls connect()

                    pygame.display.set_mode((Width,Height))
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
        text = font(25).render(user_input, True, (255, 255, 255))
        text_x = textbox.x + (textbox.width - text.get_width()) / 2
        text_y = textbox.y + (textbox.height - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))

        pygame.display.update()

        await asyncio.sleep(0)