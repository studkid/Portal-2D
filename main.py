import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
import connection
import levels
import test_code
import account
from Utils import GlobalVariables
from Levels import PlayLevel

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill(GlobalVariables.Background_Color)

pygame.display.set_caption("Portal 2D")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

buttons: Dict[str, MenuButton] = {
    #"connect_button":  MenuButton(50, 120, "Connection", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "stats_button":  MenuButton(50, 120, "Stats", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "play_button": MenuButton(50, 170, "Play", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
}

async def main():
    
    sign_up_button = MenuButton(GlobalVariables.Width - 150, 50, "Sign up", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)
    log_in_button = MenuButton(GlobalVariables.Width - 150, 90, "Log in", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)
    log_off_button = MenuButton(GlobalVariables.Width - 150, 90, "Log off", GlobalVariables.font(24), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor, False)

    sign_up_button.rect.right = GlobalVariables.Width - 50
    log_in_button.rect.right = GlobalVariables.Width - 50
    log_off_button.rect.right = GlobalVariables.Width - 50

    def send_data(): 
        """
        Send position to server
        :return: None
        """
        name = GlobalVariables.Account_Username if (GlobalVariables.Account_Username != "") else "User"
        data = str(GlobalVariables.net.id) + ":" + str(100) + "," + str(270) + ":" + "False" + ":" + str(name) + ":-500,5000" + ":-1" + ":0" + ":None,None" + ":0" + ":-1"
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

    while True:
        logged = GlobalVariables.Account_Username is not ""

        screen.blit(background, (0,0))

        clock.tick(GlobalVariables.FPS)

        mouse_pos = pygame.mouse.get_pos()

        title_text = GlobalVariables.font(50).render("Portal 2D", True, GlobalVariables.Text_Forecolor)
        title_rect = pygame.Rect(50, 50, title_text.get_width(), title_text.get_height())

        user_text = GlobalVariables.font(30).render("Welcome, " + GlobalVariables.Account_Username, True, GlobalVariables.Text_Forecolor)
        user_rect = user_text.get_rect(right=GlobalVariables.Width - 50, top=50)

        screen.blit(title_text, title_rect)

        data = parse_data(send_data())
        name = data[3]
        connected = (name != "User" and GlobalVariables.Account_Username != "")
        connection_text = ("Connected to " + name) if connected else "Searching for a connection..."
        connection_text = GlobalVariables.font(30).render(connection_text, True, GlobalVariables.Text_Forecolor)
        connection_rect = pygame.Rect(50, 550, connection_text.get_width(), connection_text.get_height())
        screen.blit(connection_text, connection_rect)

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

        if logged:
            log_off_button.active = True
            sign_up_button.active = False
            log_in_button.active = False

            screen.blit(user_text, user_rect)
            log_off_button.check_hover(mouse_pos)
            log_off_button.update(screen)

        else:
            log_off_button.active = False
            sign_up_button.active = True
            log_in_button.active = True

            sign_up_button.check_hover(mouse_pos)
            sign_up_button.update(screen)
            log_in_button.check_hover(mouse_pos)
            log_in_button.update(screen)

        if connected:
            for key in buttons:
                buttons[key].active = True
        else:
            for key in buttons:
                buttons[key].active = False
        
        for key in buttons:
            buttons[key].check_hover(mouse_pos)
            buttons[key].update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if buttons["connect_button"].check_click(mouse_pos):
                #    await connection.connect_screen()
                #    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["stats_button"].check_click(mouse_pos):
                    await levels.level_screen()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["play_button"].check_click(mouse_pos):
                    await test_code.test_screen()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if sign_up_button.check_click(mouse_pos) and sign_up_button.active == True:
                    await account.sign_up()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if log_in_button.check_click(mouse_pos) and log_in_button.active == True:
                    await account.log_in()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if log_off_button.check_click(mouse_pos) and log_off_button.active == True:
                    GlobalVariables.Account_ID = ""
                    GlobalVariables.Account_Username = ""
                    logged = False

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())