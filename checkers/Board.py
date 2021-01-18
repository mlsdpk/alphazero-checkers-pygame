import pygame
import numpy as np
from .Piece import Piece
from collections import deque


class Board:

    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.grid_size = self.width / 8
        self.grid = [[0 for i in range(8)] for j in range(8)]

        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'BLUE': (0, 0, 255),
            'GREY': (150, 150, 150),
            'GREEN': (0, 255, 0),
            'LGREEN': (144, 238, 144),
            'YELLOW': (255, 255, 0),
            'RED': (255, 0, 0)
        }

        self.init_grid()
        self.valid_pieces = []
        self.selected_piece = None
        self.piece_set = None
        self.piece_free_grids = None
        self.capture_pieces = None
        self.no_capture_pieces_count = 0
        self.king_side = np.array([0, 0])
        self.grid_buffer = deque()
        self.winner_status = None

    def init_grid(self):
        """Initialize(Reset) Grid Board
        """
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

                if self.grid[row][col].status == 'king':
                    lft_row_front, lft_col_front = row + player_turn, col - 1
                    lft_row_back, lft_col_back = row + (player_turn *
                                                        (-1)), col - 1

                    rgt_row_front, rgt_col_front = row + player_turn, col + 1
                    rgt_row_back, rgt_col_back = row + (player_turn *
                                                        (-1)), col + 1

                    front_left_empty = False
                    back_left_empty = False
                    front_right_empty = False
                    back_right_empty = False

                    # ----- defining the conditions for grid emptiness -----------
                    if self.is_between_boundaries(lft_row_front, lft_col_front):
                        if self.grid[lft_row_front][lft_col_front] == 0:
                            front_left_empty = True

                    if self.is_between_boundaries(lft_row_back, lft_col_back):
                        if self.grid[lft_row_back][lft_col_back] == 0:
                            back_left_empty = True

                    if self.is_between_boundaries(rgt_row_front, rgt_col_front):
                        if self.grid[rgt_row_front][rgt_col_front] == 0:
                            front_right_empty = True

                    if self.is_between_boundaries(rgt_row_back, rgt_col_back):
                        if self.grid[rgt_row_back][rgt_col_back] == 0:
                            back_right_empty = True
                    # ----------------------------------------------------

                    # check if the corner grids are empty
                    if front_left_empty and back_left_empty and front_right_empty and back_right_empty:
                        free_moves.append((row, col))
                        continue
                    elif front_left_empty or back_left_empty or front_right_empty or back_right_empty:
                        free_moves.append((row, col))

                    self.find_valid_moves(player_turn, row, col)

                    self.grid[row][col].valid_grids = []

                    if len(self.capture_pieces) > 0:
                        force_captures.append((row, col))

                elif self.grid[row][col].status == 'man':
                    left_grid_row, left_grid_col = row + player_turn, col - 1
                    right_grid_row, right_grid_col = row + player_turn, col + 1

                    left_grid_empty = False
                    right_grid_empty = False

                    if self.is_between_boundaries(left_grid_row, left_grid_col):
                        if self.grid[left_grid_row][left_grid_col] == 0:
                            left_grid_empty = True

                    if self.is_between_boundaries(right_grid_row,
                                                  right_grid_col):
                        if self.grid[right_grid_row][right_grid_col] == 0:
                            right_grid_empty = True

                    if left_grid_empty and right_grid_empty:
                        free_moves.append((row, col))
                        continue
                    elif left_grid_empty or right_grid_empty:
                        free_moves.append((row, col))

                    self.find_valid_moves(player_turn, row, col)
                    self.grid[row][col].valid_grids = []

                    if len(self.capture_pieces) > 0:
                        force_captures.append((row, col))

        self.valid_pieces = force_captures if (
            len(force_captures) > 0) else free_moves

        # decide win/loss/draw conditions
        if not (len(self.valid_pieces) > 0):
            self.winner_status = -1 * player_turn
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

        # recursively find valid moves of kings and men
        player_status = self.grid[curr_row][curr_col].status
        self.validate_grids_recursively(player_turn, player_status)

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

    def validate_single_corner_grid(self, selected_row, selected_col,
                                    corner_row, corner_col, grid_dir,
                                    player_turn, player_status):
        """ The function does three things:

                - checks if a grid is empty, if empty, store that position
                  to "self.piece_free_grids"
                - if its not empty, checks if there is an own piece or enemy
                  piece in the grid
                - if enemy piece, it looks for one more grid diagonally
                - if that grid is empty, store the empty piece position,
                  update the "self.caputure_pieces" accordingly.

                l - left, f - front, b - back, r - right

                Attributes which are mutated by this method:
                    self.piece_set, self.capture_pieces, self.piece_free_grids

        Args:
            param1: The selected (parent) piece row
            param2: The selected piece col
            param3: The row of a grid we want to validate, at the corner of the selected piece
            param4: The col of a grid we want to validate, at the corner of the selected piece
            param5: The direction of the corner grid from the selected piece.
            param6: The turn of the player (1 or -1)
            param7: The status of the player (king or man)

        Returns:
            This function returns None but mutates some instance attributes as stated above.

        """
        if self.is_between_boundaries(corner_row, corner_col):
            # if it is free space, add to valid positions
            if self.is_free_space(corner_row, corner_col):
                self.piece_free_grids.append((corner_row, corner_col))
            else:
                # else, only explore further if it's opponent piece
                if not self.is_same_player(corner_row, corner_col, player_turn):
                    # find new piece
                    if grid_dir == 'lf':
                        new_corner_row, new_corner_col = corner_row + player_turn, corner_col - 1
                    elif grid_dir == 'lb':
                        new_corner_row, new_corner_col = corner_row + (
                            -1 * player_turn), corner_col - 1
                    elif grid_dir == 'rf':
                        new_corner_row, new_corner_col = corner_row + player_turn, corner_col + 1
                    elif grid_dir == 'rb':
                        new_corner_row, new_corner_col = corner_row + (
                            -1 * player_turn), corner_col + 1

                    # check to make sure between boundaries
                    if self.is_between_boundaries(new_corner_row,
                                                  new_corner_col):
                        # if another grid is free, we can move to there
                        if self.is_free_space(new_corner_row, new_corner_col):
                            if player_status == 'king':
                                if (new_corner_row, new_corner_col
                                   ) not in self.capture_pieces:
                                    # append new grid as moved location (key) and store capture piece and parent (value)
                                    self.capture_pieces[(new_corner_row,
                                                         new_corner_col)] = [
                                                             (corner_row,
                                                              corner_col),
                                                             (selected_row,
                                                              selected_col)
                                                         ]
                                    # append new piece to piece set for further exploration
                                    self.piece_set.add(
                                        (new_corner_row, new_corner_col))
                            elif player_status == 'man':
                                self.capture_pieces[(new_corner_row,
                                                     new_corner_col)] = [
                                                         (corner_row,
                                                          corner_col),
                                                         (selected_row,
                                                          selected_col)
                                                     ]
                                # append new piece to piece set for further exploration
                                self.piece_set.add(
                                    (new_corner_row, new_corner_col))

    def validate_grids_recursively(self, player_turn, player_status):
        """ Find the valid moves at the corner grids of both man and king pieces.

        Args:
            param1: The turn of the player
            param2: The status of the player - "king" or "man"

        Returns:
            This function returns itself.

        """
        # base case
        if len(self.piece_set) == 0:
            return True
        else:

            if player_status == 'man':
                # takeout random piece from set
                curr_row, curr_col = self.piece_set.pop()

                # find two corner piece at front of man piece
                left_grid_row, left_grid_col = curr_row + player_turn, curr_col - 1
                right_grid_row, right_grid_col = curr_row + player_turn, curr_col + 1

                # validating two grids in front of a "man" piece
                grids_m = [(left_grid_row, left_grid_col),
                           (right_grid_row, right_grid_col)]
                grid_dir = ['lf', 'rf']

                for i in range(len(grids_m)):
                    self.validate_single_corner_grid(curr_row, curr_col,
                                                     grids_m[i][0],
                                                     grids_m[i][1], grid_dir[i],
                                                     player_turn, player_status)

            elif player_status == 'king':
                # takeout random piece from set
                curr_row, curr_col = self.piece_set.pop()

                lft_row_front, lft_col_front = curr_row + player_turn, curr_col - 1
                lft_row_back, lft_col_back = curr_row + (
                    -1 * player_turn), curr_col - 1

                rgt_row_front, rgt_col_front = curr_row + player_turn, curr_col + 1
                rgt_row_back, rgt_col_back = curr_row + (
                    -1 * player_turn), curr_col + 1

                # validating four grids around a "king" piece
                grids_k = [(lft_row_front, lft_col_front),
                           (lft_row_back, lft_col_back),
                           (rgt_row_front, rgt_col_front),
                           (rgt_row_back, rgt_col_back)]
                grid_dir = ['lf', 'lb', 'rf', 'rb']

                for i in range(len(grids_k)):
                    self.validate_single_corner_grid(curr_row, curr_col,
                                                     grids_k[i][0],
                                                     grids_k[i][1], grid_dir[i],
                                                     player_turn, player_status)

            return self.validate_grids_recursively(player_turn, player_status)

    def is_between_boundaries(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7

    def is_free_space(self, row, col):
        return self.grid[row][col] == 0

    def is_same_player(self, row, col, player_turn):
        return self.grid[row][col].player == player_turn

    def move_piece(self, mouse_x, mouse_y, player_turn):

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

            # add 1 move with no capture-pieces
            self.no_capture_pieces_count += 1

            # update the position attribute of the piece
            self.grid[selected_row][selected_col].position = (selected_row,
                                                              selected_col)

            # make changes on the status of a piece based on its moved position
            if self.grid[selected_row][selected_col].position[
                    0] == 0 and player_turn == -1:
                self.grid[selected_row][selected_col].status = 'king'

                self.king_side[0] = 1
            elif self.grid[selected_row][selected_col].position[
                    0] == 7 and player_turn == 1:
                self.grid[selected_row][selected_col].status = 'king'
                self.king_side[1] = 1

            self.grid[self.selected_piece[0]][self.selected_piece[1]] = 0

            while (selected_row, selected_col) in self.capture_pieces:

                capture_piece = self.capture_pieces[(selected_row,
                                                     selected_col)][0]
                self.grid[capture_piece[0]][capture_piece[1]] = 0

                selected_row, selected_col = self.capture_pieces[(
                    selected_row, selected_col)][1]

                # clear no_piece_capture_piece
                self.no_capture_pieces_count = 0

            self.selected_piece = None

            # if there is no piece captured for more then 100 turns
            # considered as draw
            if self.no_capture_pieces_count >= 100:
                print("No piece captured for more than 100 turns.")
                self.winner_status = 0

            # If both sides have king piece:
            if self.king_side.all():
                self.grid_buffer.append(np.array(self.grid))
                if len(self.grid_buffer) > 8:
                    if (self.grid_buffer[-1] == self.grid_buffer[0]).all():
                        self.winner_status = 0
                        print("Same Board State for 3 times.")
                    self.grid_buffer.popleft()

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

                    if self.grid[row][col].player == -1:
                        color = self.colors['BLACK']

                    pygame.draw.circle(
                        screen,
                        color, (col * self.grid_size + self.grid_size / 2,
                                row * self.grid_size + self.grid_size / 2),
                        self.grid_size / 3,
                        draw_top_right=self.grid[row][col].status == 'king')

        if self.selected_piece is not None:
            pygame.draw.rect(screen, self.colors['LGREEN'],
                             (self.selected_piece[1] * self.grid_size,
                              self.selected_piece[0] * self.grid_size,
                              self.grid_size, self.grid_size))

            pygame.draw.circle(
                screen,
                self.colors['WHITE']
                if player_turn == 1 else self.colors['BLACK'],
                (self.selected_piece[1] * self.grid_size + self.grid_size / 2,
                 self.selected_piece[0] * self.grid_size + self.grid_size / 2),
                self.grid_size / 3,
                draw_top_right=self.grid[self.selected_piece[0]][
                    self.selected_piece[1]].status == 'king')

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
                    screen,
                    self.colors['WHITE']
                    if player_turn == 1 else self.colors['BLACK'],
                    (c * self.grid_size + self.grid_size / 2,
                     r * self.grid_size + self.grid_size / 2),
                    self.grid_size / 3,
                    draw_top_right=self.grid[r][c].status == 'king')
