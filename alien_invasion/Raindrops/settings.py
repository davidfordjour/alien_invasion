class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings."""
        self.screen_width = 1200    # Screen settings
        self.screen_height = 800
        self.bg_colour = (230,230,230)
        self.ship_speed_factor = 5    # Ship settings
        self.bullet_speed_factor = 10 # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = 60, 60, 60
        self.bullets_allowed = 3

        self.alien_speed_factor = 10  # Alien settings
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.reset_rain = 0     # Returns raindrop to the top of the screen