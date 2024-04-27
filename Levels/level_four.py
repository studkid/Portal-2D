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

    count = 0
    
    pButton = PlayerButton(450, 220 - 75, 30)

    button = ButtonObject(980, 385, 0)

    players = [ Player(50, 520, True), Player(50, 520, False) ]

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
        if not players[0].completed and door.try_exit(players[0], pressed_keys):
            players[0].completed = True
            Timer.stop_timer()
            GlobalVariables.complete_level(4, Timer.elapsed_time // 1000)
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

        laser.draw()

        button.checkActive(dropper.sprites(), players)
        button.draw(screen)

        pButton.draw(screen)

        if players[0].rect().colliderect(laser.bounding_rect):
            players[0].x = 50
            players[0].y = 520

        if not players[0].completed:
            players[0].move(pressed_keys, platforms, dt)
            players[0].jump(dt)
            players[0].update(platforms, dt)

        players[0].draw(screen)
        
        if players[0].interactButton(pressed_keys, pButton):
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
                    players[0].pickupCube(event.button, dropper.sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectedObj = None

        pygame.display.update()

        await asyncio.sleep(0)