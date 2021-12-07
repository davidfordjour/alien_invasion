import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from alien import Alien



def run_game():     # Initialise game and create a screen object.
    pygame.init()   # Initialises background settings for Pygame.
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)


    ship = Ship(ai_settings, screen)     # Make a ship.
    bullets = Group()   # Make a group to store bullets in.
    alien_bullets = Group()     # Make a group to store alien bullets in.
    aliens = Group()    # Make a group to store aliens in.
    alien = Alien(ai_settings, screen)


    gf.create_fleet(ai_settings, screen, ship, aliens)    # Create the fleet of aliens.


    while True:  # Start the main loop for the game.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets, alien_bullets, alien)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.fire_alien_bullet(ai_settings, screen, alien_bullets, alien, aliens, stats)
            gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, alien_bullets
                                 , bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  alien_bullets, play_button)




run_game()

