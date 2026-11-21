import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''
        A class to represent a single alien in the fleet.
    '''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        self.image = pygame.image.load('images/alien.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        '''
            Return True if the alien is at the adge of the screen.
        '''
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        '''
            Move the alin to the right.
        '''

        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


class AlienBoss(Alien):
    '''
        A class to represent the alien boss.
    '''

    def __init__(self, ai_game):
        super().__init__(ai_game)

        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/REDBOSS.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midtop
        self.rect.centery = self.screen_rect.top + 170

        self.x = float(self.rect.x)
        self.direction = 1

        self.shoot_cooldown = 4000  # Cooldown time in milliseconds
        self.last_shot_time = pygame.time.get_ticks()  # Time of the last shot

        self.boss_health = self.settings.boss_hp

    def blit_me(self):
        '''
            Draw the alien boss to the screen.
        '''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''
            Move the alien boss.
        '''

        if self.check_edges():
            self.direction *= -1

        self.x += self.settings.boss_speed * self.direction
        self.rect.x = self.x

    def check_edges(self):
        '''
            Return True if the alien is at the adge of the screen.
        '''
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


        

       