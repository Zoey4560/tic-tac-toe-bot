from game import Game
from bruteBot import BruteBot
from randomBot import RandomBot
import random

def printBoard(board):
    for row in board:
        string = ''
        for item in row:
            string += str(item)+' ' if item is not None else '_ '
        print(string)

class HumanPlayer:
    moveMap = {
        1: [2,0],
        2: [2,1],
        3: [2,2],
        4: [1,0],
        5: [1,1],
        6: [1,2],
        7: [0,0],
        8: [0,1],
        9: [0,2]
    }
    def getMove(self, board, whichPlayerAmI):
        print('It\'s your turn, player '+str(whichPlayerAmI))
        printBoard(board)
        print('Play a move with your numpad')
        print('                     7, 8, 9')
        print('                     4, 5, 6')
        print('                     1, 2, 3')
        moveInput = None
        while moveInput is None:
            i = int(input('What\'s your move? '))
            if (0 < i < 10):
                moveInput = i
            else:
                print('That\'s not a valid move!')


        return self.moveMap[moveInput]

class ConsoleGame(Game):
    def __init__(self, player0, player1):
        if random.choice([True, False]):
            print('First player goes first!')
            swap = player0
            player0 = player1
            player1 = swap
        else:
            print('Second player goes first!')
        super().__init__(player0, player1)

player0 = BruteBot()
player1 = HumanPlayer()
winners = {'players': {player0.__class__.__name__: 0, player1.__class__.__name__: 0, 'none': 0}, 'turnOrder': {0: 0, 1: 0, 'none': 0}}
playerHit10000 = False
for i in range(1,10000): # run 10,000 games
    consoleGame = ConsoleGame(player0, player1)
    winner = consoleGame.startGame()
    if winner is not None:
        winnerName = consoleGame.players[winner].__class__.__name__
        print('The winner is player '+ str(winner)+', '+winnerName)
        winners['players'][winnerName] += 1
        winners['turnOrder'][winner] += 1
    else:
        print('Stalemate!')
        winners['players']['none'] += 1
        winners['turnOrder']['none'] += 1
    print(winners)
    printBoard(consoleGame.board)
    #input('play again?')
