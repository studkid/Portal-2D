import pygame 
import pygame.freetype 
import asyncio
import DatabaseUtil 

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


    
    #loop over the users and print the user data to the screen
    def print_users():
        GAME_FONT.render_to(screen, (30, 300), "Registered Users: ", (255, 255, 255))
        users = DatabaseUtil.list_users()
        for i in range (len(users)):
            GAME_FONT.render_to(screen, (30, 340 + (40*i)), "username: " + str(users[i][1]) + "    password: " + str(users[i][2]), (100, 100, 100))

    register_box1 = InputBox(150, 100, 140, 32)
    register_box2 = InputBox(150, 150, 140, 32)
    login_box1 = InputBox(575, 100, 140, 32)
    login_box2 = InputBox(575, 150, 140, 32)
    input_boxes = [register_box1, register_box2, login_box1, login_box2]

    #remove the text from the textboxes  
    def clear_textboxes(): 
        for box in input_boxes:
                box.active = True
                box.text = ""
                box.update()

    current_user = ["", ""]

    run = True

    while run:
        screen.fill((0,0,0))

        for box in input_boxes:
            box.draw(screen)

        GAME_FONT.render_to(screen, (275, 5), "(press Enter to register/login)", (255, 255, 255))
        GAME_FONT.render_to(screen, (register_box1.rect.left - 120, register_box1.rect.y - 50), "Create User", (255, 255, 255))
        GAME_FONT.render_to(screen, (register_box1.rect.left - 120, register_box1.rect.y + 10), "username: ", (100, 100, 100))
        GAME_FONT.render_to(screen, (register_box2.rect.left - 120, register_box2.rect.y + 10), "password: ", (100, 100, 100))
        GAME_FONT.render_to(screen, (login_box1.rect.left - 120, login_box1.rect.y - 50), "Login", (255, 255, 255))
        GAME_FONT.render_to(screen, (login_box1.rect.left - 120, login_box1.rect.y + 10), "username: ", (100, 100, 100))
        GAME_FONT.render_to(screen, (login_box2.rect.left - 120, login_box2.rect.y + 10), "password: ", (100, 100, 100))

        #display the currently logged in user
        if current_user == ["", ""]:
            GAME_FONT.render_to(screen, (30, 230), "Login Status: not logged in", (255, 255, 255))
        else:
            GAME_FONT.render_to(screen, (30, 230), "Login Status: logged in as " + current_user[0], (255, 255, 255))

        #display the list of users in the database
        print_users()

        #handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if(input_boxes[0].text != "" and input_boxes[1].text != ""): #if the user has entered registration info
                        if(DatabaseUtil.create_user(input_boxes[0].text, input_boxes[1].text)): #try to create a user
                            clear_textboxes()
                    elif(input_boxes[2].text != "" and input_boxes[3].text != ""): #if the user has entered login info
                        if(DatabaseUtil.authenticate_user(input_boxes[2].text, input_boxes[3].text)): #try to authenticate the user
                            current_user = [input_boxes[2].text, input_boxes[3].text]
                            clear_textboxes()
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(run_game())