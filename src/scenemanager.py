import pygame
import src.scene as Scene
import src.game as Game
import sys

class SceneManager():
    def __init__(self, display: pygame.Surface, game: Game, framerate:int = None):
        self.active_scene = Scene.MainMenuScene(display, game)
        self.clock = pygame.time.Clock()
        self.framerate = framerate if framerate else 60
        self.running = True
    def is_quit_event(self, event):
        exit_program = event.type == pygame.QUIT

        return exit_program
        
    def run(self): 
        while self.running and self.active_scene is not None:
            # Getting all pressed keys each loop
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            for event in pygame.event.get():
                if self.is_quit_event(event):
                    self.running = False
                else:
                    filtered_events.append(event)

            # Managing the Keys Pressed
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()
            self.active_scene = self.active_scene.next_scene

            # Update Display Each Loop
            pygame.display.flip()
            self.clock.tick(self.framerate)

        pygame.quit()
        sys.exit()