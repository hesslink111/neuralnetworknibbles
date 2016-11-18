from tkinter import Toplevel, LabelFrame, Label, Scale, Button, HORIZONTAL, N, W, E, S, GROOVE


class SingleSimView:
    """View class for a simulation of a single snake. This view contains controls for the simulation step interval and
        buttons for starting, stopping, and stepping the simulation. The main view contains an 8x8 grid to show the
        game board for the simulation."""

    def __init__(self):
        self.window = Toplevel(padx=5, pady=5)
        self.window.title("Simulation")

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.resizable(width=False, height=False)

        self.listeners = []

        self.create_controls()
        self.create_simulation_panel()

    def create_controls(self):
        self.control_frame = LabelFrame(self.window, text="Controls", padx=5, pady=5)
        self.control_frame.grid(row=0, column=0, sticky=N+W+E+S)

        self.interval_label = Label(self.control_frame, text="Interval")
        self.interval_label.grid(row=0, columnspan=2)

        self.interval_slider = Scale(self.control_frame, from_=5, to_=1000,
                                     orient=HORIZONTAL, command=self.set_interval)
        self.interval_slider.grid(row=1, columnspan=2)

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

        self.moves_label = Label(self.simulation_frame, text="Moves: ")
        self.moves_label.grid(row=2, column=1, sticky=W)

        self.score_label = Label(self.simulation_frame, text="Score: ")
        self.score_label.grid(row=3, column=1, sticky=W)

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

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.window.withdraw()

    def close(self):
        self.window.destroy()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def show_game_board(self, gameboard, moves, score):
        boardtext = ""
        for y in reversed(range(8)):
            for x in range(8):
                boardtext += str("#" if gameboard.board[y][x] == -1 else "f" if gameboard.board[y][x] == 1 else "-")
                if x < 7:
                    boardtext += "  "
            if y > 0:
                boardtext += "\n"

        self.board_label['text'] = boardtext
        self.moves_label['text'] = "Moves: {:6d}".format(moves)
        self.score_label['text'] = "Score: {:6d}".format(score)
