import pygame
from Utils import GlobalVariables

class InputBox:

        def __init__(self, x, y, w, h, default_text="", is_pwd = False):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = GlobalVariables.Text_Forecolor
            self.text = default_text
            self.pwd_txt = ""
            self.default_txt = default_text
            self.txt_surface = GlobalVariables.font(24).render(default_text, True, self.color)
            self.active = False
            self.is_pwd = is_pwd

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = GlobalVariables.Text_Hovercolor if self.active else GlobalVariables.Text_Forecolor
                
                if self.text is self.default_txt and self.active:
                    self.text = ""
                elif len(self.text) <= 0 and not self.active:
                    self.text = self.default_txt
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.pwd_txt = self.pwd_txt[:-1]
                    elif event.key != pygame.K_RETURN:
                        if len(self.text) < 10 and not self.is_pwd:
                            self.text += event.unicode
                        elif len(self.text) < 20 and self.is_pwd:
                            self.text += "*"
                            self.pwd_txt += event.unicode

        def update(self):
            self.txt_surface = GlobalVariables.font(24).render(self.text, True, self.color)

        def draw(self, screen):
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x + (self.rect.w - self.txt_surface.get_width()) / 2, self.rect.y + (self.rect.h - self.txt_surface.get_height()) / 2))
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)
