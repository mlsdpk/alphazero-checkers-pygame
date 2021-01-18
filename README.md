# alphazero-checkers-pygame

Web application for Checkers Board Game. The AI we use is the AlphaGo Zero algorithm implemented by DeepMind.


## Project Description

Alphazero is a breakthrough application of reinforcement learning in board games. Thus, this work will try implementing RL to checkers game. First, a user interface is made for multiplayer checkers game. We also created a checkers bot with Minimax algorithm to serve as training agent for our model. Monte Carlo tree search along with policy and value networks will be integrated to our model in the next stage. 


## Overview



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

## Checkers game rules

- White pieces move first.
- Normal Pieces may only move one diagonal space forward (towards their opponents pieces).
- Pieces must stay on the dark squares.
- To capture an opposing piece, you can jump over it by moving two diagonal spaces in the direction of the the opposing piece.
- A piece may jump forward over multiple of opponent's pieces to capture them.
- When a piece reaches the last row on your opponent's side, that piece becomes a king.
- King pieces may still only move one space at a time in forwards or backwards direction during a non-capturing move.
- When capturing an opponent's piece(s) with king piece, it may move two spaces diagonally forward or backwards.
- There is no limit on the number of king pieces a player can have
- The game is won when you capture all of your opponent's piece.
- If a position is repeated three times by both players, the game will result in a draw.
