# Connect4Game 使用指南

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Issues](https://img.shields.io/github/issues/AcaiHi/Unified_Interface_for_PettingZoo_Player_Matches)

本指南介紹如何運行 Connect4Game，並提供主要功能的說明和範例程式碼。

> ⚠️ **Note:**  本項目使用 Python 3.8 及以上版本，如無法正常運行，請檢查您的 Python 版本是否兼容。

---

## 📁 1. 資料夾結構

每個同學的代碼均應放置在以學號命名的資料夾中，例如 CXXXXXXXXX 和 FXXXXXXXXX。結構如下：

```
.
├── Arena.py
├── CXXXXXXXXX
│   ├── __init__.py
│   ├── my.weights.h5
│   └── players.py
├── Dockerfile
├── FXXXXXXXXX
│   ├── __init__.py
│   ├── my.weights.h5
│   └── players.py
├── README.md
├── _players.py
├── connect4.py
├── dockerUse.md
├── environment.yaml
├── main.py
└── utils.py
```

- **CXXXXXXXXX** 和 **FXXXXXXXXX** 資料夾中應包含每位同學的 players.py 和 my.weights.h5（模型權重文件）。
- **Arena.py** 模塊負責玩家對戰邏輯。

> ℹ️ **Note:**  請確保每個資料夾中包含相應的模型權重文件，否則將無法進行玩家對戰。

---

## 🕹️ 2. Connect4Game 的主要功能

以下是對 Connect4Game 的所有功能描述，並附上範例程式碼來演示如何使用這些方法：

### 1. **init**(self)

- **功能**: 初始化 Connect4 遊戲環境，設置棋盤大小、動作數量，並初始化狀態緩存。
- **範例**:
  ```python
  game = Connect4Game()  # 初始化遊戲
  ```

> ⚠️ **Note:**  請在初始化遊戲後調用 `update_state_cache()` 方法以保證狀態的一致性。

### 2. update\_state\_cache(self)

- **功能**: 更新遊戲環境的狀態緩存，包括觀察值、動作掩碼、遊戲是否結束等信息。在每次執行 `env.step()` 和 `env.reset()` 後應該調用此方法。
- **範例**:
  ```python
  game.update_state_cache()  # 更新狀態緩存
  ```

### 3. getInitBoard(self)

- **功能**: 重置遊戲環境並返回初始空棋盤。棋盤是 6x7 的 2D 陣列，0 表示空格。
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

> ℹ️ **Note:**  請確保棋盤初始化後無其他殘留的狀態，以防影響遊戲流程。

### 4. getCurrentPlayer(self)

- **功能**: 返回當前玩家，1 表示玩家1，-1 表示玩家2。
- **範例**:
  ```python
  current_player = game.getCurrentPlayer()
  print(current_player)  # Output: 1 表示玩家1
  ```

### 5. getBoardSize(self)

- **功能**: 返回棋盤大小（行數與列數）。
- **範例**:
  ```python
  board_size = game.getBoardSize()
  print(board_size)  # Output: (6, 7)
  ```

### 6. getActionSize(self)

- **功能**: 返回可用動作的數量，即可以放置棋子的列數。
- **範例**:
  ```python
  action_size = game.getActionSize()
  print(action_size)  # Output: 7
  ```

### 7. getValidMoves(self)

- **功能**: 返回當前棋盤的有效動作，1 表示該列可以放置棋子，0 表示不能。
- **範例**:
  ```python
  valid_moves = game.getValidMoves()
  print(valid_moves)  # Output: [1 1 1 1 1 1 1] 表示所有列均可放置棋子
  ```

### 8. getNextState(self, action)

- **功能**: 執行指定動作並返回下一步棋盤狀態和下一位玩家。
- **範例**:
  ```python
  next_board, next_player = game.getNextState(2)  # 在第3列放置棋子
  print(next_board)
  print(next_player)  # Output: 玩家2進入下一回合
  ```

### 9. getGameResult(self)

- **功能**: 獲取遊戲結果：
  - 1: 玩家1勝利
  - -1: 玩家2勝利
  - 1e-4: 平局
  - 0: 遊戲尚未結束
- **範例**:
  ```python
  result = game.getGameResult()
  print(result)  # Output: 0 表示遊戲尚未結束
  ```

### 10. getCanonicalForm(self, player)

- **功能**: 返回當前玩家的棋盤狀態，棋盤的值乘以當前玩家（1 或 -1），以便於不同玩家看到各自的視角。
- **範例**:
  ```python
  board = game.getCanonicalForm(game.getCurrentPlayer())
  print(board)  # 顯示當前玩家的棋盤
  ```

### 11. display(self)

- **功能**: 顯示當前棋盤狀態，X 表示玩家1，O 表示玩家2，. 表示空格。
- **範例**:
  ```python
  game.display()
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

### 12. setEnvState(self, board, player)

- **功能**: 設置環境為指定的棋盤狀態和玩家，通過回放棋盤上的每一步操作來重現當前局面。
- **範例**:
  ```python
  board = np.array([
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, -1, 0, 0],
      [0, 0, 0, 1, -1, 0, 0]
  ])
  game.setEnvState(board, 1)  # 設置當前狀態為玩家1的回合
  game.display()
  ```

> ⚠️ **Note:**  在使用 `setEnvState()` 時，確保棋盤狀態合法且與遊戲邏輯一致，以避免出現異常情況。

---

## 👤 3. Player 的簡要介紹

main.py 需要兩個自定義 Player，這些 Player 必須有 `play()` 方法，用於執行遊戲中的行動。

### 1. RandomPlayer

- **說明**: 隨機選擇有效動作。
- **範例**:
  ```python
  class RandomPlayer(Player):
      def __init__(self, game):
          self.game = game

      def play(self):
          valid_moves = self.game.getValidMoves()
          return np.random.choice(np.where(valid_moves == 1)[0])
  ```

> ⚠️ **Note:**  `RandomPlayer` 不會考慮遊戲策略，因此只能用於測試隨機對手的行為。

### 2. DQNPlayer

- **說明**: 基於深度強化學習的 DQN 模型 Player，需要設定一些參數並具備 `play()` 方法。引入參數時，可以參考 `model_path` 的寫法來指定模型的路徑。

- **設定參數範例**:

  ```python
  DQNPlayer_args = dotdict({
      'lr': 0.001,
      'gamma': 0.95,
      'epsilon_start': 1.0,
      'epsilon_min': 0.01,
      'epsilon_decay': 0.5,
      'model_path': './my.weights.h5'  # 模型權重的路徑
  })
  ```

> ⚙️ **注意**: 請確保在訓練後保存模型，方便後續載入進行對戰。

### DQN Player 的建構注意事項和如何訓練

**如何設置 DQN Player：**

1. **定義參數 (`DQNPlayer_args`)**:
   - 首先，定義一些參數如學習率 (`lr`)、折扣因子 (`gamma`) 和探索設置 (`epsilon_start`、`epsilon_min`、`epsilon_decay`)。這些設置對於控制 DQN 模型的學習行為至關重要。

2. **創建模型類 (`DQNModel`)**:
   - `DQNModel` 類定義了用於近似每個動作的 Q 值的神經網絡架構。這個網絡由多個全連接層和一個輸出層組成，用於預測動作值。

3. **實例化 DQN Player (`DQNPlayer`)**:
   - 使用 `DQNPlayer` 類與環境進行交互。Player 類保持主模型 (`model`) 和目標模型 (`target_model`) 以穩定訓練過程。
   - 使用重放緩衝區 (`memory`) 存儲經驗，並通過隨機批次的抽樣來進行學習。
   - `play` 方法是每個 Player 的關鍵部分，該方法使用 epsilon-greedy 策略來平衡探索和利用。

4. **訓練與目標更新**:
   - 訓練過程涉及從重放緩衝區中抽樣經驗，使用目標網絡計算目標 Q 值，並使主模型擬合當前 Q 值和目標 Q 值之間的損失。
   - 目標模型會定期更新，以匹配主模型的權重，從而幫助穩定學習過程。

5. **保存與加載模型**:
   - `save` 和 `load` 方法用於將模型權重保存到文件中，並在需要時將其加載回來。

**訓練 DQN Player：**

在訓練 DQN Player 時，可以使用 `RandomPlayer` 作為對手來積累經驗。

```python
from tqdm import tqdm

