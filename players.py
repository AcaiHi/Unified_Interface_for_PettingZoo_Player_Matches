# players.py
import numpy as np

class Player:
    def play(self, board):
        """
        Given the current board state, returns the chosen action.
        This is an abstract method to be implemented by different player types.
        """
        pass

class RandomPlayer(Player):
    def __init__(self, game):
        """
        Initializes the RandomPlayer.
        game: The game instance.
        """
        self.game = game

    def play(self, board):
        """
        Chooses a random valid action from the current board state.
        """
        valids = self.game.getValidMoves(board, 1)  # Get valid moves
        valid_actions = np.where(valids == 1)[0]  # Get the indices of valid actions
        return np.random.choice(valid_actions)  # Randomly choose one of the valid actions

class HumanPlayer(Player):
    def __init__(self, game):
        """
        Initializes the HumanPlayer.
        game: The game instance.
        """
        self.game = game

    def play(self, board):
        """
        Allows the human player to choose an action from the current board state.
        """
        valids = self.game.getValidMoves(board, 1)
        valid_actions = np.where(valids == 1)[0]
        print("Valid moves:", valid_actions)
        while True:
            action = int(input())
            if action in valid_actions:
                break
            else:
                print("Invalid move. Please try again.")
        return action

import tensorflow as tf
from tensorflow.keras import layers
from collections import deque
import random
import os

# 建立 DQN 
class DQNModel(tf.keras.Model):
    def __init__(self, action_size):
        super(DQNModel, self).__init__()
        self.flatten = layers.Flatten()
        self.dense1 = layers.Dense(128, activation='relu')
        self.dense2 = layers.Dense(128, activation='relu')
        self.out = layers.Dense(action_size, activation='linear')

    def call(self, x):
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return self.out(x)

class DQNPlayer(Player):
    def __init__(self, game, args):
        super().__init__()  # Initialize the base Player class
        self.game = game
        self.args = args
        self.action_size = game.getActionSize()
        self.model = self._build_model()
        self.memory = deque(maxlen=2000)  # Experience replay buffer
        self.batch_size = 64  # Batch size for training
        self.gamma = args.gamma  # Discount factor

    def _build_model(self):
        model = DQNModel(self.action_size)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.args.lr),
                      loss='mse')
        return model

    def play(self, board):
        """
        Given the board state, predict the action using the DQN model.
        """
        board_input = np.array(board).reshape(-1, self.game.board_x, self.game.board_y, 1)
        valid_moves = self.game.getValidMoves(board, 1)

        q_values = self.model.predict(board_input, verbose=0)[0]

        q_values[valid_moves == 0] = -float('inf')

        best_action = np.argmax(q_values)

        return best_action

    def remember(self, state, action, reward, next_state, done):
        """
        Store experiences in the replay buffer.
        """
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        """
        Train the model using experiences sampled from the replay buffer.
        """
        if len(self.memory) < self.batch_size:
            return  # Not enough samples to train

        # Sample a mini-batch from the memory
        minibatch = random.sample(self.memory, self.batch_size)

        # Prepare training data
        state_batch = []
        target_batch = []

        for state, action, reward, next_state, done in minibatch:
            state_input = np.array(state).reshape(-1, self.game.board_x, self.game.board_y, 1)
            next_state_input = np.array(next_state).reshape(-1, self.game.board_x, self.game.board_y, 1)

            # Predict Q-values for the current state
            q_values = self.model.predict(state_input, verbose=0)[0]

            if done:
                q_values[action] = reward
            else:
                # Predict Q-values for the next state
                next_q_values = self.model.predict(next_state_input, verbose=0)[0]
                q_values[action] = reward + self.gamma * np.amax(next_q_values)

            state_batch.append(state_input[0])
            target_batch.append(q_values)

        # Convert to numpy arrays for training
        state_batch = np.array(state_batch)
        target_batch = np.array(target_batch)

        # Train the model
        self.model.fit(state_batch, target_batch, epochs=100, verbose=0)
        print(model.summary())

    def load(self, filepath):
        filepath = f"{filepath}.weights.h5" if not filepath.endswith(".weights.h5") else filepath
        self.model.load_weights(filepath)

    def save(self, filepath):
        filepath = f"{filepath}.weights.h5" if not filepath.endswith(".weights.h5") else filepath
        self.model.save_weights(filepath)
