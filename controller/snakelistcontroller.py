from controller.singlesimcontroller import SingleSimController
from view.snakelist import SnakeList


class SnakeListController:
    """Controller for a Generation and Gene Pool snake list views. Can instantiate a SingleSimController to simulate
        a selected snake."""

    def __init__(self, simulation_service):
        self.simulation_service = simulation_service

        self.generation_window = SnakeList("Generation")
        self.generation_window.add_listener(self)

        self.genepool_window = SnakeList("Gene Pool")
        self.genepool_window.add_listener(self)

    def show_generation_window(self):
        self.generation_window.set_title(
            "Generation {:d}".format(self.simulation_service.current_generation_number))

        self.generation_window.set_snakes(self.simulation_service.current_generation.snakes)
        self.generation_window.show()

    def show_genepool_window(self):
        self.genepool_window.set_snakes(self.simulation_service.genepool.snakes)
        self.genepool_window.show()

    def on_close_snakelist_window(self, snakelist_window):
        snakelist_window.hide()

    def on_click_snake(self, snake):
        # Open a window showing the snake simulation
        single_sim_controller = SingleSimController(snake)

