from threading import Thread, Lock
from time import sleep

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

        self.simulation_step_loop_lock = Lock()
        self.step_loop_interval = 5
        self.simulation_step_loop_active = False
        self.can_update_window = True

    def on_close_simulation_window(self):
        self.simulation_step_loop_active = False
        self.can_update_window = False
        self.singlesimview.close()

    def on_set_interval(self, interval_value):
        self.step_loop_interval = interval_value

    def on_click_start(self):
        if not self.simulation_step_loop_active:
            self.simulation_step_loop_active = True
            simulation_step_loop_thread = Thread(target=self.simulation_step_loop)
            simulation_step_loop_thread.start()

    def on_click_pause(self):
        self.simulation_step_loop_active = False

    def on_click_step(self):
        self.simulation_step()

    def simulation_step_loop(self):
        self.simulation_step_loop_lock.acquire()
        while self.simulation_step_loop_active:
            self.simulation_step()
            sleep(self.step_loop_interval/1000)
        self.simulation_step_loop_lock.release()

    def simulation_step(self):

        if self.evaluation.current_game.finished:
            self.simulation_step_loop_active = False
        else:
            self.evaluation.current_game.step()                              # Step the current game

        if self.can_update_window:
            self.singlesimview.show_game_board(self.evaluation.board,
                                               self.evaluation.current_game.moves,
                                               self.evaluation.current_game.score)
