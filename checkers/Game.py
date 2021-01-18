import pygame
from .Board import Board


class Game:

    def __init__(self, p1, p2, screen):

        self.player1 = p1
        self.player2 = p2

        if not (self.player1 == "human" and self.player2 == "human"):
            raise NotImplementedError

        self.SCREEN = screen
        self.board = Board()
        self.player_turn = 1  # white always start first
        self.running = True
        self.mode = 0

    def update(self):
        '''
            Game Modes
            0 - Check Mode
            1 - Selection Mode
            2 - Active Mode
            3 - End Mode
        '''
        if self.board.winner_status is not None:
            if self.board.winner_status == 0:
                print("Draw.")
            else:
                print(
                    f"Congratulations! Player {self.board.winner_status} wins.")

            self.__init__(self.SCREEN)
            self.update()

        # Mode 0 - Find all the valid pieces of current player
        if self.mode == 0:
            # if there are moves available, change the mode to 1
            if self.board.find_valid_pieces(self.player_turn):
                self.mode = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if self.mode == 1:
                    if self.board.selection_mode(mouse_x, mouse_y,
                                                 self.player_turn):
                        self.mode = 2

                if self.mode == 2:
                    self.board.valid_pieces = []
                    if self.board.find_valid_moves(self.player_turn):
                        self.mode = 3
                    else:
                        self.mode = 0

                elif self.mode == 3:
                    if self.board.move_piece(mouse_x, mouse_y,
                                             self.player_turn):
                        self.player_turn = -1 * self.player_turn

                    self.mode = 0

    def render(self):

        # Fill the background with white
        self.SCREEN.fill((0, 0, 0))

        # Render board
        self.board.render(self.SCREEN, self.player_turn)

        # Update the display
        pygame.display.update()
