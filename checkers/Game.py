import sys
sys.path.append("..")

import pygame
from .Board import Board
from minimax.Minimax import MiniMax

class Game:

    def __init__(self, p1, p2, screen, p1_depth=1, p2_depth=1):

        self.player1 = p1
        self.player2 = p2

        if self.player1 == "human":
            print("Player 1 (human) chooses white piece.")
        elif self.player1 == "minimax":
            if p1_depth <= 0: p1_depth = 1
            print(f"Player 1 (minimax) chooses white piece with depth {p1_depth}.")
            self.minimax1 = MiniMax(p1_depth)
        else:
            raise NotImplementedError

        if self.player2 == "human":
            print("Player 2 (human) chooses black piece.")
        elif self.player2 == "minimax":
            if p2_depth <= 0: p2_depth = 1
            print(f"Player 2 (minimax) chooses black piece with depth {p2_depth}.")
            self.minimax2 = MiniMax(p2_depth)
        else:
            raise NotImplementedError

        self.SCREEN = screen
        self.board = Board()
        self.player_turn = 1  # white always start first
        self.ai_turn = False
        self.running = True
        self.mode = 0
        self.mouse_clicked = False
        self.mouse_x = self.mouse_y = None

    def update(self):
        '''
            Game Modes
            0 - Check Mode
            1 - Selection Mode
            2 - Active Mode
            3 - End Mode
        '''
        # Mode 0 - Find all the valid pieces of current player
        if self.mode == 0:
            # if there are moves available, change the mode to 1
            if self.board.find_valid_pieces(self.player_turn):
                self.mode = 1

        # after mode 0, 
        # self.board.valid_pieces contains all the valid moves
        # for the current player

        # Now, decide who will play (HUMAN or AI)

        # if white turn
        if self.player_turn == 1:
            # check it is human or ai, if it is ai
            if self.player1 == "minimax":
                # set ai turn to be true
                self.ai_turn = True

        # if black turn
        else:
            # check it is human or ai, if it is ai
            if self.player2 == "minimax":
                # set ai turn to be true
                self.ai_turn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # human move
            if event.type == pygame.MOUSEBUTTONDOWN and not self.ai_turn:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                self.mouse_clicked = True

        # ai move
        if self.ai_turn:
            # self.board is passed into move function of minimax
            # as a pass-by-reference
            if self.player_turn == 1:
                self.minimax1.move(self.board, self.player_turn)
            else:
                self.minimax2.move(self.board, self.player_turn)
            self.board.valid_pieces = []
            self.ai_turn = False
            self.player_turn = -1 * self.player_turn
            self.mode = 0
        
        if self.mouse_clicked:
            if self.mode == 1:
                if self.board.selection_mode(self.mouse_x, self.mouse_y, self.player_turn):
                    self.mode = 2

            if self.mode == 2:
                self.board.valid_pieces = []
                if self.board.find_valid_moves(self.player_turn):
                    self.mode = 3
                    self.mouse_clicked = False
                else:
                    self.mode = 0

            elif self.mode == 3:
                if self.board.move_piece(self.mouse_x, self.mouse_y, self.player_turn):
                    self.player_turn = -1 * self.player_turn

                self.mode = 0
                self.mouse_clicked = False

        if self.board.winner_status is not None:
            if self.board.winner_status == 0:
                print("Draw.")
            else:
                print(
                    f"Congratulations! Player {self.board.winner_status} wins.")

            self.running = False
            # self.__init__(self.SCREEN)
            # self.update()

    def render(self):

        # Fill the background with white
        self.SCREEN.fill((0, 0, 0))

        # Render board
        self.board.render(self.SCREEN, self.player_turn)

        # Update the display
        pygame.display.update()
