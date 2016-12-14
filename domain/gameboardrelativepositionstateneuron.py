from domain.neuron import Neuron


class GameBoardRelativePositionStateNeuron(Neuron):
    """Input neuron class for sensing the position on the game board relative to the snake's position and
        orientation."""

    def __init__(self, game_board, position, gamesnake):
        Neuron.__init__(self)
        self.game_board = game_board
        self.position = position
        self.gamesnake = gamesnake

    def calculate_result(self):
        self.result = self.game_board.piece_at_x_y(self.position.x + self.gamesnake.position.x,
                                                   self.position.y + self.gamesnake.position.y)

    def calculate_result_up(self):
        self.result = self.game_board.piece_at_x_y(-self.position.y + self.gamesnake.position.x,
                                                   self.position.x + self.gamesnake.position.y)

    def calculate_result_left(self):
        self.result = self.game_board.piece_at_x_y(-self.position.x + self.gamesnake.position.x,
                                                   -self.position.y + self.gamesnake.position.y)

    def calculate_result_down(self):
        self.result = self.game_board.piece_at_x_y(self.position.y + self.gamesnake.position.x,
                                                   -self.position.x + self.gamesnake.position.y)
