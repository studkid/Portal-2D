import pygame

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
        self.canJump = True
        self.jump_count = 14 ## a variable that holds numbers of count jump
        self.count = 14 ## count for jumping ( will be used as countdown in jumping )
        self.gravity = 0.5
        self.velocity = 0

    
    def rect(self): ## is only used when setting up the display such as pygame.draw.rect( screen, (0,0,255), player.rect() )
        return pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self, platforms): ## platforms is an array for all Rect objects in the level that player can get on
        self.set_gravity(platforms)
        self.check_collision(platforms, 0, -1)

    def move(self, pressed_keys, platforms):
        if pressed_keys[pygame.K_d]:
            if self.x + self.size_x != self.background_x:
                self.x += 5
                self.check_collision(platforms, 1, 1)
        if pressed_keys[pygame.K_a]:
            if self.x != 0:
                self.x -= 5
                self.check_collision(platforms, -1, 1)
        if pressed_keys[pygame.K_SPACE] and self.canJump:
            self.isJump = True
            self.canJump = False
            self.count = self.jump_count
            self.velocity = 10
            self.check_collision(platforms, 0, 1)

    def jump(self, platforms):
        if self.isJump:
            if self.count >= -self.jump_count:
                add_y = 1
                if self.count < 0:
                    add_y = -1
                self.check_collision(platforms, 0, 1)
                if self.y - self.count**2 * 0.1 * add_y > 0:
                    self.y -= self.count**2 * 0.1 * add_y
                else:
                    self.count = 0
                self.count -= 1
            else:
                self.isJump = False
                self.count = self.jump_count

    def set_gravity(self, platforms):
        if not self.isJump:
            self.velocity += self.gravity
            for platform in platforms:
                if not self.rect().colliderect(platform):
                    self.y += self.velocity

    def check_collision(self, platforms, x, y):
        rect = self.rect()
        for platform in platforms:
            if rect.colliderect(platform):
                if x > 0: 
                    self.x = platform.left - self.size_x
                elif x < 0:
                    self.x = platform.right
                elif y < 0:
                    self.y = platform.top - self.size_y
                    self.velocity = 0
                    self.isJump = False
                    self.canJump = True
                elif y > 0:
                    self.y = platform.bottom
                    self.velocity = 0