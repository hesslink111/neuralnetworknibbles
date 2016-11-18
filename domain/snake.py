class Snake:
    """Domain class containing information about a snake and its evaluation, including its genetic encoding."""

    def __init__(self, encoding):
        self.encoding = encoding
        self.score = 0
        self.moves = 0
        self.size = 0


