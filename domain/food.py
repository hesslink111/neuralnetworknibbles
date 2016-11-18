from domain.board import Position


class Food:
    def __init__(self, board, xorshift, position=None):
        self.position = position
        self.board = board
        self.xorshift = xorshift

    def randomize_position(self, hideprev=True):
        if hideprev:
            self.board.clear_piece_at(self.position)

        self.position = Position(self.xorshift.randrange(0, 8), self.xorshift.randrange(0, 8))
        while self.board.is_piece_at(self.position):
            self.position = Position(self.xorshift.randrange(0, 8), self.xorshift.randrange(0, 8))

        self.board.set_piece_at(self.position, 1)
