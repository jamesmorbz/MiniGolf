import pygame
class Button():
    def __init__(self, button_id, color, x, y, width, height, text, font):
        self.button_id = button_id  
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font: pygame.font.Font = font

    def draw(self, win: pygame.Surface, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        text = self.font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + 2))

    def hover(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.x and mouse[0] < self.x + self.width:
            if mouse[1] > self.y and mouse[1] < self.y + self.height:
                return True
            
        return False