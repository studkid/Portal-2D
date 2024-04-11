import pygame
from sys import exit
import math
from game_settings import *


pygame.init()

#platforms
platform = pygame.Rect( 100,300,200,50 )


#tab/window settings
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( "2D Portal" )
clock = pygame.time.Clock()

#portal gun  
class Pgun( pygame.sprite.Sprite ):
    def __init__( self ):
        super().__init__()
        self.pos = pygame.math.Vector2( PGUN_START_X, PGUN_START_Y ) #sets position when you first load the game
        self.image = pygame.transform.rotozoom( pygame.image.load( "img/pgun/pgun.png" ).convert_alpha(), 0, PGUN_SIZE )
        self.base_pgun_image = self.image
        self.hitbox_rect = self.base_pgun_image.get_rect( center = self.pos )
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED #reminder to change to lock on to player
        self.shoot = False
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2( 0, 0 ) #sets how far away the portal gun is away from the player
      
#locks aims the pgun twords wherever the mouse is 
    def pgun_rotation( self ):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_pgun = ( self.mouse_coords[ 0 ] - self.hitbox_rect.centerx )
        self.y_change_mouse_pgun = ( self.mouse_coords[ 1 ] - self.hitbox_rect.centery )
        self.angle = math.degrees( math.atan2( self.y_change_mouse_pgun, self.x_change_mouse_pgun ) )
        self.image = pygame.transform.rotate( self.base_pgun_image, -self.angle )
        self.rect = self.image.get_rect( center = self.hitbox_rect.center )
       

    def user_input (self ):
        self.velocity_x = 0
        self.velocity_y = 0

#basic key bindings 
#wasd movment used for testing
#will change so the portal gun follows the player
        keys = pygame.key.get_pressed()
        if keys[ pygame.K_w ]:
            self.velocity_y = -self.speed
        if keys[ pygame.K_s ]:
            self.velocity_y = self.speed
        if keys[ pygame.K_d ]:
            self.velocity_x = self.speed
        if keys[ pygame.K_a ]:
            self.velocity_x = -self.speed
    #bullet test code
        if keys[ pygame.K_h ]:
            BULLET_LIFETIME = 0

#used for testing diagonal movemnt
        #if self.velocity_x != 0 and self.velocity_y != 0:
            #self.velocity_x /= math.sqrt(2)
            #self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == ( 1, 0, 0 ): #( 1, 0, 0 ) means left click
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
        

#sets a delay when you shoot
    def is_shooting( self ): 
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate( self.angle )
            self.bullet = Bullet( spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle )
            bullet_group.add( self.bullet )
            all_sprites_group.add( self.bullet )

            
#moves hitbox
    def move( self ):
        self.pos += pygame.math.Vector2( self.velocity_x, self.velocity_y )
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update( self ):
        self.user_input()
        self.move()
        self.pgun_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

#sets up shooting the bullet and the bullet movement
class Bullet( pygame.sprite.Sprite ):
    def __init__( self, x, y, angle ):
        super().__init__()
        self.image = pygame.image.load( "img/pgun/bullet.png" ).convert_alpha()
        self.image = pygame.transform.rotozoom( self.image, 0, BULLET_SCALE ) #adjust bullet size
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.x_vel = math.cos( self.angle * ( 2*math.pi/360 ) ) * self.speed #adjust the x velocity for the bullet when shot
        self.y_vel = math.sin( self.angle * ( 2*math.pi/360 ) ) * self.speed 
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks() #gets the time that the bullet was created
        self.collide = False


    def bullet_movement( self ):  
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int( self.x )
        self.rect.y = int( self.y )

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime: #despawn bullet if it goes to far
            self.kill() 
        
        if self.rect.colliderect(platform):
            self.collide = True
            self.bullet_col()
            #test code
            #print( 'nice' )
        else:
            self.collide = False

 #gets rid of bullet image and spawns portal
    def bullet_col( self ):
        spawn_portal_pos =  self.x, self.y
        self.bullet = Portal( spawn_portal_pos[0], spawn_portal_pos[1], self.angle )
        bullet_group.add( self.bullet )
        all_sprites_group.add( self.bullet )
        self.kill() 
        self.collide = False
      

    def update( self ):
        self.bullet_movement()
        
        
class Portal( pygame.sprite.Sprite ):
    def __init__( self, x, y, angle ):
        super().__init__()
        self.image = pygame.image.load( "img/Portal_Blue.png" ).convert_alpha()
        self.image = pygame.transform.rotozoom( self.image, 0, PORTAL_SCALE ) #adjust portal size
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )
        self.x = x
        self.y = y
        self.angle = angle
        self.spawn_time = pygame.time.get_ticks()
        self.spawned_portals = SPAWNED_PORTALS


    def portal_count( self ):
        if pygame.mouse.get_pressed() == ( 1, 0, 0 ): #( 1, 0, 0 ) means left click
            self.spawned_portals = self.spawned_portals + 1
            print( self.spawned_portals )


    def max_portals( self ):
        
        if self.spawned_portals >= 6:
            self.kill()
            self.spawned_portals = 0
            print( self.spawned_portals )
    

    def update( self ):
        self.portal_count()
        self.max_portals()

        



pgun = Pgun()

all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

all_sprites_group.add( pgun )

