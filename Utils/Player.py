import pygame

class Player():

    def __init__(self, x, y, background_x, background_y):
        self.x = x
        self.y = y
        self.background_x = background_x
        self.background_y = background_y
        self.screen = pygame.display.set_mode((background_x, background_y))
        self.isJump = False
        self.count = 12 ## count for jumping
        self.gravity = 0.5
        self.velocity = 0

    
    def rect(self): ## is only used when setting up the display such as pygame.draw.rect( screen, (0,0,255), player.rect() )
        return pygame.Rect(self.x, self.y, 40, 40)

    def update(self, preseed_keys, platforms): ## platforms is an array for all Rect objects in the level that player can get on
        self.move(preseed_keys)
        self.set_gravity()
        self.check_collision(platforms)
        pygame.draw.rect(self.screen, (255,0,0), (self.x, self.y, 40, 40))

    def move(self, pressed_keys):
        if pressed_keys[pygame.K_d]:
            if self.x + 40 != self.background_x:
                self.x += 5
        if pressed_keys[pygame.K_a]:
            if self.x != 0:
                self.x -= 5
        if pressed_keys[pygame.K_SPACE] and not self.isJump:
            self.isJump = True
            self.count = 12
            self.velocity = -10

    def jump(self):
        if self.isJump:
            if self.count >= -12:
                add_y = 1
                if self.count < 0:
                    add_y = -1
                self.y -= self.count**2 * 0.1 * add_y
                self.count -= 1
            else:
                self.isJump = False
                self.count = 12

    def set_gravity(self):
        if not self.isJump:
            self.velocity += self.gravity
            self.y += self.velocity

    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect().colliderect(platform):
                if self.velocity > 0:
                    self.y = platform.top - 40
                    self.velocity = 0
                    self.isJump = False
                elif self.velocity < 0:
                    self.y = platform.bottom
                    self.velocity = 0