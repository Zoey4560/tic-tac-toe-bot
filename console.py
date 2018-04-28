from game import Game
from occupyBot import OccupyBot
from randomBot import RandomBot
from treeBot import TreeBot
import random
import math

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
        print('The match is ', p0name, ' and ', p1name)
        super().__init__(player0, player1)

    def doTurn(self):
        super().doTurn()
        # Game.printBoard(self.board)
        # input('next?')


winners = {'players': {'none': 0}, 'turnOrder': {0: 0, 1: 0, 'none': 0}}
for i in range(1,10000): # run 10,000 games
    # player0 = random.choice([TreeBot(), OccupyBot(), RandomBot()])
    # player1 = random.choice([TreeBot(), OccupyBot(), RandomBot()])
    player0 = TreeBot()
    player1 = HumanPlayer()
    consoleGame = ConsoleGame(player0, player1)
    winner = consoleGame.runGame()
    if winner is not None:
        winnerName = consoleGame.players[winner].__class__.__name__
        print('The winner is player '+ str(winner)+', '+winnerName)
        if winnerName not in winners['players']:
            winners['players'][winnerName] = 0
        winners['players'][winnerName] += 1
        winners['turnOrder'][winner] += 1
    else:
        print('Stalemate!')
        winners['players']['none'] += 1
        winners['turnOrder']['none'] += 1
    print(winners)
    Game.printBoard(consoleGame.board)
    # input('play again?')
