import pygame
import asyncio
import account
from Utils import GlobalVariables
from PortalDatabase import DatabaseUtil

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Levels")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height)) 

async def level_screen():

    def printLevels():
        levels = DatabaseUtil.get_levels()
        for i in range (len(levels)):
            levelId = GlobalVariables.font(28).render("Level " + str(levels[i][0]), True, GlobalVariables.Text_Forecolor)
            levelId_Rect = pygame.Rect(100, 100, levelId.get_width(), levelId.get_height())
            levelName = GlobalVariables.font(28).render(str(levels[i][1]), True, GlobalVariables.Text_Forecolor)
            levelName_Rect = pygame.Rect(100, 100, levelName.get_width(), levelName.get_height())
            levelTarget = GlobalVariables.font(28).render("Target time : " + str(levels[i][2]), True, GlobalVariables.Text_Forecolor)
            levelTarget_Rect = pygame.Rect(100, 100, levelTarget.get_width(), levelTarget.get_height())

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

        printLevels()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

        await asyncio.sleep(0)