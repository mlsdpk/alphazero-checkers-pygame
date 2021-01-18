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
python main.py -w human -b human
```

Required arguments:

- -w player: Set the white player to either human or AIs (human,minimax0,minimax1,alphazero)
- -b player: Set the black player to either human or AIs (human,minimax0,minimax1,alphazero)

Optional arguments:
- -h, --help: Show the help message and exit

