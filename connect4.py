# connect4.py
import numpy as np
from pettingzoo.classic import connect_four_v3

class Connect4Game:
    def __init__(self):
        """
        Initializes the Connect4 game environment using PettingZoo.
        Sets up the game board dimensions and action size based on the observation space.
        """
        self.env = connect_four_v3.env()  # Initialize the Connect Four environment
        self.env.reset()  # Reset the environment to start a new game
        self.action_size = self.env.action_space(self.env.agents[0]).n  # Number of possible actions
        obs_shape = self.env.observation_space(self.env.agents[0]).spaces['observation'].shape  # Get board shape
        self.board_x = obs_shape[0]  # Number of rows in the board
        self.board_y = obs_shape[1]  # Number of columns in the board
        self.num_players = len(self.env.agents)  # Number of players (typically 2)

    def getInitBoard(self):
        """
        Resets the game environment and returns the initial empty game board.
        The board is represented as a 2D array where each cell is either empty (0),
        occupied by player 1 (1), or occupied by player 2 (-1).
        """
        self.env.reset()  # Reset the environment
        observation = self.env.observe(self.env.agent_selection)['observation']  # Get the observation for the current player
        board = observation[:, :, 0] - observation[:, :, 1]  # Calculate the board state from the observation
        return board

    def getBoardSize(self):
        """
        Returns the size of the game board (rows, columns).
        """
        return (self.board_x, self.board_y)

    def getActionSize(self):
        """
        Returns the number of possible actions (columns where a piece can be placed).
        """
        return self.action_size

    def getNextState(self, board, player, action):
        """
        Given the current board, player, and action, returns the next state of the board and the next player.
        Simulates dropping a piece into the specified column (action).
        """
        next_board = np.copy(board)  # Copy the board to simulate the next state
        for row in range(self.board_x - 1, -1, -1):  # Start from the bottom row
            if next_board[row, action] == 0:  # Find the first empty spot in the column
                next_board[row, action] = player  # Place the player's piece in the spot
                break
        next_player = -player  # Switch to the other player
        return next_board, next_player

    def getValidMoves(self, board, player):
        """
        Returns a list of valid moves for the current board.
        A move is valid if the top cell of the column is empty (i.e., 0).
        """
        valid_moves = [1 if board[0, col] == 0 else 0 for col in range(self.board_y)]  # Check if the top row is empty for each column
        return np.array(valid_moves)

    def getGameEnded(self, board, player):
        """
        Checks if the game has ended by evaluating the current board for a win, loss, or draw.
        Returns 1 if the current player wins, -1 if the other player wins, a small value for a draw, and 0 otherwise.
        """
        # Check horizontal win
        for row in range(self.board_x):
            for col in range(self.board_y - 3):
                if abs(sum(board[row, col:col+4])) == 4:  # Check 4 consecutive pieces in a row
                    return player

        # Check vertical win
        for row in range(self.board_x - 3):
            for col in range(self.board_y):
                if abs(sum(board[row:row+4, col])) == 4:  # Check 4 consecutive pieces in a column
                    return player

        # Check diagonal wins
        for row in range(self.board_x - 3):
            for col in range(self.board_y - 3):
                # Check main diagonal (\)
                if abs(sum(board[range(row, row+4), range(col, col+4)])) == 4:
                    return player
                # Check anti-diagonal (/)
                if abs(sum(board[range(row, row+4), range(col+3, col-1, -1)])) == 4:
                    return player

        # Check for a draw (if no empty spaces)
        if np.all(board != 0):
            return 1e-4  # Draw

        return 0  # Game not ended

    def getCanonicalForm(self, board, player):
        """
        Returns the canonical form of the board for the current player.
        The canonical form is the board as seen from the perspective of the current player.
        """
        return board * player  # Multiply board by player to get the canonical form

    def getSymmetries(self, board, pi):
        """
        Returns symmetrical versions of the board and policy vector (pi).
        Flips the board and policy horizontally to generate symmetrical states.
        """
        pi_board = np.reshape(pi, (self.board_y,))  # Reshape the policy vector to match the board dimensions
        l = []

        # Original board and policy
        l.append((board, pi))

        # Flipped board and policy
        flipped_board = np.fliplr(board)  # Flip the board horizontally
        flipped_pi = np.fliplr(np.reshape(pi_board, (1, self.board_y))).flatten()  # Flip the policy vector
        l.append((flipped_board, flipped_pi))

        return l

    def stringRepresentation(self, board):
        """
        Returns a string representation of the board, useful for caching.
        """
        return board.tobytes()

    def display(self, board):
        """
        Displays the current board state in a human-readable format.
        'X' represents player 1, 'O' represents player 2, and '.' represents an empty space.
        """
        print(" -----------------------")
        for y in range(self.board_x):
            print("|", end="")
            for x in range(self.board_y):
                piece = board[y][x]
                if piece == 1:
                    print(" X ", end="")
                elif piece == -1:
                    print(" O ", end="")
                else:
                    print(" . ", end="")
            print("|")
        print(" -----------------------")
