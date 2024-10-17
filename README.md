### 1. Connect4Game 的可用函式

`Connect4Game` 提供了各種操作遊戲的方法，這裡列出了一些常用的函式並附有範例輸出。

#### `getInitBoard(self)`
- **功能**: 重置遊戲並返回初始空棋盤，棋盤為 2D 陣列，0 表示空格，1 表示玩家1，-1 表示玩家2。
- **範例**:
  ```python
  board = game.getInitBoard()
  print(board)
  # Output: 
  # [[0 0 0 0 0 0 0]
  #  [0 0 0 0 0 0 0]
  #  [0 0 0 0 0 0 0]
  #  [0 0 0 0 0 0 0]
  #  [0 0 0 0 0 0 0]
  #  [0 0 0 0 0 0 0]]
  ```

#### `getBoardSize(self)`
- **功能**: 返回棋盤大小（行數與列數）。
- **範例**:
  ```python
  board_size = game.getBoardSize()
  print(board_size)
  # Output: (6, 7)
  ```

#### `getActionSize(self)`
- **功能**: 返回可用動作數量（可放置棋子的列數）。
- **範例**:
  ```python
  action_size = game.getActionSize()
  print(action_size)
  # Output: 7
  ```

#### `getNextState(self, board, player, action)`
- **功能**: 給定棋盤、玩家和動作，返回下一步的棋盤狀態和下一位玩家。
- **範例**:
  ```python
  next_board, next_player = game.getNextState(board, 1, 2)
  print(next_board)
  # Output: 在第二列新增了一個玩家1的棋子
  ```

#### `getValidMoves(self, board, player)`
- **功能**: 返回當前棋盤的有效動作（哪些列可以放置棋子）。
- **範例**:
  ```python
  valid_moves = game.getValidMoves(board, 1)
  print(valid_moves)
  # Output: [1 1 1 1 1 1 1]  # 所有列均可放置棋子
  ```

#### `getGameEnded(self, board, player)`
- **功能**: 判斷遊戲是否結束，返回：
  - `1`: 當前玩家勝利
  - `-1`: 對手勝利
  - `1e-4`: 平局
  - `0`: 遊戲尚未結束
- **範例**:
  ```python
  result = game.getGameEnded(board, 1)
  print(result)
  # Output: 0  # 遊戲尚未結束
  ```

#### `display(self, board)`
- **功能**: 顯示當前棋盤狀態，`X` 表示玩家1，`O` 表示玩家2，`.` 表示空格。
- **範例**:
  ```python
  game.display(board)
  # Output:
  #  -----------------------
  # | .  .  .  .  .  .  .  |
  # | .  .  .  .  .  .  .  |
  # | .  .  .  .  .  .  .  |
  # | .  .  .  .  .  .  .  |
  # | .  .  .  .  .  .  .  |
  # | .  .  .  .  .  .  .  |
  #  -----------------------
  ```

### 2. 如何使用 Player

要在 Connect 4 中運行自定義的 Player，需要先繼承 `Player` 類別並實作 `play` 方法。以下是使用 `RandomPlayer` 和 `HumanPlayer` 的範例：

#### RandomPlayer
隨機選擇一個合法動作：
```python
class RandomPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        valid_actions = np.where(valid_moves == 1)[0]
        return np.random.choice(valid_actions)
```

#### HumanPlayer
讓使用者手動選擇動作：
```python
class HumanPlayer(Player):
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        valid_actions = np.where(valid_moves == 1)[0]
        print("Valid moves:", valid_actions)
        while True:
            action = int(input("Choose a move: "))
            if action in valid_actions:
                break
            print("Invalid move. Try again.")
        return action
```

### 3. 深度強化學習的 Player 封裝

如果要使用深度強化學習的 Player，例如 `DQNPlayer`，需要理解以下幾個要點：
1. **模型架構**：需要定義神經網路模型，用於預測每個動作的 Q 值。這個架構需要根據棋盤狀態輸入進行預測。
2. **超參數設置**：必須設置學習率（`lr`）、折扣因子（`gamma`）等超參數，用來調整模型訓練的行為。
3. **模型存取**：模型的參數可以通過檔案保存與載入，方便後續訓練與推理。

以下是簡單的封裝範例，涵蓋如何初始化、決策、保存與載入模型：
```python
class DQNPlayer(Player):
    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.model = self._build_model()

    def _build_model(self):
        # 定義 DQN 模型架構
        model = DQNModel(self.game.getActionSize())
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=self.args.lr),
                      loss='mse')
        return model

    def play(self, board):
        board_input = np.array(board).reshape(-1, self.game.board_x, self.game.board_y, 1)
        valid_moves = self.game.getValidMoves(board, 1)
        q_values = self.model.predict(board_input, verbose=0)[0]
        q_values[valid_moves == 0] = -float('inf')
        best_action = np.argmax(q_values)
        return best_action

    def save_model(self, filepath):
        # 保存模型參數
        self.model.save_weights(filepath)

    def load_model(self, filepath):
        # 載入已保存的模型參數
        self.model.load_weights(filepath)
```

### 4. 如何進行對戰

學生可以通過以下範例進行自定義 Player 之間的對戰：

```python
from players import DQNPlayer, RandomPlayer
from Arena import Arena
from connect4 import Connect4Game

def main():
    game = Connect4Game()

    # 設置玩家
    args = dotdict({'lr': 0.001, 'gamma': 0.95, 'epsilon': 0.1})
    dqn_player = DQNPlayer(game, args)
    dqn_player.load('./dqn_model.weights.h5')
    opponent_player = RandomPlayer(game)

    # 開始對戰
    arena = Arena(dqn_player, opponent_player, game)
    results = arena.playGames(20)

    # 顯示結果
    print(f"DQNPlayer wins: {results[0]}")
    print(f"RandomPlayer wins: {results[1]}")
    print(f"Draws: {results[2]}")

if __name__ == "__main__":
    main()
```


PS. Dockerfile 可以啟用GPU支援，但是需要在主機上安裝NVIDIA Container Toolkit (cuda>=12.4)，並且在執行docker時加上`--gpus all`參數。

PS. environment.yaml 放了一些常用的套件可以直接用 conda 創建環境，`conda env create -f environment.yaml`。