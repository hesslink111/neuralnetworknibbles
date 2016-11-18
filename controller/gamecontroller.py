from threading import Thread, Lock
from time import sleep

from controller.snakelistcontroller import SnakeListController
from service.simulationservice import SimulationService
from view.dashboard import *
from view.gameview import *
from util.encoding import *


class GameController:
    """Class for controlling the simulation and the game view. Starts by showing the deprecated view for generating
        the first encoding. All views are instantiated in the main thread."""

    def __init__(self):

        # Initialize services
        self.simulation_service = SimulationService()

        self.window = DashboardWindow()
        self.window.add_listener(self)

        self.simulation_window = SimulationWindow()
        self.simulation_window.add_listener(self)

        self.simulation_step_loop_active = False
        self.simulation_step_loop_lock = Lock()
        self.step_loop_interval = 5
        self.simulation_speed = 0

        # Initialize other controllers
        self.snakelist_controller = SnakeListController(self.simulation_service)

        self.window.run()

    def on_click_generate_encoding(self):
        encoding = Encoder.generate_encoding()
        self.window.display_encoding(list(map(round, encoding[0:20])))

    def on_click_show_simulation(self):
        self.window.hide()

        # Show generation information
        # Show game
        evaluation = self.simulation_service.current_snake_evaluation
        self.simulation_window.show_game_board(evaluation.board,
                                               self.simulation_service.current_snake_number,
                                               evaluation.current_game.moves,
                                               evaluation.current_game.score)

        self.simulation_window.show_generation_number(self.simulation_service.current_generation_number)
        self.simulation_window.show_generation_best(self.simulation_service.current_generation.best_snake.score)
        self.simulation_window.show_genepool_info(self.simulation_service.genepool.best_snake.score,
                                                  self.simulation_service.genepool.average_score)

        self.simulation_window.show()

    def on_close_simulation_window(self):
        self.simulation_window.hide()
        self.simulation_step_loop_active = False
        self.window.show()

    def on_click_step(self):
        self.simulation_step()

    def on_click_start(self):
        if not self.simulation_step_loop_active:
            self.simulation_step_loop_active = True
            simulation_step_loop_thread = Thread(target=self.simulation_step_loop)
            simulation_step_loop_thread.start()

    def on_click_pause(self):
        self.simulation_step_loop_active = False

    def on_click_view_snake(self):
        pass

    def on_click_view_generation(self):
        self.snakelist_controller.show_generation_window()

    def on_click_view_genepool(self):
        self.snakelist_controller.show_genepool_window()

    def on_set_interval(self, interval_value):
        self.step_loop_interval = interval_value

    def on_set_speed(self, speed_value):
        self.simulation_speed = speed_value

    def simulation_step_loop(self):
        self.simulation_step_loop_lock.acquire()
        while self.simulation_step_loop_active:
            self.simulation_step()
            sleep(self.step_loop_interval/1000)
        self.simulation_step_loop_lock.release()

    def simulation_step(self):
        evaluation = self.simulation_service.current_snake_evaluation

        for i in range(self.simulation_speed):

            if evaluation.current_game.finished:
                if evaluation.game_number < 1:
                    evaluation.start_next_game()                            # Start a new game
                else:
                    evaluation.save_snake_statistics()
                    if self.simulation_service.current_snake_number < 20:
                        self.simulation_service.start_next_evaluation()     # Simulate a different snake
                        evaluation = self.simulation_service.current_snake_evaluation
                    else:
                        self.simulation_service.start_next_generation()     # Create the next generation
                        evaluation = self.simulation_service.current_snake_evaluation

                        # Update generation information
                        self.simulation_window.show_generation_number(self.simulation_service.current_generation_number)

                        # Update genepool information
                        self.simulation_window.show_genepool_info(
                            self.simulation_service.genepool.best_snake.score,
                            self.simulation_service.genepool.average_score)

            else:
                evaluation.current_game.step()                              # Step the current game

        self.simulation_window.show_game_board(evaluation.board,
                                               self.simulation_service.current_snake_number,
                                               evaluation.current_game.moves,
                                               evaluation.current_game.score)

        self.simulation_window.show_generation_best(self.simulation_service.current_generation.best_snake.score)




