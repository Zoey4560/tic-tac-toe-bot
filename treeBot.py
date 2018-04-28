import random
import copy
from game import Game

tree = {
    0: {},
    1: {}
}

# Search the tree and back trace victory
class TreeBot:
    @classmethod
    def computeTree(Class, player=None):
        board = [
            None, None, None,
            None, None, None,
            None, None, None]
        Class.scoreMoves(board, player, 0)

    def getMove(this, board, whichPlayerAmI):
        if not tree[whichPlayerAmI]:
            this.computeTree(whichPlayerAmI)
        moveScores = tree[whichPlayerAmI][this.hashBoard(board)]
        legalMoveScores = [x for i, x in enumerate(moveScores) if board[i] is None]

        maxScore = max(legalMoveScores)
        bestMoves = [i for i, j in enumerate(moveScores) if j == maxScore and board[i] is None]

        # Game.printBoard(board)
        # cleanBoard = [False if board[i] is not None else j for i, j in enumerate(moveScores)]
        # Game.printBoard(cleanBoard)
        # print(bestMoves)

        return random.choice(bestMoves)

    @classmethod
    def hashBoard(Class, board):
        return ''.join(map(lambda x: '_' if x is None else str(x), board))

    @classmethod
    def scoreMoves(Class, board, whichPlayerAmI, whichPlayersTurnIsIt):
        if Game.whoWon(board) == whichPlayerAmI:
            return 1
        elif Game.whoWon(board) == (0 if whichPlayerAmI == 1 else 1):
            return -1
        elif not Game.spacesAreOpen(board):
            return 0
        else:
            if Class.hashBoard(board) in tree[whichPlayerAmI]:
                nextMoves = tree[whichPlayerAmI][Class.hashBoard(board)]
            else:
                nextMoves = Class.descendTree(board, whichPlayerAmI, whichPlayersTurnIsIt)
                tree[whichPlayerAmI][Class.hashBoard(board)] = nextMoves

            if whichPlayerAmI == whichPlayersTurnIsIt:
                return max(nextMoves)
            else:
                    #discounted future value of non-perfect play
                    # 10% average remaining moves score
                nonP = 0.1 * float(sum(nextMoves)) / len([x for i, x in enumerate(nextMoves) if board[i] is None])
                return round(min(nextMoves) + nonP, 16)

    @classmethod
    def descendTree(Class, board, whichPlayerAmI, whichPlayersTurnIsIt):
        nextMoves = []
        for i, move in enumerate(board):
            if move is None:
                nextBoard = copy.deepcopy(board)
                nextBoard[i] = whichPlayersTurnIsIt
                nextPlayer = 0 if whichPlayersTurnIsIt is 1 else 1
                moveValue = Class.scoreMoves(nextBoard, whichPlayerAmI, nextPlayer)
                nextMoves.append(moveValue)
            else:
                nextMoves.append(0)
        return nextMoves
