import pygame
from src.colours import Colours
from src.button import Button
from src.game import Game
from pygame.locals import K_ESCAPE, MOUSEBUTTONDOWN, K_SPACE
import math

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


class ScorecardScene(Scene):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.game_state: Game  = game
        self.width = 400
        self.height = 400
        self.column_width = 20
        self.column_height = 5

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("ESC Pressed!")
                if event.key == K_SPACE:
                    self.next_scene = MainMenuScene(self.screen, self.game_state)
    
    def update(self):
        pass
    
    def render(self):
        self.screen.fill(self.colours.LightRed)
        startx = (self.screen_width - self.width) /2
        starty = (self.screen_height - self.height) /2
        y_padding = 5
        number_of_rows = 19 # 18 holes + 1 header row
        pygame.draw.rect(self.screen, self.colours.Grey, (startx, starty, self.width, self.height))

        for i in range(1,3):
            pygame.draw.line(self.screen, (0,0,0), (startx + (i * (self.width/3)), starty), (startx + (i * (self.width/3)), starty + self.height -1), 1)

        for hole in range(number_of_rows):
            if hole == 0:  # Display all headers for rows
                hole_header = self.font.render('Hole', True, (0,0,0))
                self.screen.blit(hole_header, (startx + (1 *(self.width)/6) - (hole_header.get_width()/2) , starty + y_padding))
                par_header = self.font.render('Par', True, (0,0,0))
                self.screen.blit(par_header, (startx +(3 *(self.width)/6) - (par_header.get_width()/2), starty + y_padding))
                stroke_header = self.font.render('Stroke', True, (0,0,0))
                self.screen.blit(stroke_header, (startx +(5 *(self.width)/6) - (stroke_header.get_width()/2), starty + y_padding))
                press_mouse_to_continue = self.font.render('Press SPACE to continue...', True, (0,0,0))
                self.screen.blit(press_mouse_to_continue, ((self.screen_width - press_mouse_to_continue.get_width())/2 , self.screen_height - press_mouse_to_continue.get_height() - 10 ))
            else:  
                pygame.draw.line(self.screen, (0,0,0), (startx, starty + (hole * (self.height/number_of_rows))), (startx + self.width-1, starty + (hole * (self.height / number_of_rows))), 1)
                hole_number_text = self.font.render(str(hole), 1, (0,0,0))
                self.screen.blit(hole_number_text, (startx +(1 *(self.width)/6) - (hole_number_text.get_width()/2), starty + y_padding + ((hole) * (self.height/number_of_rows))))

                par_score = self.game_state.par_scores.get(str(hole)) 
                par_score_text = self.font.render(str(par_score), 1, (0,0,0))
                self.screen.blit(par_score_text, (startx +(3 *(self.width)/6) - (par_score_text.get_width()/2), starty + y_padding + ((hole) * (self.height/number_of_rows))))

                hole_score = self.game_state.scorecard.get(str(hole))    

                if hole_score is not None:
                    if hole_score < par_score:
                        color = (0,166,0)
                    elif hole_score > par_score:
                        color = (255,0,0)
                    else:
                        color = (0,0,0)

                    hole_score_text = self.font.render(str(hole_score), 1, color)
                    self.screen.blit(hole_score_text, ((startx +(5 *(self.width)/6) - (hole_score_text.get_width()/2), starty + y_padding + ((hole) * (self.height/number_of_rows)))))
                else:
                    unknown_hole_score_text = self.font.render('-', 1, (0,0,0))
                    self.screen.blit(unknown_hole_score_text, (startx +(5 *(self.width)/6) - (unknown_hole_score_text.get_width()/2), starty + y_padding + ((hole) * (self.height/number_of_rows))))


    def terminate(self):
        self.next_scene = None

