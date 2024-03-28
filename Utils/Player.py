import pygame
import os

class Player():

    def __init__(self, x, y, background_x, background_y):
        self.x = x
        self.y = y
        self.background_x = background_x
        self.background_y = background_y
        self.size_x = 40 ## change to other number if need ( width size of player )
        self.size_y = 40 ## change to other number if need ( height size of player )
        self.screen = pygame.display.set_mode((background_x, background_y))
        self.isJump = False
        self.isJumping = False
        self.canJump = True
        self.hitPlatform = False
        self.jump_count = 14 ## a variable that holds numbers of count jump
        self.count = 14 ## count for jumping ( will be used as countdown in jumping )
        self.gravity = 0.5
        self.velocity = 0

    
    def rect(self): ## is only used when setting up the display such as pygame.draw.rect( screen, (0,0,255), player.rect() )
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
                self.check_collision(platforms, 1, 1)
        if pressed_keys[pygame.K_a]:
            if self.x >= 0:
                self.x -= 0.5 * dt
                self.check_collision(platforms, -1, 1)
        if pressed_keys[pygame.K_SPACE] and self.canJump:
            self.isJump = True
            self.isJumping = True
            self.canJump = False
            self.count = self.jump_count
            self.velocity = 10 * dt * 0.05
            self.check_collision(platforms, 0, 1)

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
        if self.y > self.background_y:
            self.y = 0

    def check_collision(self, platforms, x, y):
        rect = self.rect()
        for platformObj in platforms:
            platform = platformObj.rect
            if rect.colliderect(platform):
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
                if rect.top > platform.top and rect.top < platform.bottom + 1:
                    self.y = platform.bottom
                    self.count = 0
                    self.isJump = False
                    self.isJumping = False
                    self.canJump = False
                    self.hitPlatform = True
                    break