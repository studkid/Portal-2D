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

    playerList = [Player(50, 270, True), Player(50, 270, False)]
    pButton = PlayerButton(200, height - 50, 30)
    playerList[1].pGun.add(Portal(1000, 650, 180, 1))

    button = ButtonObject(230, 285, 0)
    pygame.display.update()

    running = True
    while running:
        dt = clock.tick(60)
        portals = [playerList[0].pGun.sprite, playerList[1].pGun.sprite]

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
                playerList[0].mouseInput(event.button, dropper.sprite)
                if event.button == 1:
                    selectedObj = findObject(dropper.sprites(), mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        #teleport
        if all(isinstance(x, Portal) for x in portals):
            for player in playerList:
                player.portalWarp(portals)

        # Move Object
        if selectedObj:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selectedObj.rect.centerx
            dy = mouseY - selectedObj.rect.centery
            selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
            selectedObj.speed = math.hypot(dx, dy) * 0.1
            selectedObj.rect.center = (mouseX, mouseY)

        if button.Active:
            wallList[2].active = False
        else:
            wallList[2].active = True

        screen.fill(backgroundColor)

        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj and obj.runPhysics:
                obj.move(dt)
            obj.bounce(1280, 720, wallList)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)
        dropper.drawHitbox(screen)

        button.checkActive(dropper.sprites(), [playerList[0]])
        button.draw(screen)
        
        pressed_keys = pygame.key.get_pressed()
        playerList[0].move(pressed_keys, wallList, dt)
        playerList[0].jump(dt)
        for player in playerList:
            player.update(wallList, dt)
            player.draw(screen)
            player.drawHitbox(screen)

        if playerList[0].interactButton(pressed_keys, pButton):
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