class LevelScene(Scene):
    def __init__(self, level, screen, game):
        super().__init__(screen)
        self.level_locked_text_showing = False
        self.level_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/music.mp3")
        self.swing_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/golf_ball_hit.mp3")
        self.putt_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/inHole.wav")

        # self.arrow_sprite: pygame.image = pygame.image.load("data/gfx/logo.png")
        # self.arrow_sprite: pygame.image = pygame.transform.scale(self.arrow_sprite, (30, 100))
        self.game_state: Game = game
        self.level_complete: bool = False
        self.level_name = level
        self.ball_in_hole = False
        self.ball_moving = False
        self.shots = 0
        self.par = self.game_state.par_scores.get(str(level))
        self.par_text = self.font.render(f"Par: {self.par}", True, self.colours.White)
        self.load_level()
        pygame.mixer.Sound.play(self.level_music)
        pygame.mixer.Sound.set_volume(self.level_music, 0.01)
    
    def load_level(self):
        self.ball_width = 5
        self.hole_width = 10

        self.ball_position = (100,100)
        self.hole_position = (400,100)
        self.ball = pygame.draw.circle(self.screen, (0,0,0), self.ball_position, self.ball_width)
        self.hole = pygame.draw.circle(self.screen, (255,255,255), self.hole_position, self.hole_width)
        
        # self.arrow_location = (100,100)

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
            score_text = self.font.render(self.displayScore(), True, self.colours.White)
            self.screen.blit(score_text, ((self.screen_width - score_text.get_width())/2, (self.screen_height - score_text.get_height())/2))
            pygame.display.update()
            pygame.time.wait(1000)
            self.next_scene = ScorecardScene(self.screen, self.game_state)

        if self.ball.colliderect(self.hole):
            self.completed_level()
            self.level_complete = True

    def render(self):
        self.screen.fill(self.colours.LightGreen)

        self.screen.blit(self.par_text, (10, 10))

        self.hole = pygame.draw.circle(self.screen, (255,255,255), self.hole_position, self.hole_width)

        self.ball = pygame.draw.circle(self.screen, (0,0,0), self.ball_position, self.ball_width)
        # self.screen.blit(self.arrow_sprite, (self.arrow_location))

    def take_a_shot(self):
        if not self.ball_moving:
            self.ball_moving = True
            pygame.mixer.Sound.play(self.swing_music, fade_ms=1)
            pygame.mixer.Sound.set_volume(self.swing_music, 0.02)
            self.shots += 1
            self.update_ball()
    
    def update_ball(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.ball_position = mouse_x, mouse_y
        self.ball_moving = False

    def completed_level(self):
        pygame.mixer.Sound.play(self.putt_music)
        pygame.mixer.Sound.set_volume(self.putt_music, 0.02)
        self.game_state.update_last_completed_level(self.level_name)
        self.game_state.update_scorecard(self.level_name, self.shots)
        pygame.mixer.Sound.stop(self.level_music)
    
    def displayScore(self):
        if self.shots == 1:
            text = "Hole in 1!"
        elif self.shots == self.par - 4:
            text = "Condor!"
        elif self.shots == self.par - 3:
            text = "Albatross!"
        elif self.shots == self.par - 2:
            text = "Eagle!"
        elif self.shots == self.par - 1:
            text = "Birdie!"
        elif self.shots == self.par:
            text = "Par"
        elif self.shots == self.par + 1:
            text = "Bogey :("
        elif self.shots == self.par + 2:
            text = "Double Bogey :("
        elif self.shots == self.par + 3:
            text = "Triple Bogey :("
        else:
            text = f"+{(self.shots - self.par)} :("

        return text

    def get_player_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.ball_position = mouse_x, mouse_y
        # ball_x, ball_y = self.ball_position
        # angle = (math.atan2(mouse_y-(ball_y),mouse_x-(ball_x))) * (180/math.pi)
        # self.arrow_sprite = pygame.transform.rotate(self.arrow_sprite, 360-angle)
        # self.arrow_location = (self.ball_position)

class MainMenuScene(Scene):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.game_state: Game = game
        self.level_locked_text_showing = False
        self.menu_buttons: list[Button] = self.main_menu_buttons()
        self.music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/main_menu_music.mp3")
        self.clicked_level: str = None
        pygame.mixer.Sound.play(self.music)
        pygame.mixer.Sound.set_volume(self.music, 0.00)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == self.user_event:
                self.level_locked_text_showing = False

        if any(pygame.mouse.get_pressed()):
            self.clicked_level = self.check_buttons()
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
        self.blit_buttons()
        current_score = self.font.render(f"Current Score: {self.game_state.current_score}", True, self.colours.White)
        self.screen.blit(current_score, (0, self.screen_height - current_score.get_height()))

        if self.level_locked_text_showing:
            self.update_alert_text()
            alert_text_surface = self.font.render(self.alert_text, True, self.colours.White)
            self.screen.blit(alert_text_surface, (self.screen_width - alert_text_surface.get_width(), self.screen_height - alert_text_surface.get_height())) 

    def blit_buttons(self):
        for button in self.menu_buttons:
            button.draw(self.screen)
    
    def check_buttons(self):
        for button in self.menu_buttons:
            if button.hover():
                return button.button_id
        else:
            return None

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

    