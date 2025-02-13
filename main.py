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
    from CXXXXXXXXX.players import RandomPlayer
    random_player = RandomPlayer(game)
    arena = Arena(player1, random_player, game)

    num_training_games = 20  # Number of games to play for training
    print(f"Training the DQNPlayer with {num_training_games} games...")
    from tqdm import tqdm
    for _ in tqdm(range(num_training_games)):
        arena.playGame()  # Play games to accumulate experiences for training
        player1.train()  # Train the DQN model after each game
        player1.update_target_model()  # Update the target model periodically


    # 初始化 FXXXXXXXXX 的 DQNPlayer，並使用其專屬的 args
    player2 = F_DQNPlayer(game, args_in_F)
    arena = Arena(player2, random_player, game)

    print(f"Training the DQNPlayer with {num_training_games} games...")
    from tqdm import tqdm
    for _ in tqdm(range(num_training_games)):
        arena.playGame()  # Play games to accumulate experiences for training
        player2.train()  # Train the DQN model after each game
        player2.update_target_model()  # Update the target model periodically

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
