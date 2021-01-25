import sys
sys.path.append("..")

import copy
from checkers.Board import Board

class MiniMax:
    def __init__(self, depth=1):
        self.depth = depth

    def minimax(self, board, depth, max_player, player_turn, ai_turn):

        if depth == 0 or board.winner_status is not None:
            return board.evaluate(ai_turn), None

        if max_player:
            maxEval = float('-inf')
            best_move = None

            movable_grids = self.find_all_movable_grids(board, player_turn)

            for valid_piece in movable_grids.keys():
                # for each valid grid of valid piece
                for valid_grid in movable_grids[valid_piece]:

                    # create new board object by moving valid piece to valid grid
                    # this make sure that we are copying (not just reference)
                    new_board = copy.deepcopy(board)
                    new_board.move(valid_piece, valid_grid, player_turn)

                    # run minimax recursively
                    evaluation = self.minimax(new_board, depth-1, False, -1*player_turn, ai_turn)[0]

                    if evaluation > maxEval:
                        maxEval = evaluation
                        best_move = [valid_piece, valid_grid]

            return maxEval, best_move

        else:
            minEval = float('inf')
            best_move = None

            movable_grids = self.find_all_movable_grids(board, player_turn)

            for valid_piece in movable_grids.keys():
                # for each valid grid of valid piece
                for valid_grid in movable_grids[valid_piece]:

                    # create new board object by moving valid piece to valid grid
                    new_board = copy.deepcopy(board)
                    new_board.move(valid_piece, valid_grid, player_turn)

                    # run minimax recursively
                    evaluation = self.minimax(new_board, depth-1, True, -1*player_turn, ai_turn)[0]

                    if evaluation < minEval:
                        minEval = evaluation
                        best_move = [valid_piece, valid_grid]

            return minEval, best_move


    def move(self, board, player_turn):

        _, best_move = self.minimax(copy.deepcopy(board), self.depth, True, player_turn, player_turn)
        if best_move is not None:
            board.find_valid_moves(player_turn, best_move[0][0], best_move[0][1])
            board.move(best_move[0], best_move[1], player_turn)
        return board

    def find_all_movable_grids(self, board, player_turn):

        # first find the valid pieces of current player
        # this will store valid pieces in the board.valid_pieces
        # if board has valid pieces
        if board.find_valid_pieces(player_turn):
            valid_pieces = board.valid_pieces
        # else, not implemented yet
        else:
            return {}

        # find all the movable grids and store in the dict
        # dict - {valid_piece: valid grids}
        movable_grids = {}

        # use valid pieces to find all the valid movable grids of each piece
        for piece in valid_pieces:
            # this will store all valid grids of current valid piece
            # in the board.grid[piece[0]][piece[1]].valid_grids
            board.find_valid_moves(player_turn, piece[0], piece[1])

            # store in the movable_grid dict
            movable_grids[(piece[0], piece[1])] = board.grid[piece[0]][piece[1]].valid_grids

        return movable_grids

