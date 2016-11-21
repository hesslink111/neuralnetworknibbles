from queue import Queue


class TKUIThread:
    """Class to contain and manage communication with the UI thread."""

    def __init__(self, tkroot):
        self.queue = Queue()
        self.tkroot = tkroot
        self.begin_loop()

    def begin_loop(self):
        self.check_queue()

    def check_queue(self):
        while not self.queue.empty():
            f = self.queue.get(0)
            f()
        self.tkroot.after(100, self.check_queue)

    def run_on_ui_thread(self, func):
        self.queue.put(func)
