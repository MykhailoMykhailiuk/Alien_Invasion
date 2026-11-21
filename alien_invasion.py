import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien, AlienBoss
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard
from drop import Drop


class AlienInvasion:
    '''
        Overall class to manage game behaviour and assets.
    '''

    def __init__(self):
        '''
            Initialize the game and create game resources.
        '''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.boss_max_hp = self.settings.boss_hp
        self.boss_hp = self.boss_max_hp
        
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))

        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.score_board = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_boss = AlienBoss(self)
        self.drop = Drop(self)
        
        self._create_fleet()

        # Set the background colour.
        self.bg_colour = pygame.image.load('images/background.jpg').convert()

        self.game_active = False
        self.play_button = Button(self, "Play")

    def _check_play_button(self, mouse_pos):
        '''
            Start a new game when the player clicks Play.
        '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game stats.
            self.settings.initialize_dynamic_settings()
            self.boss_max_hp = self.settings.boss_hp
            self.boss_hp = self.boss_max_hp
            self.stats.reset_stats()
            self.score_board.prep_score()
            self.score_board.prep_high_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()
            self.game_active = True
            self.drop.reset()

            self.bullets.empty()
            self.boss_bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_events(self):
        '''
            Respond to keypresses and mouse events.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_score()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_keydown_event(self, event):
        '''
            Respondes to keypresses.
        '''
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        '''
            Respond to key releases.
        '''
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''
            Create a new bullet and add it to the bullets group.
        '''
        if len(self.bullets) < self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_boss_bullet(self):
        '''
            Create a new bullet an add it to the boss_bullets group.
        '''

        new_bullet = Bullet(self, character='alien_boss')
        self.boss_bullets.add(new_bullet)

    def _check_boss_cooldown(self):
        '''
            Check if the alien boss can shoot.
        '''
        current_time = pygame.time.get_ticks()

        if current_time - self.alien_boss.last_shot_time >= self.alien_boss.shoot_cooldown:
            self._fire_boss_bullet()
            self.alien_boss.last_shot_time = current_time

    def _update_bullets(self):
        '''
            Update position of bullets and get rid of old bullets.
        '''
        self.bullets.update()
        self.boss_bullets.update()

        # Remove the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for bullet in self.boss_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.boss_bullets.remove(bullet)

        if self._check_level():
            self._check_boss_cooldown()
            self._check_bullet_boss_collision()
            self._check_bullet_ship_collision()
        else:
            self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        '''
            Respond to bullet-alien collision.
        '''
        # Remove any bullets and aliens that have collided.

        collisions = pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens) * self.stats.score_multiplier
            self.score_board.prep_score()
            self.score_board.check_high_score()

        # If all aliens destroyed, create a new fleet of aliens. 
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.score_board.prep_level()

    def _check_bullet_boss_collision(self):
        '''
            Respond to bullet-alien boss collision.
        '''

        collisions = pygame.sprite.spritecollide(
            self.alien_boss,
            self.bullets,
            True
        )

        if collisions:
            self.boss_hp -= self.settings.boss_hp * 0.05 * len(collisions) * self.stats.score_multiplier

        if self.boss_hp <= 0:
            self.stats.score += self.settings.boss_hp
            self.score_board.prep_score()
            self.score_board.check_high_score()
            self.bullets.empty()
            self.boss_bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.stats.level += 1
            self.score_board.prep_level()
            # Scale the next boss
            self.boss_max_hp += self.settings.boss_hp_increase
            self.boss_hp = self.boss_max_hp

    def _check_bullet_ship_collision(self):
        '''
            Respond to bullet-ship collision.
        '''

        collisions = pygame.sprite.spritecollide(
            self.ship,
            self.boss_bullets,
            True
        )

        if collisions:
            self._ship_hit()

    def _check_drop_ship_collision(self):
        '''
            Respond to drop-ship collision.
        '''

        if self.ship.rect.colliderect(self.drop.rect):
            self._apply_drop_effects(self.drop.drop_type)
            self.drop.reset()

    def _apply_drop_effects(self, drop_type):
        '''
            Applies the drop effects.
        '''
        if drop_type == 'x2 points':
            self.stats.score_multiplier = 2
            self.stats.score_multiplier_until = pygame.time.get_ticks() + 10_000
            self.score_board.prep_score()
            self.score_board.check_high_score()
        elif drop_type == 'rapid fire':
            self.settings.bullet_limit = min(
                self.settings.bullet_limit + 5,
                self.settings.bullet_limit_max
            )
        elif drop_type == 'extra ship':
            self.stats.ship_left += 1
            self.score_board.prep_ships()

    def _remove_rapid_fire_effect(self):
        '''
            Remove one level of rapid fire after the ship is hit.
        '''
        self.settings.bullet_limit = max(
            self.settings.bullet_limit - 5,
            self.settings.bullet_limit_min
        )

    def _create_alien(self, x_position, y_position):
        '''
            Create an alien and place it in the row.
        '''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        '''
            Respond appropriately if any aliens have reached an edge. 
        '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''
            Drop the entire fleet and change the fleet direction.
        '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        '''
            Create the fleet of aliens.
        '''
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width ans one alien height. 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _ship_hit(self):
        '''
            Respond to the ship been hit by an alien.
        '''

        if self.stats.ship_left > 0:
            self._remove_rapid_fire_effect()

            # Decrement ship_left
            self.stats.ship_left -= 1
            self.score_board.prep_ships()

            # Get rid of any remaining buletsand aliens
            self.bullets.empty()
            self.boss_bullets.empty()
            if not self._check_level():
                self.aliens.empty()

                # Create a new fleet and center the ship
                self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        '''
            Update the position of all aliens in the fleet.
        '''
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        '''
            Check if any alien reache the bottom of the screen.
        '''

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_screen(self):
        '''
            Update images on the screen, and flip the new screen.
        '''
        self.screen.blit(self.bg_colour, (0,0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.boss_bullets.sprites():
            bullet.draw_bullet()
        self.ship.blit_me()

        if self.game_active and self.drop.active:
            self.drop.blit_me()
            self._check_drop_ship_collision()

        if self._check_level():
            self.alien_boss.blit_me()
            self.score_board.prep_alien_boss_health_bar()
        else:
            self.aliens.draw(self.screen)

        game_over = not self.game_active and self.stats.ship_left == 0
        self.score_board.show_score(game_over=game_over)

        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_level(self):
        return self.stats.level % 5 == 0

    def run_game(self):
        '''
            Start the main loop for the game.
        '''
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self.drop.update()
                if pygame.time.get_ticks() >= self.stats.score_multiplier_until:
                    self.stats.score_multiplier = 1
                if self._check_level():
                    self.alien_boss.update()
                else:
                    self._update_aliens()
                

            self._update_screen()
            self.clock.tick(60)


if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()