import pygame
from src.levels import Levels
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
        self.levels = Levels()
        self.par_scores = self.levels.par_scores
        self.par_strokes = sum(list(self.levels.par_scores.values()))
        
    def get_current_level(self):
        return self.current_level

    def update_current_level(self, level):
        self.current_level = level
    
    def update_last_completed_level(self, level):
        self.last_completed_level = level
        self.highest_level_completed = max(self.highest_level_completed, level)
        self.next_level = self.highest_level_completed + 1

    def update_scorecard(self, level, shots):
        self.scorecard[str(level)] = shots
        self.current_score = sum(list(self.scorecard.values()))

    def check_if_level_unlocked(self, level):
        if level > self.next_level:
            return False
        else:
            return True


    