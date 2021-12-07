import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from alien_bullet import AlienBullet
import random



def check_keydown_events(event, ai_settings, screen, ship, sb, bullets, stats
                         , aliens, alien_bullets, alien):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        high_score_saver(stats)
        sys.exit()
    elif event.key == pygame.K_p:       # Press 'P' to start game.
        high_score_loader(stats)
        sb.prep_high_score()
        start_game(ai_settings, stats, aliens, bullets, screen, ship, alien_bullets, alien)



def high_score_loader(stats):
    """Uploads high score."""
    high_score = open("HighScore.txt", "r")
    stats.high_score = int(high_score.read())

def high_score_saver(stats):
    """Saves the game's high score."""
    high_score = open("HighScore.txt", "w")
    high_score.write(str(stats.high_score))



def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb,  play_button, ship, aliens,
                 bullets, alien_bullets, alien):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, sb, bullets, stats
                                 , aliens, alien_bullets, alien)
            



        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)



def start_game(ai_settings, stats, aliens, bullets, screen, ship, alien_bullets, alien):
    """Different ways to start the game."""
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of aliens and bullets.
    empty_ab(aliens, bullets)


    create_fleet(ai_settings, screen, ship, aliens)     # Create a new fleet
    ship.center_ship()      # Center the ship



def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens,bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        #start_game(ai_settings, stats, aliens, bullets, screen, ship)

        # Reset the game statistics and scoreboard images.
        reset_game(stats, sb)


        # Empty the list of aliens and bullets.
        empty_ab(aliens, bullets)

def reset_game(stats, sb):
    """Resets the game statistics when a new game is started."""
    stats.reset_stats()
    stats.game_active = True

    sb.prep_images()

def empty_ab(aliens, bullets):
    """Empty the list of aliens and bullets."""
    aliens.empty()
    bullets.empty()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  alien_bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_colour)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()


    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)

    pygame.display.flip()   # Make the most recently drawn screen visible

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets
                   ):
    """Update position of bullets and get rid of old bullets."""
    bullets.update()    # Update bullet positions.


    for bullet in bullets.copy():       # Get rid of bullets that have disappeared
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)



    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, alien_bullets
                    ,bullets):
    """Update position of alien bullets and get rid of old alien bullets."""
    alien_bullets.update()  # Update bullet positions.

    for alien_bullet in alien_bullets.copy():  # Get rid of bullets that have disappeared
        if alien_bullet.rect.bottom >= 800:
            alien_bullets.remove(alien_bullet)

    check_bullet_ship_collisions(screen, stats, sb, ship,alien_bullets, ai_settings, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        crash_sound()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points *len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


def check_bullet_ship_collisions(screen, stats, sb, ship,alien_bullets, ai_settings, aliens, bullets):
    """Respond to alien bullet-ship collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.spritecollideany(ship,  alien_bullets)

    if collisions:
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)





def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """When entire fleet is destroyed a new level is started."""

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        laser_sound()
        bullets.add(new_bullet)

def fire_alien_bullet(ai_settings, screen, alien_bullets, alien, aliens, stats):
    """For aliens to start randomly firing bullets."""

    for alien in aliens:
        if random.randrange(1600) == 0 and len(aliens) <= random.randrange(28):
            new_bullet = AlienBullet(ai_settings, screen, alien, aliens)
            laser_sound()
            alien_bullets.add(new_bullet)








def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.y = alien.rect.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)




    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)





def check_fleet_edges(ai_settings, aliens):
    """Respond appropiately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    # Decrement ships left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        crash_sound()

        sb.prep_ships()     # Update scoreboard.

        # Empty the list of aliens and bullets.
        empty_ab(aliens, bullets)

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleeper(1)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def sleeper(seconds):
    """Pauses the game."""
    sleep(seconds)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break



def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def laser_sound():
    """Sounds for the laser."""
    pygame.mixer.init()
    firing_sound = pygame.mixer.Sound('sounds/laser.wav')
    firing_sound.play()

def crash_sound():
    """Sounds for the crash."""
    pygame.mixer.init()
    crashing_sound = pygame.mixer.Sound('sounds/collision.wav')
    crashing_sound.play()

