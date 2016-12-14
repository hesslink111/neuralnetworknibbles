from functools import reduce

from domain.gameboardrelativepositionstateneuron import GameBoardRelativePositionStateNeuron
from domain.direction import Direction
from domain.neuron import Neuron
from domain.position import Position
from domain.sigmoidneuron import SigmoidNeuron
from domain.synapse import Synapse


class SnakeNeuralNet:
    """Class to represent the neural network of a given genetic encoding. Parts of the network require access to the
        game board. To simulate the snake's perspective, this class requires knowledge of the gamesnake's orientation
        and position. This class used to require the numeric position of the mouse, but that information has since been
        encoded into the game board."""

    def __init__(self, encoding, game_board, gamesnake, mouse):
        # Encoding is a 256*130*1 + 130*3 list of synapse values
        self.input = [GameBoardRelativePositionStateNeuron] * 256
        self.hidden = [Neuron] * 130
        self.output = [Neuron] * 3

        self.gamesnake = gamesnake

        # Create input neurons
        i = 0
        for y in range(-8, 8):
            for x in range(-8, 8):
                self.input[i] = GameBoardRelativePositionStateNeuron(game_board, Position(x, y), gamesnake)
                i += 1

        # Hidden neurons
        for j in range(130):
            synapses = [0] * 256
            for k in range(256):
                synapses[k] = Synapse(self.input[k], encoding[j * 256 + k])
            self.hidden[j] = SigmoidNeuron(synapses)

        # Output neurons
        for j in range(3):
            synapses = [0] * 130
            for k in range(130):
                synapses[k] = Synapse(self.hidden[k], encoding[130 * 256 + j * 130 + k])
            self.output[j] = SigmoidNeuron(synapses)

    def evaluate(self):
        # Input neurons
        if self.gamesnake.direction == Direction.right:
            for j in range(256):  # 68 neurons
                self.input[j].calculate_result()
        elif self.gamesnake.direction == Direction.left:
            for j in range(256):  # 68 neurons
                self.input[j].calculate_result_left()
        elif self.gamesnake.direction == Direction.up:
            for j in range(256):  # 68 neurons
                self.input[j].calculate_result_up()
        else:
            for j in range(256):  # 68 neurons
                self.input[j].calculate_result_down()

        for j in range(130):  # 68 neurons
            self.hidden[j].calculate_result()

        # Output neurons
        for j in range(3):  # 3 output neurons
            self.output[j].calculate_result()

        final_values = [(Direction.up, self.output[0]),
                        (Direction.right, self.output[1]),
                        (Direction.down, self.output[2])]
        choice = reduce(lambda x, y: x if x[1].result > y[1].result else y, final_values)
        return (self.gamesnake.direction + choice[0]) % 4
