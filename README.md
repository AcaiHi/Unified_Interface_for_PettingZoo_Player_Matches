# Connect4Game 使用指南
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Issues](https://img.shields.io/github/issues/AcaiHi/Unified_Interface_for_PettingZoo_Player_Matches)

本指南介紹 `Connect4Game` 的可用函式、資料夾結構以及如何運行 `main.py` 進行 Connect 4 遊戲的對戰。

## 1. 資料夾結構

每個同學的代碼均應放置在以學號命名的資料夾中，例如 `CXXXXXXXXX` 和 `FXXXXXXXXX`。每個資料夾應該包含以下內容：

```
.
├── Arena.py
├── CXXXXXXXXX
│   ├── __init__.py
│   ├── my.weights.h5
│   └── players.py
├── Dockerfile
├── FXXXXXXXXX
│   ├── __init__.py
│   ├── my.weights.h5
│   └── players.py
├── README.md
├── _players.py
├── connect4.py
├── dockerUse.md
├── environment.yaml
├── main.py
└── utils.py
```

- `CXXXXXXXXX` 和 `FXXXXXXXXX` 資料夾中應包含每位同學的 `players.py` 和相應的權重文件 `my.weights.h5`，供 `main.py` 對戰使用。
- `Arena.py` 是用於執行玩家對戰的模塊，與 `main.py` 一同使用。

## 2. Connect4Game 的主要功能

以下是對 `Connect4Game` 的所有功能描述，並附上範例程式碼來演示如何使用這些方法：

### 1. `__init__(self)`
- **功能**: 初始化 Connect4 遊戲環境，設置棋盤大小、動作數量，並初始化狀態緩存。
- **範例**:
  ```python
  game = Connect4Game()  # 初始化遊戲
  ```

### 2. `update_state_cache(self)`
- **功能**: 更新遊戲環境的狀態緩存，包括觀察值、動作掩碼、遊戲是否結束等信息。在每次執行 `env.step()` 和 `env.reset()` 後應該調用此方法。
- **範例**:
  ```python
  game.update_state_cache()  # 更新狀態緩存
  ```

### 3. `getInitBoard(self)`
- **功能**: 重置遊戲環境並返回初始空棋盤。棋盤是 6x7 的 2D 陣列，`0` 表示空格。
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

### 4. `getCurrentPlayer(self)`
- **功能**: 返回當前玩家，`1` 表示玩家1，`-1` 表示玩家2。
- **範例**:
  ```python
  current_player = game.getCurrentPlayer()
  print(current_player)  # Output: 1 表示玩家1
  ```

### 5. `getBoardSize(self)`
- **功能**: 返回棋盤大小（行數與列數）。
- **範例**:
  ```python
  board_size = game.getBoardSize()
  print(board_size)  # Output: (6, 7)
  ```

### 6. `getActionSize(self)`
- **功能**: 返回可用動作的數量，即可以放置棋子的列數。
- **範例**:
  ```python
  action_size = game.getActionSize()
  print(action_size)  # Output: 7
  ```

### 7. `getValidMoves(self)`
- **功能**: 返回當前棋盤的有效動作，1 表示該列可以放置棋子，0 表示不能。
- **範例**:
  ```python
  valid_moves = game.getValidMoves()
  print(valid_moves)  # Output: [1 1 1 1 1 1 1] 表示所有列均可放置棋子
  ```

### 8. `getNextState(self, action)`
- **功能**: 執行指定動作並返回下一步棋盤狀態和下一位玩家。
- **範例**:
  ```python
  next_board, next_player = game.getNextState(2)  # 在第3列放置棋子
  print(next_board)
  print(next_player)  # Output: 玩家2進入下一回合
  ```

### 9. `getGameResult(self)`
- **功能**: 獲取遊戲結果：
  - `1`: 玩家1勝利
  - `-1`: 玩家2勝利
  - `1e-4`: 平局
  - `0`: 遊戲尚未結束
- **範例**:
  ```python
  result = game.getGameResult()
  print(result)  # Output: 0 表示遊戲尚未結束
  ```

### 10. `getCanonicalForm(self, player)`
- **功能**: 返回當前玩家的棋盤狀態，棋盤的值乘以當前玩家（1 或 -1），以便於不同玩家看到各自的視角。
- **範例**:
  ```python
  board = game.getCanonicalForm(game.getCurrentPlayer())
  print(board)  # 顯示當前玩家的棋盤
  ```

### 11. `display(self)`
- **功能**: 顯示當前棋盤狀態，`X` 表示玩家1，`O` 表示玩家2，`.` 表示空格。
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

### 12. `setEnvState(self, board, player)`
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

## 3. 運行 `main.py`

`main.py` 會調用兩位同學的 `DQNPlayer` 進行對戰。代碼中的 `CXXXXXXXXX` 和 `FXXXXXXXXX` 對應同學的代碼，具體如下：

- `CXXXXXXXXX` 和 `FXXXXXXXXX` 資料夾分別包含每位同學的 `players.py` 文件和 `DQNPlayer_args` 配置。
- 在運行對戰時，`main.py` 會初始化每位同學的 `DQNPlayer` 並使用專屬的權重和參數，最後執行一系列遊戲來決定勝負。

### 執行步驟

1. 在終端運行以下命令，開始 100 場對戰：
   ```bash
   python main.py
   ```
   輸出將會顯示兩位同學的對戰結果，包括每位玩家的勝場數和平局數。

2. 範例輸出：
   ```
   Starting 100 games between C_DQNPlayer and F_DQNPlayer...

   Results after 100 games:
   C_DQNPlayer wins: 45
   F_DQNPlayer wins: 50
   Draws: 5
   ```