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
        user_times = DatabaseUtil.get_level_times(GlobalVariables.Account_Username)

        user_has_completion = user_times is not None

        
        block_width = 300 
        block_height = 100 
        padding = 30 
        start_x = 100 
        start_y = 150
        x = start_x
        y = start_y

        for i in range (len(levels)):

            levelInfo = GlobalVariables.font(24).render("Level " + str(levels[i][0]) + " | " + str(levels[i][1]), True, GlobalVariables.Text_Forecolor)
            levelInfo_Rect = pygame.Rect(x, y, levelInfo.get_width(), levelInfo.get_height())

            y += padding

            levelTarget = GlobalVariables.font(24).render("Target time : " + str(levels[i][2]) + " Minutes | ", True, GlobalVariables.Text_Forecolor)
            levelTarget_Rect = pygame.Rect(x, y, levelTarget.get_width(), levelTarget.get_height())
            
            x += 320 + padding

            if user_has_completion:
                try:
                    if user_times[i][2] is not None:
                        userTimeCompleted = GlobalVariables.font(24).render("Completed in : " + str(user_times[i][2]) + " Minutes", True, GlobalVariables.Text_Forecolor)
                    else:
                        userTimeCompleted = GlobalVariables.font(24).render("Not completed", True, GlobalVariables.Text_Forecolor)
                except IndexError:
                    userTimeCompleted = GlobalVariables.font(24).render("Not completed", True, GlobalVariables.Text_Forecolor)
            else:
                userTimeCompleted = GlobalVariables.font(24).render("Not completed", True, GlobalVariables.Text_Forecolor)
            
            userTimeCompleted_Rect = pygame.Rect(x, y, userTimeCompleted.get_width(), userTimeCompleted.get_height())

            screen.blit(levelInfo, levelInfo_Rect)
            screen.blit(levelTarget, levelTarget_Rect)
            screen.blit(userTimeCompleted, userTimeCompleted_Rect)

            y += 80
            x -= (320 + padding)

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