
import pygame

from settings import Settings
from ship import Ship
import game_functions as gf

from pygame.sprite import Group

from game_stats import GameStats

def run_game():

    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("alien invasion")

    stats=GameStats(ai_settings)
    ship=Ship(ai_settings=ai_settings,screen=screen)
    bullets=Group()
    aliens=Group()

    gf.create_fleet(ai_settings,screen,aliens)
    while True:

        gf.check_evets(ai_settings,screen,ship,bullets)
        ship.update()

        gf.update_bullets(aliens,bullets)

        gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)

run_game()
