import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''
        A class to manage bullets fired from the ship.
    '''

    def __init__(self, ai_game, character='ship'):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.character = character
        self.colour = self.settings.bullet_colour

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height)
        if self.character == 'alien_boss':
            self.rect.midtop = ai_game.alien_boss.rect.midbottom
        else:
            self.rect.midbottom = ai_game.ship.rect.midtop

        # Store the bullet position as a float
        self.y = float(self.rect.y)

    def update(self):
        '''
            Move the bullet up the screen.
        '''
        if self.character == 'alien_boss':
            self.y += self.settings.bullet_speed
            self.rect.y = self.y
        else:
            self.y -= self.settings.bullet_speed
            self.rect.y = self.y

    def draw_bullet(self):
        '''
            Draw the bullet to the screen.
        '''            
        if self.character == 'alien_boss':
            self.colour = self.settings.bullet_colour['alien_boss']
        else:
            self.colour = self.settings.bullet_colour['ship']

        pygame.draw.rect(self.screen, self.colour, self.rect)
