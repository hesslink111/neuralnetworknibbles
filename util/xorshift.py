class XorShift:
    """Class for generating pseudo-random numbers based on a seed. This allows us to generate predictable sequences
        so we can play the same games. Based on xorshift+ from https://en.wikipedia.org/wiki/Xorshift"""

    def __init__(self):
        self.state = [1921003817, 838877476]

    def random(self):
        x = self.state[0]
        y = self.state[1]

        self.state[0] = y
        x ^= (x << 23) & 0x7FFFFFFF
        self.state[1] = x ^ y ^ (x >> 17) ^ (y >> 26)

        return self.state[1] + y & 0x7FFFFFFF

    def randrange(self, start, stop):
        return (self.random() % (stop - start)) + start


