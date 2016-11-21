from tkinter import Toplevel, Label, Scrollbar, VERTICAL, W, S, E, N, Listbox, END
from tkinter.ttk import Treeview


class SnakeListView:
    """View class for a window containing a scrollable list of snakes. Each snake should be selectable. Double clicking
        a snake triggers a callback in any observers."""

    def __init__(self, title):
        self.snakes = []

        self.window = Toplevel(padx=5, pady=5)
        self.window.title(title)
        self.window.withdraw()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.resizable(width=False, height=False)

        self.listeners = []

        self.create_info_label()
        self.create_snake_list()

    def create_info_label(self):

        infotext = "Click on any snake to view its simulation and encoding"

        self.info_label = Label(self.window, text=infotext)
        self.info_label.grid(row=0, column=0, columnspan=1, sticky=N+E+S+W)

    def create_snake_list(self):

        self.snake_listview_scrollbar = Scrollbar(self.window, orient=VERTICAL)
        self.snake_listview_scrollbar.grid(row=1, column=1, sticky=N+E+S+W)

        self.snake_listbox = Listbox(self.window)
        self.snake_listbox.grid(row=1, column=0, sticky=N+E+S+W)

        self.snake_listview_scrollbar.config(command=self.snake_listbox.yview)
        self.snake_listbox.config(yscrollcommand=self.snake_listview_scrollbar.set)

        self.snake_listbox.bind('<Double-1>', self.click_snake)

    def set_title(self, title):
        self.window.title(title)

    def set_snakes(self, snakes):
        self.snake_listbox.delete(0, END)

        self.snakes = snakes
        for snake in self.snakes:
            self.snake_listbox.insert(END, snake.score)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.window.withdraw()

    def on_close(self):
        for listener in self.listeners:
            listener.on_close_snakelist_window(self)

    def click_snake(self, event):
        selections = self.snake_listbox.curselection()
        if len(selections) > 0:
            snake = self.snakes[int(selections[0])]
            for listener in self.listeners:
                listener.on_click_snake(snake)


