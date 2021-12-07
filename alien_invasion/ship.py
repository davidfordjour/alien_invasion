import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialise the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.ship_loader(screen)

        self.ship_positioner()      # Starts each new ship at the bottom of screen.

        self.directions()       # Movement flag

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.centerx    # Update rect oject from self.center.
        self.rect.centery = self.centery


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

    def ship_loader(self, screen):
        """Load the ship and its rect"""
        self.image = pygame.image.load('images/ship.bmp')  # Load the ship and its rect.
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def ship_positioner(self):
        """Starts each new ship at a designated position"""
        self.rect.centerx = self.screen_rect.centerx  # Start each new ship at the bottom of the screen.
        self.rect.bottom = self.screen_rect.bottom

        self.centerx = float(self.rect.centerx)  # Store a decimal value for the ship's center
        self.centery = float(self.rect.centery)

    def directions(self):
        """Contains the directions that the ship can move in."""
        self.moving_right = False  # Movement flag
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False