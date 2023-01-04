import pygame
class Button():
    def __init__(self, button_id, color, x, y, width, height, text, font, text_position="top"):
        self.button_id = button_id  
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_items: list[str] = [text]
        self.font: pygame.font.Font = font
        self.text_position = text_position

    def add_text(self, text):
        self.text_items.append(text)

    def draw(self, win: pygame.Surface): 
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        for index, text in enumerate(self.text_items):
            text: pygame.Surface = self.font.render(text, 1, (0,0,0))
            if self.text_position == "top":
                if index > 0:
                    previous_text = self.font.render(self.text_items[index-1], 1, (0,0,0))
                    win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + 2 + previous_text.get_height()))
                else:
                    win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + 2))
            elif self.text_position == "middle":
                if index > 0:
                    previous_text = self.font.render(self.text_items[index-1], 1, (0,0,0))
                    win.blit(text, (self.x + (self.width/2 - text.get_width()/2), (self.y + (self.height/2 - text.get_height()/2))))
                else:
                    win.blit(text, (self.x + (self.width/2 - text.get_width()/2), (self.y + (self.height/2 - text.get_height()/2))))

    def hover(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.x and mouse[0] < self.x + self.width:
            if mouse[1] > self.y and mouse[1] < self.y + self.height:
                return True
            
        return False