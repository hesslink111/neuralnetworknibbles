from tkinter import Toplevel, Label, Scrollbar, VERTICAL, W, S, E, N
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

        self.listeners = []

        self.create_info_label()
        self.create_snake_list()

    def create_info_label(self):

        infotext = "Click on any snake to view its simulation and encoding"

        self.info_label = Label(self.window, text=infotext)
        self.info_label.grid(row=0, column=0)

    def create_snake_list(self):
        self.items = []

        self.snake_treeview = Treeview(self.window, columns=(1, 2, 3))
        self.snake_treeview.grid(row=1, column=0)

        self.snake_treeview_scrollbar = Scrollbar(self.window, orient=VERTICAL)
        self.snake_treeview_scrollbar.grid(row=1, column=1, sticky=N+E+S+W)

        self.snake_treeview_scrollbar.config(command=self.snake_treeview.yview)
        self.snake_treeview.config(yscrollcommand=self.snake_treeview_scrollbar.set)

        self.snake_treeview.heading('#0', text="Name")
        self.snake_treeview.heading(1, text="Moves")
        self.snake_treeview.heading(2, text="Size")
        self.snake_treeview.heading(3, text="Score")

        self.snake_treeview.bind('<Double-1>', self.click_snake)

    def set_title(self, title):
        self.window.title(title)

    def set_snakes(self, snakes):
        for item in self.items:
            self.snake_treeview.delete(item)
        self.items = []
        self.snakes = snakes
        for i in range(len(self.snakes)):
            self.items.append(self.snake_treeview.insert("", i, i, text="", values=(self.snakes[i].moves,
                                                               self.snakes[i].size,
                                                               self.snakes[i].score)))

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
        selection = self.snake_treeview.selection()
        if len(selection) > 0:
            item = selection[0]
            if self.snake_treeview.exists(item):
                for listener in self.listeners:
                    listener.on_click_snake(self.snakes[int(item)])


