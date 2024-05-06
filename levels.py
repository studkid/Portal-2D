import pygame
import asyncio
import account
import connection
from Utils import GlobalVariables
from PortalDatabase import DatabaseUtil
from Utils.MenuButton import MenuButton
from Levels import PlayLevel

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D - Stats")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height)) 

async def level_screen():

    def printLevels():
        
        levels = DatabaseUtil.get_levels()
        user_times = DatabaseUtil.get_level_times(GlobalVariables.Account_Username)

        user_has_completion = user_times is not None
        completed_levels = [level[1] for level in user_times] if user_has_completion else []

        padding = 30 
        start_x = 100 
        start_y = 150
        x = start_x
        y = start_y

        for i in range (len(levels)):

            levelInfo = GlobalVariables.font(24).render("Level " + str(levels[i][0]) + " | " + str(levels[i][1]), True, GlobalVariables.Text_Forecolor)
            levelInfo_Rect = pygame.Rect(x, y, levelInfo.get_width(), levelInfo.get_height())

            y += padding

            targetMinute = 0
            targetTime = levels[i][2]

            while (targetTime > 60):
                targetTime -= 60
                targetMinute += 1
            if targetTime < 10:
                levelTarget = GlobalVariables.font(24).render("Target time : " + str(targetMinute) + ":0" + str(targetTime) + " | ", True, GlobalVariables.Text_Forecolor)
            else:
                levelTarget = GlobalVariables.font(24).render("Target time : " + str(targetMinute) + ":" + str(targetTime) + " | ", True, GlobalVariables.Text_Forecolor)
            levelTarget_Rect = pygame.Rect(x, y, levelTarget.get_width(), levelTarget.get_height())
            
            x += 240 + padding

            if levels[i][0] in completed_levels:
                try:
                    secondsTime = user_times[completed_levels.index(levels[i][0])][2]
                    minutesTime = 0
                    if secondsTime is not None:
                        while secondsTime > 60:
                            secondsTime -= 60
                            minutesTime += 1
                        if secondsTime < 10:
                            userTimeCompleted = GlobalVariables.font(24).render("Completed in : " + str(minutesTime) + ":0" + str(secondsTime), True, GlobalVariables.Text_Forecolor)
                        else:
                            userTimeCompleted = GlobalVariables.font(24).render("Completed in : " + str(minutesTime) + ":" + str(secondsTime), True, GlobalVariables.Text_Forecolor)
                        if user_times[completed_levels.index(levels[i][0])][2] < levels[i][2]:
                            screen.blit(GlobalVariables.Medal_Image, (x + 255, y - 2))
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
            x -= (240 + padding)


    if GlobalVariables.Account_Username == "":
        running = False
        await account.log_in()
    else:
        running = True

    #connect_button = MenuButton(GlobalVariables.Width - 150, 50, "Connect/Host", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor)
    #connect_button.rect.right = GlobalVariables.Width - 50

    global levelStarted
    levelStarted = False

    def send_data(): 
        """
        Send position to server
        :return: None
        """
        global levelStarted
        name = GlobalVariables.Account_Username if (GlobalVariables.Account_Username != "") else "User"
        roomId = "-1"
        levelStarted = True
        data = str(GlobalVariables.net.id) + ":" + str(100) + "," + str(270) + ":" + "False" + ":" + str(name) + ":1168,170" + ":-1" + ":0" + ":None,None" + ":0" + ":" + str(roomId)
        reply = GlobalVariables.net.send(data)
        return reply

    @staticmethod
    def parse_data(data): 
        #try:
        pos = data.split(":")[1].split(",")
        left = data.split(":")[2]
        name = data.split(":")[3]
        cube = data.split(":")[4].split(",")
        cubeState = data.split(":")[5]
        angle = data.split(":")[6]
        portalPos = data.split(":")[7].split(",")
        portalRot = data.split(":")[8]
        roomId = data.split(":")[9]
        return int(float(pos[0])), int(float(pos[1])), left, name, int(float(cube[0])), int(float(cube[1])), cubeState, int(float(angle)), portalPos[0], portalPos[1], int(float(portalRot)), int(roomId) #TODO: get cube pos, only use it if the current player isnt controlling cube
        #except:
        #    return 0,0

    while running:
        screen.blit(background, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        title_text = GlobalVariables.font(50).render("Level Stats", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        screen.blit(title_text, title_rect)

        esc_text = GlobalVariables.font(24).render("back - ESC", True, GlobalVariables.Text_Forecolor)
        screen.blit(esc_text, (GlobalVariables.Width - 190, 50))

        data = parse_data(send_data())
        p2room = data[11]
        if len(str(p2room)) > 2:
            if str(p2room) == "101":
                await PlayLevel.play_level(1)
                pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if str(p2room) == "102":
                await PlayLevel.play_level(2)
                pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if str(p2room) == "103":
                await PlayLevel.play_level(3)
                pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if str(p2room) == "104":
                await PlayLevel.play_level(4)
                pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if str(p2room) == "105":
                await PlayLevel.play_level(5)
                pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))

        #connect_button.check_hover(mouse_pos)
        #connect_button.update(screen)

        printLevels()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if connect_button.check_click(mouse_pos):
                #    await connection.connect_screen()
                #    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

        await asyncio.sleep(0)