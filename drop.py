import random

import pygame

class Drop:
    '''
        A class to represent game boosts.
    '''

    LABELS = {
        'x2 points': 'x2',
        'rapid fire': '>>',
        'extra ship': '+1'
    }

    def __init__(self, ai_game):

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Background image
        self.image = pygame.image.load('images/wooden_box1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.y = float(self.rect.y)

        self.active = False
        self.last_drop = pygame.time.get_ticks()

        # Font for the overlay text
        self.font = pygame.font.SysFont(None, 28)

        # Will be set when the drop spawn
        self.drop_type = None
        self.label_surface = None

    def _pick_type(self):
        '''
            Re-roll the drop type for a new spawn.
        '''

        self.drop_type = random.choice(self.settings.drop_types)
        label_text = self.LABELS.get(self.drop_type, '')
        return label_text

    def _render_drop_label(self):
        '''
            Pre-render drop label.
        '''
        label_text = self._pick_type()

        if label_text:
            base = self.font.render(label_text, True, (255, 255, 255))
            outline = self.font.render(label_text, True, (0, 0, 0, 0))

            surface = pygame.Surface(
                (base.get_width() + 2, base.get_height() + 2),
                pygame.SRCALPHA
            )

            surface.blit(outline, (0, 1))
            surface.blit(outline, (2, 1))
            surface.blit(outline, (1, 0))
            surface.blit(outline, (1, 2))
            surface.blit(base, (1, 1))
            self.label_surface = surface
        else:
            self.label_surface = None


    def update(self):
        '''
            Spawn a drop when ready and move it down the screen.
        '''
        current_time = pygame.time.get_ticks()

        if not self.active:
            if current_time - self.last_drop >= self.settings.drop_cooldown:
                self._render_drop_label()
                self.rect.x = random.randint(
                    0, self.settings.screen_width - self.rect.width
                )
                self.y = float(-self.rect.height)
                self.rect.y = self.y
                self.last_drop = current_time
                self.active = True
            return

        self.y += self.settings.drop_speed
        self.rect.y = self.y

        if self.rect.top >= self.settings.screen_height:
            self.active = False

    def reset(self):
        self.active = False
        self.last_drop = pygame.time.get_ticks()
        self.drop_type = None
        self.label_surface = None

    def blit_me(self):
        self.screen.blit(self.image, self.rect)
        if self.label_surface:
            label_rect = self.label_surface.get_rect(center=self.rect.center)
            self.screen.blit(self.label_surface, label_rect)


