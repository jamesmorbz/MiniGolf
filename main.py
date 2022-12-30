import sys

import logging
import pygame
from pygame.locals import RESIZABLE, WINDOWRESIZED, VIDEORESIZE
import os 
from src.button import Button
from src.game import Game

light_green = (0,196,0)
grey = (147,147,147)
screen_width, screen_height = 640,480
number_of_holes = 18

def main_menu_buttons():
    global light_green
    global grey
    global screen_width
    global screen_height
    global number_of_holes

    buttons = []

    buttons_in_row = 3
    number_of_rows = number_of_holes/buttons_in_row

    button_width = 160
    button_height = 50

    padding_width = screen_width/20
    padding_height = screen_height/20

    area_width = screen_width - 2*padding_width
    area_height = screen_height - 2*padding_height

    spacing_width =  (area_width - button_width * buttons_in_row) / (buttons_in_row + 1)
    spacing_height = (area_height - number_of_rows * button_height) / number_of_rows 

    # assert (buttons_in_row * spacing_width + 1) + (buttons_in_row * button_width) < area_width

    for i in range(number_of_holes):
        nth_button = i % buttons_in_row
        button_row = i // buttons_in_row
        button_x = padding_width + ((nth_button + 1) * spacing_width + nth_button * button_width)
        button_y = padding_height + ((button_row) * spacing_height + button_row * button_height)
        button = Button(i+1, grey, button_x, button_y, button_width, button_height, f"Level {i+1}", FONT) 
        buttons.append(button)

    return buttons

def blit_buttons(buttons: list[Button], display: pygame.Surface):
    for button in buttons:
        button.draw(display)

def check_buttons(buttons: list[Button]):
    for button in buttons:
        if button.hover():
            return button.button_id
    else:
        return None

def load_level(level, display: pygame.Surface):
    
    display.fill(light_green)
    ball = pygame.draw.circle(display, (0,0,0), (100,200), 10)
    hole = pygame.draw.circle(display, (255,255,255), (400,200), 10)
    
def main():

    global light_green
    global grey
    global screen_width
    global screen_height
    global number_of_holes

    draw_text = False
    main_menu = True

    hide_text_event = pygame.USEREVENT + 1
    main_menu_music: pygame.mixer.Sound = pygame.mixer.Sound("data/sfx/main_menu_music.mp3")

    display = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

    pygame.display.set_caption("Mini Golf")
    
    pygame.display.set_icon(pygame.image.load("data/gfx/putter.jpg"))

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    
    pygame.mixer.Sound.play(main_menu_music)
    pygame.mixer.Sound.set_volume(main_menu_music, 0.02)

    while True:
        
        if main_menu:
            display.fill(light_green)
            main_menu_buttons_list = main_menu_buttons()

            blit_buttons(main_menu_buttons_list, display)
            
            if any(pygame.mouse.get_pressed()):
                clicked_level = check_buttons(main_menu_buttons_list)
                if clicked_level is not None:
                    if game.check_if_level_unlocked(clicked_level):
                        main_menu = False
                        pygame.mixer.Sound.stop(main_menu_music)
                    else:
                        alert_text = f"Level {clicked_level} Locked! - Please Complete Level {game.next_level} First!"     
                        draw_text = True
                        pygame.time.set_timer(hide_text_event, 1000, 1)

            if draw_text:
                alert_text_surface = ALERTFONT.render(alert_text, True, (0,0,0))
                display.blit(alert_text_surface, (screen_width - alert_text_surface.get_width(), screen_height - alert_text_surface.get_height())) 

        else:
            load_level(clicked_level, display)
            
        for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    display = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                    screen_width, screen_height = display.get_size()
                if event.type == WINDOWRESIZED:
                    display = pygame.display.set_mode((display.get_width(), display.get_height()), RESIZABLE)
                    screen_width, screen_height = display.get_size()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == hide_text_event:
                    draw_text = False

        pygame.display.update()
        

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("comicsansms", 12)
    ALERTFONT = pygame.font.SysFont("comicsansms", 20)
    
    game = Game()
    main()
