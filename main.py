import argparse
import pygame
from checkers.Game import Game

parser = argparse.ArgumentParser(allow_abbrev=False)

parser.add_argument('--p1',
                    action='store',
                    type=str,
                    choices=['human', 'minimax', "alphazero"],
                    help='Set the white player to either human or AIs')

parser.add_argument('--p2',
                    action='store',
                    type=str,
                    choices=['human', 'minimax', "alphazero"],
                    help='Set the black player to either human or AIs')

parser.add_argument('--p1_depth',
                    action='store',
                    type=int,
                    default=1,
                    help='Set the black player to either human or AIs')

parser.add_argument('--p2_depth',
                    action='store',
                    type=int,
                    default=1,
                    help='Set the black player to either human or AIs')

args = parser.parse_args()

# initialize pygame
pygame.init()
width, height = 640, 640
SCREEN = pygame.display.set_mode([width, height])

def main():

    # initialize game object
    game = Game(args.p1, args.p2, SCREEN, args.p1_depth, args.p2_depth)

    while game.running:

        # Update
        game.update()

        # Render
        game.render()

    pygame.quit()


if __name__ == "__main__":
    main()
