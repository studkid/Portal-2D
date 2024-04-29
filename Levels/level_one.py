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

background = pygame.Surface((GlobalVariables.Width, GlobalVariables.Height))
background.fill((255, 255, 255))

pygame.display.set_caption("Portal 2D - Level one")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((GlobalVariables.Width, GlobalVariables.Height))

async def Level(): ### TODO - MAKE A LEVEL ONE DESIGN
    platforms = [
        Platform(0, GlobalVariables.Height - 20, GlobalVariables.Width, 20, False, 0),
        Platform(600, GlobalVariables.Height - 200, 20, 180, False, 1),
        Platform(0, GlobalVariables.Height - 200, 20, 180, True, 0),
        Platform(GlobalVariables.Width - 20, 0, 20, 250, True, 0),
    ]

    selectedObj = None

    dropper = CubeDropper(150, 0, 180, 3)
    dropper.add(CubeObj(0, 0, 0.0999, 0.2))
    dropper.spawnCube()
    
    pButton = PlayerButton(300, GlobalVariables.Height - 75, 30)

    button = ButtonObject(680, GlobalVariables.Height - 35, 0)

    players = [ Player(50, 520, True), Player(50, 520, False) ]

    door = ExitDoor(1100, GlobalVariables.Height - 150)

    pygame.display.update()


    running = True
    while running:
        screen.blit(background, (0,0))

        dt = clock.tick(GlobalVariables.FPS)
        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))
        
        ## Level one design

        door.door_status(button)
        door.update(screen)
        if not players[0].completed and door.try_exit(players[0], pressed_keys):
            players[0].completed = True
            Timer.stop_timer()
            GlobalVariables.complete_level(1, Timer.elapsed_time // 1000)
            if players[0].completed and players[1].completed:
                running = False
                Timer.start_time = 0
                Timer.elapsed_time = 0
                return
            
        if not Timer.timer_started:
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

        button.checkActive(dropper.sprites(), players)
        button.draw(screen)

        pButton.draw(screen)

        if not players[0].completed:
            players[0].move(pressed_keys, platforms, dt)
            players[0].jump(dt)
            players[0].update(platforms, dt)

        players[0].draw(screen)
        
        if players[0].interactButton(pressed_keys, pButton):
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
                    Timer.timer_started = False
                    running = False

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                players[0].pickupCube(event.button, dropper.sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        pygame.display.update()

        await asyncio.sleep(0)