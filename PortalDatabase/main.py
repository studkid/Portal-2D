import pygame 
import pygame.freetype #for woring with text
import asyncio
import mysql.connector #for database connection
import hashlib #for password encryption

#game loop
async def run_game():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window

    #color/font initialization for textboxes
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 32)
    GAME_FONT = pygame.freetype.SysFont("Arial", 24)
    
    
    #inputbox class from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    class InputBox:

        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.txt_surface = FONT.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

        def update(self):
            # Resize the box if the text is too long.
            width = max(200, self.txt_surface.get_width()+10)
            self.rect.w = width

        def draw(self, screen):
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)


    #initialize the database
    mydb = mysql.connector.connect(
        host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
        user="user", # <---- username for the MySQL account. YOU HAVE TO SET THIS to one that YOU have in PHPMyAdmin
        password="Password123$", # <---- password for the MySQL account. YOU HAVE TO SET THIS to one that YOU have in PHPMyAdmin
        database="portalgame"
    )

    def create_user(username, password):

        #hash the password
        password_bytes = str(password).encode("utf-8")
        hashed_password = hashlib.sha256(password_bytes).hexdigest() 

        #store the data as Tuples so they can be used in a query
        user_name = (username,)
        user_data = (username, hashed_password)      

        #create the queries with blank spaces for the data
        find_user = ("SELECT * FROM GameUser "
                    "WHERE username = %s")
        add_user = ("INSERT INTO GameUser "
                    "(username, password) "
                    "VALUES (%s, %s)")
        
        #execute query and get the result
        cursor = mydb.cursor()
        cursor.execute(find_user, user_name)
        result = cursor.fetchall()

        #if the query comes back empty, the username is available and an account can be created
        if result == []:
            cursor = mydb.cursor()
            cursor.execute(add_user, user_data)
            mydb.commit()
            print("username available, creating account...")
            return True
        #if the query does NOT come back empty, there is already an account with that username
        else:
            print("there is already an account with that username")
            return False
        
    #get the users from the database
    def list_users():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM GameUser")
        userlist = mycursor.fetchall()
        return userlist
    
    #loop over the users and print the user data to the screen
    def print_users():
        GAME_FONT.render_to(screen, (30, 260), "Registered Users: ", (255, 255, 255))
        users = list_users()
        for i in range (len(users)):
            GAME_FONT.render_to(screen, (30, 300 + (40*i)), "username: " + str(users[i][1]) + "    password: " + str(users[i][2]), (255, 255, 255))

    input_box1 = InputBox(150, 100, 140, 32)
    input_box2 = InputBox(150, 150, 140, 32)
    input_boxes = [input_box1, input_box2]

    #remove the text from the textboxes  
    def clear_textboxes(): 
        for box in input_boxes:
                box.active = True
                box.text = ""
                box.update()

    run = True

    while run:
        screen.fill((0,0,0))

        for box in input_boxes:
            box.draw(screen)

        GAME_FONT.render_to(screen, (input_box1.rect.left - 120, input_box1.rect.y - 50), "Create User  (press Enter to register)", (255, 255, 255))
        GAME_FONT.render_to(screen, (input_box1.rect.left - 120, input_box1.rect.y + 10), "username: ", (255, 255, 255))
        GAME_FONT.render_to(screen, (input_box2.rect.left - 120, input_box2.rect.y + 10), "password: ", (255, 255, 255))

        #display the users in the database
        print_users()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if(input_boxes[0].text != "" and input_boxes[1].text != ""): #if there is no empty textbox
                        if(create_user(input_boxes[0].text, input_boxes[1].text)): #try to create a user
                            clear_textboxes()
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(run_game())