# 初始化對戰環境
random_player = RandomPlayer(game)
arena = Arena(player1, random_player, game)

# 訓練遊戲次數
num_training_games = 20  # Number of games to play for training
print(f"Training the DQNPlayer with {num_training_games} games...")

# 開始訓練
for _ in tqdm(range(num_training_games)):
    arena.playGame()  # Play games to accumulate experiences for training
    player1.train()  # Train the DQN model after each game
    player1.update_target_model()  # Update the target model periodically
```

> ⚠️ **Note:** 在訓練過程中，應定期保存模型權重，以便在發生意外中斷時不會丟失訓練進度。

---

## 🚀 4. 運行 main.py

main.py 會調用兩位同學的 DQNPlayer 進行對戰。代碼中的 CXXXXXXXXX 和 FXXXXXXXXX 對應同學的代碼，具體如下：

- **CXXXXXXXXX** 和 **FXXXXXXXXX** 資料夾分別包含每位同學的 `players.py` 文件和 `DQNPlayer_args` 配置。
- 在運行對戰時，`main.py` 會初始化每位同學的 DQNPlayer 並使用專屬的權重和參數，最後執行一系列遊戲來決定勝負。

### 更詳細的運行教學

1. **初始化環境變量**: 在運行 `main.py` 前，請確保環境變量已正確設置，以避免 TensorFlow 輸出多餘的日誌。

   ```python
   import os
   os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 僅顯示錯誤級別的日誌
   ```

2. **導入必要模塊**: 請確保正確導入所需的模塊。

   ```python
   import sys
   from Arena import Arena
   ```

3. **初始化遊戲和玩家**:

   - 使用 `connect4.py` 初始化 Connect4 遊戲環境。
   - 從資料夾中導入 CXXXXXXXXX 和 FXXXXXXXXX 各自的 DQNPlayer。

   ```python
   from connect4 import Connect4Game
   game = Connect4Game()

   from CXXXXXXXXX.players import DQNPlayer as C_DQNPlayer
   from CXXXXXXXXX.players import DQNPlayer_args as args_in_C

   from FXXXXXXXXX.players import DQNPlayer as F_DQNPlayer
   from FXXXXXXXXX.players import DQNPlayer_args as args_in_F

   # 初始化 CXXXXXXXXX 的 DQNPlayer，並使用其專屬的 args
   player1 = C_DQNPlayer(game, args_in_C)

   # 初始化 FXXXXXXXXX 的 DQNPlayer，並使用其專屬的 args
   player2 = F_DQNPlayer(game, args_in_F)
   ```

4. **設置對戰並運行**:

   - 利用 `Arena` 來設置兩個玩家的對戰，並進行 100 場遊戲來評估雙方的表現。

   ```python
   # 設定對戰
   arena = Arena(player1, player2, game)

   # 開始對戰
   num_games = 100
   print(f"Starting {num_games} games between C_DQNPlayer and F_DQNPlayer...")
   results = arena.playGames(num_games, verbose=False)
   ```

5. **顯示結果**:

   - 顯示對戰的最終結果，包括每個玩家的勝場數以及平局數。

   ```python
   # 顯示結果
   print(f"\nResults after {num_games} games:")
   print(f"C_DQNPlayer wins: {results[0]}")
   print(f"F_DQNPlayer wins: {results[1]}")
   print(f"Draws: {results[2]}")
   ```

6. **完整程式碼**: 以下是 main.py 的完整程式碼供參考：

   ```python
   import os
   import sys
   from Arena import Arena

   os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

   def main():
       from connect4 import Connect4Game
       game = Connect4Game()
       
       from CXXXXXXXXX.players import DQNPlayer as C_DQNPlayer
       from CXXXXXXXXX.players import DQNPlayer_args as args_in_C

       from FXXXXXXXXX.players import DQNPlayer as F_DQNPlayer
       from FXXXXXXXXX.players import DQNPlayer_args as args_in_F

       # 初始化 CXXXXXXXXX 的 DQNPlayer，並使用其專屬的 args
       player1 = C_DQNPlayer(game, args_in_C)

       # 初始化 FXXXXXXXXX 的 DQNPlayer，並使用其專屬的 args
       player2 = F_DQNPlayer(game, args_in_F)

       # 設定對戰
       arena = Arena(player1, player2, game)

       # 開始對戰
       num_games = 100
       print(f"Starting {num_games} games between C_DQNPlayer and F_DQNPlayer...")
       results = arena.playGames(num_games, verbose=False)

       # 顯示結果
       print(f"\nResults after {num_games} games:")
       print(f"C_DQNPlayer wins: {results[0]}")
       print(f"F_DQNPlayer wins: {results[1]}")
       print(f"Draws: {results[2]}")

   if __name__ == "__main__":
       main()
   ```

> ⚠️ **Note:**  在運行對戰前，請檢查模型是否已成功加載，避免因模型未加載導致的錯誤。

---

## 🖥️ 5. Docker 與環境設定

- **啟用 GPU 支援**：

  ```bash
  docker run --gpus all my_connect4_image
  ```

- **環境配置**：

  ```bash
  conda env create -f environment.yaml
  ```

> ℹ️ **Note:**  請確保您的 Docker 和 Conda 已安裝正確，並且有適當的權限運行上述命令。

