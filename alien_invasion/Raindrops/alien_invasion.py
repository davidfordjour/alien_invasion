import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group

def run_game():     # Initialise game and create a screen object.
    pygame.init()   # Initialises background settings for Pygame.
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)     # Make a ship.
    bullets = Group()   # Make a group to store bullets in.
    aliens = Group()    # Make a group to store aliens in.

    gf.create_fleet(ai_settings, screen, ship, aliens)    # Create the fleet of aliens.


    while True:  # Start the main loop for the game.
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        bullets.update()
        gf.update_bullets(bullets)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)




run_game()
