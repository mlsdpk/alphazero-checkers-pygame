import pygame
import numpy as np

class Board:

    def __init__(self):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.grid_size = self.width / 8
        self.grid = np.zeros((8,8))

        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GREY': (150, 150, 150)
        }

        self.init_grid()

    def init_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if (row%2==0 and col%2!=0) or (row%2!=0 and col%2==0):
                    self.grid[row][col] = 1 if row < 3 else -1 if row > 4 else 0

    def update(self):
        pass

    def render(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):

                if row%2 == 0:
                    color = self.colors['WHITE'] if col%2 == 0 else self.colors['GREY']
                else:
                    color = self.colors['GREY'] if col%2 == 0 else self.colors['WHITE']

                pygame.draw.rect(screen, color,
                    (col*self.grid_size, row*self.grid_size, self.grid_size, self.grid_size))

                if self.grid[row][col] == 1:
                    color = self.colors['WHITE']
                elif self.grid[row][col] == -1:
                    color = self.colors['BLACK']

                pygame.draw.circle(
                    screen,
                    color,
                    (col*self.grid_size + self.grid_size/2, row*self.grid_size + self.grid_size/2),
                    self.grid_size/3
                )
