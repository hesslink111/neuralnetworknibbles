from domain.evaluation import Evaluation
from domain.genepool import GenePool
from domain.generation import Generation


class SimulationService:
    """Service class for maintaining the gene pool, the current generation, and the current snake evaluation."""

    def __init__(self):

        # Save best snakes
        self.genepool = GenePool()

        self.current_generation_number = 0
        self.current_generation = Generation(self.genepool)
        self.previous_generations = []

        # Set up first evaluation
        self.current_snake_number = 0
        self.start_next_evaluation()

    def start_next_evaluation(self):
        if self.current_snake_number > 0:
            self.current_generation.test_best(self.current_snake_evaluation.snake)

        self.current_snake_evaluation = Evaluation(self.current_generation.snakes[self.current_snake_number])
        self.current_snake_number += 1

    def start_next_generation(self):
        self.genepool.add_snakes(self.current_generation.snakes)
        self.current_generation = Generation(self.genepool)
        self.current_generation_number += 1

        self.current_snake_number = 0
        self.start_next_evaluation()


