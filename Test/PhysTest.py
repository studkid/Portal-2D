import asyncio
import pygame
import random
import math

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Utils import GlobalVariables
from Utils.PhysObj import CubeObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform
from Utils.CubeDropper import CubeDropper
from Utils.Player import Player
from Utils.PlayerButton import PlayerButton
from Utils.Portal_gun import Portal

backgroundColor = (255, 255, 255)
plaformColor = (41, 41, 41)
(width, height) = (1280, 720)
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

# dropper = pygame.sprite.Group()
wallList = [
    Platform(0, height - 20, width, 20, True, 0),
    Platform(200, 300, 100, 20, True, 0),
    Platform(700, 500, 20, 200, False, 2),
    Platform(150, 400, 100, 20, True, 1),
    Platform(100, 500, 100, 20, True, 1),
    Platform(150, 600, 100, 20, True, 1),
]

async def PhysTest():
    pygame.init()
    
    screen.fill(backgroundColor)
    selectedObj = None
    clock = pygame.time.Clock()

    dropper = CubeDropper(1130, 0, 135, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()

    players = [
        Player(50, 270, True, str(GlobalVariables.net.id) == str(0)), # change this to be 'if the other player is not controlling cube, then true'
        Player(100, 270, False, False)
    ]
    players[0].name = GlobalVariables.Account_Username
    pButton = PlayerButton(200, height - 50, 30)
    players[1].pGun.add(Portal(1000, 650, 180, 1))

    button = ButtonObject(230, 285, 0)
    pygame.display.update()

    def send_data(): 
        """
        Send position to server
        :return: None
        """
        print(dropper.sprite.rect.x)
        data = str(GlobalVariables.net.id) + ":" + str(players[0].x) + "," + str(players[0].y) + ":" + str("True" if players[0].leftSide == True else "False") + ":" + str(GlobalVariables.Account_Username) + ":" + str(dropper.sprite.rect.x) + "," + str(dropper.sprite.rect.y)
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
        print(left)
        #print(data.split(":"))
        return int(float(pos[0])), int(float(pos[1])), left, name, int(float(cube[0])), int(float(cube[1])) #TODO: get cube pos, only use it if the current player isnt controlling cube
        #except:
        #    return 0,0

    running = True
    while running:
        dt = clock.tick(60)
        portals = [players[0].pGun.sprite, players[1].pGun.sprite]

        for event in pygame.event.get():
            # Exit handler
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                players[0].mouseInput(event.button, dropper.sprite)
                if event.button == 1:
                    selectedObj = findObject(dropper.sprites(), mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        #teleport
        if all(isinstance(x, Portal) for x in portals):
            for player in players:
                player.portalWarp(portals) # MAY HAVE TO CHANGE THIS TO JUST PLAYER 1
            for i, obj in enumerate(dropper.sprites()):
                obj.portalWarp(portals)

        # Move Object
        #if selectedObj:
        #    mouseX, mouseY = pygame.mouse.get_pos()
        #    dx = mouseX - selectedObj.rect.centerx
        #    dy = mouseY - selectedObj.rect.centery
        #    selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
        #    selectedObj.speed = math.hypot(dx, dy) * 0.1
        #    selectedObj.rect.center = (mouseX, mouseY)

        if button.Active:
            wallList[2].active = False
        else:
            wallList[2].active = True

        screen.fill(backgroundColor)

        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj and obj.runPhysics and players[0].controllingCube:
                obj.move(dt)
            obj.bounce(1280, 720, wallList)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)
        dropper.drawHitbox(screen)

        button.checkActive(dropper.sprites(), players)
        button.draw(screen)
        
        pressed_keys = pygame.key.get_pressed()
        players[0].move(pressed_keys, wallList, dt)
        players[0].jump(dt)

        if(players[0].controllingCube == False):
            print("using server cube pos")
            players[1].x, players[1].y, dummy0, players[1].name, dropper.sprite.rect.x, dropper.sprite.rect.y = parse_data(send_data()) ##        
        else:
            players[1].x, players[1].y, dummy0, players[1].name, dummy1, dummy2 = parse_data(send_data()) ## 
        
        for player in players:
            player.update(wallList, dt)
            player.draw(screen)
            player.drawHitbox(screen)

        if players[0].interactButton(pressed_keys, pButton):
            dropper.spawnCube()


        pButton.draw(screen)
        # pButton.drawHitbox(screen)

        for wall in wallList:
            wall.draw(screen)
        pygame.display.flip()
        
        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.rect.x-x, obj.rect.y-y) <= obj.size:
            return obj
    return None