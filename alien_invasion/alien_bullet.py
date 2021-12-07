import pygame
from pygame.sprite import Sprite



class AlienBullet(Sprite):
    """A class to manage bullets fired from random Aliens in the fleet."""

    def __init__(self, ai_settings, screen, alien, aliens):
        """Create a bullet object at a random Alien's current position."""
        super(AlienBullet, self).__init__()
        self.screen = screen


        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width,
                                ai_settings.alien_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom

        self.y = float(self.rect.y) # Store the bullet's position as a decimal value.

        self.colour = ai_settings.alien_bullet_colour
        self.speed_factor = ai_settings.alien_bullet_speed_factor


    def update(self):
        """Move the bullet down the screen."""
        self.y += self.speed_factor     # Update the decimal position of the bullet.
        self.rect.y = self.y        # Update the rect position.


    def draw_alien_bullet(self):
        """Draw the alien bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)













