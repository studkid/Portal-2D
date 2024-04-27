import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
from Test import PhysTest
from Test import PlayerTest
from Test import DoorTest
from Utils import GlobalVariables
from Test import Portal_test

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Test")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

buttons: Dict[str, MenuButton] = {
    "phys_test_button":  MenuButton(50, 120, "Physics Test", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "player_test_button":  MenuButton(50, 170, "Player Test", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "door_test_button":  MenuButton(50, 220, "Door Test", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    ### add a key name of button and a value of MenuButton for your code to test with
    ### make sure your MenuButton is 50 extra y value from previous button
    ### will also need to add an if statement on almost bottom for your button
}

async def test_screen():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = GlobalVariables.font(50).render("Test code", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["phys_test_button"].check_click(mouse_pos):
                    await PhysTest.PhysTest()
                if buttons["player_test_button"].check_click(mouse_pos):
                    await PlayerTest.PlayerTest()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["door_test_button"].check_click(mouse_pos):
                    await DoorTest.DoorTest()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))

        pygame.display.update()

        await asyncio.sleep(0)