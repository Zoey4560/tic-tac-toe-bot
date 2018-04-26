import random
import copy
from game import Game

# Search the tree and back trace victory
class TreeBot:
    def getMove(self, board, whichPlayerAmI):
        winningMoveCount = self.getWinningMoves(board, whichPlayerAmI, whichPlayerAmI, True)
        maxScore = max(winningMoveCount)
        if maxScore > 0:
            bestMoveNumerals = [i for i, j in enumerate(winningMoveCount) if j == maxScore]
        else:
            #nothing but stalemates left. Python's max() returns False for [False, 0.0] so pick non-false/valid moves
            bestMoveNumerals = [i for i, j in enumerate(winningMoveCount) if j is not False]

        # print(board)
        # self.visualizeBoard(winningMoveCount)

        return Game.numeralToPosition(random.choice(bestMoveNumerals))

    def visualizeBoard(self, board):
        pretty = [[0,0,0],[0,0,0],[0,0,0]]
        for i, count in enumerate(board):
            p = Game.numeralToPosition(i)
            pretty[p[0]][p[1]] = count
        print('  ', pretty[0])
        print('  ', pretty[1])
        print('  ', pretty[2])

    def getWinningMoves(self, board, whichPlayerAmI, whichPlayersTurnIsIt, isTopLevel, movesMade=0):
        if Game.whoWon(board) == whichPlayerAmI:
            return True
        elif Game.whoWon(board) == (0 if whichPlayerAmI == 1 else 1):
            return -1
        elif not Game.spacesAreOpen(board):
            return 0
        else:
            winningArray = []
            for i, row in enumerate(board):
                for j, move in enumerate(row):
                    if move is None:
                        nextBoard = copy.deepcopy(board)
                        nextBoard[i][j] = whichPlayersTurnIsIt
                        otherPlayer = 0 if whichPlayersTurnIsIt is 1 else 1
                        nextBoard = self.getWinningMoves(nextBoard, whichPlayerAmI, otherPlayer, False, movesMade + 1)
                        winningArray.append(nextBoard)
                    else:
                        winningArray.append(False)
            if isTopLevel:
                resultArray = []
                for x in winningArray:
                    if x is False:
                        resultArray.append(False)
                    elif x is True:
                        resultArray.append(100) # it's a winning move!
                    else:
                        resultArray.append(x)
                return resultArray
            else:
                return sum(winningArray) / movesMade
