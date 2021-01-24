import argparse
import pygame
from checkers.Game import Game

parser = argparse.ArgumentParser(allow_abbrev=False)

parser.add_argument('-w',
                    action='store',
                    type=str,
                    choices=['human', 'minimax0', "minimax1", "alphazero"],
                    help='Set the white player to either human or AIs')

parser.add_argument('-b',
                    action='store',
                    type=str,
                    choices=['human', 'minimax0', "minimax1", "alphazero"],
                    help='Set the black player to either human or AIs')

args = parser.parse_args()

# initialize pygame
pygame.init()
width, height = 640, 640
SCREEN = pygame.display.set_mode([width, height])

def main():

    # initialize game object
    game = Game(args.w, args.b, SCREEN)

    while game.running:

        # Update
        game.update()

        # Render
        game.render()

    pygame.quit()


if __name__ == "__main__":
    main()
