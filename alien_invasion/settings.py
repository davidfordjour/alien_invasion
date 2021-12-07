class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings."""
        self.screen_settings()      # Screen settings

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_settings()
        self.alien_bullet_settings()


        self.fleet_drop_speed = 1   # Fleet settings


        self.speedup_scale = 1.1    # How quickly the game speeds up

        self.score_scale = 1.5      # How quickly the alien point values increase

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2
        self.alien_bullet_speed_factor = 1

        self.alien_speed_factor = 0.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def bullet_settings(self):
        """Creates bullet settings."""
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = 60, 60, 60
        self.bullets_allowed = 3

    def screen_settings(self):
        """Creates screen settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

    def alien_bullet_settings(self):
        """Creates bullet settings."""
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_colour = 255, 0, 0
        self.alien_bullets_allowed = 1



