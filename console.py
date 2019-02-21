from game import Game
from occupyBot import OccupyBot
from randomBot import RandomBot
from treeBot import TreeBot
from neuralBot import NeuralBot
from geneticTrainer import GeneticTrainer
from qTableBot import QTableBot
from qNetworkBot import QNetworkBot
import random
import math
import matplotlib.pyplot as plt

class HumanPlayer:
    def getMove(self, board, whichPlayerAmI):
        print('It\'s your turn, player '+str(whichPlayerAmI))
        Game.printBoard(board)
        print('Play a move with your numpad')
        print('                     7, 8, 9')
        print('                     4, 5, 6')
        print('                     1, 2, 3')
        moveInput = None
        while moveInput is None:
            # input = None
            try:
                inp = input('What\'s your move? ')
                i = int(inp)
                if (0 < i < 10):
                    moveInput = i
                else:
                    raise
            except:
                if inp == 'exit':
                    exit()
                if inp == 'thermonuclearwar':
                    print('How about we work up to chess first?')
                    exit()
                print('That\'s not a valid move!')


        return self.numpadToBoardIndex(moveInput)

    @staticmethod
    def numpadToBoardIndex(n):
        return 3*(2 - math.floor((n-1)/3)) + (n-1)%3

class ConsoleGame(Game):
    def __init__(self, player0, player1):
        if random.choice([True, False]):
            swap = player0
            player0 = player1
            player1 = swap
        p0name = player0.__class__.__name__
        p1name = player1.__class__.__name__
        # print('The match is ', p0name, ' and ', p1name)
        super().__init__(player0, player1, False)

    # def doTurn(self):
    #     Game.printBoard(self.board)
    #     print(self.currentPlayer().__class__.__name__, self.currentPlayerIndex())
    #     super().doTurn()
    #     input('next?')
    # def setupGame(self):
        # self.board = [None, 1, 1,
        #                 0, None, None,
        #                 0, None, None]
        # self.isTurnPlayer0 = True


    def replayGame(self):
        print('--')
        self.setupGame()
        for move in self.moveHistory:
            print(self.currentPlayer().__class__.__name__, self.currentPlayerIndex())
            try:
                print(self.currentPlayer().debug(self.board, self.currentPlayerIndex()))
            except Exception as e:
                pass # print(e)
            self.makeMove(move)
            self.nextPlayer()
            self.printBoard(self.board)

bestNeuralBot = GeneticTrainer.getBestBot()

for n in range(0,1): # run n sessions
    winners = {'none': 0}
    gameScoreCoefs = []
    # player0 = random.choice([TreeBot(), OccupyBot(), RandomBot(), bestNeuralBot, QTableBot()])
    # player1 = random.choice([TreeBot(), OccupyBot(), RandomBot(), bestNeuralBot, QTableBot()])
    player0 = QNetworkBot()
    player1 = OccupyBot()
    # player0.playSelf()
    # input()

    for i in range(0,10000): # run i games
        consoleGame = ConsoleGame(player0, player1)
        winner = consoleGame.runGame()
        if winner is not None:
            winnerName = winner.__class__.__name__
            # print('The winner is player '+ str(winner)+', '+winnerName)
            # if winnerName == 'RandomBot':
            #     print('Random Won')
            #     consoleGame.replayGame()
            #     input('next?')
            if winnerName not in winners:
                winners[winnerName] = 0
            winners[winnerName] += 1


        else:
            # print('Stalemate!')
            winners['none'] += 1
        for p in [player0, player1]:
            if hasattr(p, 'reportGame'):
                p.reportGame(consoleGame)
        p0name = player0.__class__.__name__
        p0wins = winners[p0name] if p0name in winners else 0
        winningCoef = (p0wins + winners['none']*.5)/(i+1)
        print(n, i, winningCoef, winners)
        gameScoreCoefs.append(winningCoef)
        # print(gameScoreCoefs)
        # input()


        # input()
        # Game.printBoard(consoleGame.board)
    print(winners)

    plt.plot(gameScoreCoefs)
plt.legend()
plt.show()


    # input('play again?')
