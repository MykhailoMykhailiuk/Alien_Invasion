class GameStats:
    '''
        Track statistic for Alien Invasion.
    '''

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        self.high_score = self.load_score()

    def reset_stats(self):
        '''
            Initialize statistics that can change during the game.
        '''

        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.score_multiplier = 1
        self.score_multiplier_until = 0

    def save_score(self):
        '''
            Save the high score to the file.
        '''
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def load_score(self):
        '''
            Load the high score form the file.
        '''

        try:
            with open('high_score.txt', 'r') as file:
                high_score = int(file.read())
                self.high_score = high_score
        except FileNotFoundError:
            self.high_score = 0

        return self.high_score
        