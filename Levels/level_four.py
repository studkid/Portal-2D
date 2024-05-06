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
from Laser import Laser
from Utils.Portal_gun import Portal

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Level four")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def Level(): ### TODO - MAKE A LEVEL FOUR DESIGN
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, False, 0),
        Platform(400, 0, 20, 200, False, 1),
        Platform(400, 200, 100, 20, False, 1),
        Platform(700, 0, 20, 250, True, 0),
        Platform(600, 250, 120, 20, False, 1),
        Platform(0, GlobalVariables.Height - 200, 20, 180, True, 0),
        Platform(900, 400, 200, 20, False, 2),
    ]

    laser = Laser.Laser((0, 300), 0, platforms, screen)

    selectedObj = None

    dropper = CubeDropper(0, 0, 225, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCubeAway()

    count = 0
    
    pButton = PlayerButton(450, 220 - 75, 30)

    button = ButtonObject(980, 385, 0)

    players = [
        Player(50, 520, True, str(GlobalVariables.net.id) == str(0)), 
        Player(50, 520, False, False)
    ]
    players[0].name = GlobalVariables.Account_Username

    door = ExitDoor(1100, GlobalVariables.Height - 150)

    global hasStarted
    hasStarted = False
    levelComplete = False
    global completionTimer
    completionTimer = 160
    finalTime = 0
    global frameTimer
    frameTimer = 0

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
            roomId = "4"
        else:
            roomId = "104"
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
        global frameTimer
        
        print("PLAYER 2 IS IN ROOM " + str(p2room))
        if type(frameTimer) is int:
            if (str(p2room) == "-1" or str(p2room) == "100" or str(p2room) == "0") and frameTimer > 60:
                frameTimer = 0
                print("attempting to exit")
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

    laser_text = GlobalVariables.font(14).render("If you get hit by a laser, you'll get sent back to the start.", True, GlobalVariables.Text_NameColor)
    
    running = True
    while running:
        frameTimer += 1

        screen.blit(background, (0,0))

        dt = clock.tick(GlobalVariables.FPS)
        portals = [players[0].pGun.sprite, players[1].pGun.sprite]
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))

        screen.blit(laser_text, (770, 310))
        
        ## Level four design

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
        #    mouseX, mouseY = pygame.mouse.get_pos()
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

        laser.draw()

        button.checkActive(dropper.sprites(), players)
        button.draw(screen)

        pButton.draw(screen)

        if players[0].rect().colliderect(laser.bounding_rect):
            players[0].x = 150
            players[0].y = 520

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
            dropper.sprite.runPhysics = False
        elif(cubeState == "1"):
            players[0].cubeState = "1"
            players[0].controllingCube = True

        if players[0].controllingCube == False and Timer.elapsed_time > 5:
            dropper.sprite.runPhysics = False

        print("player cube state: " + players[0].cubeState)
        print("running physics?" + str(dropper.sprite.runPhysics))
        
        for player in players:
            player.update(platforms, dt)
            player.draw(screen)
            #player.drawHitbox(screen)
        
        if players[0].interactButton(pressed_keys, pButton):
            if count == 0:
                dropper.add(CubeObj(0, 0, 0.0999, 0.2))
                count += 1
            dropper.spawnCube()
            players[0].cubeState = "11"
            players[0].controllingCube = True
            dropper.sprite.runPhysics = True

        
        for wall in platforms:
            wall.draw(screen)

        if levelComplete and completionTimer > 0:
            completionTimer -= 1
            completionText = GlobalVariables.font(50).render("Level completed in " + str(finalTime // 1000) + " seconds!", True, (0, 0, 0))
            screen.blit(completionText, (GlobalVariables.Width/2 - completionText.get_width()/2, GlobalVariables.Height/2))

        if completionTimer == 0:
            if levelComplete:
                GlobalVariables.complete_level(4, finalTime // 1000)
            frameTimer = 0
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
                if count > -1:
                    players[0].mouseInput(event.button, dropper.sprite)
                else:
                    players[0].mouseInput(event.button)
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