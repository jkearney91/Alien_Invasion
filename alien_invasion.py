import sys

import pygame

from settings import Settings
import settings
print(settings.__file__)
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """"Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode(
             (self.settings.screen_width, self.settings.screen_height,))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.firing = False
        self.last_shot_time = 0
        self.bullet_cooldown = 0.1  # seconds between bullets



    def run_game(self):
        """Start the main loop for the game."""
        while True:
            dt = self.clock.tick(60) / 1000  # seconds per frame
            self._check_events()
            self.ship.update(dt)
            self._update_screen()
            self.bullets.update()
            self._update_bullets()
            


           
    def _update_screen(self):
            # Update images on the screen, and flip to the new screen.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            pygame.display.flip()

    def _check_events(self):
         # Respond to keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
     """Respond to key presses."""
     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        self.ship.moving_right = True
     elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        self.ship.moving_left = True
     elif event.key == pygame.K_q:
         sys.exit()
     elif event.key == pygame.K_SPACE:
         if not self.firing:
             self.firing = True
             self._fire_bullet()
    
    def _check_keyup_events(self, event):
     """Respond to key releases."""
     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        self.ship.moving_right = False
     elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        self.ship.moving_left = False
     elif event.key == pygame.K_SPACE:
         self.firing = False
    
    def _fire_bullet(self):
        current_time = pygame.time.get_ticks() / 1000  # convert to seconds
        if current_time - self.last_shot_time >= self.bullet_cooldown:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.last_shot_time = current_time

    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update the bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
           

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()