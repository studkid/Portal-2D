import pygame
import asyncio
import account
from Utils import GlobalVariables

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Levels")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def level_screen():

    if GlobalVariables.Account_Username == "":
        running = False
        await account.log_in()
    else:
        running = True

    while running:
        screen.blit(background, (0,0))

        title_text = GlobalVariables.font(50).render("Levels", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

        await asyncio.sleep(0)