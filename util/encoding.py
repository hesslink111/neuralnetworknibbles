from random import *


class Encoder:
    """Class which contains static functions for generating genetic encodings for snakes."""

    numinputs = 256
    numhidden = 130
    numoutputs = 3

    encoding_length = numinputs * numhidden + numhidden * numoutputs

    @staticmethod
    def generate_encoding():
        encoding = [0] * Encoder.encoding_length
        for i in range(Encoder.encoding_length):
            encoding[i] = uniform(-1, 1)

        return encoding


