from domain.board import Position, Direction


class GameSnake:
    """Domain class for a snake game piece. Has knowledge of the game board. GameSnake has a list of BodyParts based
        on the current size of the snake."""

    def __init__(self, board, xorshift, position=None):
        self.board = board
        self.xorshift = xorshift
        self.head = BodyPart(position)
        self.position = position
        self.tail = self.head
        self.body = [self.head]
        self.direction = Direction.left

        self.previous_tail = BodyPart(None)
        self.previous_head = BodyPart(None)

    def reset(self):
        for bodypart in self.body:
            self.board.clear_piece_at(bodypart.position)

        self.board.set_piece_at(self.head.position, -1)
        self.tail = self.head
        self.body = [self.head]

    def randomize_position(self):
        self.board.clear_piece_at(self.position)

        self.position = Position(self.xorshift.randrange(0, 8), self.xorshift.randrange(0, 8))
        while self.board.is_piece_at(self.position):
            self.position = Position(self.xorshift.randrange(0, 8), self.xorshift.randrange(0, 8))

        self.board.set_piece_at(self.position, -1)

        # Set head position
        self.head.position = self.position

    def move(self, direction):
        if not self.is_valid_move_direction(direction):
            direction = self.direction
        self.direction = direction

        # Save previous positions
        self.previous_tail = self.tail
        self.previous_head = self.head

        if direction == Direction.up:
            self.head = BodyPart(Position(self.head.position.x, self.head.position.y + 1))
        elif direction == Direction.down:
            self.head = BodyPart(Position(self.head.position.x, self.head.position.y - 1))
        elif direction == Direction.left:
            self.head = BodyPart(Position(self.head.position.x - 1, self.head.position.y))
        else:
            self.head = BodyPart(Position(self.head.position.x + 1, self.head.position.y))

        # Update body
        self.position = self.head.position
        self.body.append(self.head)
        self.body.remove(self.tail)
        self.tail = self.body[0]

    def update_board_position(self):
        self.board.clear_piece_at(self.previous_tail.position)
        self.board.set_piece_at(self.head.position, -1)

    def is_valid_move_direction(self, direction):
        return (self.direction == Direction.left and not direction == Direction.right
                or self.direction == Direction.right and not direction == Direction.left
                or self.direction == Direction.up and not direction == Direction.down
                or self.direction == Direction.down and not direction == Direction.up)

    def add_tail_piece(self):
        self.tail = self.previous_tail
        self.body.insert(0, self.tail)
        self.previous_tail = BodyPart(None)


class BodyPart:
    """Represents a segment of a snake. Has a position and nothing else."""

    def __init__(self, position):
        self.position = position
