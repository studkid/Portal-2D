import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
from Utils.InputTextBox import InputBox
from Utils import GlobalVariables
from PortalDatabase import DatabaseUtil

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Account")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

user_text = GlobalVariables.font(24).render("Username:", True, GlobalVariables.Text_Forecolor)
user_rect = pygame.Rect(GlobalVariables.Width / 2 - 150, GlobalVariables.Height / 2 - 40, user_text.get_width(), user_text.get_height())

pwd_text = GlobalVariables.font(24).render("Password:", True, GlobalVariables.Text_Forecolor)
pwd_rect = pygame.Rect(GlobalVariables.Width / 2 - 150, GlobalVariables.Height / 2 + 35, pwd_text.get_width(), pwd_text.get_height())

async def sign_up():

    signup_button = MenuButton(GlobalVariables.Width / 2 - 50, GlobalVariables.Height / 2 + 150, "SIGN UP", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor)
    
    inputs: Dict[str, InputBox] = {
        "username":  InputBox(GlobalVariables.Width / 2, GlobalVariables.Height / 2 - 50, 300, 50, ""),
        "password":  InputBox(GlobalVariables.Width / 2, GlobalVariables.Height / 2 + 25, 300, 50, "", True),
    }

    def clear_textboxes(): 
        for key in inputs:
                inputs[key].text = ""
                inputs[key].update()

    error_txt = GlobalVariables.font(24).render("the username is unavailable", True, GlobalVariables.Text_Forecolor)
    error_rect = pygame.Rect(GlobalVariables.Width / 2 - 250, GlobalVariables.Height / 2 - 150, pwd_text.get_width(), pwd_text.get_height())

    error = False

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))

        title_text = GlobalVariables.font(50).render("Sign up", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)
        screen.blit(user_text, user_rect)
        screen.blit(pwd_text, pwd_rect)

        signup_button.check_hover(mouse_pos)
        signup_button.update(screen)

        if error:
            screen.blit(error_txt, error_rect)

        for key in inputs:
            inputs[key].draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if signup_button.check_click(mouse_pos):
                    if(DatabaseUtil.create_user(inputs["username"].text, inputs["password"].pwd_txt)):
                        GlobalVariables.Account_Username = inputs["username"].text
                        clear_textboxes()
                        running = False
                    else:
                        error = True
            for key in inputs:
                inputs[key].handle_event(event)
        
        for key in inputs:
                inputs[key].update()

        pygame.display.update()

        await asyncio.sleep(0)

async def log_in():

    login_button = MenuButton(GlobalVariables.Width / 2 - 50, GlobalVariables.Height / 2 + 150, "LOG IN", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor)
    signup_button = MenuButton(GlobalVariables.Width / 2 - 150, GlobalVariables.Height / 2 + 200, "Don't have an account? Sign up", GlobalVariables.font(18), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor)

    inputs: Dict[str, InputBox] = {
        "username":  InputBox(GlobalVariables.Width / 2, GlobalVariables.Height / 2 - 50, 300, 50, ""),
        "password":  InputBox(GlobalVariables.Width / 2, GlobalVariables.Height / 2 + 25, 300, 50, "", True),
    }
    
    error_txt = GlobalVariables.font(24).render("either username or password was incorrect", True, GlobalVariables.Text_Forecolor)
    error_rect = pygame.Rect(GlobalVariables.Width / 2 - 250, GlobalVariables.Height / 2 - 150, pwd_text.get_width(), pwd_text.get_height())

    error = False
    
    def clear_textboxes(): 
        for key in inputs:
                inputs[key].text = ""
                inputs[key].update()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))

        title_text = GlobalVariables.font(50).render("Log in", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)
        screen.blit(user_text, user_rect)
        screen.blit(pwd_text, pwd_rect)

        login_button.check_hover(mouse_pos)
        login_button.update(screen)
        signup_button.check_hover(mouse_pos)
        signup_button.update(screen)

        if error:
            screen.blit(error_txt, error_rect)

        for key in inputs:
            inputs[key].draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.check_click(mouse_pos):
                    if(DatabaseUtil.authenticate_user(inputs["username"].text, inputs["password"].pwd_txt)):
                        GlobalVariables.Account_Username = inputs["username"].text
                        clear_textboxes()
                        running = False
                    else:
                        error = True
                if signup_button.check_click(mouse_pos):
                     running = False
                     await sign_up()
            for key in inputs:
                inputs[key].handle_event(event)
        
        for key in inputs:
                inputs[key].update()

        pygame.display.update()

        await asyncio.sleep(0)