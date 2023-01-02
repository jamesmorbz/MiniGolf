import pygame

class Game:
    def __init__(self):
        self.current_score: int = 0
        self.par: int = 0
        self.current_level = 0
        self.last_completed_level = 0
        self.highest_level_completed = 0 
        self.next_level = 1
        self.putt_sound: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/golf_ball_hit.mp3")
        self.scorecard = {}

    def get_current_level(self):
        return self.current_level

    def update_current_level(self, level):
        self.current_level = level
    
    def update_last_completed_level(self, level):
        self.last_completed_level = level
        self.highest_level_completed = max(self.highest_level_completed, level)
        self.next_level = self.highest_level_completed + 1

    def update_scorecard(self, level, shots):
        self.scorecard[level] = shots
        self.current_score = sum(list(self.scorecard.values()))

    def check_if_level_unlocked(self, level):
        if level > self.next_level:
            return False
        else:
            return True

    def displayScore(self, stroke, par):
        if stroke == 0:
            text = "Skipped"
        elif stroke == par - 4:
            text = "-4!"
        elif stroke == par - 3:
            text = "Albatross!"
        elif stroke == par - 2:
            text = "Eagle!"
        elif stroke == par - 1:
            text = "Birdie!"
        elif stroke == par:
            text = "Par"
        elif stroke == par + 1:
            text = "Bogey :("
        elif stroke == par + 2:
            text = "Double Bogey :("
        elif stroke == par + 3:
            text = "Triple Bogey :("
        else:
            text = "+ " + str(stroke - par) + " :("


    