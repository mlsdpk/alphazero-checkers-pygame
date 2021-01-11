import pygame
import numpy as np
from .Piece import Piece


class Board:

    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.grid_size = self.width / 8
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GREY': (150, 150, 150),
            'GREEN': (0, 255, 0),
            'LGREEN': (144, 238, 144),
            'YELLOW': (255, 255, 0)
        }

        self.init_grid()
        self.valid_pieces = []
        self.selected_piece = None
        self.piece_set = None
        self.piece_free_grids = None
        self.capture_pieces = None

    def init_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and
                                                       col % 2 == 0):
                    self.grid[row][col] = Piece(
                        row, col,
                        1) if row < 3 else Piece(row, col, -1) if row > 4 else 0

    def selection_mode(self, mouse_x, mouse_y, player_turn):

        selected_row, selected_col = int(mouse_y // self.grid_size), int(
            mouse_x // self.grid_size)

        if (selected_row, selected_col) in self.valid_pieces:
            self.grid[selected_row][selected_col].selected = True
            self.selected_piece = (selected_row, selected_col)
            return True

    def find_valid_pieces(self, player_turn):
        force_captures = []
        free_moves = []

        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if not isinstance(self.grid[row][col], Piece):
                    continue
                if self.grid[row][col].player != player_turn:
                    continue

                left_grid_row, left_grid_col = row + player_turn, col - 1
                right_grid_row, right_grid_col = row + player_turn, col + 1

                Left = False
                Right = False
                if left_grid_row >= 0 and left_grid_row <= 7 and left_grid_col >= 0 and left_grid_col <= 7:
                    if self.grid[left_grid_row][left_grid_col] == 0:
                        Left = True

                if right_grid_row >= 0 and right_grid_row <= 7 and right_grid_col >= 0 and right_grid_col <= 7:
                    if self.grid[right_grid_row][right_grid_col] == 0:
                        Right = True

                if Left and Right:
                    free_moves.append((row, col))
                    continue
                elif Left or Right:
                    free_moves.append((row, col))

                self.find_valid_moves(player_turn, row, col)
                self.grid[row][col].valid_grids = []

                if len(self.capture_pieces) > 0:
                    force_captures.append((row, col))

        self.valid_pieces = force_captures if (
            len(force_captures) > 0) else free_moves
        return (len(self.valid_pieces) > 0)

    def find_valid_moves(self, player_turn, row=None, col=None):

        curr_row, curr_col = (
            row,
            col) if row is not None and col is not None else self.selected_piece

        # set is used here to avoid addition of same piece multiple times
        self.piece_set = {(curr_row, curr_col)}
        self.piece_free_grids = []

        # dict - {(after_captured_grid): [(capture_piece), (parent_grid)]}
        self.capture_pieces = {}

        # recursively find valid moves
        self.find_valid_moves_recursive(player_turn)

        self.grid[curr_row][curr_col].valid_grids = [
            *self.capture_pieces
        ] if len(self.capture_pieces) > 0 else self.piece_free_grids

        if len(self.grid[curr_row][curr_col].valid_grids) > 0:
            return True
        elif self.selected_piece is not None:
            self.grid[self.selected_piece[0]][
                self.selected_piece[1]].selected = False
            self.selected_piece = None
            return False

        return False

    def find_valid_moves_recursive(self, player_turn):
        # base case
        if len(self.piece_set) == 0:
            return True
        else:
            # takeout random piece from set
            curr_row, curr_col = self.piece_set.pop()

            # find corner piece locations of that piece
            left_grid_row, left_grid_col = curr_row + player_turn, curr_col - 1
            right_grid_row, right_grid_col = curr_row + player_turn, curr_col + 1

            # check to make sure between boundaries (left)
            if self.is_between_boundaries(left_grid_row, left_grid_col):
                # if it is free space, add to valid positions
                if self.is_free_space(left_grid_row, left_grid_col):
                    self.piece_free_grids.append((left_grid_row, left_grid_col))
                else:
                    # else, only explore further if it's opponent piece
                    if not self.is_same_player(left_grid_row, left_grid_col,
                                               player_turn):
                        # find new left piece
                        new_left_grid_row, new_left_grid_col = left_grid_row + player_turn, left_grid_col - 1

                        # check to make sure between boundaries (new left)
                        if self.is_between_boundaries(new_left_grid_row,
                                                      new_left_grid_col):
                            # if another grid is free, we can move to there
                            if self.is_free_space(new_left_grid_row,
                                                  new_left_grid_col):
                                # append new grid as moved location (key) and store capture piece and parent (value)
                                self.capture_pieces[(new_left_grid_row,
                                                     new_left_grid_col)] = [
                                                         (left_grid_row,
                                                          left_grid_col),
                                                         (curr_row, curr_col)
                                                     ]
                                # append new piece to piece set for further exploration
                                self.piece_set.add(
                                    (new_left_grid_row, new_left_grid_col))

            # check to make sure between boundaries (right)
            if self.is_between_boundaries(right_grid_row, right_grid_col):
                # if it is free space, add to valid positions
                if self.is_free_space(right_grid_row, right_grid_col):
                    self.piece_free_grids.append(
                        (right_grid_row, right_grid_col))
                else:
                    # else, only explore further if it's opponent piece
                    if not self.is_same_player(right_grid_row, right_grid_col,
                                               player_turn):
                        # find new left piece
                        new_right_grid_row, new_right_grid_col = right_grid_row + player_turn, right_grid_col + 1

                        # check to make sure between boundaries (new right)
                        if self.is_between_boundaries(new_right_grid_row,
                                                      new_right_grid_col):
                            # if another piece is free
                            if self.is_free_space(new_right_grid_row,
                                                  new_right_grid_col):
                                # append new grid as moved location (key) and store capture piece and parent (value)
                                self.capture_pieces[(new_right_grid_row,
                                                     new_right_grid_col)] = [
                                                         (right_grid_row,
                                                          right_grid_col),
                                                         (curr_row, curr_col)
                                                     ]
                                # append new piece to piece set for further exploration
                                self.piece_set.add(
                                    (new_right_grid_row, new_right_grid_col))

            return self.find_valid_moves_recursive(player_turn)

    def is_between_boundaries(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7

    def is_free_space(self, row, col):
        return self.grid[row][col] == 0

    def is_same_player(self, row, col, player_turn):
        return self.grid[row][col].player == player_turn

    def move_piece(self, mouse_x, mouse_y):

        selected_row, selected_col = int(mouse_y // self.grid_size), int(
            mouse_x // self.grid_size)

        # if row,col is outside of board
        if not self.is_between_boundaries(selected_row, selected_col):
            return False

        if (selected_row, selected_col) in self.grid[self.selected_piece[0]][
                self.selected_piece[1]].valid_grids:

            self.grid[self.selected_piece[0]][
                self.selected_piece[1]].valid_grids = []
            self.grid[self.selected_piece[0]][
                self.selected_piece[1]].selected = False
            self.grid[selected_row][selected_col] = self.grid[
                self.selected_piece[0]][self.selected_piece[1]]
            self.grid[self.selected_piece[0]][self.selected_piece[1]] = 0

            while (selected_row, selected_col) in self.capture_pieces:

                capture_piece = self.capture_pieces[(selected_row,
                                                     selected_col)][0]
                self.grid[capture_piece[0]][capture_piece[1]] = 0

                selected_row, selected_col = self.capture_pieces[(
                    selected_row, selected_col)][1]

            self.selected_piece = None
            return True

        else:
            self.grid[self.selected_piece[0]][
                self.selected_piece[1]].valid_grids = []
            self.grid[self.selected_piece[0]][
                self.selected_piece[1]].selected = False
            self.selected_piece = None
            return False

    # rendering stuffs
    def render(self, screen, player_turn):

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):

                if row % 2 == 0:
                    color = self.colors[
                        'WHITE'] if col % 2 == 0 else self.colors['GREY']
                else:
                    color = self.colors[
                        'GREY'] if col % 2 == 0 else self.colors['WHITE']

                pygame.draw.rect(screen, color,
                                 (col * self.grid_size, row * self.grid_size,
                                  self.grid_size, self.grid_size))

                if self.grid[row][col] != 0:

                    if self.grid[row][col].player == 1:
                        color = self.colors['WHITE']
                    elif self.grid[row][col].player == -1:
                        color = self.colors['BLACK']

                    pygame.draw.circle(
                        screen, color,
                        (col * self.grid_size + self.grid_size / 2,
                         row * self.grid_size + self.grid_size / 2),
                        self.grid_size / 3)

        if self.selected_piece is not None:
            pygame.draw.rect(screen, self.colors['LGREEN'],
                             (self.selected_piece[1] * self.grid_size,
                              self.selected_piece[0] * self.grid_size,
                              self.grid_size, self.grid_size))

            pygame.draw.circle(
                screen, self.colors['WHITE']
                if player_turn == 1 else self.colors['BLACK'],
                (self.selected_piece[1] * self.grid_size + self.grid_size / 2,
                 self.selected_piece[0] * self.grid_size + self.grid_size / 2),
                self.grid_size / 3)

            for x, y in self.grid[self.selected_piece[0]][
                    self.selected_piece[1]].valid_grids:
                pygame.draw.rect(screen, self.colors['LGREEN'],
                                 (y * self.grid_size, x * self.grid_size,
                                  self.grid_size, self.grid_size))

        if len(self.valid_pieces) > 0:
            for r, c in self.valid_pieces:
                pygame.draw.rect(screen, self.colors['YELLOW'],
                                 (c * self.grid_size, r * self.grid_size,
                                  self.grid_size, self.grid_size))

                pygame.draw.circle(
                    screen, self.colors['WHITE']
                    if player_turn == 1 else self.colors['BLACK'],
                    (c * self.grid_size + self.grid_size / 2,
                     r * self.grid_size + self.grid_size / 2),
                    self.grid_size / 3)
