class Settings:
    '''
        A class to stiore all settings for the game.
    '''

    def __init__(self):
        '''
            Initialize the game settings.
        '''

        self.screen_width = 1200
        self.screen_height = 900

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_colour = {
            'ship': ('green'),
            'alien_boss': ('red')
        }
        self.bullet_limit = 5
        self.bullet_limit_min = 5
        self.bullet_limit_max = 20
        self.bullet_speed = 2.5

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien points increase
        self.score_scale = 2

        self.boss_hp = 500
        self.boss_hp_increase = 500

        # Boss health bar settings
        self.health_bar_width = 400
        self.health_bar_height = 20
        self.health_bar_bg_colour = (60, 60, 60)
        self.health_bar_border_colour = (255, 255, 255)
        self.health_bar_fill_colour = (220, 40, 40)
        self.health_bar_fill_low_colour = (255, 180, 0)   # when HP is low

        # Drop settings
        self.drop_speed = 2
        self.drop_cooldown = 20_000
        self.drop_types = ['x2 points', 'rapid fire', 'extra ship']

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''
            Initialize setting that change throughout the game.
        '''
        self.bullet_limit = self.bullet_limit_min
        self.ship_speed = 2
        self.alien_speed = 0.5
        self.alien_points = 10
        self.boss_speed = 1.0

        # Fleet directions of 1 represent right; -1 reperesent left
        self.fleet_direction = 1

    def increase_speed(self):
        '''
            Increase speed settings.
        '''
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
