class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
       
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (222, 222, 222)

        # Ship settings.
        self.ship_speed = 25
        
        #Bullet settings.
        self.bullet_speed = 15.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 220)
        self.bullets_allowed = 3