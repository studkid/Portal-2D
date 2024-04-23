import pygame
import asyncio
import math

from Utils.Player import Player
from Utils.PhysObj import CubeObj
from Utils.ButtonObject import ButtonObject
from Utils.Platform import Platform
from Utils.CubeDropper import CubeDropper
from Utils.ExitDoor import ExitDoor
from Utils.PlayerButton import PlayerButton
from Utils import GlobalVariables

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Door Test")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def Level(): ### TODO - MAKE A LEVEL FIVE DESIGN
    platform_color = (41,41,41)
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, False, None),
        Platform(600, GlobalVariables.Height - 200, 20, 180, False, None),
        Platform(0, GlobalVariables.Height - 200, 20, 180, True, None),
        Platform(1050, GlobalVariables.Height - 530, 20, 180, True, None),
    ]

    selectedObj = None

    dropper = CubeDropper(150, 0, 180, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()
    
    pButton = PlayerButton(300, GlobalVariables.Height - 75, 30)

    button = ButtonObject(680, GlobalVariables.Height - 35, 0)

    player = Player(50, 270, True)

    door = ExitDoor(1100, GlobalVariables.Height - 130)

    pygame.display.update()


    running = True
    while running:
        screen.blit(background, (0,0))

        dt = clock.tick(GlobalVariables.FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        
        ## Level five design

        door.door_status(button)
        door.update(screen)
        if door.try_exit(player, pressed_keys):
            GlobalVariables.complete_level(1, 10) ## TODO - the 10 is time, edit this when the timer is set up

        for platform in platforms: 
            pygame.draw.rect(screen, platform_color, platform)

        if selectedObj:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selectedObj.rect.centerx
            dy = mouseY - selectedObj.rect.centery
            selectedObj.angle = math.atan2(dy, dx) + 0.5 * math.pi
            selectedObj.speed = math.hypot(dx, dy) * 0.1
            selectedObj.rect.center = (mouseX, mouseY)

        for i, obj in enumerate(dropper.sprites()):
            if obj != selectedObj and obj.runPhysics:
                obj.move(dt)
            obj.bounce(1280, 720, platforms)
            obj.collide(dropper.sprites()[i+1:])
        dropper.update()
        dropper.draw(screen)

        button.checkActive(dropper.sprites())
        button.draw(screen)

        pButton.draw(screen)

        player.move(pressed_keys, platforms, dt)
        player.jump(dt)
        player.update(platforms, dt)
        player.draw(screen)
        
        if player.interactButton(pressed_keys, pButton):
            dropper.spawnCube()
        
        for wall in platforms:
            wall.draw(screen)
        pygame.display.flip()

        ## Event Handler

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
                player.pickupCube(event.button, dropper.sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        pygame.display.update()

        await asyncio.sleep(0)