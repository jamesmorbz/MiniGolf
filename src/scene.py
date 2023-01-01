import pygame
import sys
from src.colours import Colours
from src.button import Button
from src.game import Game
from pygame.locals import K_ESCAPE
def blit_buttons(buttons: list[Button], display: pygame.Surface):
        for button in buttons:
            button.draw(display)

def check_buttons(buttons: list[Button]):
    for button in buttons:
        if button.hover():
            return button.button_id
    else:
        return None

class Scene():
    def __init__(self, screen):
        self.next_scene = self
        self.screen: pygame.Surface = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.user_event = pygame.USEREVENT + 1
        self.colours = Colours()
        self.font = pygame.font.SysFont("comicsansms", 12)

    def process_input(self, events, pressed_keys):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None

class LevelScene(Scene):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.level_locked_text_showing = False
        # self.music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/game_music.mp3")
        self.game_state: Game = game
        self.clicked_level: str = None
        # pygame.mixer.Sound.play(self.music)
        # pygame.mixer.Sound.set_volume(self.music, 0.02)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("ESC Pressed!")
                
    def update(self):
        pass
            
    def render(self):
        self.screen.fill(self.colours.Black)
       

class MainMenuScene(Scene):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.level_locked_text_showing = False
        self.menu_buttons = self.main_menu_buttons()
        self.music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/main_menu_music.mp3")
        self.game_state: Game = game
        self.clicked_level: str = None
        pygame.mixer.Sound.play(self.music)
        pygame.mixer.Sound.set_volume(self.music, 0.02)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == self.user_event:
                self.level_locked_text_showing = False

        if any(pygame.mouse.get_pressed()):
            self.clicked_level = check_buttons(self.menu_buttons)
            if self.clicked_level is not None:
                if self.game_state.check_if_level_unlocked(self.clicked_level):
                    self.next_scene = LevelScene(self.screen, self.game_state)
                    pygame.mixer.Sound.stop(self.music)
                else:
                    self.level_locked_text_showing = True
                    pygame.time.set_timer(self.user_event, 1000, 1)

    def update(self):
        pass
    
    def update_alert_text(self):
        if self.clicked_level is not None:
            self.alert_text = f"Level {self.clicked_level} Locked! - Please Complete Level {self.game_state.next_level} First!"
            
    def render(self):
        self.screen.fill(self.colours.LightGreen)
        blit_buttons(self.menu_buttons, self.screen)

        if self.level_locked_text_showing:
            self.update_alert_text()
            alert_text_surface = self.font.render(self.alert_text, True, self.colours.White)
            self.screen.blit(alert_text_surface, (self.screen_width - alert_text_surface.get_width(), self.screen_height - alert_text_surface.get_height())) 

    def main_menu_buttons(self):
        number_of_holes = 18
        buttons = []

        buttons_in_row = 3
        number_of_rows = number_of_holes/buttons_in_row

        button_width = 160
        button_height = 50

        padding_width = self.screen_width/20
        padding_height = self.screen_height/20

        area_width = self.screen_width - 2*padding_width
        area_height = self.screen_height - 2*padding_height

        spacing_width =  (area_width - button_width * buttons_in_row) / (buttons_in_row + 1)
        spacing_height = (area_height - number_of_rows * button_height) / number_of_rows 

        for i in range(number_of_holes):
            nth_button = i % buttons_in_row
            button_row = i // buttons_in_row
            button_x = padding_width + ((nth_button + 1) * spacing_width + nth_button * button_width)
            button_y = padding_height + ((button_row) * spacing_height + button_row * button_height)
            button = Button(i+1, self.colours.Grey, button_x, button_y, button_width, button_height, f"Level {i+1}", self.font) 
            buttons.append(button)

        return buttons

    