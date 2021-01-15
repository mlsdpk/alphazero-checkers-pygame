class Piece:

    def __init__(self, row, col, player):

        self.position = (row, col)
        self.player = player
        self.status = 'man'
        self.selected = False
        self.valid_grids = []
