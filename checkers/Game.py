import pygame
from .Board import Board

class Game:
    def __init__(self, screen):
        self.SCREEN = screen
        self.running = True

        self.board = Board()

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):

        # Fill the background with white
        self.SCREEN.fill((0, 0, 0))

        # Render board
        self.board.render(self.SCREEN)

        # Update the display
        pygame.display.update()
