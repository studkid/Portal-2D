import sys
import pygame
import os
import math
from Utils import GlobalVariables

class Player():

    def __init__(self, x, y, first_player = True):
        self.x = x
        self.y = y
        self.background_x = GlobalVariables.Width
        self.background_y = GlobalVariables.Height
        self.size_x = GlobalVariables.Player_size_X
        self.size_y = GlobalVariables.Player_size_Y
        self.isJump = False
        self.isJumping = False
        self.canJump = True
        self.hitPlatform = False
        self.jump_count = 14 ## a variable that holds numbers of count jump
        self.count = 14 ## count for jumping ( will be used as countdown in jumping )
        self.runningCount = 0
        self.gravity = 0.5
        self.velocity = 0
        self.running = False
        self.runningAnim = False
        self.allowAnim = False
        self.rightStandingImage = GlobalVariables.FirstPlayer_RightStandingImage
        self.leftStandingImage = GlobalVariables.FirstPlayer_LeftStandingImage
        self.rightRunningImage = GlobalVariables.FirstPlayer_RightRunningImage
        self.leftRunningImage = GlobalVariables.FirstPlayer_LeftRunningImage
        if not first_player:
            self.rightStandingImage = GlobalVariables.SecondPlayer_RightStandingImage
            self.leftStandingImage = GlobalVariables.SecondPlayer_LeftStandingImage
            self.rightRunningImage = GlobalVariables.SecondPlayer_RightRunningImage
            self.leftRunningImage = GlobalVariables.SecondPlayer_LeftRunningImage
        self.leftSide = False
        self.image = self.rightStandingImage
        self.cube = None
        self.completed = False

    def draw(self, screen):
        if self.cube:
            self.cube.rect.center = self.rect().center
        return screen.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self, platforms, dt): ## platforms is an array for all Rect objects in the level that player can get on
        self.set_gravity(platforms, dt)
        if self.isJump:
            self.check_collision(platforms, 0, 1)
        else:
            self.check_collision(platforms, 0, -1)

    def move(self, pressed_keys, platforms, dt):
        if pressed_keys[pygame.K_d]:
            if self.x + self.size_x <= self.background_x:
                self.x += 0.5 * dt
                self.check_collision(platforms, 1, 0)
                self.running = True
                self.leftSide = False
                if self.allowAnim:
                    self.runningAnim = True
                else:
                    self.runningAnim = False
                self.runningCount += 1
        if pressed_keys[pygame.K_a]:
            if self.x >= 0:
                self.x -= 0.5 * dt
                self.running = True
                self.leftSide = True
                if self.allowAnim:
                    self.runningAnim = True
                else:
                    self.runningAnim = False
                self.check_collision(platforms, -1, 0)
                self.runningCount += 1
        if pressed_keys[pygame.K_SPACE] and self.canJump:
            self.isJump = True
            self.isJumping = True
            self.canJump = False
            self.count = self.jump_count
            self.velocity = 10 * dt * 0.05
            self.check_collision(platforms, 0, 1)
        if self.runningCount >= 5 and self.running and self.runningAnim:
            if self.leftSide:
                self.image = self.leftRunningImage
            else:
                self.image = self.rightRunningImage
            self.runningCount = 0
            self.allowAnim = False
        elif self.runningCount >= 5 and self.running and not self.runningAnim:
            if self.leftSide:
                self.image = self.leftStandingImage
            else:
                self.image = self.rightStandingImage
            self.runningCount = 0
            self.allowAnim = True
        if not pressed_keys[pygame.K_a] and not pressed_keys[pygame.K_d]:
            if self.leftSide:
                self.image = self.leftStandingImage
            else:
                self.image = self.rightStandingImage
            self.running = False
            self.allowAnim = False
            self.runningAnim = False
            self.runningCount = 0


    def jump(self, dt):
        if self.count >= -self.jump_count:
            if self.count >= 0 and self.isJump:
                add_y = 1
                self.actually_jump(add_y)
            if self.count < 0:
                self.isJump = False
                add_y = -1
                self.actually_jump(add_y)
        else:
            self.isJumping = False
            self.isJump = False
            self.count = self.jump_count
    
    def actually_jump(self, add_y):
        if self.y - self.count**2 * 0.1 * add_y > 0:
            self.y -= self.count**2 * 0.1 * add_y
        else:
            self.count = 0
        self.count -= 1

    def set_gravity(self, platforms, dt):
        if not self.isJump and not self.isJumping:
            self.velocity += self.gravity
            count = 0
            for platform in platforms:
                if not self.rect().colliderect(platform):
                    if self.hitPlatform == True:
                        self.y += self.velocity * 0.02 * dt
                    else:
                        if count <= 3:
                            self.y += self.velocity * 0.05 * dt
                            count+= 1
                else:
                    break
        elif not self.isJump and self.isJumping:
            self.velocity += self.gravity
            on_platform = False
            for platform in platforms:
                if self.rect().colliderect(platform):
                    on_platform = True
                    break
            if not on_platform:
                self.y += self.velocity * 0.05 * dt
        if self.y > self.background_y - 20:
            self.y = self.background_y - 20 - self.size_y

    
    def check_collision(self, platforms, x, y):
        rect = self.rect()
        for platformObj in platforms:
            platform = platformObj.rect
            if rect.colliderect(platform) and platformObj.active and (not platformObj.collision == 2 or self.cube != None):
                if x > 0: 
                    self.x = platform.left - self.size_x
                    break
                elif x < 0:
                    self.x = platform.right
                    break
                elif y < 0:
                    self.y = platform.top - self.size_y
                    self.velocity = 0
                    self.isJump = False
                    self.canJump = True
                    self.hitPlatform = False
                    break
                elif y > 0:
                    self.y = platform.bottom
                    break
            if rect.left >= platform.left - self.size_x and rect.right <= platform.right + self.size_x and y > 0:
                if rect.top - platform.bottom + 2 > platform.top and rect.top < platform.bottom + 1:
                    self.y = platform.bottom
                    self.count = 0
                    self.isJump = False
                    self.isJumping = False
                    self.canJump = False
                    self.hitPlatform = True
                    break

    def interactButton(self, pressed_keys, button) -> bool:
        if pressed_keys[pygame.K_e] and self.rect().colliderect(button.rect):
            return button.activate()
        return False
    
    def pickupCube(self, mouse, cube):
        if not self.cube and mouse == 3 and self.rect().colliderect(cube.rect):
            cube.runPhysics = False
            self.cube = cube
        elif self.cube and mouse == 3:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = self.rect().centerx - mouseX
            dy = self.rect().centery - mouseY

            self.cube.runPhysics = True
            self.cube.speed = 2
            self.cube.angle = math.atan2(-dy,-dx) + math.pi/2
            self.cube = None

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect(), 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect().center, 5)