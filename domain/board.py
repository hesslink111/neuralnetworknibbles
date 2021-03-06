class Board:
    """An 8x8 grid for a simulation. Contains an instance of the xorshift random class. Has helper methods for
        for determining the presence of obstacles or food."""

    def __init__(self, xorshift):
        self.board = [[0]*8]+[[0]*8]+[[0]*8]+[[0]*8]+[[0]*8]+[[0]*8]+[[0]*8]+[[0]*8]
        self.xorshift = xorshift

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j] = 0

    def clear_piece_at(self, position):
        if position is not None and self.is_position_in_range(position):
            self.board[position.y][position.x] = 0

    def set_piece_at(self, position, value):
        if position is not None and self.is_position_in_range(position):
            self.board[position.y][position.x] = value

    def is_piece_at(self, position):
        return position is None or not self.is_position_in_range(position) or self.board[position.y][position.x] == 1

    def piece_at(self, position):
        return position is None or not self.is_position_in_range(position) or self.board[position.y][position.x]

    def piece_at_x_y(self, x, y):
        return -1 if not self.is_position_in_range_x_y(x, y) else self.board[y][x]

    def is_position_in_range(self, position):
        return 0 <= position.x < 8 and 0 <= position.y < 8

    def is_position_in_range_x_y(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8





