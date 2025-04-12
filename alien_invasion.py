import sys
import pygame
import random

from settings import Settings
import settings
print(settings.__file__)
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create stars: x, y, brightness, speed
        self.stars = []
        for _ in range(100):
            x = random.randint(0, self.settings.screen_width)
            y = random.randint(0, self.settings.screen_height)
            brightness = random.randint(300, 600)
            speed = random.uniform(1.0, 3.0)
            self.stars.append([x, y, brightness, speed])

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.firing = False
        self.last_shot_time = 0
        self.bullet_cooldown = 0.1
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            dt = self.clock.tick(60) / 1000
            self._check_events()
            self.ship.update(dt)
            self._update_screen()
            self.bullets.update()
            self._update_bullets()
            self._update_aliens()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _check_fleet_edges(self):
        """Respond correctly if any aliens have reached the edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleets direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        # Update and draw stars
        for star in self.stars:
            star[1] += star[3]  # Move star down
            if star[1] > self.settings.screen_height:
                star[1] = 0
                star[0] = random.randint(0, self.settings.screen_width)
            brightness = star[2] + random.randint(-10, 10)
            brightness = max(100, min(255, brightness))
            star[2] = brightness
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (star[0], int(star[1])), 1)

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw ship and aliens
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit() 
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.firing:
                self.firing = True
                self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.firing = False

    def _fire_bullet(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_shot_time >= self.bullet_cooldown:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.last_shot_time = current_time

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
         # Check for any bullets that have hit aliens.
         # If so, get rid of the bullet, and the alien.
            collisions = pygame.sprite.groupcollide(
             self.bullets, self.aliens, True, True)
    
    def _update_aliens(self):
        """Update positions of all the aliens."""
        self.aliens.update()
        self._check_fleet_edges()
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
