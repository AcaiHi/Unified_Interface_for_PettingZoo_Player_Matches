from tqdm import tqdm
import numpy as np

class Arena():
    def __init__(self, player1, player2, game):
        """
        Initializes the Arena with two players and a game instance.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game

    def playGame(self, verbose=False):
        """
        Plays a single game between player1 and player2.
        Returns: 1 if player1 wins, -1 if player2 wins, 0 for a draw.
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1  # Player 1 starts
        self.game.getInitBoard()  # Initialize game board
        it = 0

        while True:
            it += 1
            if verbose:
                print("Turn", str(it), "Player", str(curPlayer))
                self.game.display()

            player = players[curPlayer + 1]
            action = player.play()

            valids = self.game.getValidMoves()  # Ensure action is valid
            if valids[action] == 0:
                assert valids[action] > 0

            next_board, next_player = self.game.getNextState(action)
            r = self.game.getGameResult()  # Check if game ended
            if r != 0:
                if verbose:
                    print("Game over: Turn", str(it), "Result", str(r))
                    self.game.display()
                return r

            curPlayer = next_player  # Switch player

    def playGames(self, num, verbose=False):
        """
        Plays multiple games between player1 and player2.
        Returns: A tuple (oneWon, twoWon, draws) indicating results.
        """
        num = int(num / 2)  # Half games start with player1, half with player2
        oneWon, twoWon, draws = 0, 0, 0

        # First set of games with player1 starting
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        # Switch players for second set of games
        self.player1, self.player2 = self.player2, self.player1

        # Second set of games with player2 starting
        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws
