import pygame
import asyncio
from typing import Dict
from Utils.MenuButton import MenuButton
from Test import PhysTest
from Test import PlayerTest
from Test import DoorTest
from Test import Portal_test
from Utils import GlobalVariables
from Levels import PlayLevel

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
    "portal_test_button":  MenuButton(50, 270, "Portal Test", GlobalVariables.font(30), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "level_one_button":  MenuButton(50, 320, "    - Level One", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "level_two_button":  MenuButton(50, 370, "    - Level Two", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "level_three_button":  MenuButton(50, 420, "    - Level Three", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "level_four_button":  MenuButton(50, 470, "    - Level Four", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    "level_five_button":  MenuButton(50, 520, "    - Level Five", GlobalVariables.font(28), GlobalVariables.Text_Forecolor, GlobalVariables.Text_Hovercolor),
    ### add a key name of button and a value of MenuButton for your code to test with
    ### make sure your MenuButton is 50 extra y value from previous button
    ### will also need to add an if statement on almost bottom for your button
}

async def test_screen():
    running = True

    global levelStarted
    levelStarted = False

    def send_data(): 
        """
        Send position to server
        :return: None
        """
        global levelStarted
        name = GlobalVariables.Account_Username if (GlobalVariables.Account_Username != "") else "User"
        roomId = "0"
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
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0,0))
        
        title_text = GlobalVariables.font(50).render("Select a Level", True, GlobalVariables.Text_Forecolor)
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
                if buttons["portal_test_button"].check_click(mouse_pos):
                    await Portal_test.PortalTest()
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["level_one_button"].check_click(mouse_pos):
                    await PlayLevel.play_level(1)
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["level_two_button"].check_click(mouse_pos):
                    await PlayLevel.play_level(2)
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["level_three_button"].check_click(mouse_pos):
                    await PlayLevel.play_level(3)
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["level_four_button"].check_click(mouse_pos):
                    await PlayLevel.play_level(4)
                    pygame.display.set_mode((GlobalVariables.Width,GlobalVariables.Height))
                if buttons["level_five_button"].check_click(mouse_pos):
                    await PlayLevel.play_level(5)

        pygame.display.update()

        await asyncio.sleep(0)