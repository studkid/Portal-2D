import pygame

class MenuButton():
    def __init__(self, x, y, text, font, color, hover_color, active = True):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = pygame.Rect(x, y, self.rendered_text.get_width(), self.rendered_text.get_height())
        self.active = active

    def update(self, screen):
        if self.active:
            screen.blit(self.rendered_text, self.rect)
    
    def check_click(self, mouse_pos):
        if mouse_pos[0] in range (self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def check_hover(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.rendered_text = self.font.render(self.text, True, self.color)