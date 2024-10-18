import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque
import random
import os

class Player:
    def play(self):
        """
        Abstract method to be implemented by different player types.
        """
        pass

class RandomPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self):
        valid_moves = self.game.getValidMoves()  # 從 game 取得有效行動
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
        self.target_model = self._build_model()  # Target network for stable Q-learning
        self.target_model.set_weights(self.model.get_weights())  # Sync weights initially
        self.memory = deque(maxlen=2000)
        self.batch_size = 64
        self.gamma = args.gamma
        self.epsilon = args.epsilon_start  # Epsilon for exploration
        self.epsilon_min = args.epsilon_min
        self.epsilon_decay = args.epsilon_decay
        self.previous_state = None
        self.previous_action = None
        
        if args.model_path:
            self.load(args.model_path)

    def _build_model(self):
        model = DQNModel(self.action_size)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.args.lr), loss='mse')
        return model

    def play(self):
        """
        Predict the action using epsilon-greedy strategy.
        This method also stores the previous state-action pair in memory when a new action is taken.
        """
        current_state = self.game.getCanonicalForm(self.game.getCurrentPlayer())  # 直接從 game 中取得棋盤狀態

        if self.previous_state is not None:
            # 如果前一個狀態存在，這意味著新的狀態將被記住
            reward = self.getReward()
            done = self.game.getGameResult() != 0
            self.remember(self.previous_state, self.previous_action, reward, current_state, done)

        valid_moves = self.game.getValidMoves()  # 獲取有效行動掩碼
        valid_actions = np.where(valid_moves == 1)[0]  # 獲取有效行動的索引

        if len(valid_actions) == 0:  # 如果沒有合法動作
            raise ValueError("No valid actions available!")

        if np.random.rand() <= self.epsilon:
            # 隨機選擇一個合法動作（探索）
            action = np.random.choice(valid_actions)
        else:
            # 預測行動（利用）
            state_input = np.array(current_state).reshape(-1, self.game.board_x, self.game.board_y, 1)
            q_values = self.model.predict(state_input, verbose=0)[0]
            q_values[valid_moves == 0] = -float('inf')  # 掩蓋無效行動
            action = np.argmax(q_values)

        # 更新上一步狀態和行動
        self.previous_state = current_state
        self.previous_action = action

        return action

    def getReward(self):
        """
        Calculates the reward based on the game state.
        """
        result = self.game.getGameResult()
        if result == 1:  # Player 1 wins
            return 1
        elif result == -1:  # Player 2 wins
            return -1
        elif result == 1e-4:  # Draw
            return 0.5
        return 0  # No reward for ongoing game

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
            return  # Not enough samples to train

        minibatch = random.sample(self.memory, self.batch_size)
        state_batch, target_batch = [], []

        for state, action, reward, next_state, done in minibatch:
            state_input = np.array(state).reshape(-1, self.game.board_x, self.game.board_y, 1)
            next_state_input = np.array(next_state).reshape(-1, self.game.board_x, self.game.board_y, 1)

            # Predict current state Q-values
            q_values = self.model.predict(state_input, verbose=0)[0]

            if done:
                q_values[action] = reward  # Terminal state
            else:
                # Predict next state Q-values using the target model
                next_q_values = self.target_model.predict(next_state_input, verbose=0)[0]
                q_values[action] = reward + self.gamma * np.amax(next_q_values)

            state_batch.append(state_input[0])
            target_batch.append(q_values)

        state_batch = np.array(state_batch)
        target_batch = np.array(target_batch)

        # Train the model
        self.model.fit(state_batch, target_batch, epochs=1, verbose=0)

        # Update epsilon (exploration rate)
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
