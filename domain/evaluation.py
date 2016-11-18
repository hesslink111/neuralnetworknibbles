from copy import deepcopy
from domain.board import Board
from domain.mouse import Mouse
from domain.gamesnake import GameSnake
from domain.neuralnetwork import SnakeNeuralNet
from util.xorshift import XorShift


class Evaluation:
    """Class to contain and simulate multiple games for a single snake. Possibly unnecessary now that only one game is
        executed for each snake."""

    def __init__(self, snake):
        self.snake = snake
        self.xorshift = XorShift()
        self.board = Board(self.xorshift)
        self.mouse = Mouse(self.board, self.xorshift)
        self.gamesnake = GameSnake(self.board, self.xorshift)
        self.game_number = 0
        self.current_game = None

        # Create neural network
        self.neural_net = SnakeNeuralNet(self.snake.encoding, self.board, self.gamesnake, self.mouse)

        # Create the first game
        self.start_next_game()

    def start_next_game(self):
        self.xorshift.state = [1921003811, 838877472]
        self.current_game = Game(self.snake, self.neural_net, self.gamesnake, self.board, self.mouse)
        self.game_number += 1

    def save_snake_statistics(self):
        self.snake.score = self.current_game.score
        self.snake.moves = self.current_game.moves
        self.snake.size = self.current_game.size


class Game:
    """Class to contain the logic and calculations for a single game of Snake."""

    def __init__(self, snake, neural_net, gamesnake, board, mouse):
        self.snake = snake
        self.neural_net = neural_net
        self.gamesnake = gamesnake
        self.board = board
        self.mouse = mouse
        self.moves = 0
        self.score = 0
        self.size = 1
        self.finished = False
        self.states_reached = []

        # Clear the board
        self.board.clear_board()

        # Randomize the gamesnake and food positions and add them to the board
        self.gamesnake.reset()
        self.gamesnake.randomize_position()

        self.mouse.randomize_position()

    def step(self):
        self.moves += 1
        self.score += self.size * self.size

        snakemove = self.neural_net.evaluate()

        self.gamesnake.move(snakemove)

        # Check if snake still alive
        if self.moves > 500:
            self.finished = True

        if self.board.is_piece_at(self.gamesnake.position):
            if self.gamesnake.position.x == self.mouse.position.x and self.gamesnake.position.y == self.mouse.position.y:
                self.size += 1
                self.states_reached = []
                if self.size < 64:
                    self.gamesnake.add_tail_piece()
                    self.gamesnake.update_board_position()
                    self.mouse.randomize_position(False)  # Do not hide previous food
                else:
                    self.finished = True
            else:
                self.finished = True
        else:
            self.gamesnake.update_board_position()

        # Save the current state of the board and snake
        if (self.board.board, self.gamesnake.position.x, self.gamesnake.position.y) in self.states_reached:
            self.finished = True
        self.states_reached.append(deepcopy((self.board.board, self.gamesnake.position.x, self.gamesnake.position.y)))
