import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque
import random
import os
from utils import dotdict

class Player:
    def play(self):
        """
        Abstract method to be implemented by different player types.
        The `play` method must be implemented in each subclass to define specific behavior.
        """
        pass

class RandomPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self):
        valid_moves = self.game.getValidMoves()
        valid_actions = np.where(valid_moves == 1)[0]
        return np.random.choice(valid_actions)

class HumanPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self):
        valid_moves = self.game.getValidMoves()
        valid_actions = np.where(valid_moves == 1)[0]
        print("Valid moves:", valid_actions)
        while True:
            action = int(input("Choose your action: "))
            if action in valid_actions:
                break
            else:
                print("Invalid move. Please try again.")
        return action

"""
How to set up a DQN Player:

1. **Define Parameters (`DQNPlayer_args`)**:
   - First, define the parameters like learning rate (`lr`), discount factor (`gamma`), and exploration settings (`epsilon_start`, `epsilon_min`, `epsilon_decay`). These settings are crucial for controlling the learning behavior of the DQN model.

2. **Create the Model Class (`DQNModel`)**:
   - The `DQNModel` class defines the architecture of the neural network that will be used to approximate the Q-values for each action. This consists of multiple fully connected layers and an output layer to predict the action values.

3. **Instantiate the DQN Player (`DQNPlayer`)**:
   - Use the `DQNPlayer` class to interact with the environment. The player class maintains the main model (`model`) and a target model (`target_model`) to stabilize training.
   - It uses a replay buffer (`memory`) to store experiences and learn from them by sampling random batches during training.
   - The `play` method is a crucial part of each player and must be implemented. It decides actions using an epsilon-greedy strategy to balance exploration and exploitation.

4. **Training and Target Update**:
   - The training process involves sampling experiences from the replay buffer, calculating target Q-values using the target network, and fitting the main model to minimize the loss between current Q-values and target Q-values.
   - The target model is updated periodically to match the weights of the main model, which helps stabilize learning.

5. **Save and Load Model**:
   - The `save` and `load` methods are used to save the model weights to a file and load them back when needed.
"""


DQNPlayer_args = dotdict({
    'lr': 0.001,
    'gamma': 0.95,
    'epsilon_start': 1.0,
    'epsilon_min': 0.01,
    'epsilon_decay': 0.5,
    # 'model_path': './my.weights.h5'
})

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
        super().__init__()
        self.game = game
        self.args = args
        self.action_size = game.getActionSize()
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())
        self.memory = deque(maxlen=2000)
        self.batch_size = 64
        self.gamma = args.gamma
        self.epsilon = args.epsilon_start
        self.epsilon_min = args.epsilon_min
        self.epsilon_decay = args.epsilon_decay
        self.previous_state = None
        self.previous_action = None

    def _build_model(self):
        model = DQNModel(self.action_size)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.args.lr), loss='mse')
        return model

    def play(self):
        """
        Predict the next action using epsilon-greedy strategy.
        """
        current_state = self.game.getCanonicalForm(self.game.getCurrentPlayer())

        if self.previous_state is not None:
            reward = self.getReward()
            done = self.game.getGameResult() != 0
            self.remember(self.previous_state, self.previous_action, reward, current_state, done)

        valid_moves = self.game.getValidMoves()
        valid_actions = np.where(valid_moves == 1)[0]

        if len(valid_actions) == 0:
            raise ValueError("No valid actions available!")

        if np.random.rand() <= self.epsilon:
            action = np.random.choice(valid_actions)  # Random action (exploration)
        else:
            state_input = np.array(current_state).reshape(-1, self.game.board_x, self.game.board_y, 1)
            q_values = self.model.predict(state_input, verbose=0)[0]
            q_values[valid_moves == 0] = -float('inf')  # Mask invalid actions
            action = np.argmax(q_values)

        self.previous_state = current_state
        self.previous_action = action

        return action

    def getReward(self):
        """
        Calculates the reward based on the game state.
        """
        result = self.game.getGameResult()
        if result == 1:
            return 1  # Win
        elif result == -1:
            return -1  # Loss
        elif result == 1e-4:
            return 0.5  # Draw
        return 0  # Ongoing

    def remember(self, state, action, reward, next_state, done):
        """
        Store experiences in the replay buffer.
        """
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        """
        Train the DQN model using experiences sampled from the replay buffer.
        """
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        state_batch, target_batch = [], []

        for state, action, reward, next_state, done in minibatch:
            state_input = np.array(state).reshape(-1, self.game.board_x, self.game.board_y, 1)
            next_state_input = np.array(next_state).reshape(-1, self.game.board_x, self.game.board_y, 1)

            q_values = self.model.predict(state_input, verbose=0)[0]

            if done:
                q_values[action] = reward
            else:
                next_q_values = self.target_model.predict(next_state_input, verbose=0)[0]
                q_values[action] = reward + self.gamma * np.amax(next_q_values)

            state_batch.append(state_input[0])
            target_batch.append(q_values)

        state_batch = np.array(state_batch)
        target_batch = np.array(target_batch)

        self.model.fit(state_batch, target_batch, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        """
        Update the target model weights with the trained model's weights.
        """
        self.target_model.set_weights(self.model.get_weights())

    def load(self, filepath):
        filepath = f"{filepath}.weights.h5" if not filepath.endswith(".weights.h5") else filepath
        self.model.load_weights(filepath)

    def save(self, filepath):
        filepath = f"{filepath}.weights.h5" if not filepath.endswith(".weights.h5") else filepath
        self.model.save_weights(filepath)