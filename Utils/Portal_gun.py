import pygame
import math
from Utils.Game_settings import *

pGunSprites = [pygame.image.load("Assets/8bitPortalGun_Sprite_Blue.png"), pygame.image.load("Assets/8bitPortalGun_Sprite_Orange.png")]
portalSprites = [pygame.image.load("Assets/8bitPortal_Sprite_Blue.png"), pygame.image.load("Assets/8bitPortal_Sprite_Orange.png")]
bulletSprites = [pygame.image.load("Assets/LazerBlast_Blue.png"), pygame.image.load("Assets/LazerBlast_Orange.png")]

#portal gun  
class Pgun( pygame.sprite.GroupSingle ):
    def __init__( self, firstPlayer ):
        super().__init__()
        if firstPlayer:
            self.playerNum = 0
        else: 
            self.playerNum = 1
        self.pos = pygame.math.Vector2( PGUN_START_X, PGUN_START_Y ) #sets position when you first load the game
        self.image = pygame.transform.scale(pGunSprites[self.playerNum], (32 * 2, 21 * 2))
        self.base_pgun_image = self.image
        self.hitbox_rect = self.base_pgun_image.get_rect( center = self.pos )
        self.rect = self.hitbox_rect.copy()
        self.shoot_cooldown = 0
        self.angle = 0
        self.gun_barrel_offset = pygame.math.Vector2( 0, 0 ) #sets how far away the portal gun is away from the player
        self.portalPos = (0,0)
        self.portalRot = 0
      
#locks aims the pgun twords wherever the mouse is 
    def pgun_rotation( self ):
        if self.playerNum == 0:
            self.mouse_coords = pygame.mouse.get_pos()
            self.x_change_mouse_pgun = ( self.mouse_coords[ 0 ] - self.hitbox_rect.centerx )
            self.y_change_mouse_pgun = ( self.mouse_coords[ 1 ] - self.hitbox_rect.centery )
            self.angle = math.degrees( math.atan2( self.y_change_mouse_pgun, self.x_change_mouse_pgun ) )
            self.image = pygame.transform.rotate( self.base_pgun_image, -self.angle )
            self.rect = self.image.get_rect( center = self.hitbox_rect.center )
        else:
            self.image = pygame.transform.rotate( self.base_pgun_image, -self.angle )
            self.rect = self.image.get_rect( center = self.hitbox_rect.center )

#sets a delay when you shoot
    def is_shooting( self ): 
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.rect.center + self.gun_barrel_offset.rotate( self.angle )
            self.sprite = Bullet( spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.playerNum )
         
#moves hitbox
    def move( self ):
        self.pos += pygame.math.Vector2( self.velocity_x, self.velocity_y )
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update( self, platforms ):
        self.rect.center = self.hitbox_rect.center
        #if self.playerNum == 0:
        self.pgun_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if type(self.sprite) is Bullet:
            collided = self.sprite.update(platforms)
            if collided:
                self.spawnPortal(self.sprite.rect.center, collided)
        elif self.sprite:
            self.sprite.update()

    def spawnPortal(self, center, platform):
        top = abs(center[1] - platform.rect.top)
        bottom = abs(center[1] - platform.rect.bottom)
        left = abs(center[0] - platform.rect.left)
        right = abs(center[0] - platform.rect.right)
        collide = min(min(top, bottom), min(left, right))
        pos = (0, 0)
        angle = 0

        if collide == top:
            pos = (center[0], platform.rect.top - 10)
            angle = 270
        elif collide == bottom:
            pos = (center[0], platform.rect.bottom + 10)
            angle = 90
        elif collide == left:
            pos = (platform.rect.left - 10, center[1])
            angle = 0
        elif collide == right:
            pos = (platform.rect.right + 10, center[1])
            angle = 180

        self.portalPos = pos
        self.portalRot = angle
        self.sprite = Portal(pos[0], pos[1], angle, self.playerNum)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)
        if self.sprite:
            self.sprite.drawHitbox(screen)

#sets up shooting the bullet and the bullet movement
class Bullet( pygame.sprite.Sprite ):
    def __init__( self, x, y, angle , playerNum):
        super().__init__()
        self.image = pygame.transform.scale(bulletSprites[playerNum], (25 * 2, 9 * 2))
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = ( x, y )
        self.speed = BULLET_SPEED
        self.x_vel = math.cos( angle * ( 2*math.pi/360 ) ) * self.speed #adjust the x velocity for the bullet when shot
        self.y_vel = math.sin( angle * ( 2*math.pi/360 ) ) * self.speed 
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks() #gets the time that the bullet was created
        self.bullet_offset = pygame.math.Vector2( 0, 0 )

    def bullet_movement( self, platforms ) -> bool:  
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int( self.x )
        self.rect.y = int( self.y )

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime: #despawn bullet if it goes to far
            self.kill() 
        
        for platform in platforms:
            if self.rect.colliderect( platform ) and platform.active:
                if platform.isPortable:
                    return platform
                else:
                    self.kill()
                    return None
            
        return None

    def update( self, platform ) -> bool:
        return self.bullet_movement(platform)
    
    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)
        
class Portal( pygame.sprite.Sprite ):
    def __init__( self, x, y, angle, playerNum ):
        super().__init__()
        self.image = pygame.transform.scale(portalSprites[playerNum], (29 * 2, 57 * 2))
        self.image = pygame.transform.rotate(self.image, angle)
        self.playerNum = playerNum
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )
        self.x = x
        self.y = y
        self.angle = angle
        self.spawn_time = pygame.time.get_ticks()
        self.spawned_portals = SPAWNED_PORTALS
        self.spawned_portals = 0
        self.p_shoot = False

    def drawHitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)