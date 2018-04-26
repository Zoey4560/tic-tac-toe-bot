import math
import random
from game import Game

# Check how much of each win condition
#   I occupy, and pick the one
#   that looks the best
class OccupyBot:
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
        # Game.printBoard(winBoard)
        # print('loss')
        # Game.printBoard(enemiesWinBoard)
        # print('composite')
        # Game.printBoard(compositeWinBoard)

        # print('     Score: ', maxScore)
        # print('     Moves: ', bestMoveNumerals)

        return random.choice(bestMoveNumerals)

    def createWinBoard(self, board, whichPlayer):
        winBoard = [0] * 9
        for winCondition in Game.WIN_CONDITIONS:
            testResult = self.testWinCondition(winCondition, board, whichPlayer)
            for boardIndex in winCondition:
                if Game.isMoveValid(board, boardIndex):
                    if testResult is not False:
                            winBoard[boardIndex] += testResult
                else:
                    winBoard[boardIndex] = False
        return winBoard


    #returns an integer with how many moves already in place or false if not available
    def testWinCondition(self, winCondition, board, whichPlayerAmI):
        points = 0.0
        for boardIndex in winCondition:
            occupant = board[boardIndex]
            if occupant is not None and occupant != whichPlayerAmI:
                return False # player occupies this spot. Can't win
            elif occupant == whichPlayerAmI:
                if points >= 1: # I already have one of these spots, this makes 2. I CAN WIN!
                    return 100
                points += 1 # I have this spot. Solution looking good
            else:
                points += 0.1 # space uncocupied, but i can still win in this solution

        return points
