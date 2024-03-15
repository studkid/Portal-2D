import pygame
import pygame.freetype
import asyncio
import mysql.connector

#game loop
async def run_game():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window

    #initialize the text font
    GAME_FONT = pygame.freetype.SysFont("Arial", 24)

    #initialize the database
    mydb = mysql.connector.connect(
        host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
        user="user", # <---- username for the MySQL account. YOU HAVE TO SET THIS to one that YOU have in PHPMyAdmin
        password="Password123$", # <---- password for the MySQL account. YOU HAVE TO SET THIS to one that YOU have in PHPMyAdmin
        database="portalgame"
    )
    #get the data from the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM GameUser")
    myresult = mycursor.fetchall()

    #background = pygame.image.load('Path.jpg').convert()
    player = pygame.Rect((300, 250, 25, 50))
    run = True

    while run:
        screen.fill((0,0,0))

        #loop over the myresult array and print the user data from the database
        for x in myresult:
            GAME_FONT.render_to(screen, (40, 350 + (40*x[0])), "username: " + str(x[1]) + ", password: " + str(x[2]), (255, 255, 255))

        #screen.bli(background, (0,0))
        pygame.draw.rect(screen, (0,0,255), player)

        key_pressed = pygame.key.get_pressed()
        if(key_pressed[pygame.K_LEFT]):
            if(player.left != 0):
                player.move_ip(-1,0)
        elif(key_pressed[pygame.K_RIGHT]):
            if(player.right != SCREEN_WIDTH):
                player.move_ip(1,0)
        elif(key_pressed[pygame.K_UP]):
            if(player.right != 0):
                player.move_ip(0,-1)
        elif(key_pressed[pygame.K_DOWN]):
            if(player.right != SCREEN_HEIGHT):
                player.move_ip(0,1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(run_game())