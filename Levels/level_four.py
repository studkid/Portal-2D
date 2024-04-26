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

pygame.display.set_caption("Portal 2D - Level four")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def Level(): ### TODO - MAKE A LEVEL FOUR DESIGN
    platform_color = (41,41,41)
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, False, None),
        Platform(400, 0, 20, 200, False, None),
        Platform(400, 200, 100, 20, False, None),
        Platform(700, 0, 20, 250, True, None),
        Platform(600, 250, 120, 20, False, None),
        Platform(0, GlobalVariables.Height - 200, 20, 180, True, None),
        Platform(900, 400, 200, 20, False, None),
    ]

    selectedObj = None

    dropper = CubeDropper(0, 0, 225, 3)

    count = 0
    
    pButton = PlayerButton(450, 220 - 75, 30)

    button = ButtonObject(980, 385, 0)

    player = Player(50, 520, True)
    playerTwo = Player(50, 520, False)

    door = ExitDoor(1100, GlobalVariables.Height - 150)

    pygame.display.update()


    running = True
    while running:
        screen.blit(background, (0,0))

        dt = clock.tick(GlobalVariables.FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        
        ## Level four design

        door.door_status(button)
        door.update(screen)
        if not player.completed and door.try_exit(player, pressed_keys):
            player.completed = True
            GlobalVariables.complete_level(1, 10) ## TODO - the 10 is time, edit this when the timer is set up
            if player.completed and playerTwo.completed:
                running = False
                return

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

        if not player.completed:
            player.move(pressed_keys, platforms, dt)
            player.jump(dt)
            player.update(platforms, dt)

        player.draw(screen)
        
        if player.interactButton(pressed_keys, pButton):
            if count == 0:
                dropper.add(CubeObj(0, 0, 0.0999, 0.2))
                count += 1
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
                if count > 0:
                    player.pickupCube(event.button, dropper.sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        pygame.display.update()

        await asyncio.sleep(0)