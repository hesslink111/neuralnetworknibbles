from domain.neuron import Neuron
from math import e


class SigmoidNeuron(Neuron):
    """Represents a hidden neuron inside the neural network. Aggregates input from synapses, k, and generates a result
        based on (1 / ( 1 + e^k )), which will be a number in the range of (0, 1)"""

    def __init__(self, synapses):
        Neuron.__init__(self)
        self.synapses = synapses

    def calculate_result(self):
        synsum = sum(map(lambda syn: syn.get_value(), self.synapses))
        self.result = 1 / (1 + e ** -synsum)
