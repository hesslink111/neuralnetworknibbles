from math import *
from functools import reduce

from domain.board import Position, Direction


class SnakeNeuralNet:
    def __init__(self, encoding, game_board, gamesnake, food):
        # Encoding is a 256*130*1 + 130*3 list of synapse values
        self.neurons = [[Neuron] * 256] + [[Neuron] * 130]
        self.neurons += [[Neuron] * 3]
        self.gamesnake = gamesnake

        # Create input neurons
        i = 0
        for y in range(-8, 8):
            for x in range(-8, 8):
                self.neurons[0][i] = GameBoardRelativePositionStateNeuron(game_board, Position(x, y), gamesnake)
                i += 1

        # self.neurons[0][64] = PieceXPositionNeuron(gamesnake)
        # self.neurons[0][65] = PieceYPositionNeuron(gamesnake)
        # self.neurons[0][66] = PieceXPositionNeuron(food)
        # self.neurons[0][67] = PieceYPositionNeuron(food)
        # self.neurons[0][68] = PieceXDirectionNeuron(gamesnake)
        # self.neurons[0][69] = PieceYDirectionNeuron(gamesnake)

        # Hidden neurons
        for i in range(1, 2):
            for j in range(130):
                synapses = [0] * 256
                for k in range(256):
                    synapses[k] = Synapse(self.neurons[i - 1][k], encoding[(i - 1) * 256 * 130 + j * 256 + k])
                self.neurons[i][j] = SigmoidNeuron(synapses)

        # Output neurons
        for j in range(3):
            synapses = [0] * 130
            for k in range(130):
                synapses[k] = Synapse(self.neurons[1][k], encoding[1 * 130 * 256 + j * 130 + k])
            self.neurons[2][j] = SigmoidNeuron(synapses)

    def evaluate(self):
        # Input neurons
        if self.gamesnake.direction == Direction.right:
            for i in range(1):  # 8 layers
                for j in range(256):  # 68 neurons
                    self.neurons[i][j].calculate_result()
        elif self.gamesnake.direction == Direction.left:
            for i in range(1):  # 8 layers
                for j in range(256):  # 68 neurons
                    self.neurons[i][j].calculate_result_left()
        elif self.gamesnake.direction == Direction.up:
            for i in range(1):  # 8 layers
                for j in range(256):  # 68 neurons
                    self.neurons[i][j].calculate_result_up()
        else:
            for i in range(1):  # 8 layers
                for j in range(256):  # 68 neurons
                    self.neurons[i][j].calculate_result_down()

        for i in range(1, 2):  # 8 layers
            for j in range(130):  # 68 neurons
                self.neurons[i][j].calculate_result()

        # Output neurons
        for j in range(3):  # 3 output neurons
            self.neurons[2][j].calculate_result()

        final_values = [(Direction.up, self.neurons[2][0]),
                        (Direction.right, self.neurons[2][1]),
                        (Direction.down, self.neurons[2][2])]
        choice = reduce(lambda x, y: x if x[1].result > y[1].result else y, final_values)
        return Direction((self.gamesnake.direction.value + choice[0].value) % 4)


class Synapse:
    def __init__(self, input_neuron, weight):
        self.input_neuron = input_neuron
        self.weight = weight

    def get_value(self):
        return self.input_neuron.result * self.weight


class Neuron:
    def __init__(self):
        self.result = 0

    def calculate_result(self):
        pass


class PieceXPositionNeuron(Neuron):
    def __init__(self, piece):
        Neuron.__init__(self)
        self.piece = piece

    def calculate_result(self):
        self.result = self.piece.position.x / 32 - 1


class PieceYPositionNeuron(Neuron):
    def __init__(self, piece):
        Neuron.__init__(self)
        self.piece = piece

    def calculate_result(self):
        self.result = self.piece.position.y / 32 - 1


class PieceXDirectionNeuron(Neuron):
    def __init__(self, piece):
        Neuron.__init__(self)
        self.piece = piece

    def calculate_result(self):
        if self.piece.direction == Direction.left:
            self.result = -1
        elif self.piece.direction == Direction.right:
            self.result = 1
        else:
            self.result = 0


class PieceYDirectionNeuron(Neuron):
    def __init__(self, piece):
        Neuron.__init__(self)
        self.piece = piece

    def calculate_result(self):
        if self.piece.direction == Direction.down:
            self.result = -1
        elif self.piece.direction == Direction.up:
            self.result = 1
        else:
            self.result = 0


class GameBoardRelativePositionStateNeuron(Neuron):
    def __init__(self, game_board, position, gamesnake):
        Neuron.__init__(self)
        self.game_board = game_board
        self.position = position
        self.gamesnake = gamesnake

    def calculate_result(self):
        self.result = self.game_board.piece_at_x_y(self.position.x, self.position.y)

    def calculate_result_up(self):
        self.result = self.game_board.piece_at_x_y(-self.position.y, self.position.x)

    def calculate_result_left(self):
        self.result = self.game_board.piece_at_x_y(-self.position.x, -self.position.y)

    def calculate_result_down(self):
        self.result = self.game_board.piece_at_x_y(self.position.y, -self.position.x)


class SigmoidNeuron(Neuron):
    def __init__(self, synapses):
        Neuron.__init__(self)
        self.synapses = synapses

    def calculate_result(self):
        synsum = sum(map(lambda syn: syn.get_value(), self.synapses))
        self.result = 1 / (1 + e ** -synsum)
