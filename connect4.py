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
        self.current_player = self.env.agent_selection  # Keep track of the current player

        # 緩存環境狀態信息
        self.observation = None
        self.action_mask = None
        self.termination = False
        self.truncation = False
        self.reward = 0
        self.info = {}

        # 保存當前的棋盤狀態
        self.board = np.zeros((self.board_x, self.board_y))  # 初始時棋盤是空的

        # 初始化緩存的觀察值和動作掩碼
        self.update_state_cache()

    def update_state_cache(self):
        """
        Updates the cached observation, action mask, termination, truncation, and info.
        This method should be called after every env.step() and env.reset().
        """
        self.observation, self.reward, self.termination, self.truncation, self.info = self.env.last()
        if not (self.termination or self.truncation):
            self.action_mask = np.array(self.observation['action_mask'])
        else:
            self.action_mask = np.zeros(self.action_size)  # No valid moves if game is over

        # 更新棋盤狀態
        self.board = self.observation['observation'][:, :, 0] - self.observation['observation'][:, :, 1]
        self.current_player = self.env.agent_selection

    def getInitBoard(self):
        """
        Resets the game environment and returns the initial empty game board.
        """
        self.env.reset()  # Reset the environment
        self.update_state_cache()  # Update cached state
        return self.board

    def getCurrentPlayer(self):
        """
        Returns the current player as 1 (Player 1) or -1 (Player 2).
        """
        return 1 if self.current_player == self.env.agents[0] else -1

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

    def getValidMoves(self):
        """
        Returns the list of valid moves based on the current environment state.
        No need to pass the board as it's now handled internally.
        """
        return self.action_mask

    def getNextState(self, action):
        """
        Executes the given action and returns the next board state and the next player.
        """
        self.env.step(action)  # Perform action
        self.update_state_cache()  # Update cached state
        next_board = self.board  # Now we can just return the cached board
        next_player = self.getCurrentPlayer()
        return next_board, next_player

    def getGameResult(self):
        """
        Returns the result of the game:
        1 if Player 1 wins, -1 if Player 2 wins, 1e-4 for a draw, and 0 if not ended.
        """
        if self.termination or self.truncation:
            player_0_reward = self.env.rewards['player_0']
            player_1_reward = self.env.rewards['player_1']
            # print(f"====================Game result: { 'Player 1' if player_0_reward == 1 else 'Player 2' if player_1_reward == 1 else 'Draw' }!!!====================")
            if player_0_reward == 1:
                return 1  # Player 1 wins
            elif player_1_reward == 1:
                return -1  # Player 2 wins
            else:
                return 1e-4  # Draw
        return 0  # Game not ended

    def getCanonicalForm(self, player):
        """
        Returns the canonical form of the board for the current player.
        """
        return self.board * player  # Simply return the board multiplied by player

    def display(self):
        board = self.getCanonicalForm(self.getCurrentPlayer())
        """
        Displays the current board state.
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

    def setEnvState(self, board, player):
        """
        Simulates the environment to match a given board and player.
        This method replays all the moves from an empty state to reach the desired state.
        """
        self.env.reset()  # Reset the environment to the initial state
        self.update_state_cache()

        # Set the initial current player to 'player_1' or 'player_2' based on the game state
        expected_player = 'player_1' if player == 1 else 'player_2'

        # Replay the moves based on the provided board
        for col in range(self.board_y):
            col_values = board[:, col]
            for row in range(self.board_x - 1, -1, -1):
                if col_values[row] != 0:  # If a piece is placed in this column
                    # Before taking action, ensure the correct player is active
                    if self.env.agent_selection != ('player_1' if col_values[row] == 1 else 'player_2'):
                        self.env.step(None)  # Skip the current player's turn to match the expected player
                    self.env.step(col)  # Simulate the move
                    self.update_state_cache()

        # Set the current player
        self.current_player = expected_player
        self.env.agent_selection = self.current_player
        self.update_state_cache()

