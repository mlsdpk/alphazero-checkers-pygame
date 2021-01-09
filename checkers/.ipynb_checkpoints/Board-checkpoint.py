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

    def init_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if (row%2==0 and col%2!=0) or (row%2!=0 and col%2==0):
                    self.grid[row][col] = Piece(row, col, 1) if row < 3 else Piece(row, col, -1) if row > 4 else 0

    def selection_mode(self, mouse_x, mouse_y, player_turn):
        print(f"x: {mouse_x//80}, {mouse_y//80}")

        selected_row, selected_col = mouse_y//80, mouse_x//80

        # if row,col is outside of board
        if selected_row < 0 or selected_row > 7 or selected_col < 0 or selected_col > 7:
            return False

        # if no piece in grid
        if self.grid[selected_row][selected_col] == 0:
            return False

        # if selected opponent's piece
        if self.grid[selected_row][selected_col].player != player_turn:
            return False

        self.grid[selected_row][selected_col].selected = True
        self.selected_piece = (selected_row, selected_col)

        return True
    
    def find_valid_pieces(self, player_turn):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                
                if not isinstance(self.grid[row][col], Piece):
                    continue
                if self.grid[row][col].player != player_turn:
                    continue
        
                left_grid_row, left_grid_col = row+player_turn, col-1
                right_grid_row, right_grid_col = row+player_turn, col+1
                
                if left_grid_row >= 0 and left_grid_row <= 7 and left_grid_col >= 0 and left_grid_col <= 7:
                    if self.grid[left_grid_row][left_grid_col] == 0:
                        self.valid_pieces.append((row,col))
                        continue
                if right_grid_row >= 0 and right_grid_row <= 7 and right_grid_col >= 0 and right_grid_col <= 7:
                    if self.grid[right_grid_row][right_grid_col] == 0:
                        self.valid_pieces.append((row,col))
                        continue
        print(self.valid_pieces)
        return (len(self.valid_pieces)>0)
            
    
    
    def find_valid_moves(self, player_turn):

        curr_row, curr_col = self.selected_piece

        # decide valid grids based on player turn
        left_grid_row, left_grid_col = curr_row+player_turn, curr_col-1
        right_grid_row, right_grid_col = curr_row+player_turn, curr_col+1

        # check to make sure between boundaries
        if left_grid_row >= 0 and left_grid_row <= 7 and left_grid_col >= 0 and left_grid_col <= 7:
            # if it is empty
            if self.grid[left_grid_row][left_grid_col] == 0:
                self.grid[curr_row][curr_col].valid_grids.append((left_grid_row, left_grid_col))

        if right_grid_row >= 0 and right_grid_row <= 7 and right_grid_col >= 0 and right_grid_col <= 7:
            # if it is empty
            if self.grid[right_grid_row][right_grid_col] == 0:
                self.grid[curr_row][curr_col].valid_grids.append((right_grid_row, right_grid_col))

        if len(self.grid[curr_row][curr_col].valid_grids) > 0:
            return True
        else:
            self.grid[self.selected_piece[0]][self.selected_piece[1]].selected = False
            self.selected_piece = None
            return False

    def move_piece(self, mouse_x, mouse_y):

        selected_row, selected_col = mouse_y//80, mouse_x//80

        # if row,col is outside of board
        if selected_row < 0 or selected_row > 7 or selected_col < 0 or selected_col > 7:
            return False

        if (selected_row, selected_col) in self.grid[self.selected_piece[0]][self.selected_piece[1]].valid_grids:

            self.grid[self.selected_piece[0]][self.selected_piece[1]].valid_grids = []
            self.grid[self.selected_piece[0]][self.selected_piece[1]].selected = False
            self.grid[selected_row][selected_col] = self.grid[self.selected_piece[0]][self.selected_piece[1]]
            self.grid[self.selected_piece[0]][self.selected_piece[1]] = 0
            self.selected_piece = None
            return True
        else: 
            self.grid[self.selected_piece[0]][self.selected_piece[1]].valid_grids = []
            self.grid[self.selected_piece[0]][self.selected_piece[1]].selected = False
            self.selected_piece = None
            return False
        
    # rendering stuffs
    def render(self, screen, player_turn):

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):

                if row%2 == 0:
                    color = self.colors['WHITE'] if col%2 == 0 else self.colors['GREY']
                else:
                    color = self.colors['GREY'] if col%2 == 0 else self.colors['WHITE']

                pygame.draw.rect(screen, color,
                    (col*self.grid_size, row*self.grid_size, self.grid_size, self.grid_size))

                if self.grid[row][col] != 0:

                    if self.grid[row][col].player == 1:
                        color = self.colors['WHITE']
                    elif self.grid[row][col].player == -1:
                        color = self.colors['BLACK']

                    pygame.draw.circle(
                        screen,
                        color,
                        (col*self.grid_size + self.grid_size/2, row*self.grid_size + self.grid_size/2),
                        self.grid_size/3
                    )

        if self.selected_piece is not None:
            pygame.draw.rect(screen, self.colors['LGREEN'],
                (self.selected_piece[1]*self.grid_size, self.selected_piece[0]*self.grid_size, self.grid_size, self.grid_size))

            pygame.draw.circle(
                screen,
                self.colors['WHITE'] if player_turn == 1 else self.colors['BLACK'],
                (self.selected_piece[1]*self.grid_size + self.grid_size/2, self.selected_piece[0]*self.grid_size + self.grid_size/2),
                self.grid_size/3
            )

            for x, y in self.grid[self.selected_piece[0]][self.selected_piece[1]].valid_grids:
                pygame.draw.rect(screen, self.colors['LGREEN'],
                    (y*self.grid_size, x*self.grid_size, self.grid_size, self.grid_size))
                
        if len(self.valid_pieces)>0:
            for r,c in self.valid_pieces:
                pygame.draw.rect(screen, self.colors['YELLOW'],
                    (c*self.grid_size, r*self.grid_size, self.grid_size, self.grid_size))
                
                pygame.draw.circle(screen,
                    self.colors['WHITE'] if player_turn == 1 else self.colors['BLACK'],
                    (c*self.grid_size + self.grid_size/2, r*self.grid_size + self.grid_size/2),self.grid_size/3
                )