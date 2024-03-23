import pygame
import asyncio
from typing import Dict

from Utils.MenuButton import MenuButton
import Test.PhysTest

background = pygame.Surface((640, 400))
background.fill((0, 0, 255)) ## change bg color if you want to for testing

pygame.display.set_caption("Portal 2D - Test")

Width, Height = 640, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

def font(size):
    return pygame.font.SysFont("Consolas", size)

color = (255, 255, 255)
hover_color = (150, 150 ,150)

buttons: Dict[str, MenuButton] = {
    "phys_test_button":  MenuButton(50, 120, "Physics Test", font(30), color, hover_color),
}

async def test_screen():
    global FPS

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))

        ### your test code here
        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            print(pygame.K_ESCAPE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["phys_test_button"].check_click(mouse_pos):
                    await Test.PhysTest.PhysTest()
                    pygame.display.set_mode((Width,Height))

        pygame.display.update()

        await asyncio.sleep(0)