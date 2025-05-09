class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
       
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (5, 5, 30)

        # Ship settings.
        self.ship_speed = 25
        self.ship_limit = 3
        
        #Bullet settings.
        self.bullet_speed = 15.0
        self.bullet_width = 7
        self.bullet_height = 20
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_speed = 3.0
        self.fleet_drop_speed = 10

        # Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1