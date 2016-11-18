class XorShift:
    def __init__(self):
        self.state = [1921003817, 838877476]

    def random(self):
        x = self.state[0]
        y = self.state[1]

        self.state[0] = y
        x ^= x << 23 & 0xFFFFFFFF
        self.state[1] = x ^ y ^ (x >> 17) ^ (y >> 26)

        return self.state[1] + y

    def randrange(self, start, stop):
        return (self.random() % (stop - start)) + start


