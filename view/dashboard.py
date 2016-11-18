from tkinter import *


class DashboardWindow:
    """View class for the original main window of the program. This is mostly deprecated, but still contains the root
        Tk instance needed to create any further Tk windows."""

    def __init__(self):
        self.listeners = []

        self.root = Tk()
        self.root.title("Neural Nibbles")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.root.resizable(width=False, height=False)


    def run(self):
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.generate_encoding_button = Button(self.frame, text="Generate generation 0 encoding", command=self.generate_encoding)
        self.generate_encoding_button.pack(side=TOP)

        self.encoding_label = Label(self.frame, text="---")
        self.encoding_label.pack(side=TOP)

        self.show_simulation_button = Button(self.frame, text="Show simulation", command=self.show_simulation)
        self.show_simulation_button.pack(side=TOP)

        self.quit_button = Button(self.frame, text="Quit", fg="red", command=self.root.destroy)
        self.quit_button.pack(side=BOTTOM)

    def generate_encoding(self):
        for listener in self.listeners:
            listener.on_click_generate_encoding()

    def display_encoding(self, encoding):
        self.encoding_label["text"] = encoding

    def show_simulation(self):
        for listener in self.listeners:
            listener.on_click_show_simulation()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()


