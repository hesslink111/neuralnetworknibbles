from tkinter import *


class SimulationWindow:
    """This is the class for the main window of the simulation. This view contains controls for the simulation step
        interval and buttons for starting, stopping, and stepping the simulation. The main view contains an 8x8 grid
        to show the game board for the simulation. This view has a panel for generation and gene pool information."""

    def __init__(self):
        self.window = Toplevel(padx=5, pady=5)
        self.window.title("Simulation")
        self.window.withdraw()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.resizable(width=False, height=False)

        self.listeners = []

        self.create_controls()
        self.create_generation_panel()
        self.create_simulation_panel()
        self.create_genepool_frame()

    def create_controls(self):
        self.control_frame = LabelFrame(self.window, text="Controls", padx=5, pady=5)
        self.control_frame.grid(row=0, column=0, sticky=N+W+E+S)

        self.interval_label = Label(self.control_frame, text="Interval")
        self.interval_label.grid(row=0, columnspan=2)

        self.interval_slider = Scale(self.control_frame, from_=5, to_=1000,
                                     orient=HORIZONTAL, command=self.set_interval)
        self.interval_slider.grid(row=1, columnspan=2)

        self.speed_label = Label(self.control_frame, text="Simulation Speed")
        self.speed_label.grid(row=2, columnspan=2)

        self.speed_slider = Scale(self.control_frame, from_=1, to_=100, orient=HORIZONTAL, command=self.set_speed)
        self.speed_slider.grid(row=3, columnspan=2)

        self.start_button = Button(self.control_frame, text="Start", command=self.start)
        self.start_button.grid(row=4, column=0)

        self.pause_button = Button(self.control_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=4, column=1)

        self.step_button = Button(self.control_frame, text="Step", command=self.step)
        self.step_button.grid(row=5, column=0)

    def create_simulation_panel(self):
        self.simulation_frame = LabelFrame(self.window, text="Simulation", padx=5, pady=5)
        self.simulation_frame.grid(row=0, column=1, columnspan=2, sticky=N+W+E+S)

        self.board_header_label = Label(self.simulation_frame, text="Snake Simulation")
        self.board_header_label.grid(row=0, column=0)

        self.board_label = Label(self.simulation_frame, text="-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  #  -\n"
                                                             "-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  -  -\n"
                                                             "-  -  -  -  -  -  -  -",
                                 relief=GROOVE, bg='green', fg='brown', font=("Courier", 14))
        self.board_label.grid(row=1, column=0, rowspan=6)

        self.snake_number_label = Label(self.simulation_frame, text="Snake: ")
        self.snake_number_label.grid(row=1, column=1, sticky=W)

        self.view_snake_button = Button(self.simulation_frame, text="View Snake")
        self.view_snake_button.grid(row=1, column=3, sticky=E)

        self.moves_label = Label(self.simulation_frame, text="Moves: ")
        self.moves_label.grid(row=2, column=1, sticky=W)

        self.score_label = Label(self.simulation_frame, text="Score: ")
        self.score_label.grid(row=3, column=1, sticky=W)

    def create_generation_panel(self):
        self.generation_frame = LabelFrame(self.window, text="Generation", padx=5, pady=5)
        self.generation_frame.grid(row=1, column=1, sticky=N+W+E+S)

        self.generation_label = Label(self.generation_frame, text="Generation: ")
        self.generation_label.grid(row=0, column=0, sticky=W)

        self.view_generation_button = Button(self.generation_frame, text="View Generation",
                                             command=self.view_generation)
        self.view_generation_button.grid(row=0, column=1, sticky=E)

        self.generation_best_label = Label(self.generation_frame, text="Best: ")
        self.generation_best_label.grid(row=2, column=0, sticky=W)

    def create_genepool_frame(self):
        self.genepool_frame = LabelFrame(self.window, text="Gene Pool", padx=5, pady=5)
        self.genepool_frame.grid(row=1, column=2, sticky=N+W+E+S)

        self.genepool_best_label = Label(self.genepool_frame, text="Best Score: ")
        self.genepool_best_label.grid(row=0, column=0, sticky=W)

        self.view_genepool_button = Button(self.genepool_frame, text="View Gene Pool", command=self.view_genepool)
        self.view_genepool_button.grid(row=0, column=1, sticky=E)

        self.genepool_average_label = Label(self.genepool_frame, text="Average: ")
        self.genepool_average_label.grid(row=1, column=0, sticky=W)

    def on_close(self):
        for listener in self.listeners:
            listener.on_close_simulation_window()

    def start(self):
        for listener in self.listeners:
            listener.on_click_start()

    def pause(self):
        for listener in self.listeners:
            listener.on_click_pause()

    def step(self):
        for listener in self.listeners:
            listener.on_click_step()

    def set_interval(self, interval_value):
        for listener in self.listeners:
            listener.on_set_interval(self.interval_slider.get())

    def set_speed(self, speed_value):
        for listener in self.listeners:
            listener.on_set_speed(self.speed_slider.get())

    def view_snake(self):
        for listener in self.listeners:
            listener.on_click_view_snake()

    def view_generation(self):
        for listener in self.listeners:
            listener.on_click_view_generation()

    def view_genepool(self):
        for listener in self.listeners:
            listener.on_click_view_genepool()

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.window.withdraw()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def show_game_board(self, gameboard, snakenum, moves, score):
        boardtext = ""
        for y in reversed(range(8)):
            for x in range(8):
                boardtext += str("#" if gameboard.board[y][x] == -1 else "f" if gameboard.board[y][x] == 1 else "-")
                if x < 7:
                    boardtext += "  "
            if y > 0:
                boardtext += "\n"

        self.board_label['text'] = boardtext
        self.snake_number_label['text'] = "Snake: {:6d}".format(snakenum)
        self.moves_label['text'] = "Moves: {:6d}".format(moves)
        self.score_label['text'] = "Score: {:6d}".format(score)

    def show_generation_number(self, gennum):
        self.generation_label['text'] = "Generation: {:6d}".format(gennum)

    def show_generation_best(self, best_score):
        self.generation_best_label['text'] = "Best Score: {:6d}".format(best_score)

    def show_genepool_info(self, best_score, average_score):
        self.genepool_best_label['text'] = "Best Score: {:6d}".format(best_score)
        self.genepool_average_label['text'] = "Average: {:6.2f}".format(average_score)

