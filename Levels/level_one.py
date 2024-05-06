import pygame
import asyncio
import math

from Utils import Timer

from Utils.Player import Player
from Utils.PhysObj import CubeObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform
from Utils.CubeDropper import CubeDropper
from Utils.ExitDoor import ExitDoor
from Utils.PlayerButton import PlayerButton
from Utils import GlobalVariables
from Utils.Portal_gun import Portal

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Level one")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def Level(): ### TODO - MAKE A LEVEL ONE DESIGN
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, False, 0),
        Platform(710, GlobalVariables.Height - 200, 20, 180, False, 1),
        Platform(0, GlobalVariables.Height - 200, 20, 180, True, 0),
        Platform(GlobalVariables.Width - 20, 0, 20, 250, True, 0),
    ]

    selectedObj = None

    dropper = CubeDropper(150, 0, 180, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()
    
    pButton = PlayerButton(300, GlobalVariables.Height - 75, 30)

    button = ButtonObject(790, GlobalVariables.Height - 35, 0)

    players = [
        Player(50, 520, True, str(GlobalVariables.net.id) == str(0)), 
        Player(50, 520, False, False)
    ]
    players[0].name = GlobalVariables.Account_Username

    door = ExitDoor(1150, GlobalVariables.Height - 150)

    global hasStarted
    hasStarted = False
    levelComplete = False
    global completionTimer
    completionTimer = 160
    finalTime = 0

    pygame.display.update()

    def send_data(): 
        """
        Send position to server
        :return: None
        """
        print(dropper.sprite.rect.x)
        if players[0].cubeState == "11":
            cubeState = "0"
            players[0].controllingCube = False
        elif players[0].cubeState == "10":
            cubeState = "1"
            players[0].controllingCube = True
        else:
            cubeState = "-1"

        if type(players[0].pGun.sprite) is Portal:
            portalPos = players[0].pGun.portalPos
            portalRot = players[0].pGun.portalRot
        else:
            portalPos = ("None", "None")
            portalRot = 0


        global hasStarted
        if hasStarted:
            roomId = "1"
        else:
            roomId = "101"
            hasStarted = True

        data = str(GlobalVariables.net.id) + ":" + str(players[0].x) + "," + str(players[0].y) + ":" + str("True" if players[0].leftSide == True else "False") + ":" + str(GlobalVariables.Account_Username) + ":" + str(dropper.sprite.rect.x) + "," + str(dropper.sprite.rect.y) + ":" + cubeState + ":" + str(players[0].pGun.angle) + ":" + str(portalPos[0]) + "," + str(portalPos[1]) + ":" + str(portalRot) + ":" + str(roomId)
        reply = GlobalVariables.net.send(data)
        return reply

    @staticmethod
    def parse_data(data): 
        #try:
        pos = data.split(":")[1].split(",")
        left = True if data.split(":")[2] == "True" else False
        players[1].image = players[1].leftStandingImage if left else players[1].rightStandingImage
        name = data.split(":")[3]
        cube = data.split(":")[4].split(",")
        cubeState = data.split(":")[5]
        angle = data.split(":")[6]
        portalPos = data.split(":")[7].split(",")
        portalRot = data.split(":")[8]
        p2room = data.split(":")[9]

        global completionTimer
        
        print("PLAYER 2 IS IN ROOM " + str(p2room))
        if len(str(p2room)) > 2:
            if str(p2room) == "100":
                print("AHOOOOOOOOOO)))))))))))))Y")
                completionTimer = 0

        if str(portalPos[0]) == "None":
            players[1].pGun.empty()
        else:
            players[1].pGun.add(Portal(int(float(portalPos[0])), int(float(portalPos[1])), int(float(portalRot)), 1))
        print(left)
        #print(data.split(":"))
        return float(pos[0]), float(pos[1]), left, name, int(float(cube[0])), int(float(cube[1])), cubeState, int(float(angle)), portalPos[0], portalPos[1], int(float(portalRot)), p2room #TODO: get cube pos, only use it if the current player isnt controlling cube
        #except:
        #    return 0,0

    running = True
    while running:
        screen.blit(background, (0,0))

        dt = clock.tick(GlobalVariables.FPS)
        portals = [players[0].pGun.sprite, players[1].pGun.sprite]

        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))

        control1_text = GlobalVariables.font(14).render("Move left/right with A and D.", True, GlobalVariables.Text_NameColor)
        control2_text = GlobalVariables.font(14).render("Jump with SPACE.", True, GlobalVariables.Text_NameColor)
        control3_text = GlobalVariables.font(14).render("Shoot portal with LEFT CLICK.", True, GlobalVariables.Text_NameColor)
        screen.blit(control1_text, (50, 400))
        screen.blit(control2_text, (50, 420))
        screen.blit(control3_text, (50, 440))

        portal1_text = GlobalVariables.font(14).render("Portals can only be created on GRAY walls.", True, GlobalVariables.Text_NameColor)
        portal2_text = GlobalVariables.font(14).render("Players and cubes can teleport using the portals!", True, GlobalVariables.Text_NameColor)
        screen.blit(portal1_text, (860, 100))
        screen.blit(portal2_text, (860, 120))

        cube_text = GlobalVariables.font(14).render("Pick up and throw cubes with RIGHT CLICK.", True, GlobalVariables.Text_NameColor)
        screen.blit(cube_text, (100, 560))

        tiny1_text = GlobalVariables.font(14).render("TINY BUTTONS can be pressed with E when nearby.", True, GlobalVariables.Text_NameColor)
        tiny2_text = GlobalVariables.font(14).render("When pressed, tiny buttons respawn the cube.", True, GlobalVariables.Text_NameColor)
        screen.blit(tiny1_text, (330, 640))
        screen.blit(tiny2_text, (330, 660))

        red_text = GlobalVariables.font(14).render("RED WALLS block players, but allow cubes to pass.", True, GlobalVariables.Text_NameColor)
        screen.blit(red_text, (510, 470))

        big1_text = GlobalVariables.font(14).render("BIG BUTTONS can be pressed by players or cubes.", True, GlobalVariables.Text_NameColor)
        big2_text = GlobalVariables.font(14).render("When pressed, big buttons open the exit door!", True, GlobalVariables.Text_NameColor)
        screen.blit(big1_text, (760, 640))
        screen.blit(big2_text, (760, 660))

        door1_text = GlobalVariables.font(14).render("If BOTH players make it to the open door,", True, GlobalVariables.Text_NameColor)
        door2_text = GlobalVariables.font(14).render("you complete the level!", True, GlobalVariables.Text_NameColor)
        screen.blit(door1_text, (920, 530))
        screen.blit(door2_text, (920, 550))
        
        ## Level one design

        door.door_status(button)
        door.update(screen)


        if not levelComplete and door.try_exit(players[0], pressed_keys) and door.try_exit(players[1], pressed_keys):
            levelComplete = True
            Timer.stop_timer()
            finalTime = Timer.elapsed_time
            Timer.start_time = 0
            Timer.elapsed_time = 0
            
            
        if not Timer.timer_started and not levelComplete:
            Timer.start_timer()

        if Timer.timer_started and Timer.elapsed_time == 0:
            current_time = pygame.time.get_ticks() - Timer.start_time
            timer_text = GlobalVariables.font(36).render("Time: " + str(current_time // 1000) + "s", True, (0, 0, 0))
            screen.blit(timer_text, (GlobalVariables.Width - 200, 20))

        if not Timer.timer_started and Timer.elapsed_time != 0:
            timer_text = GlobalVariables.font(36).render("Time: " + str(Timer.elapsed_time // 1000) + "s", True, (0, 0, 0))
            screen.blit(timer_text, (GlobalVariables.Width - 200, 20))

        for platform in platforms: 
            platform.draw(screen)

        #if selectedObj:
        #     mouseX, mouseY = pygame.mouse.get_pos()
        #    dx = mouseX - selectedObj.rect.centerx
        #    dy = mouseY - selectedObj.rect.centery
        #    selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
        #    selectedObj.speed = math.hypot(dx, dy) * 0.1
        #    selectedObj.rect.center = (mouseX, mouseY)

        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj and obj.runPhysics:
                obj.move(dt)
            obj.bounce(1280, 720, platforms)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)

        button.checkActive(dropper.sprites(), players)
        button.draw(screen)

        pButton.draw(screen)

        if not door.try_exit(players[0], pressed_keys) or not door.try_exit(players[1], pressed_keys): #if either player isnt at the door, let them move
            players[0].move(pressed_keys, platforms, dt)
            players[0].jump(dt)
            

        if(players[0].controllingCube == False):
            print("using server cube pos")
            players[1].x, players[1].y, dummy0, players[1].name, dropper.sprite.rect.x, dropper.sprite.rect.y, cubeState, players[1].pGun.angle, dummy1, dummy2, dummy3, dummy4 = parse_data(send_data()) ##        
        else:
            players[1].x, players[1].y, dummy0, players[1].name, dummy1, dummy2, cubeState, players[1].pGun.angle, dummy3, dummy4, dummy5, dummy6 = parse_data(send_data()) ## 

        if(cubeState == "0"):
            players[0].cubeState = "0"
            players[0].controllingCube = False
        elif(cubeState == "1"):
            players[0].cubeState = "1"
            players[0].controllingCube = True
        
        for player in players:
            player.update(platforms, dt)
            player.draw(screen)
            #player.drawHitbox(screen)

        
        if players[0].interactButton(pressed_keys, pButton):
            dropper.spawnCube()
        
        for wall in platforms:
            wall.draw(screen)

        if levelComplete and completionTimer > 0:
            completionTimer -= 1
            completionText = GlobalVariables.font(50).render("Level completed in " + str(finalTime // 1000) + " seconds!", True, (0, 0, 0))
            screen.blit(completionText, (GlobalVariables.Width/2 - completionText.get_width()/2, GlobalVariables.Height/2))

        if completionTimer == 0:
            if levelComplete:
                GlobalVariables.complete_level(1, finalTime // 1000)
            running = False
            return
        pygame.display.flip()

        ## Event Handler

        for event in pygame.event.get():
            # Exit handler
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Timer.timer_started = False
                    running = False

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                players[0].mouseInput(event.button, dropper.sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        #teleport
        if all(isinstance(x, Portal) for x in portals):
            for player in players:
                player.portalWarp(portals) # MAY HAVE TO CHANGE THIS TO JUST PLAYER 1
            for i, obj in enumerate(dropper.sprites()):
                obj.portalWarp(portals)

        pygame.display.update()

        await asyncio.sleep(0)