import pygame
from .Board import Board


class Game:

    def __init__(self, screen):
        self.SCREEN = screen
        self.running = True

        self.board = Board()
        '''
            Game Modes
            0 - Check Mode
            1 - Selection Mode
            2 - Active Mode
            3 - End Mode
        '''
        self.mode = 0
        self.player_turn = 1

    def update(self):
        if self.mode == 0:
            print('Entering Mode 0')
            if self.board.find_valid_pieces(self.player_turn):
                self.mode = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if self.mode == 1:
                    print("Entering Mode 1")
                    if self.board.selection_mode(mouse_x, mouse_y,
                                                 self.player_turn):
                        self.mode = 2

                if self.mode == 2:
                    print("Entering Mode 2")
                    self.board.valid_pieces = []
                    if self.board.find_valid_moves(self.player_turn):
                        self.mode = 3
                    else:
                        self.mode = 0

                elif self.mode == 3:
                    print("Entering Mode 3")
                    if self.board.move_piece(mouse_x, mouse_y):
                        self.mode = 0
                        self.player_turn = -1 * self.player_turn
                    else:
                        self.mode = 0

    def render(self):

        # Fill the background with white
        self.SCREEN.fill((0, 0, 0))

        # Render board
        self.board.render(self.SCREEN, self.player_turn)

        # Update the display
        pygame.display.update()
