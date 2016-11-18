from domain.evaluation import Evaluation
from view.singlesimview import SingleSimView


class SingleSimController:
    """Controller class for controlling the simulation of a single game for a single snake."""

    def __init__(self, snake):
        self.snake = snake
        self.evaluation = Evaluation(snake)

        self.singlesimview = SingleSimView()
        self.singlesimview.add_listener(self)
        self.singlesimview.show_game_board(self.evaluation.board,
                                           self.evaluation.current_game.moves,
                                           self.evaluation.current_game.score)

    def on_close_simulation_window(self):
        self.singlesimview.close()

