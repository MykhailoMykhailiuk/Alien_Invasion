import pygame.font

class Button:
    '''
        A class to build buttons for the game.
    '''

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties for the button
        self.width, self.height = 160, 30
        self.text_colour = ('linen')
        self.font = pygame.font.SysFont(None, 48)

        # Build the button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepared only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''
            Turn message into rendered image and center text on the button.
        '''
        self.msg_image = self.font.render(
            msg,
            True,
            self.text_colour
        )

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''
            Draw blank button and then draw the message.
        '''
    
        self.screen.blit(self.msg_image, self.msg_image_rect)