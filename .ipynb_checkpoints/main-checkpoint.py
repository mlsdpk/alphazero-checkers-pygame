import pygame
from checkers.Game import Game

# initialize pygame
pygame.init()

width, height = 640, 640

SCREEN = pygame.display.set_mode([width, height])

def main():

    # initialize game object
    game = Game(SCREEN)

    while game.running:

        # Update
        game.update()

        # Render
        game.render()

    pygame.quit()

if __name__ == "__main__":
    main()
