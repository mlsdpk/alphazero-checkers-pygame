# alphazero-checkers-pygame

Web application for Checkers Board Game. The AI we use is the AlphaGo Zero algorithm implemented by DeepMind.

## Dependencies

- pygame >= 2.0.1

To install pygame on your platform, use the appropriate pip command:

```
pip install pygame
```

## Usage

```
python main.py --p1 human --p2 minimax --p2_depth 4
```

Required arguments:

- --p1 player: Set the white player to either human or AIs (human,minimax,alphazero)
- --p2 player: Set the black player to either human or AIs (human,minimax,alphazero)
- --p1_depth depth: Set the depth for player 1 minimax AI
- --p2_depth depth: Set the depth for player 1 minimax AI

Optional arguments:
- -h, --help: Show the help message and exit

> Note that recommended depth of the minimax AI is between 1 to 5, you can surely set higher values than 5 (depending on your computation resources).

