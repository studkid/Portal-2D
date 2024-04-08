import pygame
import asyncio
import math

import sys
import os

from Utils.Player import Player
from Utils.PhysObj import CubeObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform
from Utils.CubeDropper import CubeDropper
from Utils.ExitDoor import ExitDoor
from Utils import GlobalVariables

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Door Test")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def DoorTest():
    platform_color = (41,41,41)
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, True, None),
        Platform(200, 300, 100, 20, True, None),
        Platform(700, 500, 20, 200, False, None),
    ]

    player = Player(50, 270, True)
    selectedObj = None

    objGroup = pygame.sprite.Group()

    dropper = CubeDropper(1160, -15, 135)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()

    ###################### DOOR ######################
    door = ExitDoor(150, GlobalVariables.Height - 130)
    ###################### DOOR ######################

    button = ButtonObject(230, 285, 0)
    pygame.display.update()


    running = True
    while running:
        screen.blit(background, (0,0))

        ### your test code here

        dt = clock.tick(GlobalVariables.FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        
        ###################### DOOR ######################
        door.door_status(button)
        door.update(screen)
        door.try_exit(player, pressed_keys)
        ###################### DOOR ######################

        for platform in platforms: 
            pygame.draw.rect(screen, platform_color, platform)
            
        ## pygame.draw.rect( screen, (255,0,0,0), player.rect() )

        if selectedObj:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selectedObj.rect.x
            dy = mouseY - selectedObj.rect.y
            selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
            selectedObj.speed = math.hypot(dx, dy) * 0.1
            selectedObj.rect.x = mouseX
            selectedObj.rect.y = mouseY


        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj:
                obj.move(dt)
            obj.bounce(1280, 720, platforms)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)

        button.checkActive(dropper.sprites())
        button.draw(screen)

        player.move(pressed_keys, platforms, dt)
        player.jump(dt)
        player.update(platforms, dt)
        player.draw(screen)
        
        for wall in platforms:
            wall.draw(screen)
        pygame.display.flip()

        ### end of test code

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
                if event.button == 1:
                    selectedObj = findObject(dropper.sprites(), mouseX, mouseY)
                elif event.button == 3:
                    dropper.spawnCube()
                    print(dropper.rect.center)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        pygame.display.update()

        await asyncio.sleep(0)

def findObject(objects, x, y):
    for obj in objects:
        if math.hypot(obj.rect.x-x, obj.rect.y-y) <= obj.size:
            return obj
    return None