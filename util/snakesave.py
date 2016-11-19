from struct import unpack, pack
from util.encoding import Encoder


class SnakeSave:
    """Service class for saving and loading snake text files."""

    @staticmethod
    def save_encoding(encoding, filename):
        snake_file = open(filename, mode='wb')


        for float in encoding:
            floatbytes = pack('d', float)
            snake_file.write(floatbytes)

    @staticmethod
    def load_encoding(filename):
        snake_file = open(filename, mode='rb')
        encoding = []

        floatbytes = snake_file.read(8)
        while len(floatbytes) == 8 and len(encoding) <= Encoder.encoding_length:
            encoding.append(unpack('d', floatbytes)[0])
            floatbytes = snake_file.read(8)

        return encoding
