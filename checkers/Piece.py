class Piece:

    def __init__(self, row, col, player):

        self.position = (row, col)
        self.player = player
        self.status = 'man'
        self.selected = False
        self.valid_grids = []

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.status == other.status and self.player == other.player
