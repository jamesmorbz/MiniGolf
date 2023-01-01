import pygame
from src.game import Game
from src.scenemanager import SceneManager

screen_width, screen_height = 640,480
number_of_holes = 18
    
def main():

    display = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mini Golf")
    pygame.display.set_icon(pygame.image.load("data/gfx/putter.jpg"))

    game = Game()
    scene_manager = SceneManager(display, game)

    while True:
        scene_manager.run()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.find_channel().set_volume(0.02)
    clock = pygame.time.Clock()
    main()
