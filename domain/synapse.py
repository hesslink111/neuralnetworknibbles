class Synapse:
    """Passes a signal from a neuron to another neuron. Contains a weight value which is used to produce output to the
        containing neuron."""

    def __init__(self, input_neuron, weight):
        self.input_neuron = input_neuron
        self.weight = weight

    def get_value(self):
        return self.input_neuron.result * self.weight
