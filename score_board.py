import pygame.font
from pygame.sprite import Group

from ship import Ship 


class ScoreBoard:
    '''
        A class to report scoring information.
    '''
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font setting fo scoring information
        self.text_colour = ('white')
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_game_over()
        self.prep_alien_boss_health_bar()

    def prep_score(self):
        '''
            Turn the score into a rendered image.
        '''

        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_colour
        )

        # Display the score at the top of the screen

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''
            Turn the high score into a rendered image.
        '''

        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High score: {high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str,
            True,
            self.text_colour
        )

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self, game_over=False):
        '''
            Draw score to the screen.
        ''' 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

        if game_over:
            self.screen.blit(self.game_over_image, self.game_over_rect)

    def check_high_score(self):
        '''
            Check to see if thre is a new high score.
        '''

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        '''
            Turn the level into rendered image.
        '''

        level_str = f"Level: {str(self.stats.level)}"
        self.level_image = self.font.render(
            level_str,
            True,
            self.text_colour
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''
            Show how many ships are left.
        '''

        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, (40, 40))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_game_over(self):
        '''
            Display game over message.
        '''

        game_over_srt = "Game Over"
        game_over_font = pygame.font.SysFont(None, 72)
        self.game_over_image = game_over_font.render(
            game_over_srt,
            True,
            self.text_colour
        )
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen_rect.center
        self.game_over_rect.bottom = self.screen_rect.centery - 50

    def prep_alien_boss_health_bar(self):
        '''
            Prepare the health bar for the alien boss.
        '''
        boss_font = pygame.font.SysFont(None, 28)

        health_bar_x = (self.screen_rect.width - self.settings.health_bar_width) // 2
        health_bar_y = self.high_score_rect.midbottom[1] + 10  # Position the health bar below the boss
        
        self.health_bar_rect = pygame.Rect(
                    health_bar_x,
                    health_bar_y,
                    self.settings.health_bar_width,
                    self.settings.health_bar_height
        )

        max_health = self.ai_game.boss_max_hp
        current_health = max(0.0, self.ai_game.boss_hp)
        health_ratio = max(0.0, min(1.0, current_health / max_health))

        # Outer border
        pygame.draw.rect(self.screen,
                        self.settings.health_bar_border_colour,
                        self.health_bar_rect.inflate(4, 4),
                        border_radius=4)

        # Background
        pygame.draw.rect(self.screen,
                        self.settings.health_bar_bg_colour,
                        self.health_bar_rect,
                        border_radius=4)

        # Fill
        fill_width = int(self.health_bar_rect.width * health_ratio)
        fill_width = max(0, min(fill_width, self.health_bar_rect.width))
        if health_ratio > 0:
            fill_rect = pygame.Rect(self.health_bar_rect.x,
                                    self.health_bar_rect.y,
                                    fill_width,
                                    self.health_bar_rect.height)

            colour = (
                self.settings.health_bar_fill_low_colour if health_ratio < 0.3
                else self.settings.health_bar_fill_colour
            )
            pygame.draw.rect(self.screen, colour, fill_rect, border_radius=3)

        # HP centered on top of the bar
        hp_text = f"BOSS: {int(current_health)}/{int(max_health)}"
        text_surf = boss_font.render(hp_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.health_bar_rect.center)
        self.screen.blit(text_surf, text_rect)