import math
import random
from game import Game

# Brute force check all possible wins,
#   pick the move with the best
#   combined win conditions
class BruteBot:
    WIN_CONDITIONS = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]
    def getMove(self, board, whichPlayerAmI):

        winBoard = self.createWinBoard(board, whichPlayerAmI)
        enemiesWinBoard = self.createWinBoard(board, 1 if whichPlayerAmI == 0 else 0)
        compositeWinBoard = [False if x is False else round(x + 0.5 * y,1) for x, y in zip(winBoard, enemiesWinBoard)]



        maxScore = max(compositeWinBoard)
        if maxScore > 0 :
            bestMoveNumerals = [i for i, j in enumerate(compositeWinBoard) if j == maxScore]
        else:
            #nothing but stalemates left. Python's max() returns False for [False, 0.0] so pick non-false/valid moves
            bestMoveNumerals = [i for i, j in enumerate(compositeWinBoard) if j is not False]

        # print('win')
        # self.visualizeWinBoard(winBoard)
        # print('loss')
        # self.visualizeWinBoard(enemiesWinBoard)
        # print('composite')
        # self.visualizeWinBoard(compositeWinBoard)

        # print('     Score: ', maxScore)
        # print('     Moves: ', [Game.numeralToPosition(x) for x in bestMoveNumerals])

        return Game.numeralToPosition(random.choice(bestMoveNumerals))

    def visualizeWinBoard(self, winBoard):
        pretty = [[0,0,0],[0,0,0],[0,0,0]]
        for i, winCredit in enumerate(winBoard):
            p = Game.numeralToPosition(i)
            pretty[p[0]][p[1]] = False if winCredit is False else winCredit
        print('  ', pretty[0])
        print('  ', pretty[1])
        print('  ', pretty[2])

    def createWinBoard(self, board, whichPlayer):
        winBoard = [0] * 9
        for winCondition in self.WIN_CONDITIONS:
            testResult = self.testWinCondition(winCondition, board, whichPlayer)
            for boardNumeral in winCondition:
                if Game.isMoveValid(board, Game.numeralToPosition(boardNumeral)):
                    if testResult is not False:
                            winBoard[boardNumeral] += testResult
                else:
                    winBoard[boardNumeral] = False
        return winBoard


    #returns an integer with how many moves already in place or false if not available
    def testWinCondition(self, winCondition, board, whichPlayerAmI):
        points = 0.0
        for boardNumeral in winCondition:
            position = Game.numeralToPosition(boardNumeral)
            occupant = board[position[0]][position[1]]
            if occupant is not None and occupant != whichPlayerAmI:
                return False # player occupies this spot. Can't win
            elif occupant == whichPlayerAmI:
                if points >= 1: # I already have one of these spots, this makes 2. I CAN WIN!
                    return 100
                points += 1 # I have this spot. Solution looking good
            else:
                points += 0.1 # space uncocupied, but i can still win in this solution

        return points
