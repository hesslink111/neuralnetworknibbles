# Neural Network Nibbles - Genetically evolved neural networks capable of playing Snake

Created by William Pease | [willpease.com](http://willpease.com/resume.html)

Neural Network Nibbles (NNN) is an environment for evolving simulated brains that play Snake. NNN creates a pool of genetic encodings, which map to neural networks, and then evaluates each based on their performance in a game of Snake. The best genes are added to the gene pool and are used to create the next generation of simulated snakes.

## Purpose

- Evaluate artificial intelligence in a game of Snake
- Create neural networks to simulate a snake brain
- Use a genetic algorithm to evolve snakes
- Find the highest scoring artificially evolved snake

## Neural Network

The neural network for a snake is a three-layer feed-forward graph of neurons, with each node of each layer connected to each node of the previous layer by synapses. Neurons aggregate signals from the previous layer, while synapses apply a weight in the range of (-1, 1) to the signal they carry from one neuron to another.

The first layer of neurons consists of inputs based on the state of each position on the game board. An empty space is represented as a 0, a snake segment is a -1, and a mouse is a 1. The inputs on this layer are configured to match the perspective of the simulated snake. As the snake moves, its perspective stays centered on its head, and rotates to match its orientation.

The second/hidden layer contains sigmoid neurons, who sum the input of their synapses and apply the function (1 / ( 1 + e^-k )), which results in a new output in the range of (0, 1).

The final layer has three neurons representing the movement decision made by the snake. The possible moves are to turn right, left, or continue straight.

The first layer of the network is 256, the second is 130, and the third is 3 neurons, so the number of synapses is 256 * 130 + 130 * 3, or 33670. Each synapse is given a weight in the range (-1, 1) based on the encoding generated by the genetic algorithm.

## Genetic Algorithm

In the beginning, 100 random genetic sequences are created and added to the gene pool. The first generation generation of snakes is created through a random selection and crossover process. These genes are then mutated slightly, and then passed to the simulation engine to be evaluated. After each generation of snakes is evaluated, the gene pool is updated to include the highest scoring snakes.

##### Selection

The selection process for creating a new gene sequence is based on a weighted lottery. Higher scoring snakes from the gene pool are given more tickets in the lottery, and therefore have a higher chance of having their traits passed on to new snakes.

##### Crossover

For each new snake, segments of genetic sequences are copied from the snakes in the gene pool. The size of each segment taken is based on the number of synapses connected to a given neuron. This ensures that traits of high-performing snakes are preserved and transfered to newer generations.

##### Mutation

There is a 5% chance for any given value in a snake's genetic encoding to become randomized. This is low enough so that a new snake may maintain the characteristics of past generations, and high enough that snakes are able to evolve.

## Evaluation

Each generated snake is simulated in an 8x8 game. Every game is procedurally generated based on the same seed value, so each snake will have the oportunity to play the same game. This optimization allows us to compare evaluations based on a single game rather than an average.

The rules of the simulation are the same as the rules of Snake. The simulated snake must avoid moving beyond the boundaries of the board and colliding with obstacles, including colliding with itself. The goal of the game is for the snake to eat as many mice as possible. To deter certain behavior, the simulation is terminated if the snake moves such that a given state of the game board is ever repeated.

The snake is evaluated based on its score in the game. To encourage movement and staying within the boundaries, points are given for each successful move. To encourage growth, the amount of points given for each move is based on the square of the length of the snake during that move.
