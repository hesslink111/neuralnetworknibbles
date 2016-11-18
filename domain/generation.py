from random import *
from domain.snake import Snake


class Generation:
    def __init__(self, genepool):
        self.genepool = genepool
        self.snakes = []

        # Perform lottery to create new snakes
        worst = self.genepool.snakes[99].score
        best = self.genepool.snakes[0].score

        if best - worst <= 0:
            encoding_lottery = self.genepool.snakes
        else:
            encoding_lottery = []
            for snake in self.genepool.snakes:
                numtickets = int(10*(snake.score - worst) / (best - worst))
                encoding_lottery.extend([snake]*numtickets)

        # Create 100 new snakes based on encoding lottery
        numgenes = 256 * 130 * 1 + 130 * 3
        for i in range(20):                                 # Number of snakes
            encoding = []
            for j in range(0, 130 * 256, 256):                # Number of genes
                encoding.extend(choice(encoding_lottery).encoding[j:j+256])
                # Apply randomization
                for k in range(j, j+256):
                    if randrange(0, 200) == 0:
                        encoding[k] = uniform(-1, 1)
            for j in range(130 * 256, 130 * 256 + 3 * 130, 130):                # Number of genes
                encoding.extend(choice(encoding_lottery).encoding[j:j+130])
                # Apply randomization
                for k in range(j, j+130):
                    if randrange(0, 20) == 0:
                        encoding[k] = uniform(-1, 1)

            self.snakes.append(Snake(encoding))

        self.best_snake = self.snakes[0]

    def get_average_score(self):
        return sum(map(lambda x: x.score, self.snakes)) / len(self.snakes)

    def test_best(self, snake):
        self.best_snake = self.best_snake if self.best_snake.score > snake.score else snake



