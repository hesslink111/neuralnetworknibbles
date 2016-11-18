from random import *


class Encoder:

    numlayers = 1
    numinputs = 16
    numhidden = 10

    @staticmethod
    def generate_encoding():
        encoding = [0] * (256 * 130 * 1 + 130 * 3)
        for i in range(256 * 130 * 1 + 130 * 3):
            encoding[i] = uniform(-1, 1)

        return encoding


