import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
from Test import PhysTest
from Test import PlayerTest

background = pygame.Surface((640, 400))
background.fill((41, 41, 41))

pygame.display.set_caption("Portal 2D - Test")

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

def font(size):
    return pygame.font.SysFont("Consolas", size)

color = (255, 255, 255)
hover_color = (0, 255 ,255)

buttons: Dict[str, MenuButton] = {
    "phys_test_button":  MenuButton(50, 120, "Physics Test", font(30), color, hover_color),
    "player_test_button":  MenuButton(50, 170, "Player Test", font(30), color, hover_color),
    ### add a key name of button and a value of MenuButton for your code to test with
    ### make sure your MenuButton is 50 extra y value from previous button
    ### will also need to add an if statement on almost bottom for your button
}

async def test_screen():
    global FPS

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = font(40).render("Portal 2D - Test code", True, (255, 255, 255))
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
                    pygame.display.set_mode((Width,Height))
                if buttons["player_test_button"].check_click(mouse_pos):
                    await PlayerTest.PlayerTest()
                    pygame.display.set_mode((Width,Height))

        pygame.display.update()

        await asyncio.sleep(0)