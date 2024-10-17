from players import DQNPlayer, RandomPlayer
from Arena import Arena
from utils import dotdict

import os


def main():
    from connect4 import Connect4Game
    game = Connect4Game()

    # Set parameters for the DQNPlayer
    args = dotdict({
        'lr': 0.001,  # Learning rate
        'gamma': 0.95,  # Discount factor
    })

    # Initialize the DQNPlayer
    dqn_player = DQNPlayer(game, args)

    # Load an existing model (optional)
    if os.path.exists('./dqn_model.weights.h5'):
        dqn_player.load('./dqn_model.weights.h5')
    else:
        print("No model found, training a new model...")
        # If no model is found, train a new model using the following code
        dqn_player.train()
        dqn_player.save('./dqn_model.weights.h5')  # Save the trained model
        dqn_player.load('./dqn_model.weights.h5')  # Load the saved model

    # Set the opponent (RandomPlayer)
    opponent_player = RandomPlayer(game)

    # Create an Arena to facilitate the matches
    arena = Arena(dqn_player, opponent_player, game)

    # Start playing the matches
    num_games = 20
    print("Starting the matches between DQNPlayer and RandomPlayer...")
    results = arena.playGames(num_games)

    # Display the results
    print(f"\nResults after {num_games} games:")
    print(f"DQNPlayer wins: {results[0]}")
    print(f"RandomPlayer wins: {results[1]}")
    print(f"Draws: {results[2]}")

if __name__ == "__main__":
    main()
