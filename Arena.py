from tqdm import tqdm
import numpy as np

class Arena():
    def __init__(self, player1, player2, game):
        """
        Initializes the Arena class.
        player1, player2: Objects that implement the play(board) -> action method.
        game: Instance of the game being played.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game

    def playGame(self, verbose=False):
        """
        Plays a single game between player1 and player2.
        verbose: If set to True, displays the game state and turns.
        Returns:
        The result of the game: 1 if player1 wins, -1 if player2 wins, 0 for a draw.
        """
        players = [self.player2, None, self.player1]  # List to keep track of current players
        curPlayer = 1  # Player 1 starts the game
        self.game.getInitBoard()  # Initialize the game board inside the game class
        it = 0  # Turn counter

        while True:
            it += 1
            if verbose:
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.game.display()  # Display the board if verbose is True

            player = players[curPlayer + 1]  # Get the current player
            action = player.play()  # Call player's action method

            valids = self.game.getValidMoves()  # Get valid moves from the game
            if valids[action] == 0:  # Ensure the action is valid
                print(action)
                assert valids[action] > 0

            # 使用 getNextState 管理棋盤和玩家切換
            next_board, next_player = self.game.getNextState(action)
            r = self.game.getGameResult()  # Check if the game has ended
            if r != 0:  # If the game is over
                if verbose:
                    print("Game over: Turn ", str(it), "Result ", str(r))
                    self.game.display()  # Display final board state
                return r  # Return the result of the game

            curPlayer = next_player  # 切換到下一個玩家


    def playGames(self, num, verbose=False):
        """
        Plays multiple games between player1 and player2.
        num: The total number of games to be played (half with player1 starting and half with player2 starting).
        verbose: If set to True, displays the game states.
        Returns:
        A tuple (oneWon, twoWon, draws) indicating how many games each player won and how many ended in a draw.
        """
        num = int(num / 2)  # Divide the total games equally for both players starting
        oneWon = 0  # Counter for games won by player1
        twoWon = 0  # Counter for games won by player2
        draws = 0  # Counter for drawn games

        # First set of games where player1 starts
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose)  # Play a game
            if gameResult == 1:
                oneWon += 1  # Player1 wins
            elif gameResult == -1:
                twoWon += 1  # Player2 wins
            else:
                draws += 1  # Draw

        # Switch players for the second set of games
        self.player1, self.player2 = self.player2, self.player1

        # Second set of games where player2 starts
        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)  # Play a game
            if gameResult == -1:
                oneWon += 1  # Player1 wins
            elif gameResult == 1:
                twoWon += 1  # Player2 wins
            else:
                draws += 1  # Draw

        return oneWon, twoWon, draws  # Return the results of all games
