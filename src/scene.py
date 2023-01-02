import pygame
import sys
from src.colours import Colours
from src.button import Button
from src.game import Game
from pygame.locals import K_ESCAPE, MOUSEBUTTONDOWN
import random

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
    def __init__(self, level, screen, game):
        super().__init__(screen)
        self.level_locked_text_showing = False
        self.level_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/music.mp3")
        self.swing_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/golf_ball_hit.mp3")
        self.putt_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/inHole.wav")
        self.game_state: Game = game
        self.level_complete: bool = False
        self.level_name = level
        self.ball_in_hole = False
        self.shots = 0
        pygame.mixer.Sound.play(self.level_music)
        pygame.mixer.Sound.set_volume(self.level_music, 0.01)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("ESC Pressed!")
            if event.type == MOUSEBUTTONDOWN:
                self.take_a_shot()

    def update(self):
        if self.game_state.get_current_level() != self.level_name:
            self.game_state.update_current_level(self.level_name)

        if self.level_complete:
            self.next_scene = MainMenuScene(self.screen, self.game_state)

        if self.shots == 3:
            self.completed_level()
            self.level_complete = True

    def render(self):
        self.screen.fill(self.colours.Black)
       
    def take_a_shot(self):
        pygame.mixer.Sound.play(self.swing_music, fade_ms=1)
        pygame.mixer.Sound.set_volume(self.swing_music, 0.02)
        self.shots += 1

    def completed_level(self):
        pygame.mixer.Sound.play(self.putt_music)
        pygame.mixer.Sound.set_volume(self.putt_music, 0.02)
        self.game_state.update_last_completed_level(self.level_name)
        self.game_state.update_scorecard(self.level_name, self.shots)
        pygame.mixer.Sound.stop(self.level_music)

class MainMenuScene(Scene):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.game_state: Game = game
        self.level_locked_text_showing = False
        self.menu_buttons = self.main_menu_buttons()
        self.music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/main_menu_music.mp3")
        self.clicked_level: str = None
        pygame.mixer.Sound.play(self.music)
        pygame.mixer.Sound.set_volume(self.music, 0.00)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == self.user_event:
                self.level_locked_text_showing = False

        if any(pygame.mouse.get_pressed()):
            self.clicked_level = check_buttons(self.menu_buttons)
            if self.clicked_level is not None:
                if self.game_state.check_if_level_unlocked(self.clicked_level):
                    self.next_scene = LevelScene(level = self.clicked_level, screen = self.screen, game = self.game_state )
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
        current_score = self.font.render(f"Current Score: {self.game_state.current_score}", True, self.colours.White)
        self.screen.blit(current_score, (0, self.screen_height - current_score.get_height()))

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
            level_name = i+1
            nth_button = i % buttons_in_row
            button_row = i // buttons_in_row
            button_x = padding_width + ((nth_button + 1) * spacing_width + nth_button * button_width)
            button_y = padding_height + ((button_row) * spacing_height + button_row * button_height)
            button = Button(level_name, self.colours.Grey, button_x, button_y, button_width, button_height, f"Level {level_name}", self.font) 
            current_score = self.game_state.scorecard.get(level_name)

            if current_score is not None:
                button.add_text(str(current_score))
            buttons.append(button)

        return buttons

    