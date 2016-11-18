from domain.snake import Snake
from util.encoding import Encoder


class GenePool:
    """Represents the highest evaluated snake encodings of all time. Stores a list of 100 snakes."""

    def __init__(self):
        self.snakes = []
        for i in range(100):
            self.snakes.append(Snake(Encoder.generate_encoding()))
        self.best_snake = self.snakes[0]
        self.average_score = 0

    def add_snakes(self, snakes):
        self.snakes += snakes
        self.snakes = sorted(self.snakes, key=lambda x: x.score, reverse=True)[0:100]
        self.best_snake = self.snakes[0]
        self.average_score = sum(map(lambda x: x.score, self.snakes)) / 100
